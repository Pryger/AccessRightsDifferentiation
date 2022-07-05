import datetime

class Files:
    def __init__(self, user, name):
        self.user = user
        self.name = name

    def __log(self, message):
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y %H:%M")
        with open('log.txt', '+a') as cont:
            cont.write(f"{message} {now}\n")

    def read(self):
        self.__log(f"Файл прочитан или не существует, пользователь {self.user.name}")
        print("Файл прочитан или не существует")

    def write(self):
        self.__log(f"Файл перезаписан или не существует, пользователь {self.user.name}")
        print("Файл перезаписан или не существует")

    def create(self):
        self.__log(f"Файл создан, пользователь {self.user.name}")
        print("Файл создан")

    def remove(self):
        self.__log(f"Файл удалён или не существует, пользователь {self.user.name}")
        print("Файл удалён или не существует")

    def copy(self):
        self.__log(f"Файл скопирован или не существует, пользователь {self.user.name}")
        print("Файл скопирован или не существует")

    def move(self):
        self.__log(f"Файл перемещён или не существует, пользователь {self.user.name}")
        print("Файл перемещён или не существует")