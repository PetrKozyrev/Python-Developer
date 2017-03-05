#!/usr/bin/python3.5

from datetime import datetime as dt
import sys

print("Ежедневник, выберите действие:\n\n{0}{1}{2}{3}{4}{5}".format(
    "1. Вывести список задач\n", "2. Добавить задачу\n",
    "3. Отредактировать задачу\n", "4. Завершить задачу\n",
    "5. Начать задачу сначала\n", "6. Выход\n"
))
tasks = {}

accomplished_tasks = set()
not_accomplished_tasks = set()

while True:
    number = int(input("Введите число: "))
    if number == 1:
        date = input("Введите дату в таком порядке: год месяц день ").split()
        current_date = [dt.now().year, dt.now().month, dt.now().day]
        def list_of_tasks(date=current_date):
            for identificator in tasks:
                if identificator["date"] == date and \
                                identificator not in accomplished_tasks:
                    print(identificator)
        list_of_tasks(date)

    if number == 2:
        identificator = int(input("Введите идентификатор данной задачи "))
        name = input("Введите название задачи ")
        text = input("Введите текст задачи ")
        date = input("Введите дату, к которой задание должно быть выполнено,"
                     "в формате год месяц день ").split()
        time = input("Введите время, к которому задача должна быть выполнена, "
                     "в формате час минута секунда ").split()
        print('Статус задачи установлен на "Не выполнено"')
        not_accomplished_tasks.add(identificator)
        tasks[identificator] = {"name": name, "text": text, "date": date,
                                "time": time}

    if number == 3:
        identificator = int(input("Введите идентификатор задачи "
                                  "для редактирования "))
        if identificator not in tasks:
            raise NameError("Нету задачи с таким идентификатором!")
        if not isinstance(identificator, int):
            raise ValueError("Идентификатор должен быть целым числом!")
        name = input("Введите новое название задачи ")
        text = input("Введите новый текст задачи ")
        date = input("Введите новую дату, к которой задание должно быть "
                     "выполнено, в формате год месяц день ").split()
        time = input("Введите новое время, к которому задача должна быть "
                     "выполнена, в формате час минута секунда ").split()
        tasks[identificator]["name"] = name
        tasks[identificator]["text"] = text
        tasks[identificator]["date"] = date
        tasks[identificator]["time"] = time

    if number == 4:
        identificator = int(input("Введите идентификатор данной задачи "))
        if identificator not in tasks:
            raise NameError("Нету задачи с таким идентификатором!")
        if not isinstance(identificator, int):
            raise ValueError("Идентификатор должен быть целым числом!")
        accomplished_tasks.add(identificator)
        not_accomplished_tasks.remove(identificator)

    if number == 5:
        identificator = int(input("Введите идентификатор данной задачи "))
        if identificator not in tasks:
            raise NameError("Нету задачи с таким идентификатором!")
        if not isinstance(identificator, int):
            raise ValueError("Идентификатор должен быть целым числом!")
        not_accomplished_tasks.add(identificator)
        accomplished_tasks.remove(identificator)

    if number == 6:
        sys.exit()
