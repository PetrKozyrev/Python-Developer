# 1
number_of_plates = int(input())
detergent_amount = int(input())
while number_of_plates > 0 and detergent_amount > 0:
    number_of_plates -= 1
    detergent_amount -= 0.5
    print(detergent_amount)

    if detergent_amount == 0:
        print("Number of plates left: ", number_of_plates)
    if number_of_plates == 0:
        print("Number of detergent amount left: ", detergent_amount)
# 2
lst = input().split()
last_element_position = len(lst) - 1

while last_element_position >= 0:
    for i, el in enumerate(lst):
        if i == last_element_position:
            print(el, end=' ')
            last_element_position -= 1
# 3
lst = input().split()
while True:
    swaps = 0
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            lst[i], lst[i+1] = lst[i+1], lst[i]
            swaps += 1
    if swaps == 0:
        break
print(lst)

# 4.1 binary-decimal
binary = input()
decimal = 0
for i in range(len(binary)):
    decimal = int(binary[i]) + 2 * decimal
print(decimal)

# 4.2 decimal-binary
decimal = int(input())
binary = ''
while decimal > 0:
    remainder = decimal % 2
    decimal = decimal // 2
    binary = str(remainder) + binary
print(binary)
