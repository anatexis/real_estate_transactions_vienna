# Real estate transactions in Vienna

## Usage

PROG [-h] [--read] [--no-read] [-f FILE] [-o OUTPUT] [-K KG] [-a ADDRESS] [-d] [-l] [--show-columns SHOW_COLUMNS [SHOW_COLUMNS ...]] [-p PLOT [PLOT ...]] [-r ROWS] [--corr-c CORR_C [CORR_C ...]] [--corr-m] [-s SORT_COLUMN | -D DESCRIBE_COLUMN]

Explore data on purchasing prices of real estate transactions in Vienna (source: land register), including regulations of the land use and town plan, on-site inspection etc.

Link to original data: https://www.data.gv.at/katalog/dataset/kaufpreissammlung-liegenschaften-wien CC BY 4.0 „Datenquelle: Stadt Wien – data.wien.gv.at“

## Known bugs/limitations:

- Tested only on Linux, not on Windows.
- If you want to save a plot you have to use `-o "./"` as command line argument for the plot to be saved to the current folder. If you specify another path, there will be an error. Saving a .csv file works fine.
- probably hard to use if you don't speak German which I realized just now and don't have the time to translate it

## Recomended usage:

To start the tool type in `python explore_re_data.py` (if you have python 3.XX AND python 2 on your system, you may have to type in `python3` instead of just `python`)

In the first run, get the list of all KG codes with the options `--no-read -l`. It doesn't read in the pricing data and prints the list of all KG codes or saves it to a csv file if you specify the option `-o "path/to/file/"`

Now you can explore the dataset:

* `--KG 1805` -> filter the data for the KG with code 1805
* `-a "Mariahilfer"` -> filter the data for a specific street (here: every address with Mariahilfer in it)
* `--show-columns "predefined"` -> show only the predefined columns ('zuordnung', 'BJ', 'Gebäudehöhe', 'KG.Code', 'Erwerbsdatum', 'Strasse', "ON", 'Gst.Fl.', 'AbbruchkostEU', 'ber_Kaufpreis', 'Bauzins')
* `--show-columns "KG.Code" "Katastralgemeinde" "EZ" "PLZ" "Strasse" "ON" "Gst." "Gst.Fl." "ErwArt" "Erwerbsdatum" "Widmung" "Bauklasse" "Gebäudehöhe" "Bauweise" "Zusatz" "Schutzzone" "Wohnzone" "öZ" "Bausperre" "seit/bis" "zuordnung" "Geschoße" "parz." "VeräußererCode" "Erwerbercode" "Zähler" "Nenner" "BJ" "TZ" "Kaufpreis EUR""EUR/m2 Gfl." "AbbruchfixEU" "m3 Abbruch" "AbbruchkostEU" "FreimachfixEU""Freimachfläche" "FreimachkostEU" "Baureifgest" "% Widmung" "Baurecht" "Bis" "auf EZ" "Stammeinlage" "sonst_wid" "sonst_wid_prz" "ber_Kaufpreis" "Bauzins"` -> will show all columns (which is the default, but so you can see which columns are available)
* `-p "ber_Kaufpreis"`: will plot the two columns "ber_Kaufpreis" and "Erwerbsdatum" (default for the x-axis is
    "Erwerbsdatum" but you can specify any other column)
* `--corr-c "Erwerbsdatum" "Bauzins"`: will show the correlation between the two columns "Erwerbsdatum" and
    "Bauzins"
* `--corr-m`: will show the correlation matrix of the dataframe, can be messy if there are many columns,
    use with e.g. `--show-columns "predefined"`
* `-r 100`: will show the dataframe with the first 100 rows, will print all of them to the screen!
* `-o "./"`: will save the output(s) to the current folder

Those two options are mutually exclusive:

* `-s "Bauzins"`: sort the data by column "Bauzins" (ascending)
* `-D "Bauzins"`: describe the column "Bauzins" (mean, std, min, max, etc.)

## Options

- `-h`, `--help`: Show this help message and exit
- `--read`: Read in the pricing data file
- `--no-read`: Don't read in the pricing data file and ignore all options other than `-l` and `-o`
- `-f FILE`, `--file FILE`: Path to CSV file
- `-o OUTPUT`, `--output OUTPUT`: Path to output file folder, if you use this no data will be printed to the screen, but the data will be saved in the same folder as this script
- `-K KG`, `--KG KG`: KG code, enter without the leading 0, (use -l to get a list of all KG codes) If you use -K and -a together the dataframe will be first filtered for the KG Code and then for the address
- `-a ADDRESS`, `--address ADDRESS`: Enter (part of) an address to filter the dataframe for that address. If you use -K and -a together the dataframe will be first filterd for the KG Code and then for the address
- `-d`, `--desc`: Sort descending
- `-l`, `--list`: Prints a list of all KG codes to the screen or to a file if `-o` is used
- `--show-columns SHOW_COLUMNS [SHOW_COLUMNS ...]`: Columns to be shown, use `"all"` for all columns, "predefined" for the predefined columns, or a list of columns like `"Erwerbsdatum,BJ,KG.Code"`
- `-p PLOT [PLOT ...]`, `--plot PLOT [PLOT ...]`: Plot scatter plot of two columns, y-column is by default "Erwerbsdatum"
- `-r ROWS`, `--rows ROWS`: How many rows should be shown (= will be printed on your screen! or saved in the output file)
- `--corr-c CORR_C [CORR_C ...]`: Correlation between two columns
- `--corr-m`: Plot correlation matrix of all columns of the dataframe can be messy if there are many columns, use `"predefined"`
- `-s SORT_COLUMN`, `--sort-column SORT_COLUMN`: Column to sort by (default: ascending, use `-d` for descending)
- `-D DESCRIBE_COLUMN`, `--describe-column DESCRIBE_COLUMN`: Select which column to describe
