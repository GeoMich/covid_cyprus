from bs4 import BeautifulSoup
from datetime import datetime
import urllib
import requests
import pandas as pd
import string

import io
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import re


def find_files_from_url(url):
    """Find links to files in a website"""
    soup = BeautifulSoup(requests.get(url).text, features="html.parser")
    hrefs = []
    for a in soup.find_all("a"):
        hrefs.append(a["href"])

    return hrefs


# Isolate only those urls corresponding to daily reports
def isolate_relevant_files(list_of_links):
    substrings_in_path = [
        "Ανακοίνωση του Υπουργείου Υγείας σχετικά με νέα περιστατικά της νόσου COVID-19",
        "Ανακοίνωση του Υπουργείου Υγείας για νέα περιστατικά της νόσου COVID-19",
        "Ανακοίνωση για επιβεβαίωση κρουσμάτων κορωνοϊού",
        "anakoinosikrousmata",
    ]
    links_daily_reports = [
        link
        for link in list_of_links
        if any(substring in link for substring in substrings_in_path)
    ]

    return links_daily_reports


def print_first_x_elements(list_of_str, x):
    for i, string in enumerate(list_of_str):
        print(string)
        if i > x:
            break


map_month = {
    "Ιανουαρίου": 1,
    "Φεβρουαρίου": 2,
    "Μαρτίου": 3,
    "Απριλίου": 4,
    "Μαΐου": 5,
    "Ιουνίου": 6,
    "Ιουλίου": 7,
    "Αυγούστου": 8,
    "Σεπτεμβρίου": 9,
    "Οκτωβρίου": 10,
    "Νοεμβρίου": 11,
    "Δεκεμβρίου": 12,
}


def month_key_in_string(date_string):
    months_list = [
        month if month in date_string else None for month in map_month.keys()
    ]  # None except on matching month
    month_key = list(filter(None, months_list))  # remove None
    return month_key[0]


def replace_month_with_number(date_string):
    month_key = month_key_in_string(date_string)
    new_string = date_string.replace(month_key, str(map_month[month_key]))
    return new_string


def extract_datetime(link):

    try:
        # This uses datetime given after "upload/" in link
        date1 = link.split("uploads/")[1].split("--")[0]
        dt_report = datetime.strptime(date1, "%d%m%Y")  # .date()
    except ValueError:
        # this uses the date given before .pdf in case the above info is not provided
        date_str_gr = link.split("COVID-19")[1].split(".")[0]
        puctuation_plus = string.punctuation + "–"  # add dash
        date_str_gr = date_str_gr.translate(
            str.maketrans("", "", puctuation_plus)
        )  # strip punctuation (, or – usually)
        date1 = replace_month_with_number(date_str_gr)
        date1 = date1.lstrip()  # remove empty spaces at start
        if not any([substring in date1 for substring in ["2021", "2022"]]):
            date1 = date1 + " 2022"
        dt_report = datetime.strptime(date1, "%d %m %Y")

    return dt_report


def percent_encode_url(url):
    """encode utf-8 greek charachters to percent-encoded"""
    url_percent_encoded = (
        url.split("uploads/")[0]
        + "uploads/"
        + urllib.parse.quote(url.split("uploads/")[1].encode("utf-8"))
    )
    return url_percent_encoded


def download_pdfs(df_url):
    """Downloading pdf daily reports from url's in a df"""
    if df_url.empty:
        print("No new reports. Nothing to download.")

    for _, row in df_url.iterrows():
        date_str = row["date"]
        print(f"Downloading report (pdf) of {date_str}...")
        filename_report = row["date"].replace("-", "_")
        path_report = "../data/reports/" + filename_report + ".pdf"
        # print(url_percent_encoded)

        # download and save report as pdf
        response = requests.get(row["url_perc"])
        with open(path_report, "wb") as f:
            f.write(response.content)
        print(f"Valid url: {response.ok}")

        response.close()


map_numbers = {
    "Ένα": "1",
    "Δύο": "2",
    "Τρία": "3",
    "Τέσσερα": "4",
    "Πέντε": "5",
    "Έξι": "6",
    "Επτά": "7",
    "Εφτά": "7",
    "Οχτώ": "8",
    "Εννιά": "9",
    "Δέκα": "10",
    "Έντεκα": "11",
    "Δώδεκα": "12",
    "Δεκατρία": "13",
}


def pdf_to_text(path):
    with open(path, "rb") as fp:
        rsrcmgr = PDFResourceManager()
        outfp = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
    text = outfp.getvalue()

    return text


def number_key_in_string(date_string):
    numbers_list = [
        number if number in date_string else None for number in map_numbers.keys()
    ]  # None except on matching month
    number_key = list(filter(None, numbers_list))  # remove None

    return number_key[0]


