import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('sales_data_sample.csv', encoding='ISO-8859-1')

# Convert ORDERDATE to datetime
data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])

# User inputs for start and end date
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Filter the data based on user input
filtered_data = data[(data['ORDERDATE'] >= start_date) & (data['ORDERDATE'] <= end_date)]

# Check if the filtered data has any entries
if filtered_data.empty:
    print("No data found for the selected date range.")
else:
    # Plot the sales trend for the selected date range
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_data['ORDERDATE'], filtered_data['SALES'], marker='o', linestyle='-', color='b')
    plt.title(f'Sales Trends from {start_date} to {end_date}')
    plt.xlabel('Order Date')
    plt.ylabel('Sales')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()
