#!/bin/sh
DEST=$(git config user.destination)
BACKUP=$(git config user.backup)
DATE=$(date '+%m%d%Y_%X')
DATE=$(echo $DATE | sed -e 's/AM//' -e 's/PM//' -e 's/ //g' -e 's/://g')
sudo zip -r $DEST/backup.zip $DEST/Backup

sudo -u root sh -c "cp $DEST/backup.zip $BACKUP/backup_$DATE.zip && ls -l $BACKUP"
read x
