import copy


class Node:
    def __init__(self, d, n=None, p=None):
        self.data = d
        self.next_node = n
        self.prev_node = p


class LinkedList:
    def __init__(self):
        self.lst = []
        self.i = 0

    def add(self, key, node):
        if not isinstance(node, Node):
            raise TypeError('node must be Node instance')
        if key < 0:
            raise ValueError

        if len(self.lst) > 0:                   # если есть другие элементы
            if key < len(self.lst) - 1:         # если не последним элементом
                if key == 0:                    # если встаёт на первый элемент
                    node.next_node = self.lst[key]
                    self.lst.insert(key, node)
                else:
                    node.next_node = self.lst[key+1]  # встаёт посередине
                    self.lst[key-1].next_node = node
                    self.lst.insert(key, node)
            else:
                self.lst[len(self.lst)-1].next_node = node
                self.lst.insert(key, node)      # если последним элементом
        else:
            self.lst.insert(key, node)          # если нет других элементов

    def __len__(self):
        return len(self.lst)

    def __iter__(self):
        return self

    def __next__(self):
        for el in self.lst:
            if self.i == len(self.lst):
                raise StopIteration
            else:
                self.i += 1
                return el.data

    def __contains__(self, item):
        for node in self.lst:
            if node.data == item:
                return True
        return False

    def __add__(self, other):
        return copy.deepcopy(self.lst) + copy.deepcopy(other.lst)

first_list = LinkedList()
first_list.add(0, Node(9))
first_list.add(0, Node(8))
first_list.add(0, Node(3))
first_list.add(0, Node(2))
first_list.add(2, Node(4))
first_list.add(0, Node(1))

for node in first_list.lst:
    print(node.data)

print('-----------------------------')
print(first_list.__len__())
print('-----------------------------')
print(6 in first_list)
print(8 in first_list)
print('-----------------------------')

second_list = LinkedList()
second_list.add(0, Node(7))
second_list.add(0, Node(6))

third_list = first_list.__add__(second_list)
print(len(third_list))
print(len(first_list))
print(len(second_list))


class DoublyLinkedList(LinkedList):

    def add(self, key, node):
        if not isinstance(node, Node):
            raise TypeError('node must be Node instance')
        if key < 0:
            raise ValueError

        if len(self.lst) > 0:                   # если есть другие элементы
            if key < len(self.lst) - 1:
                if key == 0:                    # если встаёт на первый элемент
                    node.next_node = self.lst[key]
                    self.lst.insert(key, node)
                else:
                    node.next_node = self.lst[key+1]  # встаёт посередине
                    node.prev_node = self.lst[key-1]
                    self.lst[key-1].next_node = node
                    self.lst[key+1].prev_node = node
                    self.lst.insert(key, node)
            else:
                node.prev_node = self.lst[len(self.lst)-1]
                self.lst[len(self.lst)-1].next_node = node
                self.lst.insert(key, node)      # если последним элементом
        else:
            self.lst.insert(key, node)          # если нет других элементов


anotherList = DoublyLinkedList()

anotherList.add(0, Node(1))
anotherList.add(1, Node(2))
anotherList.add(2, Node(3))
anotherList.add(3, Node(4))

print('#####################################')
for node in anotherList.lst:
    print(node.next_node.data)

# print('######################')
# for node in anotherList.lst:
#     print(node.prev_node.data)


