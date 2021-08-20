import time
import pandas as pd
import numpy as np
import calendar as cal
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    """Ask user to provide city for analysis"""
    countries = ['chicago','new york city','washington']
    while True:
        try:
            city = (input("Please enter name of city :, chicago, new york city, washington\n" )).lower()
            if city in countries:
                break
            else:
                print("Please enter a valid city name: ('chicago','new york city' or 'washington')\n")
        except Exception as e:
            print("Error Occurred. {}".format(e))

    return city

def get_month():
    while True:
        try:
            month = (input("Please enter month name: (E.g: january,february, march...) or all. \n")).lower()
            month = month.title()
            if month in cal.month_name[1:13] or month == 'All':
                break
            else:
                print("Please enter a valid month name.")
        except Exception as e:
            print("Error has occurred. {}".format(e))

    return month

def get_day():
    while True:
        try:
            day = (input("Please enter day name: (E.g: monday,tuesday,wednesday...) or all. \n")).lower()
            day = day.title()
            if day in cal.day_name[0:] or day == 'All':
                break
            else:
                print("Please enter a valid day name. \n")
        except Exception as e:
            print("Error has occurred. {}".format(e))

    return day



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()


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
    # Load data file into a dataframe

    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))

    # Convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # Extract month and day of week from Start Time to create new columns

    df['Month Number'] = df['Start Time'].dt.month
    df['Weekday Name'] = df['Start Time'].dt.day_name()
    month_dict = {1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}

 #Create new column for month
    df['Month Name'] = df['Month Number'].map(month_dict)

    #Filter by month

    if month != 'All':
        df = df[df['Month Name'] == month.title()]
        if df.empty == True:
            print("Sorry! no data or records for this month. \n")
            option = str(input("Do you wish to enter different month? Yes or No. \n"))
            if option.title() == 'Yes':
                month = get_month()
                df = load_data(city,month,day)

    #Filter by day of week if applicable
    if day != 'All':

        #Filter by day of week to create new dataframe

        df = df[df['Weekday Name'] == day.title()]
        if df.empty == True:
            print("Sorry! no record for this day:.\n")
            option = str(input("Do you wish to enter different day? Yes or No. \n"))
            if option.title() == 'Yes':
                day = get_day()
                df = load_data(city,month,day)


    return df

def time_stats(df):
    """Displays statistics of the most frequent times of travel."""

    print('\nCalculating The Most Fequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Month Name'].mode()[0]
    print("The most common month from the filtered data is : {}.".format(common_month))


   # display the most common day of week
    common_day = df['Weekday Name'].mode()[0]
    print("The most common day of week filtered is : {}".format(common_day))



    # display the most common start hour
    freq_hour = df['Start Time'].dt.hour
    freq_hour = freq_hour.dropna()
    print('The Most Common Hour:', freq_hour.value_counts().idxmax())


    print("\nThis took %s Seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('The most common start Station from the filtered data is : {}'.format(Start_Station))


    # display most commonly used end station

    End_Station = df['End Station'].value_counts().idxmax()
    print("\nThe most common End Station is : {}".format(End_Station))


    # display most frequent combination of start station and end station trip

    common_start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("\nThe most requent combination of Start Station and End Station is:{}".format(common_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time

    total_travel_time = round(df['Trip Duration'].sum(),2)
    hr_travel_time = round(total_travel_time/60,2)
    day_travel_time = round(hr_travel_time/24,2)
    print("The total travel time is : {}(mins),{}(hrs),{}(days)".format(total_travel_time,hr_travel_time,day_travel_time))

    # display mean travel time

    mean_travel_time = round(df['Trip Duration'].mean(),2)
    hr_mean_time = round(mean_travel_time/60,2)
    day_mean_time = round(hr_mean_time/24,2)
    print("The Mean Travel time is : {}(mins),{}(hours),{}(days)".format(mean_travel_time,hr_mean_time,day_mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type_count = df.groupby(['User Type']).size()

    #print(user_types)
    print('The user Type counts are:\n'.format(user_type_count))


    # Display counts of gender

    try:
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this month!.")


    # Display earliest, most recent, and most common year of birth

    try:
        Earliest_Year = df['Birth Year'].min()
        print('\nEarliest_Year:',Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nNo data is available for month!.")
    try:
        Most_Recent_Year = df['Birth Year'].max()
        print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nNo data avalable for this month!.")
    try:
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month!.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Asking users whether he want to see first  5 rows of data"""

def raw_data(df):
    view_data = input("Would you like to view 5 rows of trip Enter yes or no?").lower()
    start_loc = 0
    while (view_data != 'no'):
        print(df.iloc[start_loc:start_loc+5])
        view_data = input("Do you wish to continue. Please type Yes or No.").lower()
        start_loc += 5
        while(view_data != 'no'):
            print(df.iloc[start_loc:start_loc+5])
            view_data = input ("Do you wish to continue? Enter yes or no.").lower()



def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

    """Thank the user for his feedback"""

    print("\nThank you for your Feedback.")
