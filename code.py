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
    print ("list of all the cities with airport")
    print (df)
    while True:
        command = raw_input("Input name of the city for which you want to see flight details else print 1 to exit: ")
        if (command == '1'):
            return
        if (!command.isalpha()):
            continue
        command = command.upper()
        df = pd.read_sql_query("Select * from Flights where SOURCE=" + "'" + command + "'" + " OR DESTINATION=" + "'" + command + "'", sq)
        if (df.empty):
            print ("No flight on this route")
        else:
            print tabulate(df, headers='keys', tablefmt='psql')

def Flight_staff():
    while True:
        sqlquery = raw_input("To see passengers who cleared security checkin press 6 else press 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        flight_num = raw_input("Enter flight number: ")
        count = pd.read_sql_query("Select COUNT(*) from Passengers where FLIGHT_NUMBER=" + flight_num, sq)
        df = pd.read_sql_query("Select PNR,First_Name,Last_Name,Class/Seat,Mobile_number from Passengers where FLIGHT_NUMBER=" + flight_num + " ORDER BY First_Name Last_Name", sq)
        if (df.empty):
            print ("No passenger has cleared the security checkin with this flight number or no flight exist with this number")
        else:
            print ("Total number of passengers are:")
            print (count)
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')
            sqlquery = raw_input("Type Y if want to delete this information else N: ")
            if (sqlquery.upper() == 'Y'):
                sqcur.execute("delete from Passengers where FLIGHT_NUMBER=?", flight_num)
                sq.commit()
                print ("Information is deleted successfully.")

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

def passenger():
    while True:
        print ("Want to see already booked flight details press 1")
        print ("press 4 for doing web-checkin")
        print ("press 2 to exit")
        print ("press 3 for new booking")
        sqlquery = raw_input("Input: ")
        if (sqlquery == '1' or sqlquery == '4'):
            pnr = raw_input("Enter your PNR number: ")
            last_name = raw_input("Enter your Last name: ")
            if (sqlquery == '1'):
                df = pd.read_sql_query("Select PNR,First_Name, Last_Name, Passengers.FLIGHT_NUMBER, SOURCE, DESTINATION, PRICE,DEPARTURE_TIME,ARRIVAL_TIME from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER PNR=" + "'" + pnr + "'" + " AND Last_Name=" + "'" + last_name + "'", sq)
                if (df.empty):
                    print ("No passenger with this detail")
                else:
                    print ("Your Ticket details")
                    print tabulate(df, headers='keys', tablefmt='psql')
            else:
                df = pd.read_sql_query("Select Class/Seat from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER PNR=" + "'" + pnr + "'" + " AND Last_Name=" + "'" + last_name + "'", sq)
                if (df.empty):
                    print ("No passenger with this detail")
                else:
                    sqlquery = raw_input("Press Y if want to do weeb-checking: ")
                    sqlquery = sqlquery.upper()
                    if (sqlquery == 'Y'):
                        sqcur.execute("update Passengers set Web_Checkin='Y' where PNR = " + "'" + pnr + "'")
                        sq.commit()
                        print ("Web checkin done succesfully your seat number is")
                        print tabulate(df, headers='keys', tablefmt='psql')
        elif (sqlquery == '2'):
            booking()
        else:
            return

def Passengers_details():
    while True:
        sqlquery = raw_input("To get the list and count of passengers who are either coming and going from particular station press 6 else press 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        name = raw_input("Enter airport name: ")
        name = name.upper()
        count = pd.read_sql_query("Select COUNT(*) from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER AND (SOURCE=" + "'" + name + "'" + " OR DESTINATION="+"'" + name + "'" + " OR CONNECTION=" +"'" + name + "'" +")", sq)
        df = pd.read_sql_query("Select PNR,First_Name,Last_Name,Class/Seat,Mobile_number,Passengers.FLIGHT_NUMBER,SOURCE,CONNECTION,DESTINATION from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER AND (SOURCE=" + "'" + name + "'" + " OR DESTINATION="+"'" + name + "'" + " OR CONNECTION=" +"'" + name + "'" +")", sq)
        if (df.empty):
            print ("No passenger has booked flight from this route no flight exist on this station name")
        else:
            print ("Total of passengers are:")
            print (count)
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')

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
