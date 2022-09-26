#!/bin/sh
DEST="$(git config user.destination)"
BACKUP="$(git config user.backup)"
sudo -u root sh -c "cp -r $BACKUP $DEST && ls -l $BACKUP"
read x
