#!/bin/sh


cython3 --embed -o latest.c latest.py
gcc -Os -I /usr/include/python3.6m -o latest latest.c -lpython3.6m -lpthread -lm -lutil -ldl


#gcc -Os -I /usr/local/Cellar/python/3.6.5_1/Frameworks/Python.framework/Versions/3.6/Headers 
#-L /usr/local/Cellar/python/3.6.5_1/Frameworks/Python.framework/Versions/3.6/lib 
#-o at_analyzer latest.c -lpython3.6m -lpthread -lm -lutil -ldl -v

