#!/bin/sh
set -e

ssh cartbox@"$IP" '. workon && ./manage.py update_or_create_cats_and_prods'