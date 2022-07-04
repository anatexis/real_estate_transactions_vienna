'''
get pricing data from the web or a CSV file, explore it, and plot it.
author: christoph kugler
date: 2022-06-13
'''
import textwrap
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import numpy as np


#%%

#fertig glaube ich

def read_csv(path = "https://go.gv.at/l9kaufpreissammlungliegenschaften"):
    '''
    Read the data of real estate transaction from the internet (default)
    or from your computer and return a dataframe.
    The csv-file will be stored in the same folder as script!
    (even if you did save it already somewhere else on your computer, e.g. in "Downloads".)
    '''


    #check if data is already saved as csv file in same folder as this script:

    # if file exists, read csv file from folder:
    csv_file = "kaufpreissammlung-liegenschaften.csv"
    loc_path = Path(csv_file)

    if loc_path.is_file():
        print(f'The file {csv_file} has already been downloaded')
        print(f"Reading data from {loc_path}")

        df = pd.read_csv(csv_file, sep=";", encoding="Latin-1", low_memory=False, parse_dates=["Erwerbsdatum", "BJ"])

        df["BJ"] = df["BJ"].dt.year.astype("Int64") # to get just year

    else:
        print(f'The file {csv_file} does not exist')
        print("Reading data from: " + path)

        df = pd.read_csv(path, sep=";", low_memory=False , thousands=".", decimal=",", header=0, encoding="Latin-1",
                         names=["KG.Code", "Katastralgemeinde", "EZ", "PLZ", "Strasse", "ON", "Gst.", "Gst.Fl.",
                                    "ErwArt",
                                    "Erwerbsdatum", "Widmung", "Bauklasse", "Gebäudehöhe", "Bauweise", "Zusatz",
                                    "Schutzzone", "Wohnzone", "öZ", "Bausperre", "seit/bis", "zuordnung", "Geschoße",
                                    "parz.", "VeräußererCode", "Erwerbercode", "Zähler", "Nenner", "BJ", "TZ",
                                    "Kaufpreis EUR",
                                    "EUR/m2 Gfl.", "AbbruchfixEU", "m3 Abbruch", "AbbruchkostEU", "FreimachfixEU",
                                    "Freimachfläche", "FreimachkostEU", "Baureifgest", "% Widmung", "Baurecht", "Bis",
                                    "auf EZ", "Stammeinlage", "sonst_wid", "sonst_wid_prz", "ber. Kaufpreis",
                                    "Bauzins"], parse_dates=["BJ"])

        df["Erwerbsdatum"] = pd.to_datetime(df["Erwerbsdatum"].astype(str), format='%d%m%Y.0', errors='coerce')
        # if "Erwerbsdatum" is later than dt.today (e.g. if the data is from the future),
        # the date is set to null
        df["Erwerbsdatum"] = df["Erwerbsdatum"].where(df["Erwerbsdatum"] <= dt.datetime.today(), None)


        # Get Baujahr to just show the year, use Int64 bc there are NAs in the data
        df["BJ"] = pd.to_datetime(df["BJ"], format='%Y', errors='coerce').dt.year.astype("Int64")



        # get "Bauzins" to type float (from "EUR 1.234.523,34" to 1234523.34)
        df["Bauzins"] = df["Bauzins"].str.replace("EUR", "")
        df["Bauzins"] = df["Bauzins"].str.replace(".", "")
        df["Bauzins"] = df["Bauzins"].str.replace(",", ".")
        df["Bauzins"] = df["Bauzins"].astype(float)


    # if not already saved save file in folder
    if loc_path.is_file():
        return df

    else:
        # save the dataframe to a csv file and store it in the same folder as this script
        df.to_csv("kaufpreissammlung-liegenschaften.csv", sep=";", encoding="Latin-1", index=False)
        return df

