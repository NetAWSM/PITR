TARGET=/opt/pgsql/14/data/pg_wal/
BCUR=/opt/backup_wal
BOLD=/opt/backup_wal/old
BDATE=$(date +\%d-\%m-\%y:%H:%M)
LOGWAL=/opt/logwal
FILENAME=$BDATE
EXPIRE=14
EDATE=$(date +\%d-\%m-\%y)

backup() {
tar -g $BCUR/snar -cvzf $BCUR/$FILENAME.tar.gz -C $TARGET . > $LOGWAL/$FILENAME.log 2> $LOGWAL/$FILENAME.err
}
delete() {
find $BOLD/ -mtime +$EXPIRE -delete
}
full() {
tar -cvzf $BOLD/$FILENAME.full.tar.gz -C $BCUR . > $BOLD/$FILENAME.full.log 2> $BOLD/$FILENAME.full.err
rm -rf $BCUR/*
backup
}
every() {

  tar -cvzf $BCUR/$EDATE.tar.gz $BCUR/*tar.gz --remove-files

}

rmrf() {

  rm -f $BCUR/*tar.gz

}

case $1 in
        incremental) backup ;;
        full) full ;;
        delete) delete ;;
        every) every ;;
        rmrf) rmrf ;;
esac
