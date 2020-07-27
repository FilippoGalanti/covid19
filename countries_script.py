import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import requests
import matplotlib.pyplot as plt
from countries import countries_dict
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import difflib

def countries ():

    date_url = date.today().strftime('%m-%d-%Y')
    inputValid, countries_valid  = False, False
    countries_in_scope = []

    while inputValid == False:

        url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + date_url + '.csv'
        feedback = requests.get(url)

        if feedback.status_code != 200:
            date_url = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y')
            continue
        else:
            inputValid = True

    print(countries_dict.keys())
    
    #countries in scope
    while countries_valid == False:
        country = input("Add a country or type 'continue' to move forward: ")
        
        if country == 'continue':
           countries_valid = True
           
        else:
            if country in countries_dict:
                countries_in_scope.append(country)
                print(f"{country} have been added.")
                continue
            else:
                print("Invalid input.")
                right_country = ''.join(difflib.get_close_matches(country, countries_dict, n = 1))
                print(f"Did you mean: {right_country}? {right_country} has been added")
                countries_in_scope.append(right_country)
                
    print("\n")          
    print(f"Countries that will be displayed: {', '.join(countries_in_scope)}")
    
    #Total Cases
    df = pd.read_csv(url)
    table_country = pd.pivot_table(df, values = ['Confirmed', 'Deaths'], index = 'Country_Region', aggfunc = np.sum, margins = True)
    table_country = table_country[table_country.index.isin(countries_in_scope)]

    #Daily Cases
    daily_cases_url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    df_daily_cases = pd.read_csv(daily_cases_url)
    countries_daily_cases = pd.pivot_table(df_daily_cases, index = 'Country/Region', aggfunc = np.sum, margins=True)

    #get the first avilable date (1/22/20)
    dates_list = list(df_daily_cases)[4:]
    countries_plot_cases = pd.pivot_table(df_daily_cases, values = [dates_list[0]], index = 'Country/Region', aggfunc = np.sum)
    #loop through the dates
    for i in range(1, len(dates_list)):
        append_df = pd.pivot_table(df_daily_cases, values = [dates_list[i]], index = 'Country/Region', aggfunc = np.sum)
        countries_plot_cases = pd.concat([countries_plot_cases, append_df], axis=1)
    #get the daily increases
    countries_plot_daily_cases = pd.pivot_table(df_daily_cases, values = [dates_list[0]], index = 'Country/Region', aggfunc = np.sum)
    for i in range(1, len(dates_list)):
        countries_plot_daily_cases[dates_list[i]] = countries_plot_cases[dates_list[i]] - countries_plot_cases[dates_list[i - 1]]

    countries_plot_cases = countries_plot_cases[countries_plot_cases.index.isin(countries_in_scope)].T
    countries_plot_daily_cases = countries_plot_daily_cases[countries_plot_daily_cases.index.isin(countries_in_scope)].T

    #Daily Deaths
    daily_deaths_url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    df_daily_deaths = pd.read_csv(daily_deaths_url)
    countries_daily_deaths = pd.pivot_table(df_daily_cases, index = 'Country/Region', aggfunc = np.sum, margins=True)

    #plot the first avilable date (1/22/20)
    dates_list = list(df_daily_deaths)[4:]
    countries_plot_deaths = pd.pivot_table(df_daily_deaths, values = [dates_list[0]], index = 'Country/Region', aggfunc = np.sum)
    #loop through the dates
    for i in range(1, len(dates_list)):
        append_df = pd.pivot_table(df_daily_deaths, values = [dates_list[i]], index = 'Country/Region', aggfunc = np.sum)
        countries_plot_deaths = pd.concat([countries_plot_deaths, append_df], axis=1)

    #get the daily increases
    countries_plot_daily_deaths = pd.pivot_table(df_daily_deaths, values = [dates_list[0]], index = 'Country/Region', aggfunc = np.sum)
    for i in range(1, len(dates_list)):
        countries_plot_daily_deaths[dates_list[i]] = countries_plot_deaths[dates_list[i]] - countries_plot_deaths[dates_list[i - 1]]

    countries_plot_deaths = countries_plot_deaths[countries_plot_deaths.index.isin(countries_in_scope)].T
    countries_plot_daily_deaths = countries_plot_daily_deaths[countries_plot_daily_deaths.index.isin(countries_in_scope)].T

    #set negative daily changes equal to 0
    countries_plot_daily_cases[countries_plot_daily_cases < 0] = 0
    countries_plot_daily_deaths[countries_plot_daily_deaths < 0] = 0

    #get the moving average to smooth the daily curves
    countries_plot_av_daily_cases = pd.DataFrame()
    countries_plot_av_daily_deaths = pd.DataFrame()

    for i in list(countries_plot_daily_cases):
        countries_plot_av_daily_cases[f"{i}"] = countries_plot_daily_cases[i].rolling(window = 7).mean()

    for i in list(countries_plot_daily_deaths):
        countries_plot_av_daily_deaths[f"{i}"] = countries_plot_daily_deaths[i].rolling(window = 7).mean() 

    downloadFig = input("\nDo you want to download the picture (Y/N)?").upper()

    #save dataframes to excel
    path = r'C:\Users\Filippo Galanti\Desktop\Python Course\Cool Excercises\Covid19\output_countries.xlsx'
    with pd.ExcelWriter(path) as writer:
        countries_plot_cases.to_excel(writer, sheet_name = 'Total Cases')
        countries_plot_daily_cases.to_excel(writer, sheet_name = 'Daily Cases')
        countries_plot_deaths.to_excel(writer, sheet_name = 'Total Deaths')
        countries_plot_daily_deaths.to_excel(writer, sheet_name = 'Daily Deaths')
        countries_plot_av_daily_cases.to_excel(writer, sheet_name = 'Mov Avg Cases')
        countries_plot_av_daily_deaths.to_excel(writer, sheet_name = 'Mov Avg Deaths')

    #converting date to datetime
    countries_plot_cases = countries_plot_cases.set_index(pd.to_datetime(countries_plot_cases.index))
    countries_plot_daily_cases = countries_plot_daily_cases.set_index(pd.to_datetime(countries_plot_daily_cases.index))
    countries_plot_deaths = countries_plot_deaths.set_index(pd.to_datetime(countries_plot_deaths.index))
    countries_plot_daily_deaths = countries_plot_daily_deaths.set_index(pd.to_datetime(countries_plot_daily_deaths.index))
    countries_plot_av_daily_cases = countries_plot_av_daily_cases.set_index(pd.to_datetime(countries_plot_av_daily_cases .index))
    countries_plot_av_daily_deaths = countries_plot_av_daily_deaths.set_index(pd.to_datetime(countries_plot_av_daily_deaths.index))

    max_daily_cases = countries_plot_daily_cases.sum(axis = 1).max()
    max_daily_deaths = countries_plot_daily_deaths.sum(axis = 1).max()
    max_cont_cases_increase = countries_plot_daily_cases.max(axis = 1).max()
    max_cont_deaths_increase = countries_plot_daily_deaths.max(axis = 1).max()
    id_max_cases = countries_plot_daily_cases.sum(axis = 1).idxmax()
    id_max_deaths = countries_plot_daily_deaths.sum(axis = 1).idxmax()

    #graph plotting
    fig, axes = plt.subplots(nrows = 2, ncols = 2, figsize = (14, 7), squeeze = False)
    color_list = ['#1C2833', '#7D3C98', '#E74C3C', '#27AE60', '#D4AC0D', '#DAF7A6', '#1B4F72']
    fig.patch.set_facecolor('#E5E7E9')

    countries_plot_cases.plot.line(title = 'Total Cases', legend = True, linewidth = 1, ax = axes[0, 0], grid = True, color = color_list)
    axes[0,0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[0,0].fmt_xdata = mdates.DateFormatter('%B')
    axes[0,0].legend(loc = 'best', frameon = True, fontsize = 'small')
    axes[0,0].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[0,0].set_facecolor('#F2F3F4')

    countries_plot_av_daily_cases.plot.area(title = 'Daily Cases', ax = axes[1, 0], legend = False, ylim = (0, max_daily_cases * 1.1),
                                         linewidth = 0.7, grid = True, color = color_list, stacked = True)
    axes[1,0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[1,0].fmt_xdata = mdates.DateFormatter('%B')
    axes[1,0].legend(loc = 'best', frameon = True, fontsize = 'small')
    axes[1,0].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[1,0].set_facecolor('#F2F3F4')

    countries_plot_deaths.plot.line(title = 'Total Deaths', legend = False, linewidth = 1, ax = axes[0, 1], grid = True, color = color_list)
    axes[0,1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[0,1].fmt_xdata = mdates.DateFormatter('%B')
    axes[0,1].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[0,1].set_facecolor('#F2F3F4')

    countries_plot_av_daily_deaths.plot.area(title = 'Daily Deaths', ax = axes[1, 1], legend = False, ylim = (0, max_daily_deaths * 1.1),
                                          linewidth = 0.7, grid = True, color = color_list, stacked = True)
    axes[1,1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))
    axes[1,1].grid(color = 'k', linestyle = '-', linewidth = 0.1)
    axes[1,1].fmt_xdata = mdates.DateFormatter('%B')
    axes[1,1].set_facecolor('#F2F3F4')

    if downloadFig == 'Y':
        plt.savefig(fname="Covid19_Countries.png")
    plt.show()


    
