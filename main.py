import os
from tkinter import *

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
    try:
        all_files = os.listdir(DIRECTORY)  # список файлов
        need_files = filter(lambda x: x.endswith(EXTENSION), all_files)  # фильтр
        error_files = set()
        for f in need_files:  # цикл по фильтру
            size = os.path.getsize(DIRECTORY + "\\" + f)  # считывание объёма
            if size < MIN_FILE_SIZE:
                error_files.add(ErrorFile(f, str(size)))
        if len(error_files) > 0:
            root = Tk()
            root.title("Ошибка файла")
            files_list = Listbox(width=100)

            for f in error_files:
                files_list.insert(END, f.print())
            files_list.pack()
            root.mainloop()

    except FileNotFoundError:  # обработка ошибок
        print("Путь не найден: " + DIRECTORY)


if __name__ == '__main__':
    print_hi()
