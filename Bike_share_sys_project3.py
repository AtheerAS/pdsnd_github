import time
import datetime as dt
import pandas as pd
import numpy as np
from pyfiglet import Figlet
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()
####
welcome_text = Figlet(font='slant')
print(welcome_text.renderText('Explore The US Bike Share Data'))
###

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    print(colored('Hello! Let\'s explore some US bikeshare data!', 'blue'))

    # get user input for city (chicago, new york city, washington).

    while True:
        city = input("Would you like to see data for Chicago, New York city, or Washington?").lower()
        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print(colored('\nNot quiet a valid input, try again!','red'))
        else:
            break
    while True:
        month = input("Which month? -January, February, March, April, May, June, or type 'all'").lower()
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print(colored('\nNot quiet a valid input, try again!','red'))
        else:
            break
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type 'all'").lower()
        if day.lower() not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print(colored('\nNot quiet a valid input, try again!','red'))
        else:
            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time']) #change object type
    df['day'] =  df['Start Time'].dt.day_name() #day column
    df['month'] = df['Start Time'].dt.month #month column

    #filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]
    #filter by day
    if day != 'all':
       df = df[df['day'] == day.title()]

    return df

def time_stats(df):
    print(colored('\nCalculating The Most Frequent Times of Travel...\n','green'))
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    most_common_day = df['day'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour #hour column
    most_common_hour = df['hour'].mode()[0]

    print(colored('These are some statistics regarding travel time: \n the most popular month in which bikes were shared was {}.\n the most popular day of the week in which bikes were shared was {}. \n the most popular hour in which bikes were shared was {}.','grey','on_white').format(most_common_month, most_common_day,most_common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print(colored('\nCalculating The Most Popular Stations and Trip...\n', 'green'))
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    most_frequent_station_combination = df.value_counts(['Start Station', 'End Station']).index.tolist()[0]

    print(colored('\nThe most popular start station was {}.\nThe most popular end station was {}. \nWhile the  most frequent combination of start and end stations was {}.','grey','on_white').format(common_start_station, common_end_station, most_frequent_station_combination))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print(colored('\nCalculating Trip Duration...\n','green'))
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total =dt.timedelta(seconds = total_travel_time)

    # display mean travel time
    mean_of_travel_time = df['Trip Duration'].mean()
    mean = dt.timedelta(seconds = mean_of_travel_time)

    print(colored("\nTotal travel time 'in days' was {}.\nThe mean of travel durations was {}",'grey','on_white').format(total, mean))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print(colored('\nCalculating User Stats...\n','green'))
    start_time = time.time()

    # Display counts of user types
    all_users = df['User Type'].value_counts()
    print('\nUser Stats:\n', all_users)

    # Display counts of gender
    if 'Gender'in df:
        gender_count = df['Gender'].value_counts()
        print('\nGenders:\n', gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        most_common_birth_year = df['Birth Year'].mode()[0]
        most_recent_birth_year = df['Birth Year'].min()
        earliest_birth_year = df['Birth Year'].max()
        print(colored('\nThe most_common_birth_year is {}. \nThe youngest user was born in {}.\nWhile the oldest user was born in {}.','grey','on_white').format(most_common_birth_year, earliest_birth_year, most_recent_birth_year ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#row data
def display_data(df):
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        if view_data.lower() not in ('yes', 'no', 'n', 'y', 'Yes', 'No', 'YES','NO'):
            print('\nNot a valid input, please try again with yes or no input')
        else:
            start_loc = 0
            while view_data != 'no':
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_display = input("\nDo you wish to continue?: Enter yes or no.\n").lower()
            if view_display != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