# %%
def show_specific_columns(df,which_colums):
    ''' return dataframe with certain columns
    either all columns (which_columns = "all")
    the following columns (which_columns = "predefined")
    'zuordnung', 'BJ', 'Gebäudehöhe', 'KG.Code', 'Erwerbsdatum', 'Strasse', "ON", 'Gst.Fl.', 'AbbruchkostEU', 'ber. Kaufpreis', 'Bauzins'
    or a user-input list of columns (which_columns = *user input*)
    '''
    if which_colums == [["predefined"]]:
        return df[['Erwerbsdatum','zuordnung', 'BJ', 'Gebäudehöhe', 'KG.Code',  'Strasse', "ON",
     'Gst.Fl.', 'AbbruchkostEU', 'ber. Kaufpreis', 'Bauzins']]
    else:
        which_colums = which_colums[0]
        return df[which_colums]







#%%
def sort_by_column(df, column, desc=False):
    '''
    Sort a dataframe by a column.
    Default is ascending.
    '''
    return df.sort_values(by=column, ascending=not desc)


# %%


def show_certain_KG(df, KG_code, column="KG.Code"):
    '''
    Filter rows for a certain KG.
    enter KG code without leading 0 (as shown in output of get_list_of_KG())
    to get a list of all KG codes, run get_list_of_KG()

    '''
    df = df[df[column] == KG_code]
    return df


def get_list_of_KG():
    '''
    scrape the KG from https://de.wikipedia.org/wiki/Wiener_Katastralgemeinden with BeautifulSoup
    and return a dataframe with the KG code, name, and area.
    '''
    import requests
    from bs4 import BeautifulSoup
    url = "https://de.wikipedia.org/wiki/Wiener_Katastralgemeinden"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable zebra"})
    df = pd.read_html(str(table))[0]
    df = df.iloc[:, [0, 1, 3, 5]]
    return df

#%%
def describe_column(df,column):
    '''
    describe a column of a dataframe
    '''
    return df[column].describe()

#%%

def plot_column(df,ycolumn, xcolumn="Erwerbsdatum"):
    '''
    plot two column of a dataframe
    one default column: "Erwerbsdatum"
    one user-input column
    '''
    df.plot.scatter(x=xcolumn, y=ycolumn)
    if args.output:
        '''Save plot to file'''
        plt.savefig(str(Path(args.output))+"/_"+ycolumn+"_"+xcolumn+".png")
        print("Plot saved to " + args.output)
    else:
        plt.show()

#%%

def column_correlation(df, column1, column2):
    '''
    correlation between two columns of a dataframe
    '''
    return df[column1].corr(df[column2])

#%%

