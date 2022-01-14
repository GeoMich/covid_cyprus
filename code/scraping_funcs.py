import pandas as pd
import numpy as np
import glob
import os
import utils as ut


def get_reports_urls():
    """Creates df with urls for all available pdf daily reports in PIO website"""

    URL_PIO = "https://www.pio.gov.cy/coronavirus/categories/press#30"
    print("Collecting urls for all files in PIO website...")
    list_of_links = ut.find_files_from_url(URL_PIO)
    # print("Some examples of links in website...")
    # ut.print_first_x_elements(list_of_links, 5)

    print("Getting urls corresponding to daily reports...")
    links_daily_reports = ut.isolate_relevant_files(list_of_links)
    # print("Some examples of links to daily reports...")
    # ut.print_first_x_elements(links_daily_reports, 5)

    # Extract date as datetime from url
    print("Extracting date from url...")
    dt_reports = [ut.extract_datetime(link) for link in links_daily_reports]
    # print("Some examples of datetime extracted from link...")
    # ut.print_first_x_elements(dt_reports, 5)

    # # Check if link is valid (.ok -> True if link valid, False if not)
    # valid_url = [requests.get(ut.percent_encode_url(url)).ok for url in links_daily_reports]
    # print("Some examples of checking link validity...")
    # ut.print_first_x_elements(links_daily_reports, 5)

    # Get all urls as percent-encoded
    print("Transforming urls to percent-encoded...")
    links_perc_encoded = [ut.percent_encode_url(url) for url in links_daily_reports]
    # print("Some examples of percent-encoded links..")
    # ut.print_first_x_elements(links_perc_encoded, 5)

    ### Create df with date & URLs for pdf reports

    # Add date and url in a dataframe
    df_url_reports = pd.DataFrame(
        {
            "date": dt_reports,
            "url": links_daily_reports,
            "url_perc": links_perc_encoded,
            # "valid_url_perc" : valid_url
        }
    )

    # Print last date
    df_url_reports = df_url_reports.sort_values("date")
    last_date_db = df_url_reports["date"].iloc[-1]
    print(f"Last entry in url db is from {last_date_db}")

    # Save as csv
    print("Saving url's dataframe...")
    df_url_reports.to_csv("../data/database_url_reports.csv")


def download_reports():
    """Downloading pdf of daily reports from PIO website"""

    PATH_DB = "../data/database_url_reports.csv"
    PATH_REPORTS = "../data/reports"

    # Load local database
    df_url = pd.read_csv(PATH_DB, index_col=[0])
    # df_url["date"] = pd.to_datetime(df_url["date"], format="%Y-%m-%d")

    # Missing reports in database

    # Get dates from url database
    list_dates_url = df_url["date"].replace("-", "_", regex=True).to_list()

    # Get dates from reports in data folder
    list_dates_db = [path.split(".")[0] for path in os.listdir(PATH_REPORTS)]

    # Find difference between do - check only
    missing_dates = list(set(list_dates_url) - set(list_dates_db))
    # Get only from 16_07_2021, ie when vaccination percentage appeared in the reports
    missing_dates = [d for d in missing_dates if d >= "2021_07_16"]
    print("Missing reports...")
    print(missing_dates)

    ## Download missing reports

    # URls to download
    missing_dates = [d.replace("_", "-") for d in missing_dates]
    df_url_missing = df_url.query("date in @missing_dates")
    # print(df_url_missing)

    # Download missing reports
    ut.download_pdfs(df_url_missing)


def get_info_from_reports():
    "Extract relevant info from pdf w daily reports"

    PATH_INFO_REPORTS = "../data/data_from_pdf_reports.csv"
    PATH_PDF_REPORTS = "../data/reports"

    # Get dates from reports in data folder
    paths_reports = glob.glob(PATH_PDF_REPORTS + "/*.pdf")
    list_dates_reports = [path.split(".")[0] for path in os.listdir(PATH_PDF_REPORTS)]

    # Load stored df with info from reports (if any)
    if os.path.isfile(PATH_INFO_REPORTS):
        df_hosp_unv = pd.read_csv(glob.glob(PATH_INFO_REPORTS)[0], index_col=[0])
        last_date_db = df_hosp_unv["date"].iloc[-1]
        print(f"Last day in stored data is : {last_date_db}")
        # Get dates from df
        list_dates_df = df_hosp_unv["date"].replace("-", "_", regex=True).to_list()

    # Find difference between the two
    # -- note: get only from 16_07_2021, ie when vaccination % appeared in the reports
    missing_dates = list(set(list_dates_reports) - set(list_dates_df))
    missing_dates = [d for d in missing_dates if d >= "2021_07_16"]
    print("Missing info from (existing) reports from: ")
    print(missing_dates)

    # Get info from pdfs
    paths_reports_missing = [
        path
        for path in paths_reports
        if any(missing_date in path for missing_date in missing_dates)
    ]
    # print(paths_reports_missing)
    df_hosp_unv_extra = ut.extract_info_from_reports(paths_reports_missing)
    # print(df_hosp_unv_extra)

    # Append new info if there was an info datafame in data folder
    if os.path.isfile(PATH_INFO_REPORTS):
        df_hosp_upd = pd.concat([df_hosp_unv, df_hosp_unv_extra], axis=0)
    else:
        df_hosp_upd = df_hosp_unv_extra
    # print(df_hosp_upd)

    # Append missing info from PIO if not already in df
    df_hosp_upd = ut.df_append_missing_from_PIO(df_hosp_upd)
    # print(df_hosp_upd)

    # Save as csv
    last_date = df_hosp_upd["date"].iloc[-1].replace("-", "_")
    print("Saving hospitalizations info from reposts as csv..")
    print(f"Data available until: {last_date}")
    df_hosp_upd.to_csv(PATH_INFO_REPORTS)


