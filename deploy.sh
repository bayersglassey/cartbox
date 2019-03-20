#!/bin/sh
set -e

./bump.sh
./restart.sh
./update_or_create_cats_and_prods.sh
