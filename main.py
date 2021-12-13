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
        all_files = os.listdir(DIRECTORY)  # список файлов
        need_files = filter(lambda x: x.endswith(EXTENSION), all_files)  # фильтр
        error_files = set()
        sh = shelve.open(DIRECTORY + "\\" + "last_error_file", "c")
        try:
            saved_time = sh[KEY_LAST_TIME]
        except KeyError:
            saved_time = 0.0
        last_saved_time = saved_time
        for f in need_files:  # цикл по фильтру
            file = DIRECTORY + "\\" + f
            size = os.path.getsize(file)  # считывание объёма
            c_time = os.path.getctime(file)
            if size < MIN_FILE_SIZE:
                if c_time > saved_time:
                    error_files.add(ErrorFile(f, str(size)))
                    if last_saved_time < c_time:
                        last_saved_time = c_time
        if len(error_files) > 0:
            root = Tk()
            root.title("Ошибка файла")
            files_list = Listbox(width=100)

            for f in error_files:
                files_list.insert(END, f.print())
            files_list.pack()
            root.mainloop()
            sh[KEY_LAST_TIME] = last_saved_time
    except FileNotFoundError:  # обработка ошибок
        print("Путь не найден: " + DIRECTORY)
    finally:
        sh.close()


if __name__ == '__main__':
    print_hi()
