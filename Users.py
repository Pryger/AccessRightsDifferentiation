import json
import datetime

class Users:
    def __init__(self):
        self.__get_config()
        self.isAuth = False
        self.isBlocked = False
        self.isAdmin = False
        self.countFailed = 0

    # Работа с конфигом
    def __get_config(self):
        with open('config.json', 'r') as content:
            self.users = json.loads(content.read())

    def __update_config(self):
        with open('config.json', 'w') as content:
            content.write(json.dumps(self.users))

    # Проверки и валидация
    def __check_user_exist(self, login):
        if(list(map(lambda el: el['login'], self.users)).count(login)):
            return True
        else:
            return False

    def __check_permissions_valid(self, permissions):
        av_permissions = ('000','001','010','011','100','101','110','111')
        return bool(av_permissions.count(permissions))

    def __check_status_valid(self, status):
        av_status = ('active', 'blocked')
        return bool(av_status.count(status))

    def __check_role_valid(self, role):
        av_roles = ('user', 'admin')
        return bool(av_roles.count(role))

    # Получение индекса пользователя по логину
    def __get_user_index(self, login):
        return list(map(lambda el: el['login'], self.users)).index(login)

    def __log(self, message):
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y %H:%M")
        with open('log.txt', '+a') as cont:
            cont.write(f"{message} {now}\n")



    # Аунтификация
    def auth(self, login):
        if (self.__check_user_exist(login)):
            user = self.users[self.__get_user_index(login)]
            self.name = user['login']
            self.permissions = user['permissions']
            self.isBlocked = user['status'] == 'blocked'
            self.isAdmin = user['role'] == 'admin'
            self.isAuth = True
            self.__log(f"Авторизация успешна, пользователь {self.name}")
            return True
        else:
            self.__log(f"Авторизация не удалась, логин {login}")
            return False

    # Добавление и удалиение пользователя
    def add_user(self, login, permissions = '000', role = 'user', status = 'active'):
        if(self.__check_user_exist(login) == False
        and self.__check_permissions_valid(permissions)
        and self.__check_status_valid(status)
        and self.__check_role_valid(role)
        and self.isAdmin):
            user = {
                "login": login,
                "role": role,
                "permissions": permissions,
                "status": status
            }
            self.users.append(user)
            self.__update_config()
            self.__log(f"Пользователь {login} успешно добавлен пользователем {self.name}")
            return True
        else:
            self.__log(f"Неудачная попытка добавить пользователя {login} пользователем {self.name}")
            return False

    def remove_user(self, login):
        if(self.__check_user_exist(login) and self.isAdmin):
            self.users.pop(self.__get_user_index(login))
            self.__update_config()
            self.__log(f"Пользователь {login} удалён пользователем {self.name}")
            return True
        else:
            self.__log(f"Ошибка удаления пользователя {login} пользователем {self.name}")
            return False

    # Блокировка и разблокировка пользователя
    def block_user(self, login):
        if(self.__check_user_exist(login) and self.isAdmin):
            self.users[self.__get_user_index(login)]['status'] = "blocked"
            self.__update_config()
            self.__log(f"Пользователь {login} заблокирован пользователем {self.name}")
            return True
        else:
            self.__log(f"Ошибка блокировки пользователя {login} пользователем {self.name}")
            return False

    def unblock_user(self, login):
        if(self.__check_user_exist(login) and self.isAdmin):
            self.users[self.__get_user_index(login)]['status'] = "active"
            self.__update_config()
            self.__log(f"Пользователь {login} разблокирован пользователем {self.name}")
            return True
        else:
            self.__log(f"Ошибка разблокировки пользователя {login} пользователем {self.name}")
            return False

    # Установка прав пользователю
    def set_user_permissions(self, login, permissions):
        if(self.__check_user_exist(login)
        and self.__check_permissions_valid(permissions)
        and self.isAdmin):
            self.users[self.__get_user_index(login)]['permissions'] = permissions
            self.__update_config()
            self.__log(f"Пользователю {login} выданы права {permissions} пользователем {self.name}")
            return True
        else:
            self.__log(f"Ошибка выдачи прав {permissions} пользователю {login} пользователем {self.name}")
            return False

    # Счётчик неудачных попыток
    def add_failed_counter(self, message):
        if(self.countFailed + 1 == 3):
            self.isBlocked = True
            self.users[self.__get_user_index(self.name)]['status'] = "blocked"
            self.__update_config()
            print(message)
            self.__log(f"Количество неудачных попыток равно 3, пользователь {self.name} заблокирован")
            print("Пользователь заблокирован")
        else:
            self.countFailed += 1
            self.__log(f"Неудачная попытка работы с файлом пользователя {self.name}")
            print(message)
