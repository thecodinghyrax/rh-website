import calendar

def calendar_dict_creator(year, month):
    '''
        Returns a dict with a (year, month, day, day-of-week) tuple as key and name of day as value
    '''
    cal = calendar.Calendar(firstweekday=6)

    def day_check(base, day):
        if day == base or day == base % 7:
            return True
        else:
            return False
    cal_dict ={}
    for day in cal.itermonthdays4(year, month):
        day_of_week_num = day[3]
        day_of_month = day[2]
        if day_of_month != 0:
            if day_check(0, day_of_week_num):
                cal_dict[day] = 'Monday'
            elif day_check(1, day_of_week_num):
                cal_dict[day] = 'Tuesday'
            elif day_check(2, day_of_week_num):
                cal_dict[day] = 'Wednesday'
            elif day_check(3, day_of_week_num):
                cal_dict[day] = 'Thursday'
            elif day_check(4, day_of_week_num):
                cal_dict[day] = 'Friday'
            elif day_check(5, day_of_week_num):
                cal_dict[day] = 'Saturday'
            elif day_check(6, day_of_week_num):
                cal_dict[day] = 'Sunday'
            else:
                print('The day passed doesn\'t match a day of the week!')

    return cal_dict

# to test
sept = calendar_dict_creator(2019, 8)

for key, value in sept.items():
    print('{} is {}'.format(key, value))

# Three ways to loop through a dict
# my_dict = {"one": 1,"two":2,"three":3,"four":4}
# for item in my_dict:
#     print("Key : {} , Value : {}".format(item,my_dict[item]))

# for key,value in my_dict.items():
#     print("Key : {} , Value : {}".format(key,value))

# for key in my_dict.keys():
#     print("Key : {} , Value : {}".format(key,my_dict[key]))
