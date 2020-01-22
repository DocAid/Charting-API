# library
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
x = ["Jan","Feb","March","April","May","June"]
y = [40000,32000,34000,42000,26000,45000]

plt.plot(x,y,
label= "Earnings per Month",  marker= "o", color='blue', linestyle='solid', linewidth = 3, markerfacecolor='blue',markersize=12) 
plt.xlabel('Month') 
plt.ylim(0,50000)
plt.ylabel('Earnings (in Rupees)') 
plt.legend()
plt.title("Earnings per month") 

plt.plot(x,y,
label= "Salary per month",  marker= "o", color='green', linestyle='dashed', linewidth = 3, markerfacecolor='blue',markersize=12) 
plt.savefig('docChart3.png')
    

