#!/usr/bin/bash
while true
do
  sleep 5
  touch /tmp/status.html
  cat /dev/null > /tmp/status.html
  echo "<h3>If it has any number from 400 - 500 the site is down </h3>" >> /tmp/status.html
  cat /var/log/nginx/access.log | sort -r | head -n 1| cut -d " " -f7,9 | grep '/ [4-5][0-9]\{2\}$' | awk '{print $2}' >> /tmp/status.html
done
