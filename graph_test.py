__author__ = "Kyle Calica"

import pandas as pd
import matplotlib.pyplot as plt
import arrow #may need to download

def parse_csv(csv_name, key1, key2):
	xvalues = pd.read_csv(csv_name)
	tmpx = list(data[Key1]) #line to read from this column
	tmpy = list(data[Key2])
	#might just need pandas to do all the parsing or hold in another data object and return 
	return tmpx , tmpy


def create_graph(animate=false, source='csv', xvalue, yvalue, data-title ):
# animate is a bool variable, source states where it is coming from, xvalue and yvalue is axis, data-title is whole label for graph
#option to upload from CSV, API or Station 
#use xvalue and yvalue names to label axsis

plt.plot(xvalues, yvalues)
plt.xlabel('datetime')
#plt.show() #might want to animate 
#plt.axis() --> calculate axis range? Cleaner? 


def save_graph():
	#conn = sqlite3.connect("mydatabase.db")
	#cursor = conn.cursor()


"""
1) Read the data from csv
2) load into arrays for matplotlib
3) label according to sites and values
4) option animate or not (needs PIL)
"""
		

"""
pandas can grab from csv, dba and urls! 
wants graph creation first from csv files
then can save 

class Graphs(Models.model):
	Location --> Site

	
	x-values
	y-values
"""

	
