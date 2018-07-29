#!/usr/bin/python
#coding=utf-8
import pandas as pd
import re
import os
import sys
import operator
import sqlite3
import random
import string
from tabulate import tabulate

sq = sqlite3.connect("flight_detail.db")
sqcur = sq.cursor()

def seat_number(flight_num,Class):
    val = pd.read_sql_query("Select COUNT(*) as count from Passengers where FLIGHT_NUMBER=" + flight_num, sq)
    val = int(val['count'].iloc[0]) + 1
    seat = Class + "/" + str(val)
    return seat

def generate_pnr():
    while True:
        gen = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
        df = pd.read_sql_query("Select * from Passengers where PNR=" + "'" + gen + "'", sq)
        if (df.empty):
            return gen

def booking():
    df = pd.read_sql_query("Select DISTINCT SOURCE as FLIGHT_STATIONS from Flights", sq)
    print ("list of all the cities with airport")
    print (df)
    while True:
        command = raw_input("\nPress 1 to book else press 2 to exit: ")
        if (command == '2'):
            return
        elif (command != '1'):
            continue
        board_air = (raw_input("Name of boarding station: ")).upper()
        des_air = (raw_input("Name of destination station: ")).upper()
        df = pd.read_sql_query("Select Flights.* from Flights,Passengers where SOURCE=" + "'" + board_air + "'" + " AND DESTINATION=" + "'" + des_air + "'", sq)
        if (df.empty):
            print ("No flight on this route.")
        else:
            print tabulate(df, headers='keys', tablefmt='psql')
            flight_number = raw_input("Input flight number from available flights: ")
            try:
                val = int(flight_number)
            except ValueError:
                print("Flight number should be an integer")
                continue
            count = pd.read_sql_query("Select COUNT(*) as count from Passengers where FLIGHT_NUMBER=" + flight_number, sq)
            count = int(count['count'].iloc[0])
            size = pd.read_sql_query("Select SIZE from Flights where FLIGHT_NUMBER=" + flight_number, sq)
            size = int(size['SIZE'].iloc[0])
            if (size <= count):
                print ("No more vacancy in this flight number or you entered wrong number...please enter different flight number...exit")
                continue
            df = pd.read_sql_query("Select Flights.* from Flights where SOURCE=" + "'" + board_air + "'" + " AND DESTINATION=" + "'" + des_air + "'" + " AND Flights.FLIGHT_NUMBER=" + flight_number, sq)
            if (df.empty):
                print ("wrong flight number for your source and destination")
                continue
            first_name = (raw_input("First Name: ")).upper()
            if first_name == '':
                print("Incorrect input hence exit")
                continue
            last_name = (raw_input("Last Name: ")).upper()
            if last_name == '':
                print("Incorrect input hence exit")
                continue
            Age = raw_input("Enter your Age: ")
            try:
                val = int(Age)
            except ValueError:
                print("Incorrect input hence exit")
                continue
            Nationality = (raw_input("Nationality: ")).upper()
            if Nationality == '':
                print("Incorrect input hence exit")
                continue
            Mobile_number = raw_input("Enter your MObile Number: ")
            try:
                val = int(Mobile_number)
            except ValueError:
                print("Incorrect input hence exit")
                continue
            Class = (raw_input("Enter class Either B or E: ")).upper()
            Gender = (raw_input("Enter Gender Either M or F: ")).upper()
            if (Class != 'B' or Class != 'E'):
                Class = 'E'
            if (Gender != 'M' or Gender != 'F'):
                Gender = 'M'
            Age = int(Age)
            Mobile_number = int(Mobile_number)
            values = (flight_number, first_name, last_name, Age, Nationality, Mobile_number, Gender)
            print (values)
            command = (raw_input("Press Y if all infomations are correct and want to book flight else exit: ")).upper()
            if (command == 'Y'):
                PNR = generate_pnr()
                seat = seat_number(flight_number,Class)
                values = (flight_number,PNR, first_name, last_name, Age, Nationality,'N' ,Mobile_number,seat,'N',Gender)
                sqcur.execute("INSERT INTO Passengers VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
                sq.commit()
                print ("sucessfully booked ticket.")

def Flight_details():
    df = pd.read_sql_query("Select DISTINCT SOURCE as FLIGHT_STATIONS from Flights", sq)
    print ("\nlist of all the cities with airport")
    print (df)
    while True:
        command = (raw_input("\nInput name of the city for which you want to see flight details else PRESS 1 to exit: ")).upper()
        if (command == '1'):
            return
        if (command.isalpha() != True):
            continue
        df = pd.read_sql_query("Select * from Flights where SOURCE=" + "'" + command + "'" + " OR DESTINATION=" + "'" + command + "'", sq)
        if (df.empty):
            print ("No flight on this route")
        else:
            print tabulate(df, headers='keys', tablefmt='psql')

def Flight_staff():
    while True:
        sqlquery = raw_input("\nTo see passengers who cleared security checkin PRESS 6 else PRESS 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        flight_num = raw_input("Enter flight number: ")
        try:
            val = int(flight_num)
        except ValueError:
            print("Flight number should be an integer")
            continue
        count = pd.read_sql_query("Select COUNT(*) as count from Passengers where FLIGHT_NUMBER=" + flight_num + " AND Security_Checkin='Y'", sq)
        count = count['count'].iloc[0]
        total_passenger = pd.read_sql_query("Select COUNT(*) as count from Passengers where FLIGHT_NUMBER=" + flight_num, sq)
        total_passenger = total_passenger['count'].iloc[0]
        df = pd.read_sql_query("Select PNR,First_Name,Last_Name,Gender,`Class/Seat`,Mobile_number from Passengers where FLIGHT_NUMBER=" + flight_num + " ORDER BY First_Name,Last_Name", sq)
        if (df.empty):
            print ("No passenger has cleared the security checkin with this flight number or no flight exist with this number")
        else:
            print "\nTotal number of passengers who cleared security checkin for this flight are ",count,"out of",total_passenger,"total passengers."
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')
            sqlquery = raw_input("Type Y if want to delete this information else N: ")
            if (sqlquery.upper() == 'Y'):
                sqcur.execute("delete from Passengers where FLIGHT_NUMBER=?", flight_num)
                sq.commit()
                print ("Information is deleted successfully.")

def security_personnel():
    while True:
        sqlquery = raw_input("\nFor clearing security checkin for passengers press 6 else press 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        pnr = raw_input("Enter PNR num: ")
        flight_num = raw_input("Enter flight_num: ")
        try:
            val = int(flight_num)
        except ValueError:
               print("Flight number should be an integer")
               continue
        df = pd.read_sql_query("Select * from Passengers where PNR=" + "'" + pnr + "'" + " AND FLIGHT_NUMBER=" + flight_num, sq)
        if (df.empty):
            print ("No passenger with this details.")
        else:
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')
            sqlquery = raw_input("Type Y if all the information are correct else N: ")
            if (sqlquery.upper() == 'Y'):
                sqcur.execute("update Passengers set Security_Checkin='Y' where PNR = " + "'" + pnr + "'")
                sq.commit()
                print ("Passenger can succesfully board the flight")
            else:
                sqcur.execute("update Passengers set Security_Checkin='N' where PNR = " + "'" + pnr + "'")
                sq.commit()
                print ("Passenger cannot board the flight as not cleared security check-in.")

def passenger():
    while True:
        print ("\nPress 1 to see e-ticket of already booked flight details")
        print ("press 4 for doing web-checkin")
        print ("press 2 to exit")
        print ("press 3 for new booking")
        sqlquery = raw_input("Input: ")
        if (sqlquery == '1' or sqlquery == '4'):
            pnr = raw_input("Enter your PNR number: ")
            last_name = (raw_input("Enter your Last name: ")).upper()
            df = pd.read_sql_query("Select PNR,First_Name, Last_Name, Passengers.FLIGHT_NUMBER, SOURCE, DESTINATION, PRICE,DEPARTURE_TIME,ARRIVAL_TIME from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER AND PNR=" + "'" + pnr + "'" + " AND Last_Name=" + "'" + last_name + "'", sq)
            if (df.empty):
                print ("No passenger with this detail")
            else:
                print ("Your Ticket details")
                print tabulate(df, headers='keys', tablefmt='psql')
            if (sqlquery == '4'):
                df = pd.read_sql_query("Select `Class/Seat` as seat from Passengers where PNR=" + "'" + pnr + "'" + " AND Last_Name=" + "'" + last_name + "'", sq)
                seat = df['seat'].iloc[0]
                sqlquery = (raw_input("\nPress Y if want to do web-checking: ")).upper()
                if (sqlquery == 'Y'):
                    sqcur.execute("update Passengers set Web_Checkin='Y' where PNR = " + "'" + pnr + "'")
                    sq.commit()
                    print "Web checkin is done succesfully your seat number is",seat
        elif (sqlquery == '3'):
            booking()
        elif (sqlquery == '2'):
            return

def Passengers_details():
    while True:
        sqlquery = raw_input("\nTo get the list and count of passengers who are either coming and going from particular station press 6 else press 1 to exit: ")
        if (sqlquery == '1'):
            return
        if (sqlquery != '6'):
            continue
        name = (raw_input("Enter airport name: ")).upper()
        count = pd.read_sql_query("Select COUNT(*) as count from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER AND (SOURCE=" + "'" + name + "'" + " OR DESTINATION="+"'" + name + "'" +")", sq)
        count = count['count'].iloc[0]
        df = pd.read_sql_query("Select PNR,First_Name,Last_Name,Gender,`Class/Seat`,Mobile_number,Passengers.FLIGHT_NUMBER,SOURCE,DESTINATION from Passengers,Flights where Passengers.FLIGHT_NUMBER=Flights.FLIGHT_NUMBER AND (SOURCE=" + "'" + name + "'" + " OR DESTINATION="+"'" + name + "')", sq)
        if (df.empty):
            print ("No passenger has booked flight from this route no flight exist on this station name.")
        else:
            print "Total of passengers are:",count
            print ("Passenger details")
            print tabulate(df, headers='keys', tablefmt='psql')

def main():
    while True:
        command = raw_input("\nPress S if you are Security Personnel.\nPress F if you are Flight Staff.\nPress P if Passengers.\nPress 1 to know the details of all flights departing and arriving from particular airport.\nPress 2 to see list of all passengers arriving or departing from particular airport.\nPress E to exit.\nInput: ")
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
        elif (command == "1"):
            Flight_details()
        elif (command == "2"):
            Passengers_details()

if __name__ == "__main__":
    main()
