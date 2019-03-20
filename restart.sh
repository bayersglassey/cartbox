#!/bin/sh
set -e

scp uwsgi/uwsgi.ini root@$IP:/etc/
scp uwsgi/cartbox.ini root@$IP:/etc/uwsgi.d/
echo "Restarting UWSGI..."
ssh root@$IP systemctl restart uwsgi
echo "Done!"