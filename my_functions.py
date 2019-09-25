from datetime import date, timedelta

# today as a date object
today = date.today()
print('today as a date object')
print(today)
print(today.strftime('%Y-year, %m-month, %d-day'))
print('-'*80)

# adding days to todays date object
new_day = today + timedelta(days=7)
print('adding days to todays date object')
print(new_day)
print(type(new_day))
print('-'*80)

# creating a timedelta object and getting the total # of seconds
month = timedelta(days=31)
print('creating a timedelta object and getting the total # of seconds')
print(month.total_seconds())
print('-'*80)

# create a date object from a string
date_str = '2019-12-25'
date_obj = date.fromisoformat(date_str)
print('create a date object from a string')
print(date_obj)
print(type(date_obj))
print('-'*80)

# mock post with repet
print('Create a repeting post')
# title = input('Enter the title:\n>> ')
# post_date = input('Enter the post date as \'YYYY-MM-DD\':\n>> ')
# post_time = input('Enter the event time as a string: \n>> ')
# event = input('Enter the event details:\n>> ')
# repeat = input('Enter the number of times to repeat. Leave blank if no repeat:\n>> ')

# defaults
title = 'Devotionals'
post_date = '2019-09-23'
post_time = '8:00 PM to 9:00 PM'
event = 'We will be holding our Monday night devotionals.'
repeat = '25'

# repeat needs to be cast to an int so it can be used in the range function
repeat = int(repeat)

# This check will probably not be needed if the date is passed correctly from the HTML form
while type(post_date) == str:
    try:
        post_date = date.fromisoformat(post_date)
    except:
        print('That format is not right. Use YYYY-MM-DD')
        post_date = input('Enter the post date as \'YYYY-MM-DD\':\n>> ')

# Splitting the variables allowed me use focus on the date 
event_post_start = 'Join us for {} on '.format(title)
event_post_end = ' at {}. {}'.format(post_time, event)

# This is used to determin the type of the variables
# print('Here is your event:\n')
# print('title is typeof ', type(title))
# print('post_date is typeof ', type(post_date))
# print('post_time is typeof ', type(post_time))
# print('event is typeof ', type(event))
# print('repeat is typeof ', type(repeat))

# a Similar loop can be used to add the entries to the db
for post in range(repeat):
    print(event_post_start, post_date, event_post_end)
    week = timedelta(days=7)
    post_date = post_date + week

