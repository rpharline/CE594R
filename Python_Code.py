#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 09:22:43 2023

@author: kendrickshepherd
"""

import sys

# load all of the data from a CSV file
def LoadCSV(filename):
    # ensure that the input file is a CSV file
    if(filename.split('.')[-1] !='csv'):
        print("Input must be a csv file. Please input a csv file with file extension .csv included in the end of the input file name.")
        sys.exit()
    with open(filename, 'r',encoding='utf-8-sig') as f:
        lines = [line for line in f]
    return lines

# given a line of headers (from the CSV files) and the header string of interest,
# find the column index whose character string are the same as your input
def LocateHeader(header_line,header_value):
    # separate by commas and remove trialing spaces and return signs
    headers = header_line.strip().split(",")
    return headers.index(header_value)

# This is a helper function that should not be accessed by the user
def PrecipitationValue(rainfall_num,invalid_nums):
    is_valid = False
    if rainfall_num in invalid_nums:
        return [0,is_valid]
    else:
        is_valid = True
        return [rainfall_num,is_valid]

# Compute all of the annual precipitation for all available years given the
# particular precipitation type
# date_column is the column that keeps track of the measurement dates
# precip_column is the column that keeps track of the precipitation data (that will be accumulated)
# lines holds the information from an input CSV file
# invalid_nums are numbers in precipitation data that are invalid and should be skipped
#         it should includ the numbers 999.99 and -9999
def ExtractAnnualPrecipitation(date_column,precip_col,lines,invalid_nums = []):
    current_year = 0
    years = []
    precipitation = []
    header = lines[0].strip().split(",")
    is_QPCP = header[precip_col]=="QPCP"
    is_QGAG = header[precip_col]=="QGAG"
    is_valid = False
    prev_rainfall = 0
    for i in range(1,len(lines)):
        data = lines[i].strip().split(",")
        rainfall_num = float(data[precip_col])
        [current_rainfall,is_valid] = \
            PrecipitationValue(rainfall_num,invalid_nums)
        this_year = int(data[date_column][0:4])
        if this_year > current_year:
            current_year = this_year
            years.append(current_year)
            precipitation.append(current_rainfall)
            prev_rainfall = 0
        else:
            if is_QPCP:
                precipitation[-1] += current_rainfall
            elif is_QGAG:
                if is_valid:
                    if current_rainfall < prev_rainfall:
                        precipitation[-1] += prev_rainfall
                    prev_rainfall = current_rainfall

    if is_QGAG and is_valid:
        precipitation[-1] += prev_rainfall
    return [years,precipitation]

lines = LoadCSV("Provo_Precipitation_3193744.csv")
precip_idx = LocateHeader(lines[0],"QGAG")
#precip_idx = LocateHeader(lines[0],"QPCP")

date_idx = LocateHeader(lines[0],"DATE")
invalid_nums = [999.99,-9999]

[years_list,precipitation] = \
    ExtractAnnualPrecipitation(date_idx, precip_idx,lines,invalid_nums)