def correlation_matrix(df):
    '''
    plot correlation matrix of a dataframe
    if filtered by KG.code, remove KG.code column bc then there is only one unique KG.code in the dataframe
    '''
    if args.KG:
        df_corr_mat = df.drop(columns=["KG.Code"])
        corr = df_corr_mat.corr()
    else:
        corr = df.corr()

    sns.heatmap(corr, annot=True,mask=corr.isnull())

    if args.output:
        '''Save plot to file'''
        plt.savefig(str(Path(args.output))+"/correlation_matrix.png")
        print("Plot saved to " + args.output)
    else:
        plt.show()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='PROG', formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
        Explore data on purchasing prices of real estate transactions in Vienna (source: land register),
        including regulations of the land use and town plan, on-site inspection etc.
        Link to original data: https://www.data.gv.at/katalog/dataset/kaufpreissammlung-liegenschaften-wien
        CC BY 4.0 „Datenquelle: Stadt Wien – data.wien.gv.at“
        
        modules used:
        
        pandas
        numpy
        matplotlib
        requests
        bs4
        lxml
                
        
                                              Recomended usage:
        To start the tool type in "python explore_re_data.py" (if you have python 3.XX AND python 2 on your system, you 
        may have to type in python3 instead of just python)
        
        In the first run, get the list of all KG codes with the options "--no-read -l". It doesn't read in the pricing 
        data and prints the list of all KG codes. 
        
        Decide which KG you are interested in and run the program with the corresponding KG Code E.g.: "--read -K 1805"
        to read the data with KG code 1805
        sort by "Bauzins" with --read -K 1805 -s "Bauzins"
        
        
                
     '''))

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    parser.add_argument('--read', action='store_true',help="read in the princing data file")
    parser.add_argument('--no-read', dest='read', action='store_false', help='''don't read in the pricing data file and 
    ignore all options other than -l and -o''')
    parser.set_defaults(read=True)



    parser.add_argument('-f', '--file', type=str, help='path to csv file')
    parser.add_argument('-o', '--output', type=str, help='''path to output file without extension, if you use this no data
                                                         will be printed to the screen, but the data will be saved in 
                                                         the same folder as this script''')
    parser.add_argument('-K', '--KG', type=int, help='''KG code, enter without the leading 0, (use -l to get a list of 
                                                        all KG codes)''')

    parser.add_argument('-d', '--desc', action='store_true', help='sort descending')

    parser.add_argument('-l', '--list', action='store_true', help='''Prints a list of all KG codes to the screen or to a
                                                                  file if -o is used''')

    parser.add_argument('--show-columns', type=str, nargs="+", action='append',
                        help='''columns to be shown, use "all" for all columns, "predefined" for the predefined 
                        columns, or a list of columns like "Erwerbsdatum,BJ,KG.Code"
                        ''')

    parser.add_argument('-p', '--plot', type=str, nargs="+", action='append',
                        help='''plot scatter plot of two columns,y-column is by default "Erwerbsdatum" ''')

    parser.add_argument('-r', '--rows', type=int,help='''how many rows should be shown (= will be printed on your 
                        screen! or saved in the output file)''')

    parser.add_argument('--corr', type=str, nargs="+", action='append',help="Correlation between two columns")


    # describing groups which can not be used together
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-s', '--sort-column', type=str, help='''column to sort by (default: ascending, use -d for 
                                                                descending)''')
    group1.add_argument('-D', '--describe-column', type=str, help='column to describe')



    args = parser.parse_args()

    if args.read:
        if args.file:
            df = read_csv(args.file)
        else:
            df = read_csv()


        if args.KG:
            df = show_certain_KG(df, args.KG)

        if args.show_columns:
            print(args.show_columns)
            df = show_specific_columns(df, args.show_columns)

        if not args.desc:
            args.desc = False  # default is ascending


        if args.sort_column:
            print(args.desc)
            df = sort_by_column(df, args.sort_column, args.desc)

        if args.describe_column:
            pd.set_option('display.float_format', lambda x: '%.2f' % x)
            desc_df = describe_column(df, args.describe_column)
            if args.output:
                file_path = Path(args.output+"/description_of_" + args.describe_column+ ".csv")
                desc_df.to_csv(file_path)
                print("The data has been saved to: " + str(file_path.parent) + " as \"" + str(file_path.name)+"\"")
            else:
                print(desc_df)

        if args.rows:
            pd.set_option('display.max_rows', args.rows)
            df = df.head(args.rows)

        # does not work yet
        if args.plot:
            if len(args.plot[0]) == 1:
                plot_column(df, args.plot[0][0])
            elif len(args.plot[0]) == 2:
                plot_column(df, args.plot[0][1], args.plot[0][0])
            else:
                print("Error: wrong number of arguments for --plot")



        if args.output:
            file_path = Path(args.output+"/exported_df.csv")
            df.to_csv(file_path, index=False)
            print("The data has been saved to: " + str(file_path.parent) + " as \"" + str(file_path.name)+"\"")
        else:
            print(df)

        if args.corr:
            if len(args.corr[0]) == 2:
                try:
                    print(f' The standard correlation coefficient of {args.corr[0][0]} and {args.corr[0][1]} is {column_correlation(df, args.corr[0][0], args.corr[0][1])}')
                except:
                    print("Error: wrong column type for --corr (only numeric columns are supported)")
            else:
                print("Error: wrong number of arguments for --corr")


    else:
        print("No pricing data read in")

        if args.list:
            KG_list = get_list_of_KG()
            if args.output:
                KG_list.to_csv(Path(args.output+"_list_of_KG_codes.csv"))
                print("The KG data has been saved to: " + str(Path(args.output+"list_of_KG_codes.csv")))
            else:
                pd.set_option('display.max_rows', None)
                print(KG_list)
                pd.set_option('display.max_rows', 10)

# to do:
# - add opiton to search for street name
# show all columns with predefined
# rows add to help
# show-columnsa add to help
# is -d really descending?

# describe everything better!!

# correlation matrix for "predefined" columns


