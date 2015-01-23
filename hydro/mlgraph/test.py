from datetime import datetime
from time import mktime
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


# csv_file = r"C:\Users\kacalica\Desktop\test.csv" 

def grab_data_csv(csv_file):


	#take data from csv into pandas data frame object
	data = pd.read_csv(csv_file)

	#extraction into list 
	tmpx = list(data['timedate'])
	tmpy = list(data['Xvalues'])
	date_range = len(tmpx)
	
	return tmpx, tmpy, date_range 
		
	#converts date into usable format
	#make a more general function that handles any date format 
def date_conversion(tmpx, date_range): 
	i = 0
	for date in tmpx : 
		date = time.strptime(date,"%d-%b-%y" )
		date = datetime.fromtimestamp(mktime(date))
		tmpx[i] = date
		i = i + 1 
	#converts time.struct_time object dates list into list of numbers for plot
	ml_dates = matplotlib.dates.date2num(tmpx)
	return ml_dates

def graph_data(dates, Yvalues):	
	plt.plot_date(dates, Yvalues) #plots the data
	plt.show() #actually shows the data 
	
	
# def main():	 

	# data = grab_data_csv(csv_file) 
	# dates = date_conversion(data[0], data[2])
	# print data[1]
	# print "\n"
	# print dates
	# print "\n"
	# graph_data(dates, data[1])
	

# main()