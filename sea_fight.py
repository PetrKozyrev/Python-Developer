from random import randint

class Game:
    def __init__(self, ships):
        self.battlefield = [[0] * 10 for col in range(10)]
        self.ships = ships

    def shoot_ship(self, x, y):
        if (x, y) in self.ships.positions:
            self.battlefield[x][y] = "x"
        else:
            self.battlefield[x][y] = "*"

    def look_at_the_board(self):
        for row in self.battlefield:
            print(row + '\n')

class Ships:
    def __init__(self):
        self.positions = set()
        self.prohibited_positions = set()

    def block_positions(self, row, random_number):
        row -= 1
        for i in range(3):
            self.prohibited_positions.add((row, random_number-1))
            self.prohibited_positions.add((row, random_number))
            self.prohibited_positions.add((row, random_number+1))
            row += 1

    def random_number_generator(self):
        row = randint(0, 9)
        col = randint(0, 9)
        return row, col

    def place_ships(self):
        self.place_one_ship()
        self.place_two_ships()
        self.place_three_ships()
        self.place_four_ships()

    def place_one_ship(self):
        row, col = self.random_number_generator()
        random_number = randint(0, 6)
        if row >= col:
            for i in range(4):
                self.positions.add((row, random_number + i))
                self.block_positions(row, random_number + i)
        else:
            for i in range(4):
                self.positions.add((random_number + i, col))
                self.block_positions(random_number + i, col)

    def place_two_ships(self):
        counter = 0
        while counter < 2:
            row, col = self.random_number_generator()
            random_number = randint(0, 7)
            if row >= col:
                lst = [(row, random_number), (row, random_number+1),
                        (row, random_number+2)]
                if all(i not in self.prohibited_positions for i in lst):
                    counter += 1
                    for i in range(3):
                        self.positions.add((row, random_number + i))
                        self.block_positions(row, random_number + i)

            else:
                lst = [(random_number, col), (random_number+1, col),
                       (random_number, col+2)]
                if all(i not in self.prohibited_positions for i in lst):
                    counter += 1
                    for i in range(3):
                        self.positions.add((random_number + i, col))
                        self.block_positions(random_number + i, col)

    def place_three_ships(self):
        counter = 0
        while counter < 3:
            row, col = self.random_number_generator()
            random_number = randint(0, 8)
            if row >= col:
                lst = [(row, random_number), (row, random_number+1)]
                if all(i not in self.prohibited_positions for i in lst):
                    counter += 1
                    for i in range(2):
                        self.positions.add((row, random_number + i))
                        self.block_positions(row, random_number + i)

            else:
                lst = [(random_number, col), (random_number+1, col)]
                if all(i not in self.prohibited_positions for i in lst):
                    counter += 1
                    for i in range(2):
                        self.positions.add((random_number + i, col))
                        self.block_positions(random_number + i, col)

    def place_four_ships(self):
        counter = 0
        while counter < 4:
            row, col = self.random_number_generator()
            random_number = randint(0, 9)
            if row >= col:
                lst = [(row, random_number)]
                if all(i not in self.prohibited_positions for i in lst):
                    counter += 1
                    for i in range(1):
                        self.positions.add((row, random_number + i))
                        self.block_positions(row, random_number + i)

            else:
                lst = [(random_number, col)]
                if all(i not in self.prohibited_positions for i in lst):
                    counter += 1
                    for i in range(1):
                        self.positions.add((random_number + i, col))
                        self.block_positions(random_number + i, col)
