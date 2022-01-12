import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Disable "chained_assignment" warning
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def save_figure_many_forms(fig, filename, png_w, png_h, png_scale):
    # Save figure

    # 1. This includes by default all necessary code (including Plotly.js) to render the plot
    fig.write_html(
        file=f"../plots/{filename}.html",
        include_plotlyjs="cdn",
        config=dict(displaylogo=False),
    )

    # 2. Create just a `<div>` element with the plot to embed in your web page
    fig.write_html(
        file=f"../plots/{filename}_div.html",
        include_plotlyjs=False,
        config=dict(displaylogo=False),
        full_html=False,
    )

    # 3. PNG
    fig.write_image(
        file=f"../plots/{filename}.png",
        width=png_w,
        height=png_h,
        scale=3.0,
    )


def hospitalizations_per_vaccination(df):
    """Area figure with hospizalations time series per vaccination status"""

    # Turn df to long format
    df_vacc = (
        df.drop(
            [
                "perc_hosp_unvaccinated",
                "n_hospitalized_unvaccinated",
            ],
            axis=1,
        )
        .rename(
            columns={
                "perc_hosp_vaccinated": "perc_hospitalized",
                "n_hospitalized_vaccinated": "n_hospitalized",
            }
        )
        .assign(Vaccination="Vaccinated")
    )

    df_unvacc = (
        df.drop(
            [
                "perc_hosp_vaccinated",
                "n_hospitalized_vaccinated",
            ],
            axis=1,
        )
        .rename(
            columns={
                "perc_hosp_unvaccinated": "perc_hospitalized",
                "n_hospitalized_unvaccinated": "n_hospitalized",
            }
        )
        .assign(Vaccination="Unvaccinated")
    )

    df_h1 = pd.concat([df_vacc, df_unvacc])

    # Make plot
    fig = px.area(
        df_h1,
        x="date",
        y="n_hospitalized",
        color="Vaccination",
        custom_data=["Vaccination", "perc_hospitalized"],
        width=900,
        height=600,
        color_discrete_map={
            "Unvaccinated": "#D22727",
            "Vaccinated": "#316F9A",
        },
        labels={"n_hospitalized": "Hospitalizations", "Vaccination": "Status"},
        title="Hospitalizations by vaccination status (since July 16, 2021)",
    )

    fig.update_layout(
        hoverlabel_font=dict(color="#2F2E31"),  # =white
        font=dict(size=15, color="#2F2E31"),
        legend={"traceorder": "reversed"},
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        yaxis=dict(
            showgrid=True,
            gridcolor="#FCD19C",
            gridwidth=0.2,  # tried different values, same issue
        ),
        xaxis=dict(
            showgrid=False,
            range=["2021-07-16", df_h1["date"].iloc[-1].date()],
            title="",
        ),
        hovermode="x unified",
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b>: %{y:.0f} ( %{customdata[1]:.1f}% )<extra></extra>"  # + " <br> %{x}",
    )

    # fig.show()

    # Save figure
    save_figure_many_forms(fig, "hospitalizations_per_vaccination", 900, 600, 3.0)


