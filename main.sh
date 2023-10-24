echo "###################################################################"
echo "################### Запуск backup/recovery ########################"
echo "################### Разработано в Sibur Connect ###################"
echo "###################################################################"
echo "Что делаем? (b) backup, (r) recovery: "


while :
  do
    read var
    if [ $var == 'b' ] || [ $var == "backup"  ];
      then
        echo "В разработке"
        break

    elif [ $var == "r" ] || [ $var == "recovery" ];
      then 
        echo "Запуск восстановления" #$(bash pitr)
        break

    else
      echo "Некорректно, введите: (b) backup, (r) recovery:"

    fi

done