def extract_info_text(text):
    m1 = re.search("Ποσοστό (\s*.+?)%", text)  # "\s*" ignores white space
    perc_unv = m1.group(1) if m1 else None
    if not m1.group(1).strip().isnumeric():
        m1a = re.search("στορικό εμβολιασμού(.+?)%", text)
        perc_str = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", m1a.group(1).replace(",", "."))
        perc_unv = perc_str[0]

    m2 = re.search("σήμερα, (.+?):", text)
    date_pdf = m2.group(1) if m2 else None

    m3 = re.search("(\w+?) ασθενείς COVID-19 νοσηλεύονται", text)
    hosp_num = m3.group(1) if m3 else None

    # m4 = re.search("ανίχνευσης αντιγόνου \(antigen rapid test\). -  (.+?) \(ποσοστό θετικότητας", text)
    # case_num = m4.group(1) if m4 else None

    m4 = re.search("test\.(.+?) ποσοστό", text)
    m4a = re.search("Εντοπίστηκαν(\s*.+?\s*)νέα", text)
    case_num = m4.group(1) if m4 else m4a.group(1) if m4a else None
    if case_num is not None:
        case_num = "".join(e for e in case_num if e.isalnum())  # keep only numbers
        # case_num = case_num.split("-")[1].strip()

    m5 = re.search("- (.+?) άτομ", text)
    m5a = re.search("νακοινώθηκαν (.*) θάνατ", text)
    m5b = re.search("νακοινώθηκε (.*) θάνατ", text)
    m5c = re.search("- (.+?) θάνατ", text)
    death_num = (
        m5.group(1)
        if m5
        else m5a.group(1)
        if m5a
        else m5b.group(1)
        if m5b
        else m5c.group(1)
        if m5c
        else "0"
    )

    if any(
        substring in death_num
        for substring in ["Δεν  καταγράφηκαν", "Δεν ανακοινώθηκαν"]
    ):
        death_num = "0"

    if death_num != "0":
        if not death_num.strip().isnumeric():
            word_key = number_key_in_string(death_num)
            death_num = map_numbers[word_key]
    # print(f"Deaths : {death_num}")

    info = [perc_unv, date_pdf, hosp_num, case_num, death_num]

    return info


def extract_info_from_reports(list_path_reports):
    """Returns Dataframe with relevant covid info, extracted from pdf daily reports"""

    dates_url = []
    percs_unv = []
    dates_pdf = []
    hosps_num = []
    cases_num = []
    deaths_num = []

    for report in list_path_reports:
        date_url = report.split("reports/")[1].split(".pdf")[0].replace("_", "-")
        print(date_url)
        dates_url.append(date_url)
        text = pdf_to_text(report)
        text = (
            text.replace("\n", "").replace("\xa0", "").replace("(", "").replace(")", "")
        )

        info = extract_info_text(text)
        percs_unv.append(info[0])
        dates_pdf.append(info[1])
        hosps_num.append(info[2])
        cases_num.append(info[3])
        deaths_num.append(info[4])

        print(f"Date:{info[1]}({date_url}): {info[2]} hosp ({info[0]}% unvacc)")
        print(f"{info[3]} new cases, {info[4]} deaths")

    # Turn percentages to float
    percs_unv1 = [float(perc.replace(",", ".")) for perc in percs_unv]
    cases_num1 = [float(num.replace(",", "")) for num in cases_num]
    # Put info in df
    df_hosp_unv = pd.DataFrame(
        {
            "date": dates_url,
            "hospitalizations_dailyrep": hosps_num,
            "perc_hosp_unvaccinated": percs_unv1,
            "daily new cases": cases_num1,
            "daily deaths": deaths_num,
        }
    )

    df_hosp_unv["perc_hosp_vaccinated"] = (
        100 - df_hosp_unv["perc_hosp_unvaccinated"].values
    )
    # df_hosp_unv["date"] = pd.to_datetime(df_hosp_unv["date"], format="%Y-%m-%d")
    df_hosp_unv["hospitalizations_dailyrep"] = df_hosp_unv[
        "hospitalizations_dailyrep"
    ].astype(float)
    df_hosp_unv["daily deaths"] = df_hosp_unv["daily deaths"].astype(float)

    return df_hosp_unv


missing_reports_from_PIO = pd.DataFrame(
    # "2022-01-18" :  deaths in pdf are wrong (https://tinyurl.com/56fm4rzd)-> get correct from updated pio announc.: https://tinyurl.com/y99hof7l
    {
        # "date": datetime.strptime("2021-12-05", "%Y-%m-%d"),
        "date": ["2021-12-05", "2022-01-14"],
        "hospitalizations_dailyrep": [119, 257],
        "perc_hosp_unvaccinated": [68.91, 73.16],
        "daily new cases": [307, 3042],
        "daily deaths": [0, 0],
        "perc_hosp_vaccinated": [100 - 68.91, 100 - 73.16],
    },
    index=[0, 1],
    # {
    #     # "date": datetime.strptime("2021-12-05", "%Y-%m-%d"),
    #     "date": "2021-12-05",
    #     "hospitalizations_dailyrep": 119,
    #     "perc_hosp_unvaccinated": 68.91,
    #     "daily new cases": 307,
    #     "daily deaths": 0,
    #     "perc_hosp_vaccinated": 100 - 68.91,
    # },
    # index=[0],
)


def df_append_missing_from_PIO(df):
    """If the miissng info from PIO are not already in the df -> adds them"""

    # Add missing values
    # 5.12.2022 -> the uploaded pdf for this day is the same as the one for the day before.
    # Get actual data from :
    # https://www.pio.gov.cy/%CE%B1%CE%BD%CE%B1%CE%BA%CE%BF%CE%B9%CE%BD%CF%89%CE%B8%CE%AD%CE%BD%CF%84%CE%B1-%CE%AC%CF%81%CE%B8%CF%81%CE%BF.html?id=24586#flat

    missing_dates_PIO = missing_reports_from_PIO["date"].tolist()
    # print(missing_dates_PIO)
    diff_dates = [d for d in missing_dates_PIO if d not in df["date"].tolist()]
    # print(f"Difference : {diff_dates}")
    df_extra = missing_reports_from_PIO.query("date in @diff_dates")
    # print(f"Extra df : {df_extra}")

    if not df_extra.empty:
        # need to add these to dataframe
        df_hosp_extra = pd.concat([df, df_extra], axis=0)
    else:
        df_hosp_extra = df

    return df_hosp_extra