def hospitalizations_by_severity(df):

    # Add non-icu cases
    df["no_icu"] = df["Hospitalised Cases"] - df["Incubated Cases"]
    df["icu_nointub"] = df["Cases In ICUs"] - df["Incubated Cases"]

    # Create long-form df
    df_icu_intub = (
        df.drop(["no_icu", "icu_nointub"], axis=1)
        .rename(columns={"Incubated Cases": "Patients"})
        .assign(Category="ICU, intubated")
    )

    df_icu_no_intub = (
        df.drop(["no_icu", "Incubated Cases"], axis=1)
        .rename(columns={"icu_nointub": "Patients"})
        .assign(Category="ICU, not intubated")
    )

    df_no_icu = (
        df.drop(["icu_nointub", "Incubated Cases"], axis=1)
        .rename(columns={"no_icu": "Patients"})
        .assign(Category="not ICU")
    )

    df_icu_long = pd.concat([df_icu_intub, df_icu_no_intub, df_no_icu])

    # Plot using graph objects (allows more flexibility)
    categories = ["ICU, intubated", "ICU, not intubated", "not ICU"]
    color_map = {
        "ICU, intubated": "#8E007D",
        "ICU, not intubated": "#C800AF",
        "not ICU": "#008564",
    }
    fig = go.Figure()
    for category in categories:
        df_tmp = df_icu_long.query("Category == @category")
        fig.add_trace(
            go.Scatter(
                x=df_tmp["date"],
                y=df_tmp["Patients"],
                fill="tonexty",
                name=category,
                stackgroup="one",  # to stack them
                line=dict(color=color_map[category]),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=df_icu_long["date"],
            y=df_icu_long["Severe Cases"],
            mode="lines",
            name="Severe",
            line=dict(color="#FFBD8A", width=3),
        )  # , dash="dash", "dot", FFBD8A, "#FFA45F", #75E1FF"
    )

    fig.update_layout(
        title=dict(text="Hospitalizations by severity"),
        font=dict(size=15, color="#2F2E31"),
        width=900,
        height=600,
        legend={"traceorder": "reversed"},
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        yaxis=dict(
            title=dict(text="Hospitalizations"),
            showgrid=True,
            gridcolor="#FCD19C",
            gridwidth=0.2,  # tried different values, same issue
        ),
        xaxis=dict(
            showgrid=False,
            # range=["2021-07-16","2022-01-06"],
            title="",
        ),
        hovermode="x unified",
        hoverlabel_font=dict(color="#2F2E31"),
    )

    # fig.show()

    # Save figure
    save_figure_many_forms(fig, "hospitalizations_per_severity", 900, 600, 3.0)


def cases_hosp_death(df):
    """The classical plot with time course of cases, hospitalizations & deaths"""

    # Add 7-day moving average
    df["cases_movavg"] = df["daily new cases"].rolling(window=7, center=False).mean()

    # Adjust df
    df = df[
        [
            "date",
            "daily new cases",
            "daily deaths",
            "Hospitalised Cases",
            "cases_movavg",
        ]
    ]
    df = df.fillna(0)
    df = df.rename(
        columns={
            "daily new cases": "cases",
            "daily deaths": "deaths",
            "Hospitalised Cases": "hospitalizations",
        }
    )

    # Create long-form df
    df_cases = (
        df.drop(["deaths", "hospitalizations", "cases_movavg"], axis=1)
        .rename(columns={"cases": "number"})
        .assign(Category="Cases")
    )

    df_cases_movavg = (
        df.drop(["deaths", "hospitalizations", "cases"], axis=1)
        .rename(columns={"cases_movavg": "number"})
        .assign(Category="Cases, 7-day average")
    )

    df_deaths = (
        df.drop(["cases", "hospitalizations", "cases_movavg"], axis=1)
        .rename(columns={"deaths": "number"})
        .assign(Category="Deaths")
    )

    df_hospitalizations = (
        df.drop(["cases", "deaths", "cases_movavg"], axis=1)
        .rename(columns={"hospitalizations": "number"})
        .assign(Category="hospitalizations")
    )

    df_long = pd.concat([df_cases, df_cases_movavg, df_deaths, df_hospitalizations])

    # Make plot

    fig = px.line(
        df_long,
        x="date",
        y="number",
        color="Category",
        custom_data=["Category"],
        width=900,
        height=600,
        color_discrete_map={
            "Cases": "#C5C5C5",
            "Cases, 7-day average": "#1379FD",
            "hospitalizations": "#FB202B",
            "Deaths": "#FFAE00",  # "#48D7AC",#"#FFB220",
        },
        labels={"number": "Number", "date": "", "Category": ""},
        title="Cases, hospitalizations, Deaths",
    )

    fig.update_layout(
        font=dict(size=15, color="#2F2E31"),
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        yaxis=dict(
            showgrid=True,
            gridcolor="#FCD19C",
            gridwidth=0.2,  # tried different values, same issue
        ),
        xaxis=dict(
            showgrid=False,
            # range=["2021-07-16","2022-01-06"],
            title="",
        ),
        hovermode="x unified",
    )

    fig.update_traces(
        hovertemplate="%{customdata[0]}: %{y:.0f} <extra></extra>", line=dict(width=4)
    )

    # fig.show()

    save_figure_many_forms(fig, "cases_hosp_deaths", 900, 600, 3.0)

    ##############################################################
    # Plot separately covid-induced deaths + 14-day moving average
    ##############################################################

    # Create death + death_moving_average
    df_death = df_long.query("Category=='Deaths'")
    df_death_avg = df_death.copy()
    df_death_avg["number"] = (
        df_death_avg["number"].rolling(window=14, center=False).mean()
    )
    df_death_avg["Category"] = "Deaths, 14-day average"

    df_death_long = pd.concat([df_death, df_death_avg])

    fig = px.line(
        df_death_long,
        x="date",
        y="number",
        color="Category",
        custom_data=["Category"],
        width=900,
        height=600,
        color_discrete_map={
            "Deaths": "#B9C4C5",
            "Deaths, 14-day average": "#FFAE00",  # "#FFAE00"# "#FFB220"
        },
        labels={"number": "Number", "date": "", "Category": ""},
        title="Deaths",
    )

    fig.update_layout(
        font=dict(size=15, color="#2F2E31"),
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        yaxis=dict(
            showgrid=True,
            gridcolor="#FCD19C",
            gridwidth=0.2,  # tried different values, same issue
        ),
        xaxis=dict(
            showgrid=False,
            # range=["2021-07-16","2022-01-06"],
            title="",
        ),
        hovermode="x unified",
    )

    fig.update_traces(hovertemplate="%{customdata[0]}: %{y:.0f}<extra></extra>")

    fig.update_traces(line=dict(width=7), selector=dict(name="Deaths, 14-day average"))

    # fig.show()

    save_figure_many_forms(fig, "deaths", 900, 600, 3.0)


