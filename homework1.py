#!/usr/bin/python3.5
#1
from datetime import datetime
current_minute = datetime.now().minute
print('green') if current_minute < 3 or current_minute % 5 != 0 \
                and (current_minute + 1) % 5 != 0 else print('red')
#2
area = 10 * 100
garden_bed = 15 * 25
print("Space:", area % garden_bed)

#3
import math
first_edge_x = int(input("Type first edge x coordinate: "))
first_edge_y = int(input("Type first edge y coordinate: "))

second_edge_x = int(input("Type second edge x coordinate: "))
second_edge_y = int(input("Type second edge y coordinate: "))

third_edge_x = int(input("Type third edge x coordinate: "))
third_edge_y = int(input("Type third edge y coordinate: "))

first_edge_len = math.sqrt((first_edge_x - second_edge_x) ** 2 + \
             (first_edge_y - second_edge_y)**2)

second_edge_len = math.sqrt((first_edge_x - third_edge_x) ** 2 + \
             (first_edge_y - third_edge_y)**2)

third_edge_len = math.sqrt((second_edge_x - third_edge_x) ** 2 + \
             (second_edge_y - third_edge_y)**2)

if first_edge_len ** 2 + second_edge_len ** 2 == third_edge_len ** 2 or \
    first_edge_len ** 2 + third_edge_len **2 == second_edge_len ** 2 or \
    second_edge_len ** 2 + third_edge_len ** 2 == first_edge_len ** 2:
    print("This is a right triangle!")
else:
    print("This is not a right triangle!")

