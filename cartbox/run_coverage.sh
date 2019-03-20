#!/bin/sh
coverage run --source=cart,analytics ./manage.py test --keepdb && coverage report && coverage html
