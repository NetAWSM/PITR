import os



last_day = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
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
    """Функция получения даты и парса его для бекапа постгреса"""

    while True:

        target = input("Введите дату на которую восстанавливаются wal файлы (формат d-m-y пример: 12-09-23): ")
        targetS = target.split("-")

        targetF = str(int(targetS[0]) - 1) + "-" + targetS[1] + "-" + targetS[2]
        """тут мы получаем дату для архива фул бекапа"""


        if int(targetS[0]) < 10:
            targetF = str(0) + targetF
            """Если дата меньше 10, то при минусе 1 убирается 0, мы его возвращаем обратно"""

        if targetS[0] == "01":

            targetT = targetF.split("-")
            targetT[0] = str(last_day[int(targetT[1]) - 1])
            targetT[1] = str(0) + str(int(targetT[1]) - 1)
            targetF = targetT[0] + "-" + targetT[1] + "-" + targetT[2]
            """Если дату ввели 01-05-23, то на выходе она будет 00-05-23, этот иф меняет на последний день прошлого месяца и месяц соответственно"""


        for i in os.listdir():
            if i == targetF:
                return "tar -xvf /home/net/" + targetF + "/base.tar -C ."
                break
        else:
            print("tar -xvf /home/net/" + targetF + "/base.tar -C .")
            print("Нет бекапа на дату: " + targetF)


def get_right_time():

    while True:

        time = input("Введите час и минуту на который нужно восстановить базу(0-20:37): ")
        timeS = time.split(":")

        try:  
            if 0 < int(timeS[0]) < 21:
                pass    
            else:
                print("неправильные часы")
                continue    


            if 0 < int(timeS[1]) < 60:
                pass      
            else:
                print("неправильно минуты")
                continue
            
            return time
        
        except:
            print("Непредвидмая ошибка")




def test():

    os.system(date())
    print(get_right_time())

test()
