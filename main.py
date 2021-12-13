import os
import shelve
from tkinter import *

KEY_LAST_TIME = "time"

MIN_FILE_SIZE = 50
EXTENSION = '.txt'
DIRECTORY = 'C:\\some_dir'


class ErrorFile:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    name = ""
    size = ""

    def print(self):
        return self.name + ": " + self.size + " байт"


def print_hi():
    sh = shelve
    try:
        sh = shelve.open(DIRECTORY + "\\" + "last_error_file", "c")  # файл хранения данных
        try:
            saved_time = sh[KEY_LAST_TIME]
        except KeyError:  # в случае если ещё нет файла
            saved_time = 0.0
        all_files = os.listdir(DIRECTORY)  # список файлов
        need_files = filter(lambda x:
                            x.endswith(EXTENSION) &  # по расширению
                            (os.path.getsize(DIRECTORY + "\\" + x) < MIN_FILE_SIZE) &  # по объёму
                            (os.path.getctime(DIRECTORY + "\\" + x) > saved_time),  # по времени
                            all_files)
        error_files = set()
        last_saved_time = saved_time
        for f in need_files:  # цикл по фильтру
            file = DIRECTORY + "\\" + f
            size = os.path.getsize(file)  # считывание объёма
            c_time = os.path.getctime(file)
            error_files.add(ErrorFile(f, str(size)))
            # максимальное время создания файла для фильтра на следующий запуск
            last_saved_time = max(last_saved_time, c_time)
        if len(error_files) > 0:  # если кол-во файлов больше 0
            sh[KEY_LAST_TIME] = last_saved_time  # запись максимального времени создания ошибочного файла
            root = Tk()  # создание окна
            root.title("Ошибка файла")  # заголовок окна
            files_list = Listbox(width=100)  # список для вывода

            for f in error_files:  # заполнение списка
                files_list.insert(END, f.print())
            files_list.pack()
            root.mainloop()
    except FileNotFoundError:  # обработка ошибок
        root = Tk()
        root.title("Ошибка - Путь не найден: " + DIRECTORY)
    finally:
        sh.close()


if __name__ == '__main__':
    print_hi()
