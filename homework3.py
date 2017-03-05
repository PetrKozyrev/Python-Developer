# 1
from datetime import datetime as dt

def days_to_new_year():
    current_year = dt.now().year
    if current_year % 4 == 0:
        month_dict = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
                  9: 30, 10: 31, 11: 30, 12: 31}
        number_of_days = 366
    else:
        month_dict = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
                  9: 30, 10: 31, 11: 30, 12: 31}
        number_of_days = 365

    current_month = dt.now().month
    current_day = dt.now().day

    day_of_the_year = 0
    for key, value in month_dict.items():
        if key < current_month:
            day_of_the_year += month_dict[key]
        elif key == current_month:
            day_of_the_year += current_day
    return "Days to New Year: ", number_of_days - day_of_the_year
print(days_to_new_year())

# 2
def palindrome_finder(sequence):
    sequence = str(sequence)
    i = 0
    j = len(sequence) - 1
    while True:
        if i == j:
            return True
        elif sequence[i] == sequence[j]:
            i += 1
            j -= 1
        elif sequence[i] != sequence[j]:
            return False
print(palindrome_finder(11311))

#3
def quarter_classifier(x, y):
    if x == 0 or y == 0:
        return "It's impossible to determine quarter"
    else:
        if x > 0:
            if y > 0:
                return 1
            else:
                return 4
        else:
            if y > 0:
                return 2
            else:
                return 3
print(quarter_classifier(1, 1))
