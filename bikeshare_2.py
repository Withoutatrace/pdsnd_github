import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'Project/chicago.csv',
              'new york city': 'Project/new_york_city.csv',
              'washington': 'Project/washington.csv' }

month_choice = ['all', 'january', 'february', 'march', 'april', 'may', 'june'] # define month choices
day_choice = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] # define day choices

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
    print('Please input which city you want to select data from: {}'.format(list(CITY_DATA.keys())))
    city = input()
    while True: 
        if city.lower() not in list(CITY_DATA.keys()):
            print("Oops! Please input a city from these options: Chicago, New York City, Washington")
            city = input()
        else:
            break

    # get user input for month (all, january, february, ... , june)
    print('Please input which month you want to select data from: All, January, February, March, April, May, or June?')
    month = input()
    while True: 
        if month.lower() not in month_choice:
            print("Oops! Please input a city from these options: All, January, February, March, April, May, or June?")
            month = input()
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please input which day of the week you want to select data from: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
    day = input()
    while True: 
        if day.lower() not in day_choice:
            print("Oops! Please input a city from these options: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?")
            day = input()
        else:
            break

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.dayofweek
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
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day)
        df = df[df['dayofweek'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month: ' + calendar.month_name[common_month]) # could also use dt

    # display the most common day of week
    common_day = df['dayofweek'].mode()[0]
    print('The most common day: ' + calendar.day_name[common_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour: {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common start station: ' + common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station: ' + common_end)

    # display most frequent combination of start station and end station trip
    df['Start Station'] = df['Start Station'].astype(str)
    df['End Station'] = df['End Station'].astype(str)
    freq = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    print(freq.sort_values(by='Count', ascending=False).head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time: {} seconds = {} minutes = {} hours'.format(total_travel, total_travel / 60, total_travel / 3600))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('Average travel time: {}'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of each User Type: {}'.format(user_types))

    # Display counts of gender
    gender_counts = df['Gender'].value_counts()
    print('Count of each gender: {}'.format(gender_counts))

    # Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()
    recent_year = df['Birth Year'].max()
    common_year = df['Birth Year'].mode()[0]

    print('Earliest birth year: {}'.format(earliest_year))
    print('Most recent birth year: {}'.format(recent_year))
    print('Most common birth year: {}'.format(common_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
