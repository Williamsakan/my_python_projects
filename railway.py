"""
Railway.py
This module gives answers relevant questions and share insights on Railway_new.csv file.
It reads in the .csv file, then share some insights about the data. You should run the read_csv() function first before 
running other functions

Functions:
    - read_csv: Reads in the data into our notebook or IDE
    - total_revenue: This gives the total revenue generated from all ticket sales.
    - popular_purchase_type: It tells which purchase type (Online or Station) is more popular among passengers
    - top_10_routes: It tells the top 10 most popular routes based on ticket sales volume
    - avg_price_per_class: it tells the average ticket price by ticket class (Standard vs First)
    - avg_price_by_type: It displays the ticket type and the average ticket price
    - ticket_type_and_price_corr: It shows the correlation between ticket Price and ticket type. From the result gotten,
    it shows that ticket type affects the average ticket price. After running this function, you can run the code below
    df = df.drop('ticket_type', axis=1), so that we don't have another ticket_type column
    - highest_avg_ticket_price: It shows the top 5 routes that has the highest average ticket price.
    - journey_percent: it shows the percentage ofjourneys that were delayed versus on time
    - most_delayed_routes: It shows the top 5 routes that experienced most delays
    - reasons_for_delays: It shows the top 5 reasons for delays across all journeys
    - delayed_refund_request: It tells how many delayed journeys led to refund requests.
    - refund_delayed_journeys: It tells the percentage of all refund which were caused by delayed journeys
    - refund_purchase: It tells if refunds are more common online or in station purchases
    - sales_revenue_per_month: It displays the ticket sales revenue per month in a sorted order (Descending). You can run the
    code df = df.drop('Month', axis=1) after running the function so that we don't add more column to our dataset
    - purchased_tickets_time: It displays the number tickets most frequently purchased (morning, afternoon, evening). You can
    run the code df = df.drop(['Time_of_Day', 'Hour'], axis=1) after running the function so that we don't add more column to
    our dataset
    - weekends_or_weekdays: It tells the number of delays more common during weekends compared to weekdays. You can run the 
    code df = df.drop(['DayOfWeek', 'Day_of_Week'], axis=1) after running the function so that we don't add more column to our
    dataset
"""
import numpy as np
import pandas as pd
import re

def read_csv():
    df = pd.read_csv("railway_new.csv")
    df.columns = [col.replace(" ","_") for col in df.columns]
    return df

def total_revenue(df, column='Price'):
    a = f'Total revenue generated from all ticket sales: {df[column].sum()}'
    return a

def popular_purchase_type(df, column='Purchase_Type'):
    a = f'Popular purchase type among passengers: {df[column].value_counts(ascending=False).index[0]}'
    return a

def top_10_routes(df, column1='Departure_Station', column2='Arrival_Destination'):
    route_sales = (
        df.groupby([column1, column2])
          .size()  # counts number of rows (tickets)
          .reset_index(name='Tickets_Sold')
          .sort_values(by='Tickets_Sold', ascending=False)
    )
    print("The top ten popular routes based on tickets price are given below:")
    return route_sales.head(10)

def avg_price_by_class(df, column1='Ticket_Class', column2='Price'):
    print("The average price for each Ticket class is given below:")
    return df.groupby(column1)[column2].mean().reset_index()

def avg_price_by_type(df, column1='Ticket_Type', column2='Price'):
    print("the average price for each ticket type is given below:")
    return df.groupby(column1)[column2].mean().reset_index(name='Average_Price').sort_values(by='Average_Price', ascending=False)

def ticket_type_and_price_corr(df):
    ticket_type_map = {'Advance': 0, 'Off-Peak': 1, 'Anytime': 2}
    df['ticket_type'] = df['Ticket_Type'].map(ticket_type_map).astype(int)
    a = f"correlation between Ticket_Type and Price is {df['ticket_type'].corr(df.Price)}"
    return a

def highest_avg_ticket_price(df, column1='Departure_Station', column2='Arrival_Destination', column3='Price'):
    a = (df.groupby([column1, column2])[column3].mean()
         .reset_index(name='Average_Price').sort_values(by='Average_Price', ascending=False))
    print("The top 5 highest average price for journey routes are given below:")
    return a.head(5)

