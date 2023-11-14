rm -rf /opt/pgsql/14/data/*
pg_basebackup -h s001db-ln-pg$1 -p5432 -U replicator -W -D /opt/pgsql/14/data/ --write-recovery-conf --progress --verbose
chown postgres:postgres -R /opt/pgsql/14/data
systemctl start postgresql-14.service
