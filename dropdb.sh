#!/bin/sh
python ./manage.py sqlclear fuzzitusbackend | python ./manage.py dbshell