def ascending_weeks_from_one(week_list):
    """return weeks number as increasing and not resetted by year changes"""

    ascending_weeks = []
    new_week = week_list[0]

    for i, w in enumerate(week_list):
        if (w != new_week) & (w != week_list[i - 1]):
            new_week += 1
        ascending_weeks.append(new_week)
    ascending_weeks = [wk - ascending_weeks[0] + 1 for wk in ascending_weeks]

    return ascending_weeks


# Add date corresponding to middle (Thursday) of each week


def date_in_mid_of_week(year_week):
    """returns date of middle of this week"""

    weekdates = []
    for day in range(7):
        week_date = datetime.strptime(year_week + "-{}".format(day), "%Y-W%W-%w")
        weekdates.append(week_date)
    date_mid_week = [dt for dt in weekdates if dt.weekday() == 3]  # Thursday

    return date_mid_week[0]


def hospitalizations_per_vacc_per_100_00(df, dfv):
    """Plotting hospitalizations per vaccination status per 100_000 (vaccinated or unvaccinated)people"""

    # Add weeks to hospitalization_df in ascending order (ie not reset by year)

    # Add weeks ("%V" ISO week number, with Monday as first day of week)
    df["week"] = df["date"].dt.strftime("%V")

    # Get weeks in ascending format
    week_tmp = df["week"].astype(int).values
    df["week"] = ascending_weeks_from_one(week_tmp)

    # Add week day name
    df["weekday"] = df["date"].dt.day_name()

    # Get first Thursday in list (day 0 is Monday)
    first_mid_week = df.query("weekday == 'Thursday'").loc[:, "date"].iloc[0]

    # For each week add middle-of-week's date
    df["midweek"] = df["week"].apply(lambda x: first_mid_week + timedelta(7 * (x - 1)))

    # Group_by - midweek
    dfhosp = df.groupby("midweek").mean()

    dfhosp = dfhosp.reset_index().query("midweek >= '2021-07-16'")
    dfhosp["midweek"].iloc[0]

    # Add middle-of-week for vaccination dataset
    dfv["midweek"] = dfv["YearWeekISO"].apply(lambda x: date_in_mid_of_week(x))

    # Get vacc for all data for target group "Age18+"

    age_groups_18plus = [
        "Age18_24",
        "Age25_49",
        "Age50_59",
        "Age60_69",
        "Age70_79",
        "Age80+",
    ]
    age_groups = [
        "ALL",
        "Age10_14",
        "Age15_17",
        "Age18_24",
        "Age25_49",
        "Age50_59",
        "Age60_69",
        "Age70_79",
        "Age80+",
        "Age18+",
    ]

    df18plus = (
        dfv.query("TargetGroup in @age_groups_18plus")
        .groupby(["midweek", "Vaccine"])
        .sum()
        .assign(TargetGroup="Age18+")
        .reset_index()
    )
    df18plus["Population"] = dfv["Population"].iloc[0]

    dfv2 = pd.concat([dfv, df18plus])
    dfv2 = dfv2.query("TargetGroup in @age_groups")
    dfv2["CompletingVaccinationScheme"] = dfv2.apply(
        lambda x: x["FirstDose"] if x["Vaccine"] == "JANSS" else x["SecondDose"], axis=1
    )
    dfv2["AtLeastOneDose"] = dfv2["FirstDose"]
    # OPEN QUESTION: Does the "DoseAdditional1" for Janssen refer to 3rd dose or is it an another term for second one?
    # For now I am working assuming the second case.
    dfv2["Boosted"] = dfv2.apply(
        lambda x: x["SecondDose"] + x["DoseAdditional1"]
        if x["Vaccine"] == "JANSS"
        else x["DoseAdditional1"],
        axis=1,
    )

    # Select a target group & Groupby Date and sum
    df_trg = dfv2.copy()
    df_trg = (
        dfv2.query("TargetGroup == 'Age18+'").groupby("midweek").sum().reset_index()
    )

    df_trg["Population"] = dfv2["Population"].iloc[0]
    df_trg["Denominator"] = dfv2.query("TargetGroup == 'Age18+'")["Denominator"].iloc[0]

    # Add cumulative sum and percentage of target group population
    df_trg["ComplVacc_cumsum"] = df_trg["CompletingVaccinationScheme"].cumsum()
    df_trg["ComplVacc_percent"] = df_trg.apply(
        lambda x: x["ComplVacc_cumsum"] / x["Denominator"] * 100, axis=1
    )

    df_trg["AtLeastOne_cumsum"] = df_trg["AtLeastOneDose"].cumsum()
    df_trg["AtLeastOne_percent"] = df_trg.apply(
        lambda x: x["AtLeastOne_cumsum"] / x["Denominator"] * 100, axis=1
    )

    df_trg["Boosted_cumsum"] = df_trg["Boosted"].cumsum()
    df_trg["Boosted_percent"] = df_trg.apply(
        lambda x: x["Boosted_cumsum"] / x["Denominator"] * 100, axis=1
    )

    # Merge hospitalization  & vaccination dataframes

    colums_to_merge = [
        "midweek",
        "Denominator",
        "CompletingVaccinationScheme",
        "AtLeastOneDose",
        "Boosted",
        "ComplVacc_cumsum",
        "ComplVacc_percent",
        "AtLeastOne_cumsum",
        "AtLeastOne_percent",
        "Boosted_cumsum",
        "Boosted_percent",
    ]

    dfvh = dfhosp.merge(df_trg[colums_to_merge], on="midweek", how="left")

    # Add hospitalizations per 100_000 vaccinated and 100_000 unvaccinated
    dfvh["Hosp_in_100_000_vac"] = (
        dfvh["n_hospitalized_vaccinated"] * 100_000 / dfvh["ComplVacc_cumsum"]
    )
    dfvh["Hosp_in_100_000_unvac"] = (
        dfvh["n_hospitalized_unvaccinated"]
        * 100_000
        / (dfvh["Denominator"] - dfvh["ComplVacc_cumsum"])
    )

    dfvh["ratio_hosp_unvacc_vacc"] = (
        dfvh["Hosp_in_100_000_unvac"] / dfvh["Hosp_in_100_000_vac"]
    )

    # Turn df to long format
    df_vacc = (
        dfvh.drop(["Hosp_in_100_000_unvac"], axis=1)
        .rename(columns={"Hosp_in_100_000_vac": "n_hospitalized"})
        .assign(Vaccination="Vaccinated")
    )

    df_unvacc = (
        dfvh.drop(["Hosp_in_100_000_vac"], axis=1)
        .rename(columns={"Hosp_in_100_000_unvac": "n_hospitalized"})
        .assign(Vaccination="Unvaccinated")
    )

    dfvhl = pd.concat([df_vacc, df_unvacc])

    # Make plot

    fig = px.area(
        dfvhl.query("n_hospitalized == n_hospitalized"),  # get rid of nans
        x="midweek",
        y="n_hospitalized",
        color="Vaccination",
        custom_data=["Vaccination", "ratio_hosp_unvacc_vacc"],
        width=900,
        height=600,
        color_discrete_map={
            "Unvaccinated": "#D22727",
            "Vaccinated": "#316F9A",
        },
        labels={"n_hospitalized": "Hospitalizations per 100 000 ", "Vaccination": ""},
        title="Hospitalizations by vaccination status per 100 000 (vacc & unvacc) people <br>(since July 16, 2021)",
    )

    fig.update_layout(
        hoverlabel_font=dict(color="#2F2E31"),  # =white
        font=dict(size=15, color="#2F2E31"),
        legend={"traceorder": "reversed"},
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        yaxis=dict(
            showgrid=True,
            gridcolor="#FCD19C",
            gridwidth=0.2,  # tried different values, same issue
        ),
        xaxis=dict(
            showgrid=False,
            # range=["2021-07-16", dfvhl["midweek"].iloc[-1].date()],
            title="",
        ),
        hovermode="x unified",
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[1]:.1f} times</b> more likely to <br>be hospitalized if unvacc."
        + "<br><b>%{customdata[0]}</b>: %{y:.0f} <extra></extra>",
        selector=dict(name="Unvaccinated"),
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b>: %{y:.0f} <extra></extra>",
        selector=dict(name="Vaccinated"),
    )

    # fig.update_layout(legend=dict(
    #     orientation="h",
    #     yanchor="bottom",
    #     y=0.98,
    #     xanchor="right",
    #     x=0.9
    # ))

    # fig.show()

    save_figure_many_forms(fig, "hospitalizations_per_vacc_per_100_000", 900, 600, 3.0)

    #################################################################################
    # Plot ratio unvacc:vacc for hospitalizations per 100_000 (vacc & unvacc) people
    ##################################################################################

    # get rid of nans & sort
    df_tmp = dfvhl.query("n_hospitalized == n_hospitalized").sort_values(by="midweek")

    fig = px.line(
        df_tmp,
        x="midweek",
        y="ratio_hosp_unvacc_vacc",
        width=800,
        height=500,
        labels={"ratio_hosp_unvacc_vacc": "Ratio unvaccinated : vaccinated"},
        title="How many times more likely is to be hospitalized if unvaccinated",
    )

    fig.update_layout(
        font=dict(size=15, color="#2F2E31"),
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        yaxis=dict(
            showgrid=True,
            gridcolor="#FCD19C",
            gridwidth=0.2,  # tried different values, same issue
        ),
        xaxis=dict(showgrid=False, title=""),
    )

    fig.update_traces(
        hovertemplate="%{y:.0f} times more likely<extra></extra>",
        line=dict(width=4, color="#F53E94"),
        # selector=dict(name="Deaths, 14-day average")
    )

    # fig.show()

    save_figure_many_forms(
        fig, "hospitalizations_per_vacc_per_100_000_ratio", 900, 600, 3.0
    )


