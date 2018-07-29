#!/usr/bin/python
#coding=utf-8
import numpy as np
import pandas as pd
import re
import os
import csv
from csv import *
from matplotlib import *
import sys
from openpyxl import load_workbook
from xlrd import open_workbook
import operator
import datetime
import time
import matplotlib.pyplot as plt
from datetime import *
import sqlite3
import random
import string
from tabulate import tabulate

sq = sqlite3.connect("flight_detail.db")
sqcur = sq.cursor()

def Flight_details():
    df = pd.read_sql_query("Select DISTINCT SOURCE as FLIGHT_STATIONS from Flights", sq)
    df1 = pd.read_sql_query("Select DISTINCT CONNECTION as FLIGHT_STATIONS from Flights", sq)
    df = pd.concat([df, df1], ignore_index=True)
    df = (df.drop_duplicates()).dropna(how='any',axis=0)
    print ("list of all the cities with airport")
    print (df)
    while True:
        print ("Input name of the city for which you want to see flight details else print 1 to exit")
        command = raw_input()
        if (command == '1' or command == 'None'):
            return
        df = pd.read_sql_query("Select * from Flights where SOURCE=" + "'" + command + "'" + " OR CONNECTION=" + "'" + command + "'" + " OR DESTINATION=" + "'" + command + "'", sq)
        if (df.empty):
            print ("No flight on this route")
        else:
            print (df)
            print tabulate(df, headers='keys', tablefmt='psql')
            with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
                print(df)

def Flight_staff():
    while True:
        sqlquery = raw_input("To see passengers who cleared security checkin press 6 else press 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        flight_num = raw_input("Enter flight number: ")
        count = pd.read_sql_query("Select COUNT(*) from Passengers where FLIGHT_NUMBER=" + flight_num + " ORDER BY First_Name", sq) 
        df = pd.read_sql_query("Select PNR,First_Name,Last_Name,Class/Seat,Mobile_number from Passengers where FLIGHT_NUMBER=" + flight_num + " ORDER BY First_Name Last_Name", sq)
        if (df.empty):
            print ("No passenger has cleared the securityt checkinwith this flight number or no flight exist with this number")
        else:
            print ("Total of passengers are" + count)
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')
            sqlquery = raw_input("Type Y if want to delete this information else N: ")
            if (sqlquery.upper() == 'Y'):
                sqcur.execute("delete from Passengers where FLIGHT_NUMBER=?", flight_num)
                sq.commit()
                print ("Information is deleted successfully.")
            else:
                print ("Passenger cannot board the flight as not cleared security check-in.")

def security_personnel():
    while True:
        sqlquery = raw_input("For clearing security checkin for passengers press 6 else press 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        pnr = raw_input("Enter PNR num: ")
        flight_num = raw_input("Enter flight_num: ")
        df = pd.read_sql_query("Select * from Passengers where PNR=" + "'" + pnr + "'" + " AND FLIGHT_NUMBER=" + flight_num, sq)
        if (df.empty):
            print ("No passenger with this detail")
        else:
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')
            sqlquery = raw_input("Type Y if all the information are correct else N: ")
            if (sqlquery.upper() == 'Y'):
                sqcur.execute("update Passengers set Security_Checkin='Y' where PNR = " + "'" + pnr + "'")
                sq.commit()
                print ("Passenger can succesfully board the flight")
            else:
                print ("Passenger cannot board the flight as not cleared security check-in.")
'''
def passenger():
    while True:
        #want to book flight
        #want to see past bookings
        #want to exit
        #flights with empty seats
'''
def main():
    while True:
        print ("press S if Security Personnel")
        print ("press F if Flight Staff")
        print ("press P if Passengers")
        print ("To know the details of all flights departing and arriving from particular airport press 1.")
        print ("List of passengers arriving or departing from particular airport press 2")
        print ("press E to exit.")
        command = raw_input()
        if (command.upper() == "E"):
            sqcur.close()
            sq.close()
            sys.exit()
        elif (command.upper() == "S"):
            security_personnel()
        elif (command.upper() == "F"):
            Flight_staff()
        elif (command.upper() == "P"):
            passenger()
        elif (command.upper() == "1"):
            Flight_details()
        elif (command.upper() == "2"):
            Passengers_details()

if __name__ == "__main__":
    main()
