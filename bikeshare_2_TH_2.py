import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_names = ['chicago', 'new york city', 'washington']
month_names = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
day_names = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

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
    try:
        city = input("\nPlease select which city you would like to analyze? ").lower()
    except ValueError:
        print('\nThat is not a string!')
    while (city not in city_names):
        print('\nThat is not a valid city! Please enter one of chicago, new york city or washington')
        try: city = input("\nPlease select which city you would like to analyze? ").lower()
        except ValueError:
            print('\nThat is not a string! Please enter one of chicago, new york city or washington')

    # get user input for month (all, january, february, ... , june)

    try:
        month = input("\nPlease enter which specific month you would like to analyze? Or choose all: ").lower()
    except ValueError:
        print('\nThat is not a string! Please enter a specific month or all')
    while (month not in month_names):
        print('\nThat is not a valid month! Please enter which specific month you would like to analyze - or choose all')
        try: month = input("\nPlease enter which specific month you would like to analyze? Or choose all: ").lower()
        except ValueError:
            print('\nThat is not a string! Please enter a specific month or all')

    # get user iqunput for day of week (all, monday, tuesday, ... sunday)

    try:
        day = input("\nPlease enter which specific day you would like to analyze? Or choose all: ").lower()
    except ValueError:
        print('\nThat is not a string! Please enter a specific month or all')
    while (day not in day_names):
        print('\nThat is not a valid day! Please enter which specific day you would like to analyze - or choose all')
        try: day = input("\nPlease enter which specific day you would like to analyze? Or choose all: ").lower()
        except ValueError:
            print('\nThat is not a string! Please enter a specific day or all')

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

    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the start_time column to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        #use index of months list to get corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1

        # filter by month to create the new DataFrame
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most popular month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost popular day:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nMost popular end station: ', end_station)

    # display most frequent combination of start station and end station trip
    df['combination_stations'] = df['Start Station'] + df['End Station']
    combination_station = df['combination_stations'].mode()[0]
    print('\nMost popular combination of start and end station: ', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60 / 60 /24
    print('\nTotal time travelled in days is: ', round(total_travel_time, 1), 'days')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('\nMean travel time in minutes is:', round(mean_travel_time,1), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe number of different types of user is: \n', user_types)

    # Display counts of gender - need to do something about washington ...
    try:
        gender_types = df['Gender'].value_counts()
        print('\nThe number of different types of gender is: \n', gender_types)
    except KeyError:
        print('\nThere is no gender data for washington\n')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])
        print('\nThe earliest year of birth is: ', earliest_birth)
        print('\nThe most recent year of birth is: ', most_recent_birth)
        print('\nThe most common year of birth is: ', most_common_birth)
    except KeyError:
        print('\nThere is no birth data for washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    # Ask the user if they want to see 5 lines of raw data
    i = 0
    raw = input('Would you like to see five lines of raw data? \n Type yes or no. ').lower()
    pd.set_option('display.max_columns',200)

    while True:
    # Asks if user wants to see five more lines of code
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5])
            raw = input("Would you like to see five more lines of raw data? Type yes or no. \n").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        # Ask the user if they want to restart the analysis 
        if restart.lower() != 'yes':
            print("Goodbye!")
            break

if __name__ == "__main__":
	main()
