#!/bin/sh


cython3 --embed -o latest.c latest.py
gcc -Os -I /usr/include/python3.6m -o latest latest.c -lpython3.6m -lpthread -lm -lutil -ldl