#!/bin/sh
cd $HOME/pwb/mis_articles_updater
result=$($HOME/pwbvenv/bin/python3 missingUpd.py >&1)
IMPORT_EXIT_STATUS=$?

# mail if failed


echo 'done'
echo $result
echo $IMPORT_EXIT_STATUS

#echo "Subject: 51+ import-$IMPORT_EXIT_STATUS\n\n$result" | /usr/sbin/exim -odf -i kosovojs@gmail.com
