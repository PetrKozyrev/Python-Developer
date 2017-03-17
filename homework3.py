# 1
import datetime
today = datetime.datetime.now().date()
new_year = datetime.date(datetime.datetime.now().year, 12, 31)
print((new_year - today).days)

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
