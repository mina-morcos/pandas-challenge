# Dependencies and Setup
import os
import csv
import pandas as pd

# File to Load
file_to_load = os.path.join("Resources","purchase_data.csv")

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


#PLAYER COUNT
#the total number of players 
player= len(purchase_data["SN"].value_counts())
player_count=pd.DataFrame([player], columns = ["Total Players"])
player_count

#PURCHASING ANALYSIS TOTAL
#finding number of unique items
UniqueItems = len(purchase_data["Item Name"].unique())

#averge of price 
Avgprice = purchase_data["Price"].mean()

NumPur = len(purchase_data["Item Name"])

#total rev
Rev = purchase_data["Price"].sum()

# Create new DataFrame
Purchasing_Analysis_Total = pd.DataFrame({"Number of Unique Items": [UniqueItems],
                                           "Average Price": [Avgprice],
                                           "Number of Purchases": [NumPur],
                                           "Total Revenue": [Rev]})

# DataFrame formatting
Purchasing_Analysis_Total["Average Price"] = Purchasing_Analysis_Total["Average Price"].map("${:.2f}".format)
Purchasing_Analysis_Total["Total Revenue"] = Purchasing_Analysis_Total["Total Revenue"].map("${:.2f}".format)
Purchasing_Analysis_Total = Purchasing_Analysis_Total[["Number of Unique Items", "Average Price", "Number of Purchases", "Total Revenue"]]

Purchasing_Analysis_Total

#GENDER DEMOGRAPHISC
# Grouping by gender & counting
gender = purchase_data[["SN", "Gender"]]

gender = gender.drop_duplicates()

counts = gender["Gender"].value_counts()

# List of values
total_counts = [counts[0],counts[1],counts[2]]
percents = [round((counts[0]/player)*100,2),round((counts[1]/player)*100,2),round((counts[2]/player)*100,2)]

# Creating DataFrame & setting index
gender_demo = pd.DataFrame({ "Percentage of Players": percents,"Total Count": total_counts
})
gender_demo.index = (["Male", "Female", "Other / Non-Disclosed"])
gender_demo

#PURCHASING ANALYSIS GENDER
# Group by Gender
gender = purchase_data.groupby(["Gender"])

# Data Manipulation
purch_Count = gender["SN"].count()

purch_Price = gender["Price"].mean()

purch_Value = gender["Price"].sum()

# Normalize data by deleting all duplicates adn resort
duplicates = purchase_data.drop_duplicates(subset='SN', keep="first")
grouped_dup = duplicates.groupby(["Gender"])

# Find normalized data
purch_Norm = (gender["Price"].sum() / grouped_dup["SN"].count())

# Create new DataFrame
Purch_Anal_Gen = pd.DataFrame({"Purchase Count": purch_Count,
                              "Average Purchase Price": purch_Price,
                              "Total Purchase Value": purch_Value,
                              "Normalized Totals": purch_Norm})
# DataFrame formatting
Purch_Anal_Gen["Average Purchase Price"] = Purch_Anal_Gen["Average Purchase Price"].map("${:.2f}".format)
Purch_Anal_Gen["Total Purchase Value"] = Purch_Anal_Gen["Total Purchase Value"].map("${:.2f}".format)
Purch_Anal_Gen["Normalized Totals"] = Purch_Anal_Gen["Normalized Totals"].map("${:.2f}".format)
Purch_Anal_Gen = Purch_Anal_Gen[["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]
Purch_Anal_Gen

#AGE DEMOGRAPH
# Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#database for age Demo
purchase_data["Age Demographics"]= pd.cut(purchase_data["Age"], age_bins, labels=group_names)
demographic_group =purchase_data.groupby("Age Demographics")

purchase_data.head()

#PURCHASING ANALYSIS AGE
age_purchasing_df = purchase_data
age_purchasing_df['Age Groups'] = pd.cut(purchase_data['Age'], age_bins, labels = group_names)

age_purchasing_analysis_df = age_purchasing_df[['Price', 'Age Groups']].groupby(['Age Groups']).count()
age_purchasing_analysis_df['Average Purchase Price'] = age_purchasing_df[['Price', 'Age Groups']].groupby(['Age Groups']).mean()
age_purchasing_analysis_df['Total Purchase Price'] = age_purchasing_df[['Price', 'Age Groups']].groupby(['Age Groups']).sum()
age_purchasing_analysis_df['Normalized Totals'] = (age_purchasing_analysis_df['Total Purchase Price'] / purchase_data["Age Demographics"])

age_purchasing_analysis_df['Average Purchase Price'] = age_purchasing_analysis_df['Average Purchase Price'].map('${:,.2f}'.format)
age_purchasing_analysis_df['Total Purchase Price'] = age_purchasing_analysis_df['Total Purchase Price'].map('${:,.2f}'.format)
age_purchasing_analysis_df['Normalized Totals'] = age_purchasing_analysis_df['Normalized Totals'].map('${:,.2f}'.format)

age_purchasing_analysis_df

#TOP SPENDERS
#define top spender 
top_spenders = purchase_data['Item ID'].groupby(purchase_data['SN']).count()

# set the dataframe for top spender 
top_spenders= pd.DataFrame(data=top_spenders)
top_spenders.columns = ['Purchase Count']

top_spenders['Average Purchase Price'] = round(purchase_data['Price'].groupby(purchase_data['SN']).mean(),2)
top_spenders['Total Purchase Value'] = purchase_data['Price'].groupby(purchase_data['SN']).sum()


top_spenders.sort_values(by=['Total Purchase Value'], ascending=False, inplace=True)

top_spenders['Average Purchase Price'] = top_spenders['Average Purchase Price'].map('${:,.2f}'.format)
top_spenders['Total Purchase Value'] = top_spenders['Total Purchase Value'].map('${:,.2f}'.format)

top_spenders.head()

#MOST POP ITEMS
#define most items 
most_items = purchase_data.groupby(['Item ID', 'Item Name','Price'])['Price'].agg(['count','sum'])
most_items.columns = ['Purchase Count', 'Total Purchase Value']

# set the index back at zero 
most_items.reset_index(inplace=True)
most_items.set_index(['Item ID','Item Name'] ,inplace=True)

most_items = most_items[['Purchase Count', 'Price', 'Total Purchase Value']]

#Sort the purchase count column in descending order
most_popular_items = most_items.sort_values(by='Purchase Count', ascending=False)

#farmmat of the data base 
most_popular_items['Price'] = most_popular_items['Price'].map('${:,.2f}'.format)
most_popular_items['Total Purchase Value'] = most_popular_items['Total Purchase Value'].map('${:,.2f}'.format)

most_popular_items.head()

#MOST PROFIT ITEMS
#in descending order 
most_profitable_items = most_items.sort_values(by='Total Purchase Value', ascending=False)

#the data frame 
most_profitable_items['Price'] = most_profitable_items['Price'].map('${:,.2f}'.format)
most_profitable_items['Total Purchase Value'] = most_profitable_items['Total Purchase Value'].map('${:,.2f}'.format)
most_profitable_items.head()
