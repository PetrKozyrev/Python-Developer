import sys
from diary.diary_functions import storage

conn = storage.connect()
storage.initialize(conn)

def action_show_menu():
    print('''Выберите действие:

1. Вывести список задач
2. Добавить задачу
3. Отредактировать задачу
4. Завершить задачу
5. Начать задачу сначала
q. Выход''')

def action_print_all():
    tasks = storage.print_all(conn)
    for task in tasks:
        print('{task[name]} - {task[text]} - {task[planned]} - {task[status]}'.format(task=task))

def action_exit():
    conn.close()
    sys.exit(0)

actions = {
    '1': action_print_all,
    '2': storage.add_task,
    '3': storage.modify_task,
    '4': storage.change_status_done,
    '5': storage.change_status_undone,
    'q': action_exit
}

if __name__ == '__main__':
    action_show_menu()
    while True:
        cmd = input('\nВведите команду: ')
        action = actions.get(cmd) # а почему не использовать [] вместо get?
        if action:
            if action == action_print_all or action == action_exit:
                action()
            else:
                action(conn)
        else:
            print('Неизвестная команда')

