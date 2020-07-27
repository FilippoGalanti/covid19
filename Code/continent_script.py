import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import requests
import matplotlib.pyplot as plt
from countries import countries_dict
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

def continents ():

    date_url = date.today().strftime('%m-%d-%Y')
    inputValid = False
    continent_list = ['Africa', 'Asia', 'Europa', 'North America', 'Oceania', 'Other', 'South America']

    while inputValid == False:

        url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + date_url + '.csv'
        feedback = requests.get(url)

        if feedback.status_code != 200:
            date_url = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
            continue
        else:
            inputValid = True

    #Total Cases
    df = pd.read_csv(url)
    df['Continent'] = df['Country_Region'].map(countries_dict)

    table_country = pd.pivot_table(df, values = ['Confirmed', 'Deaths'], index = 'Country_Region', aggfunc = np.sum, margins = True)
    table_continent = pd.pivot_table(df, values = ['Confirmed', 'Deaths'], index = 'Continent', aggfunc = np.sum, margins=True).sort_values(by='Confirmed', ascending=False)
    table_continent['Mortality'] = (table_continent['Deaths'] / table_continent['Confirmed']).map(lambda n: '{:.2%}'.format(n))
    total_confirmed = df['Confirmed'].sum()
    total_deaths = df['Deaths'].sum()

    #Daily Cases
    daily_cases_url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    df_daily_cases = pd.read_csv(daily_cases_url)
    df_daily_cases.insert(2, column = "Continent", value = df_daily_cases['Country/Region'].map(countries_dict))
    df_daily_cases['Cases Increase'] = (df_daily_cases.iloc[:,-1] - df_daily_cases.iloc[:,-2])
    continent_daily_cases = pd.pivot_table(df_daily_cases, values = ['Cases Increase'], index = 'Continent', aggfunc = np.sum, margins=True)

    #get the first avilable date (1/22/20)
    dates_list = list(df_daily_cases)[5:-1]
    continent_plot_cases = pd.pivot_table(df_daily_cases, values = [dates_list[0]], index = 'Continent', aggfunc = np.sum)
    #loop through the dates
    for i in range(1, len(dates_list)):
        append_df = pd.pivot_table(df_daily_cases, values = [dates_list[i]], index = 'Continent', aggfunc = np.sum)
        continent_plot_cases = pd.concat([continent_plot_cases, append_df], axis=1)
    #get the daily increases
    continent_plot_daily_cases = pd.pivot_table(df_daily_cases, values = [dates_list[0]], index = 'Continent', aggfunc = np.sum)
    for i in range(1, len(dates_list)):
        continent_plot_daily_cases[dates_list[i]] = continent_plot_cases[dates_list[i]] - continent_plot_cases[dates_list[i - 1]]

    continent_plot_cases = continent_plot_cases.T
    continent_plot_daily_cases = continent_plot_daily_cases.T

    #Daily Deaths
    daily_deaths_url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    df_daily_deaths = pd.read_csv(daily_deaths_url)
    df_daily_deaths.insert(2, column = "Continent", value = df_daily_cases['Country/Region'].map(countries_dict))
    df_daily_deaths['Death Increase'] = (df_daily_deaths.iloc[:,-1] - df_daily_deaths.iloc[:,-2])
    continent_daily_deaths = pd.pivot_table(df_daily_deaths, values = ['Death Increase'], index = 'Continent', aggfunc = np.sum, margins=True)

    #plot the first avilable date (1/22/20)
    dates_list = list(df_daily_deaths)[5:-1]
    continent_plot_deaths = pd.pivot_table(df_daily_deaths, values = [dates_list[0]], index = 'Continent', aggfunc = np.sum)
    #loop through the dates
    for i in range(1, len(dates_list)):
        append_df = pd.pivot_table(df_daily_deaths, values = [dates_list[i]], index = 'Continent', aggfunc = np.sum)
        continent_plot_deaths = pd.concat([continent_plot_deaths, append_df], axis=1)

    #get the daily increases
    continent_plot_daily_deaths = pd.pivot_table(df_daily_deaths, values = [dates_list[0]], index = 'Continent', aggfunc = np.sum)
    for i in range(1, len(dates_list)):
        continent_plot_daily_deaths[dates_list[i]] = continent_plot_deaths[dates_list[i]] - continent_plot_deaths[dates_list[i - 1]]

    continent_plot_deaths = continent_plot_deaths.T
    continent_plot_daily_deaths = continent_plot_daily_deaths.T

    #Concatenate into a single df the cases/deaths tables
    df_daily_concat = pd.concat([table_continent, continent_daily_cases, continent_daily_deaths], axis=1)

    max_daily_cases = continent_plot_daily_cases.sum(axis = 1).max()
    max_daily_deaths = continent_plot_daily_deaths.sum(axis = 1).max()
    max_cont_cases_increase = continent_plot_daily_cases.max(axis = 1).max()
    max_cont_deaths_increase = continent_plot_daily_deaths.max(axis = 1).max()
    id_max_cases = continent_plot_daily_cases.sum(axis = 1).idxmax()
    id_max_deaths = continent_plot_daily_deaths.sum(axis = 1).idxmax()

    #set negative daily changes equal to 0
    continent_plot_daily_cases[continent_plot_daily_cases < 0] = 0
    continent_plot_daily_deaths[continent_plot_daily_deaths < 0] = 0

    #get the moving average to smooth the daily curves
    continent_plot_av_daily_cases = pd.DataFrame()
    continent_plot_av_daily_deaths = pd.DataFrame()

    for i in list(continent_plot_daily_cases):
        continent_plot_av_daily_cases[f"{i}"] = continent_plot_daily_cases[i].rolling(window = 7).mean()

    for i in list(continent_plot_daily_deaths):
        continent_plot_av_daily_deaths[f"{i}"] = continent_plot_daily_deaths[i].rolling(window = 7).mean()    

    #Print Output Information
    print("\n")
    print(f"Last Updated on {date_url}")
    print("\n")
    print(f"Total Cases {total_confirmed:,} / total deaths {total_deaths:,}. Global Mortality Rate: {total_deaths / total_confirmed:.2%}.")
    print("\n")
    print(df_daily_concat)
    print(f"World Records: most cases {max_daily_cases:,} on {id_max_cases } - most deaths {max_daily_deaths:,} on {id_max_deaths}.")

    #converting date to datetime
    continent_plot_cases = continent_plot_cases.set_index(pd.to_datetime(continent_plot_cases.index))
    continent_plot_daily_cases = continent_plot_daily_cases.set_index(pd.to_datetime(continent_plot_daily_cases.index))
    continent_plot_deaths = continent_plot_deaths.set_index(pd.to_datetime(continent_plot_deaths.index))
    continent_plot_daily_deaths = continent_plot_daily_deaths.set_index(pd.to_datetime(continent_plot_daily_deaths.index))
    continent_plot_av_daily_cases = continent_plot_av_daily_cases.set_index(pd.to_datetime(continent_plot_av_daily_cases .index))
    continent_plot_av_daily_deaths = continent_plot_av_daily_deaths.set_index(pd.to_datetime(continent_plot_av_daily_deaths.index))

    downloadFig = input("\nDo you want to download the picture (Y/N)?").upper()

    #save dataframes to excel
    path = r'C:\Users\Filippo Galanti\Desktop\Python Course\Cool Excercises\Covid19\output.xlsx'
    with pd.ExcelWriter(path) as writer:
        df_daily_concat.to_excel(writer, sheet_name = 'Daily Output')
        continent_plot_cases.to_excel(writer, sheet_name = 'Total Cases')
        continent_plot_daily_cases.to_excel(writer, sheet_name = 'Daily Cases')
        continent_plot_deaths.to_excel(writer, sheet_name = 'Total Deaths')
        continent_plot_daily_deaths.to_excel(writer, sheet_name = 'Daily Deaths')
        continent_plot_av_daily_cases.to_excel(writer, sheet_name = 'Mov Avg Cases')
        continent_plot_av_daily_deaths.to_excel(writer, sheet_name = 'Mov Avg Deaths')

    #graph plotting
    fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (14, 7), squeeze = False)
    color_list = ['#1C2833', '#7D3C98', '#E74C3C', '#27AE60', '#D4AC0D', '#DAF7A6', '#1B4F72']
    fig.patch.set_facecolor('#E5E7E9')

    continent_plot_cases.plot.line(title = 'Total Cases', legend = True, linewidth = 1, ax = axes[0, 0], grid = True, color = color_list)
    axes[0,0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[0,0].fmt_xdata = mdates.DateFormatter('%B')
    axes[0,0].legend(loc = 'best', frameon = True, fontsize = 'small')
    axes[0,0].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[0,0].set_facecolor('#F2F3F4')

    continent_plot_av_daily_cases.plot.area(title = 'Daily Cases', ax = axes[1, 0], legend = False, ylim = (0, max_daily_cases * 1.1),
                                         linewidth = 0.7, grid = True, color = color_list, stacked = True)
    axes[1,0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[1,0].fmt_xdata = mdates.DateFormatter('%B')
    axes[1,0].legend(loc = 'best', frameon = True, fontsize = 'small')
    axes[1,0].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[1,0].set_facecolor('#F2F3F4')

    continent_plot_deaths.plot.line(title = 'Total Deaths', legend = False, linewidth = 1, ax = axes[0, 1], grid = True, color = color_list)
    axes[0,1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[0,1].fmt_xdata = mdates.DateFormatter('%B')
    axes[0,1].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[0,1].set_facecolor('#F2F3F4')

    continent_plot_av_daily_deaths.plot.area(title = 'Daily Deaths', ax = axes[1, 1], legend = False, ylim = (0, max_daily_deaths * 1.1),
                                          linewidth = 0.7, grid = True, color = color_list, stacked = True)
    axes[1,1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[1,1].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[1,1].fmt_xdata = mdates.DateFormatter('%B')
    axes[1,1].set_facecolor('#F2F3F4')

    if downloadFig == 'Y':
            plt.savefig(fname="Covid19_Continents.png")
    plt.show()