def group_stats_targetgroup(df, target_str):
    """Return vaccination stats for this target group in the form of dataframe"""

    DOUBLE_DOSE_VACC = ["COM", "MOD", "AZ"]
    ONE_DOSE_VACC = ["JANSS"]
    COLS_OF_INTEREST = ["FirstDose", "SecondDose", "DoseAdditional1"]

    # Get target population
    target_population = (
        df.query("TargetGroup==@target_str").loc[:, "Denominator"].iloc[0]
    )

    # Seperate single- and double-dose vaccine data & sum
    df_odv = (
        df.query("TargetGroup==@target_str & Vaccine in @ONE_DOSE_VACC")
        .loc[:, COLS_OF_INTEREST]
        .sum()
    )

    df_ddv = (
        df.query("TargetGroup==@target_str & Vaccine in @DOUBLE_DOSE_VACC")
        .loc[:, COLS_OF_INTEREST]
        .sum()
    )

    # Number of observations
    # order for stack bar is : boosted, fully-vaccinated, at-least-one dose, unvaccinated
    n_vacc_atleastone = df_odv["FirstDose"] + df_ddv["FirstDose"]
    n_vacc_full = df_odv["FirstDose"] + df_ddv["SecondDose"]
    n_vacc_boost = (
        df_odv["SecondDose"] + df_odv["DoseAdditional1"] + df_ddv["DoseAdditional1"]
    )
    n_unvacc = target_population - n_vacc_atleastone

    # Difference from previous
    dif_prev_boost = n_vacc_boost
    dif_prev_full = n_vacc_full - n_vacc_boost
    dif_prev_atleastone = n_vacc_atleastone - n_vacc_full
    dif_prev_unvacc = n_unvacc

    vacc_info = {
        "vacc_category": [
            "Boosted",
            "Fully vaccinated",
            "At least one dose",
            "Unvaccinated",
        ],
        "n_vaccinations": [n_vacc_boost, n_vacc_full, n_vacc_atleastone, n_unvacc],
        "n_diff_prev_categ": [
            dif_prev_boost,
            dif_prev_full,
            dif_prev_atleastone,
            dif_prev_unvacc,
        ],
    }

    df_target = pd.DataFrame(vacc_info)
    df_target["%_vaccinations"] = df_target["n_vaccinations"] / target_population * 100
    df_target["%_diff_prev_categ"] = (
        df_target["n_diff_prev_categ"] / target_population * 100
    )
    df_target["target_group"] = target_str
    df_target["target_population"] = target_population

    return df_target


