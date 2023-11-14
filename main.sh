echo -en '\n'
echo -en '\n'
echo -en '\n'
echo "###################################################################"
echo "################### Запуск системы LIMS ###########################"
echo "################### Разработано в Sibur Connect ###################"
echo "###################################################################"
read -p "Что делаем? (b) backup, (r) recovery, (o) obfuscation: " var


while :
  do

    if [ $var == 'b' ] || [ $var == "backup"  ];
      then
        echo "В разработке"
        break

    elif [ $var == "r" ] || [ $var == "recovery" ];
      then 
        echo "Запуск восстановления" #$(bash pitr)
        break

    elif [ $var == "o" ] || [ $var == "obfuscation" ];
      then 
        echo "Запуск скрипта обфускации" #$(bash pitr)
        break

    else
      echo "Некорректно, введите: (b) backup, (r) recovery, (o) obfuscation:"

    fi

done

