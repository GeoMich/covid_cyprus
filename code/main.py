import pandas as pd
import scraping_funcs as scr
import merging_funcs as mrg
import plots
import os
import utils as ut
import html_func as h

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
    plots.cases_hosp_death(df)
    plots.hospitalizations_per_vaccination(df)
    plots.hospitalizations_per_vacc_per_100_00(df, dfv)
    plots.hospitalizations_by_severity(df)
    plots.vaccinations_by_age(dfv)


def run():
    scrape_update_data()
    merge_datasets()
    make_plots()
    h.make_html_eng()
    h.make_html_gr()
    h.git_push_new_html()


if __name__ == "__main__":
    run()