def vaccinations_by_age(dfv):

    # Add data for 18+
    age_groups_18plus = [
        "Age18_24",
        "Age25_49",
        "Age50_59",
        "Age60_69",
        "Age70_79",
        "Age80+",
    ]

    df18plus = (
        dfv.query("TargetGroup in @age_groups_18plus")
        .groupby(["YearWeekISO", "Vaccine"])
        .sum()
        .assign(TargetGroup="Age18+")
        .reset_index()
    )
    df18plus["Population"] = dfv["Population"].iloc[0]

    dfv1 = pd.concat([dfv, df18plus])

    # Get stats for different groups

    # print(dfv1["TargetGroup"].unique())
    target_groups = [
        "ALL",
        "Age18+",
        "Age10_14",
        "Age15_17",
        "Age18_24",
        "Age25_49",
        "Age50_59",
        "Age60_69",
        "Age70_79",
        "Age80+",
    ]
    list_of_dfs = [
        group_stats_targetgroup(dfv1, target_group) for target_group in target_groups
    ]

    # Concatenate dfs to have all data in one
    df_grp = pd.concat(list_of_dfs)

    # Fix target group names
    df_grp["target_group"] = df_grp["target_group"].replace({"ALL": "All ages"})
    df_grp["target_group"] = df_grp["target_group"].str.replace("Age", "")
    df_grp["target_group"] = df_grp["target_group"].str.replace("_", "-")

    # Actual Plot

    fig = px.bar(
        df_grp,
        x="target_group",
        y="%_diff_prev_categ",
        color="vacc_category",
        color_discrete_map={
            "Boosted": "#0C456D",
            "Fully vaccinated": "#316F9A",
            "At least one dose": "#79A9CB",
            "Unvaccinated": "#D22727",
        },
        labels={
            "%_diff_prev_categ": "Percentage",
            "vacc_category": "Category",
            "target_group": "Age group",
        },
        custom_data=["vacc_category", "%_vaccinations"],
        width=900,
        height=600,
        title="Cyprus immunity wall",
    )
    # hover_data={"%_vaccinations" : ":.0f",
    #           "%_diff_prev_categ" : False,
    #           "n_stack_bar": False},

    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b> %{customdata[1]:.0f}%<extra></extra>",
        # width=[0.6]*len(target_groups)
    )

    fig.update_layout(
        font=dict(size=15, color="#2F2E31"),
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            ticktext=["<b>All<br>ages</b>", "<b>18+</b>"]
            + list(df_grp["target_group"].unique()[2:]),
            range=[-1, 10],
        ),
        legend={"traceorder": "reversed"},
        plot_bgcolor="#FFEBD9",
        paper_bgcolor="#FFEBD9",
        hoverlabel_font=dict(color="white"),
        bargap=0.25,
    )
    # fig.show()

    save_figure_many_forms(fig, "vaccinations_by_age", 900, 600, 3.0)
