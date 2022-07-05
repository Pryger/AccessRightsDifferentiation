# RW — чтение и запись, CD - создание и удаление, СM - копирование и перемещение
# 111 все права, 000 нет прав
from Users import * 
from Files import * 

def users_function(user):
    print("Введите число")
    print("1 чтобы добавить пользователя")
    print("2 чтобы удалить пользователя")
    print("3 чтобы заблокировать пользователя")
    print("4 чтобы разблокировать пользователя")
    print("5 чтобы назначить права пользователю")
    operation = input()

    while(operation != '1' and operation != '2' and operation != '3' and operation != '4' and operation != '5'):
        print("Не верная команда, попробуйте ещё раз")
        operation = input()
    
    print("Введите имя пользоватея")
    name = input()

    match operation:
        case '1':
            print("Введите права доступа (111)")
            permissions = input()
            print("Введите роль пользователя admin или user")
            role = input()
            print("Введите статус пользователя active или blocked")
            status = input()
            print("Пользователь создан") if users.add_user(name, permissions, role, status) else print("Ошибка добавления пользователя")
        case '2':
            print("Пользователь удалён") if users.remove_user(name) else print("Ошибка удаления пользователя")
        case '3':
            print("Пользователь заблокирован") if users.block_user(name) else print("Ошибка блокировки пользователя")
        case '4':
            print("Пользователь разблокирован") if users.unblock_user(name) else print("Ошибка разблокировки пользователя")
        case '5':
            print("Введите права доступа (111)")
            permissions = input()
            print("Права пользователя изменены") if users.set_user_permissions(name, permissions) else print("Ошибка установки прав пользователя")



def files_function(user):
    permissions = user.permissions
    permissions = list(permissions)

    operation = ''
    while (operation != '0'):
        print("Введите число")
        print("1 чтобы прочитать файл")
        print("2 чтобы записать в файл")
        print("3 чтобы создать файл")
        print("4 чтобы удалить файл")
        print("5 чтобы скопировать файл")
        print("6 чтобы переместить файл")
        print("0 чтобы выйти")
        operation = input()

        if(operation == '0'):
            break

        while(operation != '1' and operation != '2' and operation != '3' and operation != '4' and operation != '5' and operation != '6'):
            print("Не верная команда, попробуйте ещё раз")
            operation = input()

        print("Введите название файла")
        file_name = input()
        fs = Files(user, file_name)
        
        match operation:
            case '1':
                fs.read() if permissions[0] == '1' else user.add_failed_counter("Недостаточно прав")
            case '2':
                fs.write() if permissions[0] == '1' else user.add_failed_counter("Недостаточно прав")
            case '3':
                fs.create() if permissions[1] == '1' else user.add_failed_counter("Недостаточно прав")
            case '4':
                fs.remove() if permissions[1] == '1' else user.add_failed_counter("Недостаточно прав")
            case '5':
                fs.copy() if permissions[2] == '1' else user.add_failed_counter("Недостаточно прав")
            case '6':
                fs.move() if permissions[2] == '1' else user.add_failed_counter("Недостаточно прав")
        if(user.isBlocked == True):
            break



if __name__ == "__main__":
    users = Users()

    while(users.isAuth == False):
        print("Введите логин, чтобы авторизироваться")
        user = input()
        print("Авторизация выполнена " + user) if users.auth(user) else print("Ошибка авторизации")

    if(users.isBlocked == False):
        if(users.isAdmin == True):
            print("Введите число")
            print("1 для работы с файлами")
            print("2 для работы с пользователями")
            interface = input()
           
            while(interface != '1' and interface != '2'):
                print("Не верная команда, попробуйте ещё раз")
                interface = input()
            
            if(interface == '2'):
                users_function(users)
            else:
                files_function(users)
        else:
            files_function(users)
    else:
        print("Пользователь заблокирован") 
    

