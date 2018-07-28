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
def security_personnel():
    while True:
    #take passengers details
    #if all informations are correct press y else n
    #if press wrong again restart loop
    #if press 4 return to main menu

def Flight_staff():
     while True:
         #take passengers details
         #if all informations are correct press y else n
         #if press wrong again restart loop
         #if press 4 return to main menu

def passenger():
    while True():
        #want to book flight
        #want to see past bookings
        #want to exit
        #flights with empty seats

def main():
    while True:
    print ("press S if Security Personnel")
    print ("press F if Flight Staff")
    print ("press P if Passengers")
    print ("To know the details of all flights departing and arriving from particular airport press 1.")
    print ("List of passengers arriving or departing from particular airport press 2")
    #print ("To display the list of passengers (sorted by name) for a given airline who cleared security checkins press 3")
    #print ("To exit press 4")
    #print ("Clear a passenger for security personnel press 6")
    print ("press E to exit.")
    if (command == "4"):
       sys.exit()

if __name__ == "__main__":
    main()
