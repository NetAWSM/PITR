import os


last_day = {1: 31, 2: 28, 31: 3, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
DATA="/opt/pgsql/14/data"
WAL="/opt/wal_archive"

def postgres(cmd):
    """Функция для команд демона пг"""

    if cmd == "stop":
        return os.system("systemctl stop postgresql-14")
    elif cmd == "restart":
        return os.system("systemctl restart postgresql-14")
    elif cmd == "list":
        return os.system("systemctl list-units --state active | grep postgresql | wc -l")


def date():
    """Функция получения даты и парса его для """

    while True:

        target = input("Введите дату на которую восстанавливаются wal файлы (формат d-m-y пример: 12-09-23): ")
        targetS = target.split("-")

        targetF = str(int(targetS[0]) - 1) + "-" + targetS[1] + "-" + targetS[2]
        """тут мы получаем дату для архива фул бекапа"""


        if int(targetF[0]) < 10:
            targetF = str(0) + targetF
            """Если дата меньше 10, то при минусе 1 убирается 0, мы его возвращаем обратно"""

        if int(targetF[0]) == 00:
            targetF[0] = last_day[int(targetF[1])]
            targetF[1] = str(0) + str((int(targetF[1]) - 1))
            """Если дату ввели 01-05-23, то на выходе она будет 00-05-23, этот иф меняет на последний день прошлого месяца и месяц соответственно"""


        for i in str(os.system("ls /root")):
            if i == targetF:
                os.system("tar -xvf /opt/bkpgsql/" + targetS + "/base.tar")
                break
            else:
                print("Нет такого архива")
                print(targetF)




def t():
    """Функция для получения и парса даты, под пгбейс, постгрес.конф и тд"""
    if target == "conf":
        print("Редачим конф")

    elif target == "backup":
        print("редачим под бекап")
    else:
        pass


date()
