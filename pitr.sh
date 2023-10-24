#!/dfbin/bash
##############################################################################################################################
##                  Восстановление базы на конкретное время
###############################################################################################################################


DATA=/opt/pgsql/14/data
WAL=/opt/wal_archive
STATUS=$(systemctl list-units --state active | grep postgresql | wc -l)
OFF=$(systemctl stop postgresql-14.service)
echo -n "Введите дату на которую восстанавливаются wal файлы (формат d-m-y пример: 12-09-23): "
read targetd

get_right_time() {

  pass="Введите час на который нужно восстановить базу(0-20): "
  while :
    do
      read -p "$pass" time
      if [ $time -lt 0 ] && [ $time -gt 20 ]
        then
          echo ${pass//"Введите час на который нужно восстановить базу(0-20): "/"Введно некорректное время, введите час в диапазоне(0-20): "}
      elif [ $time -ge 0 ] && [ $time -le 20 ]
        then
          (echo $time)
          break
      fi
  done
}

targettime=$(get_right_time)
tardconf=$(echo $targetd | awk -F "-" '{print $3"-"$2"-"$1}')

#echo -n "Введите час на который нужно восстановить базу(0-20): "
#read targettime
#echo -n "Введите час, на который восстанавливаеются wal файлы (0,4,8,12,16,20): "
#read targett
DATEPB=$(echo $targetd | awk -F "-" '{print ($1-1)"-"$2"-"$3}')  #формируем дату pgbasebackup
#DATEWAL=$targetd\:$targett\:00.tar.gz  #формируем дату и время для архива wal


#Получаем время
get_time() {


  if [ $targettime -le 00 ];
    then
      (echo 00)
  elif [ 00 -lt  $targettime ] && [ $targettime -le 04 ];
    then
      (echo 04)
  elif [ 04 -lt  $targettime ] && [ $targettime -le 08 ];
    then
      (echo 08)
  elif [ 08 -lt  $targettime ] && [ $targettime -le 12 ];
    then
      (echo 12)
  elif [ 12 -lt  $targettime ] && [ $targettime -le 16 ];
    then
      (echo 16)
  elif [ 16 -lt  $targettime ] && [ $targettime -le 20 ];
    then
      (echo 20)
  fi
}

result=$(get_time)
DATEWAL=$targetd\:$result\:00.tar.gz  #формируем дату и время для архива wal


#Стопим сервис
service_off() {

  if [ 0 != $STATUS ]
    then
      ($OFF)
  fi

}

#Создаем пустую папку data
change_data() {

  tar -czvf /var/backup/recovery_$(date +\%d-\%m-\%y:%H:%M).tar.gz -C $DATA
  rm -rf $DATA
  mkdir $DATA

}

#Разархивируем папку с нужным бекапом и раздаем права и владельца
restore_data() {

  if [ 0 == $(ls $DATA |wc -l) ]
    then
      (tar -xvf /opt/bkpgsql/$DATEPB/base.tar -C $DATA);

  fi
  chmod 750 -R $DATA
  chown postgres:postgres -R $DATA

#Как вариант сделать цикл, который в случае если папка не пустае предложит из нее все удалить.

}


create_wal() {

  rm -rf /opt/wal_archive/*

  for i in $(ls /opt/backup_wal/current/);
    do
      tempd=$(echo $i | awk -F ":" '{print $1}')
      tempt=$(echo $i | awk -F ":" '{print $2}')
      if [ $tempd == $targetd ] && [ $tempt -le $result ]
        then
          tar -xzvf /opt/backup_wal/current/$i -C /opt/wal_archive
      fi

  done


  chown postgres:postgres -R /opt/wal_archive/
  chmod 750 -R /opt/wal_archive/


}

edit_config() {

  rm -f $DATA/postgresql.conf
  sed 's/#restore_command/restore_command/' /opt/pgsql/14/postgresql.default.conf > $DATA/postgresql.tmp
  sed 's/#recovery_target_time/recovery_target_time/' $DATA/postgresql.tmp > $DATA/postgresql.temp
  rm -f $DATA/postgresql.tmp
  sed "s|targettime|20$tardconf $targettime\:00:00.000000+03|" $DATA/postgresql.temp > $DATA/postgresql.conf
  rm -f $DATA/postgresql.temp

}


create_recovery() {

  touch /opt/pgsql/14/data/recovery.signal #создаем фаил восстановления
  chown postgres:postgres /opt/pgsql/14/data/recovery.signal && chmod 640 /opt/pgsql/14/data/recovery.signal #раздаем права и владельца

}




start_postgres() {

  systemctl start postgresql-14.service #стартуем сервис

}

delete_recovery() {

  rm -f /opt/pgsql/14/data/recovery.signal  #удаляем фаил восстановления
  \cp /opt/pgsql/14/data/postgresql.default.conf /opt/pgsql/14/data/postgresql.conf  #убираем recovery_target_time и restore_command
  systemctl restart postgresql-14.service   #рестартуем сервис


}

recovery_slave() {

  su - a001-backup -c "ssh s001db-ln-pg2 'bash -s' < ./recovery"
  su - a001-backup -c "ssh s001db-ln-pg3 'bash -s' < ./recovery"
 
}


if [[ -z "$targetd" ]] && [ -z "$targettime"   ] ; then
  
  echo "Что то пошло не так (переменные пустые)"
else
 
  echo "Останавливаем сервис постгреса"; sleep 2;
  service_off
  echo "Создаем пустую папку data"; sleep 2;
  change_data
  echo "Разархивируем папку с нужным бекапом и раздаем права и владельца"; sleep 2;
  restore_data
  echo "Разархивируем wal файлы"; sleep 2;
  create_wal
  echo "Редактируем postgresql.conf"; sleep 2;
  edit_config
  echo "Создаем recovery.signal"; sleep 2;
  create_recovery
  echo "Стартуем постгрес"; sleep 2;
  start_postgres
  echo "Удаляем файлы восстановления"; sleep 2;
  delete_recovery
  echo "Синхронизируем слейвы"; sleep 2;
  recovery_slave
  
fi

