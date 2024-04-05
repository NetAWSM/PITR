import os, shutil



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


def date_backup_pg():
    """Функция получения даты и парса его для бекапа постгреса"""

    while True:

        target = input("Введите дату на которую восстанавливаются wal файлы (формат d-m-y пример: 12-09-23): ")
        targetS = target.split("-")

        targetF = str(int(targetS[0]) - 1) + "-" + targetS[1] + "-" + targetS[2]
        """тут мы получаем дату для архива фул бекапа"""
        
        try:

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
                    return targetF
                
            else:
                print("tar -xvf /home/net/" + targetF + "/base.tar -C .")
                print("Нет бекапа на дату: " + targetF)

        except:

            print("Что то пошло не так")


def date_pg_conf(Date_Conf):
    """Дата для postgres.conf"""
    
    date = Date_Conf[6:] + Date_Conf[2:6] + Date_Conf[:2]
    dateR = date[:7] + str(int(date[7]) + 1)
    
    return dateR


def get_right_time():

    while True:

        time = input("Введите час и минуту на который нужно восстановить базу(20:37): ")
        timeS = time.split(":")

        try:  
            if 0 < int(timeS[0]) < 24:
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

def get_time_wal(get_time, get_date):
    """Функция формирования времени для архива инкрементального бекапа"""

    time = get_time
    date = get_date[6:] + get_date[2:6] + get_date[:2]
    #timeS = time.split(":")
    timeH = time[:2]

    if 0 < int(timeH) < 4:
        return date + ":" + "04" + ":00.tar.gz"
    elif 4 < int(timeH) < 8:
        return date + ":" + "08" + ":00.tar.gz"
    elif 8 < int(timeH) < 12:
        return date + ":" + "12" + ":00.tar.gz"
    elif 12 < int(timeH) < 16:
        return date + ":" + "16" + ":00.tar.gz"
    elif 16 < int(timeH) < 20:
        return date + ":" + "20" + ":00.tar.gz"
    else:
        return date + ":" + "00" + ":00.tar.gz"

def change_data():
    """Функция проверки очистки даты"""
    
    target = os.system("ls $DATA |wc -l")
    count = 0

    while True:
        if 0 != target:
            shutil.rmtree(DATA) #/
            os.mkdir(DATA) #/
            count += 1

        elif count > 3:
            print("Что то пошло не так")
            break
        
        else:
            break

def create_wal(wal):
    """Генерируем пул валов для восстановления на конкретную точку"""

    ls = os.listdir("/opt/backup_wal")
    waltemp = wal.split(":")
    
    for i in ls:
        temp = i.split(":")
        tempd = temp[0]
        tempt = temp[1]
        if tempd == waltemp[0] and tempt < waltemp[1]:
            os.system("tar -xzvf /opt/backup_wal" + i + " -C /opt/wal_archive")
    
    os.chmod("/opt/wal_archive/",  750) #Надо сделать рекурсивно!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    shutil.chown("/opt/wal_archive/", user='postgres', group='postgres')

def edit_config(date, time):
    """Замена значений в postgres.conf"""

    datawal = '20' + date + ' ' + time +  ':00:00.000000+03'

    with open('postgresql.conf', 'r') as f:

        old = f.read()

    restore = old.replace('#restore_command', 'restore_command')

    with open('postgresql.conf', 'w') as f:

        f.write(restore)

        #

    with open('postgresql.conf', 'r') as f:

        old = f.read()

    recovery = old.replace('#recovery_target_time', 'recovery_target_time')

    with open('postgresql.conf', 'w') as f:

        f.write(recovery)

        #

    with open('postgresql.conf', 'r') as f:

        old = f.read()

    tar = old.replace('targettime', datawal)    

    with open('postgresql.conf', 'w') as f:

        f.write(tar)
 

          
        


def main():

    date = date_backup_pg()  # Получаем дату для бекапа
    time = get_right_time()  # Получаем время
    wal_archive = get_time_wal(time, date_pg_conf(date)) #Время для архива бекапа вал файлов
    postgres("stop")
    os.system("tar -czvf /var/backup/recovery_$(date +\%d-\%m-\%y:%H:%M).tar.gz -C" + DATA)  #делаем бекап текущего каталога
    change_data() # удаляем каталог и создаем пустую папку data
    os.system("tar -xvf /opt/bkpgsql/" + date + "/base.tar -C $DATA") #Разархивируем папку с нужным бекапом и раздаем права и владельца
    os.chmod(DATA,  750) #Надо сделать рекурсивно!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    shutil.chown(DATA, user='postgres', group='postgres')
    shutil.rmtree("/opt/wal_archive/*")
    create_wal() #Проверить!!!
    edit_config(date_pg_conf(date), time)  #Меняем postgres.conf под восстановление на точку времени
        


    #os.system("tar -xvf /home/net/" + date + "/base.tar -C .") #!!!!!!!!!!!!!!!! Сюда вводим путь до папки с бекапами




#--------------Дебаг------------------

    print(date + " дата для бека")
    print(date_pg_conf(date) + " дата для конфы")
    print(time + " время")
    print(wal_archive + "Архив бекапа вал файлов")

    

main()
