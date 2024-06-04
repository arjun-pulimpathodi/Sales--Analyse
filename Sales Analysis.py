#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import matplotlib.pyplot as plt
import os


# In[47]:


# In the data sets, we have 12 months datasets and we have to merge them first


# In[48]:


files=[file for file in os.listdir('E:\\UpGrad\\Pandas-Data-Science-Tasks-master\\SalesAnalysis\\Sales_Data')]
for file in files:
    print(file)


# - These are our 12 months data and we are concatenate these files

# In[49]:


csv_files=['Sales_April_2019.csv','Sales_August_2019.csv','Sales_December_2019.csv','Sales_February_2019.csv','Sales_January_2019.csv',
           'Sales_July_2019.csv','Sales_June_2019.csv','Sales_March_2019.csv','Sales_May_2019.csv','Sales_November_2019.csv',
           'Sales_October_2019.csv','Sales_September_2019.csv']
directory='E:\\UpGrad\\Pandas-Data-Science-Tasks-master\\SalesAnalysis\\Sales_Data'

sales_data=[]

for file in csv_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    sales_data.append(df)
concatenated_df = pd.concat(sales_data, ignore_index=True)
output_file_path = 'E:\\UpGrad\\Pandas-Data-Science-Tasks-master\\SalesAnalysis\\Sales_Data\\concatenated_sales_data.csv'
concatenated_df.to_csv(output_file_path, index=False)


# - Now we have concatenated all the 12 datasets into one data set. and we are going to to analyze that data set

# In[50]:


sales=pd.read_csv('E:\\UpGrad\\Pandas-Data-Science-Tasks-master\\SalesAnalysis\\Sales_Data\\concatenated_sales_data.csv')
sales.head()


# In[51]:


sales.shape


# In[52]:


sales.info()


# In[53]:


# Checking the null vales


# In[54]:


sales.isnull().sum()


# In[55]:


((sales.isnull().sum() / len(sales)) * 100)


# - The null values are in less numbers compared to known value, so we can drop these null values

# In[56]:


sales=sales.dropna()


# In[57]:


sales.shape


# We need to add to column for analysis

# In[58]:


sales['Month']=sales['Order Date'].str[0:2]
sales.head()


# In[62]:


invalid_rows = sales[sales['Quantity Ordered'] == 'Quantity Ordered']
sales = sales.drop(invalid_rows.index)


# In[63]:


sales['Quantity Ordered'] = pd.to_numeric(sales['Quantity Ordered'])
sales['Price Each'] = pd.to_numeric(sales['Price Each'])


# In[64]:


sales.head()


# In[65]:


# Adding a colums name 'Amount' to see the totel amount individual paid for each order
sales['Amount'] = sales['Quantity Ordered'] * sales['Price Each']
sales.head()


# In[77]:


sales['City']=sales['Purchase Address'].apply(lambda x: x.split(',')[1])
sales.head()


# In[ ]:


# Now we have cleaned and made the data for analysis


# ## EDA

# ### Month v/s Sales

# In[72]:


sale_in_month=sales.groupby('Month')['Amount'].sum()


# In[68]:


sales.groupby('Month')['Amount'].sum().nlargest(3)


# - These are the top 3 Months, which they got highest sales in the year.
# - highest sale happend in December followed by October and April

# In[76]:


months = sale_in_month.index
amounts = sale_in_month.values
plt.figure(figsize=(10, 6))
plt.bar(months, amounts, color='skyblue')
plt.xlabel('Month')
plt.ylabel('Total Sales Amount')
plt.title('Total Sales Amount by Month')
plt.xticks(months)  
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# ### City v/s Sales 

# In[79]:


sale_in_city=sales.groupby('City')['Amount'].sum()
sale_in_city


# In[80]:


sales.groupby('City')['Amount'].sum().nlargest(3)


# - The city which had most sales in that year is San Francisco follwed by Los Angeles and New York City

# In[83]:


city = sale_in_city.index
amounts = sale_in_city.values
plt.figure(figsize=(10, 6))
plt.bar(city, amounts, color='skyblue')
plt.xlabel('City')
plt.ylabel('Total Sales Amount')
plt.title('Total Sales Amount by City')
plt.xticks(city,rotation=90)  
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# ###  Time v/s Sales

# - Determine which is the best time to offer discounds,combo offers etc to boost sales

# In[84]:


#we need to change the Order date to datetime object


# In[85]:


sales['Order Date']=pd.to_datetime(sales['Order Date'])


# In[86]:


sales.head()


# In[95]:


sales['Hours']=sales['Order Date'].dt.hour
sales.head()


# In[96]:


hourly_sales = sales.groupby('Hours')['Amount'].sum()
hourly_sales 


# In[99]:


hours = hourly_sales.index
amounts = hourly_sales.values


# In[101]:


plt.plot(hours, amounts, marker='o', linestyle='-', color='b')
plt.xlabel('Hours')
plt.ylabel('Total Sales Amount')
plt.title('Total Sales Amount by Hour')
plt.xticks(hours)  
plt.grid(True)
plt.show()


# - From this line chart, we can observe that the peak time of orders are between 10-11 AM and & 7-8 PM

# ### Products Sold

# In[102]:


product_sales = sales.groupby('Product')['Quantity Ordered'].sum()
product_sales


# In[103]:


top_selling_products = product_sales.sort_values(ascending=False)
top_selling_products


# In[106]:


top_selling_products.plot(kind='bar', figsize=(12, 8), color='skyblue')
plt.xlabel('Product')
plt.ylabel('Quantity Ordered')
plt.title('Top Selling Products')
plt.xticks(rotation=90, ha='right')
plt.show()


# ### Inferences

# - Highest sale happend in December followed by October and April
# - The city which had most sales in that year is San Francisco follwed by Los Angeles and New York City
# - The peak time of orders are between 10-11 AM and & 7-8 PM
# - Electronic Items are selling often. Need to make offers on electronic items which will increase the orders

# In[ ]:




