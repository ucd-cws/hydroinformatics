from datetime import datetime
from time import mktime
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#take data from csv into pandas data frame object
data = pd.read_csv("C:\\Users\\kacalica\\Desktop\\test.csv")

#extraction into list 
tmpx = list(data['timedate'])
tmpy = list(data['Xvalues'])
date_range = len(tmpx)



# date conversion 
i = 0
for date in tmpx : 
	date = time.strptime(date,"%d-%b-%y" )
	date = datetime.fromtimestamp(mktime(date))
	tmpx[i] = date
	i = i + 1 
#converts time.struct_time object dates list into list of numbers for plot
dates = matplotlib.dates.date2num(tmpx)



plt.plot_date(dates, tmpy) #plots the data
plt.show() #actually shows the data 