def get_url_with_sum_stats():
    """Check for latest url in data.gov.cy with summary daily stats"""
    base_url = "https://www.data.gov.cy/dataset/%CE%B7%CE%BC%CE%B5%CF%81%CE%AE%CF%83%CE%B9%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B4%CE%B9%CE%B1%CF%83%CF%80%CE%BF%CF%81%CE%AC%CF%82-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CF%83%CF%84%CE%B7%CE%BD-%CE%BA%CF%8D%CF%80%CF%81%CE%BF"
    list_of_links = ut.find_files_from_url(base_url)
    substrings_in_path = [
        "https://www.data.gov.cy/sites/default/files/CY%20Covid19%20Open%20Data%20-%20Extended%20-%20new"
    ]
    not_in_path = ["http://oneclick.cartodb.com"]
    url_sum_stats = [
        link
        for link in list_of_links
        if any(substring in link for substring in substrings_in_path)
        & any(substring not in link for substring in not_in_path)
    ]
    return url_sum_stats[0]


def download_sum_stats():
    """Download the csv from data.gov.cy which includes daily covid stats from beginning of pandemic

    --> note: this is not updated daily so it may have a lag
    --> (in another script) I complement these data with data from scraped daily reports
    """

    # Data scraping
    url_data = get_url_with_sum_stats()
    print("Downloading dataset...")
    df = pd.read_csv(url_data)
    # Format DF
    df1 = df.copy()
    df1 = df1.replace(":", np.nan)
    df1["date"] = pd.to_datetime(df1["date"], format="%d/%m/%Y")
    df1 = df1.sort_values("date")
    last_date_group = df1["date"].iloc[-1].date()
    print(f"Dataset contains data until {last_date_group}")

    # Save dataset
    print("Saving dataset...")
    df1.to_csv("../data/dataset_sum_daily_stats.csv")


def get_url_with_vacc_data():
    """Check for latest url in data.gov.cy with weekly vacciation data"""

    base_url = "https://www.data.gov.cy/dataset/%CE%B5%CE%B2%CE%B4%CE%BF%CE%BC%CE%B1%CE%B4%CE%B9%CE%B1%CE%AF%CE%B1-%CF%83%CF%84%CE%B1%CF%84%CE%B9%CF%83%CF%84%CE%B9%CE%BA%CE%AC-%CE%B5%CE%BC%CE%B2%CE%BF%CE%BB%CE%B9%CE%B1%CF%83%CE%BC%CF%8E%CE%BD-%CE%BA%CE%B1%CF%84%CE%AC-%CF%84%CE%B7%CF%82-%CE%BD%CF%8C%CF%83%CE%BF%CF%85-covid-19-%CE%B1%CE%BD%CE%AC-%CE%BF%CE%BC%CE%AC%CE%B4%CE%B1-%CF%83%CF%84%CF%8C%CF%87%CE%BF"
    list_of_links = ut.find_files_from_url(base_url)
    substrings_in_path = [
        "https://www.data.gov.cy/sites/default/files/CY%20Vaccination%20Data%20by%20Target%20Group"
    ]
    not_in_path = ["http://oneclick.cartodb.com"]
    url_vacc_stats = [
        link
        for link in list_of_links
        if any(substring in link for substring in substrings_in_path)
        & any(substring not in link for substring in not_in_path)
    ]
    return url_vacc_stats[0]


def download_vaccination_data():
    """Download dataset with vaccination per week, target group, vaccine, dose etc"""

    # find the correct url

    total_population = 888_005
    print("Downloading vaccination dataset...")
    url_vaccination = get_url_with_vacc_data()
    df_v1 = pd.read_csv(url_vaccination)
    df_v1["Population"] = total_population
    last_week = df_v1["YearWeekISO"].iloc[-1]
    print(f"Vaccination data are available until {last_week}.")
    print("Saving vaccination dataset...")
    df_v1.to_csv(f"../data/vaccination_dataset.csv")
