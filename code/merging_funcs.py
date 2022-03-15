import numpy as np
import pandas as pd


def add_missing_cases_deaths_to_group_data(df1, df2):
    """Add cases & deaths for dates missing from group_data"""

    print("Merging group_data with data from individual pdf reports..")

    last_date_group = df1["date"].iloc[-1].date()
    last_date_indivreports = df2["date"].iloc[-1].date()
    if last_date_indivreports > last_date_group:
        columns_keep = [
            "date",
            "daily new cases",
            "daily deaths",
            "hospitalizations_dailyrep",
        ]  # columns to add now
        df_extra = df2[columns_keep].query(
            "date > @last_date_group"
        )  # get missing dates
        df_extra = df_extra.rename(
            columns={"hospitalizations_dailyrep": "Hospitalised Cases"}
        )
        columns_diff = [
            col
            for col in df1.columns.to_list()
            if col not in df_extra.columns.to_list()
        ]  # get difference of columns
        for col in columns_diff:
            df_extra[col] = np.nan  # fill new columns with nan

        # Concatenate
        df_extra = pd.concat([df1, df_extra], axis=0)
    else:
        print("No new additional cases & death info..")
        df_extra = df1

    # Apply corrections to extended stats
    # TODO: Apply this corrections in a different function
    # Corrections 1: In summary database from data.gov.cy deaths for 2022-01-18 are 3 but according to the pdf-report is 5
    # -> use 5 (they initially announced 3, then updated to 5)
    # print(df_extra.query("date == '2022-01-18'"))
    df_extra.loc[df_extra["date"] == "2022-01-18", "daily deaths"] = 5.0
    # print(df_extra.query("date == '2022-01-18'"))
    # Corrections 2: In summary database from data.gov.cy hospitalizations for 2022-01-23 are 329 but according to the pdf-report is 238
    df_extra.loc[df_extra["date"] == "2022-01-23", "Hospitalised Cases"] = 238

    return df_extra


def add_vaccination_percentage(df1, df_vacc):
    """Add vaccination info for hospitalizations"""

    df_vacc_info = df_vacc[
        [
            "date",
            "perc_hosp_unvaccinated",
            "perc_hosp_vaccinated",
            "hospitalizations_dailyrep",
        ]
    ]
    df_vacc_info = df_vacc_info.rename(
        columns={"hospitalizations_dailyrep": "Hospitalizations from reports"}
    )
    df_extent = df1.merge(df_vacc_info, on="date", how="left")
    # last_date_boost = str(df_extent["date"].iloc[-1].date()).replace("-", "_")

    # Add numer of vacc and uvnacc hospitalisations
    df_extent["n_hospitalized_unvaccinated"] = (
        df_extent["Hospitalised Cases"] * df_extent["perc_hosp_unvaccinated"] / 100
    )
    df_extent["n_hospitalized_vaccinated"] = (
        df_extent["Hospitalised Cases"] * df_extent["perc_hosp_vaccinated"] / 100
    )

    return df_extent
