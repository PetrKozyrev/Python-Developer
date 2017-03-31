#coding: utf-8
"""
__new__(cls) - настоящий конструктор
__init__(self) - конструктор (инициализация)
__del__() - деструктор (в момент, когда объект удаляется, он вызывается неявно)
В питоне есть сборщик мусора - деструктор не используется, в других языках надо самим создавать

__int__
__float__
__bool__
__str__(Python2 ->__unicode__) unicode во втором питоне
__cmp__ => Python2

"""
from pprint import pprint

class Product(object):
    """
    Здесь будет документация к классу!
    """
    def __init__(self, title, price):
        self.title = title
        self.price = price

    # def __str__(self):
    #     """Вызывается при конвертации в str"""
    #     return self.title

    def __float__(self):
        """Вызывается при конвертации в float"""
        return self.price

    def __repr__(self):
        """
        Вызывается функцией repr() для получения строки
        "формального" представления объекта
        """
        return 'Класс: "{}"\nПродукт "{}" стоимостью "{}"'.format(
            self.__class__,  self.title, self.price)

class Cart(object):
    __slots__ = ['products', 'i'] # __slots__ запрещает добавлять к объекту не указанные там атрибуты
                                # и менять их
    def __init__(self):
        self.products = []
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        for product in self.products:
            if self.i == len(self.products):
                raise StopIteration
            else:
                self.i += 1
                return product

    def __len__(self):
        return len(self.products)

    def __getitem__(self, item):
        if item < len(self):
            return self.products[item]

    def __setitem__(self, key, value):
        # self.products.insert(key, value)
        if key < len(self):
            self.products[key] = value # такое поведение с перезаписыванием более очевидно

    def __delitem__(self, key):
        if key < len(self):
            self.products.pop(key)

    def add(self, product):
        self.products.append(product)

book = Product('Объектно-ориентированное мышление', 999.13)
book2 = Product('Совершенный код', 700.13)
book3 = Product('Шаблоны проектирования', 350.15)

cart = Cart()
cart.add(book)
cart.add(book2)
cart.add(book3)
# cart.add(book)
# del cart[1]
for p in cart:
    print('В корзине: {}'.format(p))
print("============================================")
# print('Всего товаров в корзине: {}'.format(len(cart)))
# print('Имя класса: {}'.format(Product.__name__))
# print('Имя модуля: {}'.format(Product.__module__))
# print('Кортеж базовых классов: {}'.format(Product.__bases__)) # от кого унаследован
#
# pprint(Product.__dict__) # словарь атрибутов класса (не объекта)


# print('Класс, на основе которого создан объект: {}'.format(book.__class__))
# pprint(book.__dict__)

# print(Product.__doc__) # выводит документацию по классу, сразу после названия его надо писать, без пробелов
# print(repr(book))
# print(float(book))
# print(bool(book))

# Перегрузка операторов
class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Перегрузка оператора +"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Перегрузка оператора -"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Перегрузка оператора *"""
        return Vector(self.x * other.x, self.y * other.y)

    def __lt__(self, other):
        """
        Перегрузка оператора <
        """
        return self.length() < other.length()

    def __le__(self, other):
        return self.length() <= other.length()

    def __eq__(self, other):
        """Перегрузка оператора =="""
        return self.length() == other.length()

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)



v1 = Vector(1, 5)
v2 = Vector(1, 8)
print('Сумма векторов v1 и v2 равна: {}'.format(v1 + v2))
print('Разность векторов v1 и v2 равна: {}'.format(v1 - v2))
print('Произведение векторов v1 и v2 равна: {}'.format(v1 * v2))

print('{} > {}: {}'.format(v1, v2, v1 > v2))
print('{} >= {}: {}'.format(v1, v2, v1 >= v2))
print('{} == {}: {}'.format(v1, v2, v1 == v2))
print('{} <= {}: {}'.format(v1, v2, v1 <= v2))
print('{} < {}: {}'.format(v1, v2, v1 < v2))
print('{} != {}: {}'.format(v1, v2, v1 != v2))