import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
              
              
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). 
    
    while True:
        city = input("\nWould you like to see data for chicago, new york city, or washington?\nInput name of city here: ")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("\nInvalid input, pick from; chicago, new york city, washington. Now try again!")
            
    # get user input for month (all, january, february, ... , june)
    
    while True:    
        month = input("\n Would you like to see details specific to a particular month? If yes, type name of month in words from january to june else type 'all' to apply no month filter: ")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("\nInvalid input, pick from; january-june. OR Enter name of month in words! Now try again! ")
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:
        day = input("\nType 'all' to apply no day filter OR Enter name of the day of week to filter by: ")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Invalid input! Tip: Enter name of day in words')
    print('-'*40)
    return city, month, day
    
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe      
        df = df[df['day_of_week'] == day.title()]
    return df
    
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    print("The most common month is ", months[df['month'].mode()[0]], "\n")
    # display the most common day of week
    print("The most common day of week  is ", df['day_of_week'].mode()[0], "\n")
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is ", df['hour'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0], "\n")
    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0], "\n")
    # display most frequent combination of start station and end station trip
    df['frequent_stations'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['frequent_stations'].mode()[0])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() 
    print('Total travel time in seconds: ', total_travel_time)
    
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time in seconds is: ', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df    
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    if city == 'chicago' or city == 'new york city':   
        gender = df['Gender'].value_counts()
        print(gender)
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()
        print("The earliest year of birth is ", int(earliest_birth), "\n")
        print("The most recent year of birth is ", int(recent_birth), "\n")
        print("The most common year of birth is ", int(common_year), "\n")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    """ 
    My script has to prompt the user whether they would like to see the raw data. 
    If the user answers 'yes,' then the script should print 5 rows of the data at a time, 
    then ask the user if they would like to see 5 more rows of the data. 
    The script should continue prompting and printing the next 5 rows at a time until the user chooses 'no,' 
    they do not want any more raw data to be displayed.
    """
    
    n = 1
    while True:
        raw_data = input('\nWould you like to see some raw data? Enter yes or no.\n').lower()
        if raw_data.lower() == 'yes':
            print(df[n:n+5])
            n = n+5
        else:
            break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
