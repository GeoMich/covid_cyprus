import pandas as pd
import scraping_funcs as scr
import merging_funcs as mrg
import plots
import os

# # Update your data to latest available
def scrape_update_data():
    scr.get_reports_urls()
    scr.download_reports()
    scr.get_info_from_reports()
    scr.download_sum_stats()
    scr.download_vaccination_data()


def merge_datasets():
    # Merge 3 datasets -> covid_stats_from_database, covid_stats_from_pdf_daily_reports & vaccination datasets
    # Load grouped data downloaded from database
    df_grp = pd.read_csv("../data/dataset_sum_daily_stats.csv", index_col=[0])
    df_grp["date"] = pd.to_datetime(df_grp["date"], format="%Y-%m-%d")

    # Load data gathered from individual daily reports
    df_ind = pd.read_csv("../data/data_from_pdf_reports.csv", index_col=[0])
    df_ind["date"] = pd.to_datetime(df_ind["date"], format="%Y-%m-%d")

    # Merge datasets
    df_ex1 = mrg.add_missing_cases_deaths_to_group_data(df_grp, df_ind)
    df_ex2 = mrg.add_vaccination_percentage(df_ex1, df_ind)

    # Save extented dataset
    df_ex2.to_csv("../data/dataset_extented.csv")


def make_plots():

    print("Baking the plots...")

    # Load extented dataset
    df = pd.read_csv("../data/dataset_extented.csv", index_col=[0])
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # Load vaccination data
    dfv = pd.read_csv("../data/vaccination_dataset.csv", index_col=[0])

    plots.hospitalisations_per_vaccination(df)
    plots.hospitalisations_by_severity(df)
    plots.cases_hosp_death(df)
    plots.hospitalisations_per_vacc_per_100_00(df, dfv)
    plots.vaccinations_by_age(dfv)


def make_html():
    "Create html with figures embedded"

    print("Making html file...")
    html_figs_div = [
        "cases_hosp_deaths_div.html",
        "deaths_div.html",
        "hospitalisations_per_severity_div.html",
        "hospitalisations_per_vacc_per_100_000_div.html",
        "hospitalisations_per_vacc_per_100_000_ratio_div.html",
        "hospitalisations_per_vaccination_div.html",
        "vaccinations_by_age_div.html",
    ]

    div_dict = {}
    for div_html in html_figs_div:
        with open(os.path.join("../plots/", div_html), "r") as f:
            div_dict[div_html.split(".")[0]] = f.read()

    html_str = f"""
    <!DOCTYPE html>
    <html>

    <head>
        <link rel="stylesheet" type="text/css" href="code/css/style.css">
        <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
    </head>

    <body>
        <h1>Covid-19 & Vaccination numbers in Cyprus</h1>
        <p>Produced by <i>Georgios Michail</i></p>
        
        <p>These set of graphs on the situation of the COVID-19 pandemic in Cyprus are produced & updated based on data from the ministry of health.\
            \nThe figures are interactive and you can zoom in to get details, or hover over some points to get extra information.</p>

        <h3>Cases, hospitalisations & deaths</h3>

        <p>The first two figures show the time course of the positive cases, hospitalisations and deaths related with the COVID-19.</p>
        {div_dict["cases_hosp_deaths_div"]}
        <br>
        {div_dict["deaths_div"]}
        
        <h3>Hospitalisations by vaccination</h3>

        <p>The next graph shows the hospitalisations related to COVID-19 by vaccination status. Here, one can easily  notice that the possibility \
            to be hospitalised is larger for unvaccinated people. </p>
        {div_dict["hospitalisations_per_vaccination_div"]}

        <h3>But how much more likely is to end up in hospitalised after infection if unvaccinated?</h3>
        <p>Some people based on figures similar to the previous one say that, if on one day we have 80 of hospitalised being \
            unvaccinated and 20 vaccinated, this means it's 4 times more likely to be hospitalized for unvaccinated.\
            This is actually not accurate, because when doing this calculation we don't take into account the overall size\
            of vaccinated and unvaccinated population from which this hospitalisations occur. \
            To be correct, we need to compare hospitalizations for the same number of vaccinated and unvaccinated people.\
            This is what I show in the following figure, depicting hospitalisations per 100 000 vaccinated and unvaccinated people. \
            And here it's clear the chances to get hospitalised when infected with COVID-19 if unvaccinated are from 5 up \
            to 18 times higher. </p>
        {div_dict["hospitalisations_per_vacc_per_100_000_div"]}

         <p>And here you see the ratio between hospitalisations in 100 000 unvaccinated and 100 000 vaccinated people, \
            which corresponds to how many times more likely is to get hospitalized. One can notice here the ratio is \
            increasing during peaks of the pandemic. </p>

        {div_dict["hospitalisations_per_vacc_per_100_000_ratio_div"]}

        <h3>And what about the severity of hospitalisations?</h3>

        <p>This figure splits hospitalisations in 3 categories:</p>
        <p>a. Patients not in an Intensive Care Unit (ICU)</p>
        <p>b. Patients in ICU but not ventilated</p>
        <p>c. Patients in ICU & ventilated </p></p>
        {div_dict["hospitalisations_per_severity_div"]}

        <h3>Immunity wall of Cyprus</h3>

        <p>What is the vaccination level for the different age groups? </p>
        {div_dict["vaccinations_by_age_div"]}

    </body>

    </html>
    """

    # The final string can be saved in a file
    print("Saving html file...")
    with open("../covid_cy_report.html", "w") as f:
        f.write(html_str)


def run():
    # scrape_update_data()
    # merge_datasets()
    # make_plots()
    make_html()


if __name__ == "__main__":
    run()
