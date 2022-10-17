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
        print(f'\nThe file {csv_file} has already been downloaded')
        print(f"Reading data from {loc_path}\n")

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
                                    "auf EZ", "Stammeinlage", "sonst_wid", "sonst_wid_prz", "ber_Kaufpreis",
                                    "Bauzins"], parse_dates=["BJ"])

        df["Erwerbsdatum"] = pd.to_datetime(df["Erwerbsdatum"].astype(str), format='%d%m%Y.0', errors='coerce')
        # if "Erwerbsdatum" is later than dt.today (e.g. if the data is from the future),
        # the date is set to null
        df["Erwerbsdatum"] = df["Erwerbsdatum"].where(df["Erwerbsdatum"] <= dt.datetime.today(), None)
        df["Strasse"] = df["Strasse"].astype(str).apply(lambda x: x.upper()) # for address search

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
    'zuordnung', 'BJ', 'Gebäudehöhe', 'KG.Code', 'Erwerbsdatum', 'Strasse', "ON", 'Gst.Fl.', 'AbbruchkostEU', 'ber_Kaufpreis', 'Bauzins'
    or a user-input list of columns (which_columns = *user input*)
    '''
    if which_colums == [["predefined"]]:
        return df[['Erwerbsdatum','zuordnung', 'BJ', 'Gebäudehöhe', 'KG.Code',  'Strasse', "ON",
     'Gst.Fl.', 'AbbruchkostEU', 'ber_Kaufpreis', 'Bauzins']]
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
    and return a dataframe with the KG code, name, municipal districts, and area.
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
    plt.title(f'{ycolumn} vs {xcolumn}')
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
    plt.title("Correlation Matrix")

    if args.output:
        '''Save plot to file'''
        plt.savefig(str(Path(args.output))+"/correlation_matrix.png")
        print("Plot saved to " + args.output)
    else:
        plt.show()
#%%

def filter_for_address(df, address):
    '''
    filter dataframe for address
    '''

    df_address = df[df["Strasse"].str.contains(address.upper())]
    return df_address



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='PROG', formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
        Explore data on purchasing prices of real estate transactions in Vienna (source: land register),
        including regulations of the land use and town plan, on-site inspection etc.
        Link to original data: https://www.data.gv.at/katalog/dataset/kaufpreissammlung-liegenschaften-wien
        CC BY 4.0 „Datenquelle: Stadt Wien – data.wien.gv.at“
        
        Known bugs/limitations:
        -Tested only on Linux, not on Windows.
        -If you want to save a plot you have to use '-o "./"' as command line argument for the plot to be saved to the 
        current folder. If you specify another path, there will be an error. Saving a .csv file works fine.
        - probably hard to use if you don't speak German which I realized just now and don't have the time to translate 
        it
         
        
                                              Recomended usage:
        To start the tool type in "python explore_re_data.py" (if you have python 3.XX AND python 2 on your system, you 
        may have to type in python3 instead of just python)
        
        In the first run, get the list of all KG codes with the options "--no-read -l". It doesn't read in the pricing 
        data and prints the list of all KG codes or saves it to a csv file if you specify the option -o "path/to/file/"
        
        Now you can explore the dataset:
        --KG 1805 -> filter the data for the KG with code 1805
        
        -a "Mariahilfer" -> filter the data for a specific street (here: every address with Mariahilfer in it)
        
        --show-columns "predefined" -> show only the predefined columns ('zuordnung', 'BJ', 'Gebäudehöhe', 'KG.Code', 
            'Erwerbsdatum', 'Strasse', "ON", 'Gst.Fl.', 'AbbruchkostEU', 'ber_Kaufpreis', 'Bauzins')
            
        --show-columns "KG.Code" "Katastralgemeinde" "EZ" "PLZ" "Strasse" "ON" "Gst." "Gst.Fl." "ErwArt" 
                        "Erwerbsdatum" "Widmung" "Bauklasse" "Gebäudehöhe" "Bauweise" "Zusatz" "Schutzzone" 
                        "Wohnzone" "öZ" "Bausperre" "seit/bis" "zuordnung" "Geschoße" "parz." "VeräußererCode" 
                        "Erwerbercode" "Zähler" "Nenner" "BJ" "TZ" "Kaufpreis EUR""EUR/m2 Gfl." "AbbruchfixEU" 
                        "m3 Abbruch" "AbbruchkostEU" "FreimachfixEU""Freimachfläche" "FreimachkostEU" 
                        "Baureifgest" "% Widmung" "Baurecht" "Bis" "auf EZ" "Stammeinlage" "sonst_wid" 
                        "sonst_wid_prz" "ber_Kaufpreis" "Bauzins" -> will show all columns (which is the default, but so
                        you can see which columns are available)
                        
        -p "ber_Kaufpreis" -> will plot the two columns "ber_Kaufpreis" and "Erwerbsdatum" (default for the x-axis is 
            "Erwerbsdatum" but you can specify any other column)
            
        --corr-c "Erwerbsdatum" "Bauzins" -> will show the correlation between the two columns "Erwerbsdatum" and
            "Bauzins"
        
        --corr-m -> will show the correlation matrix of the dataframe, can be messy if there are many columns,
            use with e.g. --show-columns "predefined"
        
        -r 100 -> will show the dataframe with the first 100 rows, will print all of them to the screen!
        
        -o "./" -> will save the output(s) to the current folder
        
        Those two options are mutually exclusive:
        -s "Bauzins" -> sort the data by column "Bauzins" (ascending)
        -D "Bauzins" -> describe the column "Bauzins" (mean, std, min, max, etc.) 
        
        -s "Bauzins" -d -> sort descending
        
     '''))


    parser.add_argument('--read', action='store_true',help="read in the princing data file")
    parser.add_argument('--no-read', dest='read', action='store_false', help='''don't read in the pricing data file and 
    ignore all options other than -l and -o''')
    parser.set_defaults(read=True)


    parser.add_argument('-f', '--file', type=str, help='path to csv file')
    parser.add_argument('-o', '--output', type=str, help='''path to output file folder, if you use this no 
                                                         data will be printed to the screen, but the data will be saved 
                                                         in the same folder as this script''')
    parser.add_argument('-K', '--KG', type=int, help='''KG code, enter without the leading 0, (use -l to get a list of 
                                                        all KG codes)
                                                        If you use -K and -a together the dataframe will be first 
                                                        filtered for the KG Code and then for the address''')

    parser.add_argument('-a', '--address', type=str, help='''Enter (part of) an address to filter the dataframe
                                                            for that address. If you use -K and -a together 
                                                            the dataframe will be first filterd for the KG Code and 
                                                            then for the address''')


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

    parser.add_argument('--corr-c', type=str, nargs="+", action='append', help="Correlation between two columns")

    parser.add_argument('--corr-m', action='store_true', help='''plot correlation matrix of all columns of the dataframe 
                                                            can be messy if there are many columns, use "predefined"''')

    # describing groups which can not be used together
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-s', '--sort-column', type=str, help='''column to sort by (default: ascending, use -d for 
                                                                descending)''')
    group1.add_argument('-D', '--describe-column', type=str, help='column to describe')

    args = parser.parse_args()


    if args.read: # if read is true, read in and explore the data, plot, etc.

        if args.file:
            df = read_csv(args.file)
        else:
            df = read_csv()


        if args.KG:
            df = show_certain_KG(df, args.KG)

        if args.address:
            df = filter_for_address(df, args.address)

        if args.show_columns:
            df = show_specific_columns(df, args.show_columns)

        if not args.desc:
            args.desc = False  # default is ascending


        if args.sort_column:
            if args.desc:
                print(f"Sorting by '{args.sort_column}' descending\n")
            else:
                print(f"Sorting by '{args.sort_column}' ascending\n")
            df = sort_by_column(df, args.sort_column, args.desc)

        if args.describe_column:
            pd.set_option('display.float_format', lambda x: '%.2f' % x)
            desc_df = describe_column(df, args.describe_column)
            if args.output:
                file_path = Path(args.output+"/description_of_" + args.describe_column+ ".csv")
                desc_df.to_csv(file_path)
                print("The data has been saved to: " + str(file_path.parent) + " as \"" + str(file_path.name)+"\"\n")
            else:
                print(desc_df)
                print("\n")

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
                print("Error: wrong number of arguments for --plot\n")


        if args.output:
            file_path = Path(args.output+"/exported_df.csv")
            df.to_csv(file_path, index=False)
            print("The data has been saved to: " + str(file_path.parent) + " as \"" + str(file_path.name)+"\"\n")
        else:
            print(df)
            print("\n")

        if args.corr_c:
            if len(args.corr_c[0]) == 2:
                try:
                    print(f' The standard correlation coefficient of {args.corr_c[0][0]} and {args.corr_c[0][1]} is '
                          f'{column_correlation(df, args.corr_c[0][0], args.corr_c[0][1])}\n')
                except:
                    print("Error: wrong column type for --corr-c (only numeric columns are supported)\n")
            else:
                print("Error: wrong number of arguments for --corr-c\n")

        if args.corr_m:
            correlation_matrix(df)


    else: # if args.read is False (--no-read)
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
# describe help better - more examples
# try out on windows?
# upload it before 23:59