def journey_percent(df, column='Journey_Status'):
    a = df.groupby(column).size().reset_index(name='Count').sort_values(by='Count',ascending=False)
    a['Percent'] = round(a['Count'].apply(lambda x: (x/len(df)) * 100), 2)
    print("The percentage of each Journey status are given below:")
    return a[['Journey_Status', 'Percent']]

def most_delayed_routes(df, column='Journey_Status', status='Delayed'):
    filtered_df = df[df[column] == status]
    filtered_df = filtered_df.groupby(['Departure_Station', 'Arrival_Destination']).size().reset_index(name='Count').sort_values(by='Count',ascending=False)
    print("The top 5 most delayed routes:")
    return filtered_df.head()

def reasons_for_delays(df, column='Journey_Status', status='Delayed'):
    filtered_df =  df[df[column] == status]
    print("Top 5 reasons for delays on all journey routes:")
    return filtered_df['Reason_for_Delay'].value_counts().reset_index(name='Count').sort_values(by='Count', ascending=False).head(5)

def delayed_refund_request(df, column1='Journey_Status', column2='Refund_Request', status1='Delayed', status2='Yes'): 
    a = len(df[(df[column1] == status1) & (df[column2] == status2)])
    return f'{a} delayed journeys let to refund requests'

def refund_delayed_journeys(df, column1='Refund_Request', column2='Journey_Status', status1='Yes', status2='Delayed'):
    filtered_df = df[df[column1] == status1] # This filters the df where all the Refund_Request column is 'Yes'
    a = len(filtered_df)
    filtered_df = filtered_df.groupby([column2]).size().reset_index(name='Count')
    filtered_df['Percent'] = filtered_df['Count'].apply(lambda x: (x/a) * 100)
    b = (filtered_df[filtered_df[column2] == status2].index)[0]
    return f'The percentage of all refunds caused by delayed journeys:{filtered_df.loc[b, 'Percent']:.2f}%'

def refund_purchase(df, column1='Refund_Request', column2='Purchase_Type', status='Yes'):
    filtered_df = df[df[column1] == status]
    a = list(filtered_df.groupby([column2]).size().reset_index(name='Count').sort_values(by='Count', ascending=False).Purchase_Type)[0]
    return f"The most common refund purchase type is: {a}"

def sales_revenue_per_month(df):
    df['Date_of_Purchase'] = pd.to_datetime(df['Date_of_Purchase'], format='%m/%d/%Y', errors='coerce')
    df['Month'] = df['Date_of_Purchase'].dt.month
    month_map = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    df['Month'] = df['Month'].map(month_map)
    print("An Ordered sales ticket revenue per month:")
    return display(df.groupby(['Month'])['Price'].sum().reset_index(name='Total_Sales').sort_values(by='Total_Sales', ascending=False))

def purchased_tickets_time(df):
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], format='%H:%M:%S', errors='coerce')
    df['Hour'] = df['Time_of_Purchase'].dt.hour
    conditions = [
        (df['Hour'] < 12),
        (df['Hour'] >= 12) & (df['Hour'] < 17),
        (df['Hour'] >= 17)
    ]
    choices = ['Morning', 'Afternoon', 'Evening']

    df['Time_of_Day'] = np.select(conditions, choices)

    summary = df.groupby('Time_of_Day').size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    print("The Ordered number of sales of tickets purchased during the time of day:")

    return summary

def weekends_or_weekdays(df):
    # Convert to datetime if not already
    df['Date_of_Purchase'] = pd.to_datetime(df['Date_of_Purchase'], errors='coerce')

    # Extract weekday (Monday=0, Sunday=6)
    df['DayOfWeek'] = df['Date_of_Purchase'].dt.weekday

    # Create Weekday/Weekend labels
    conditions = [
        (df['DayOfWeek'] <= 4),
        (df['DayOfWeek'] >= 5)
    ]
    choices = ['Weekday', 'Weekend']

    df['Day_Type'] = np.select(conditions, choices)

    # Optional summary
    summary = df['Day_Type'].value_counts().reset_index()
    summary.columns = ['Day_Type', 'Count']
    return summary
