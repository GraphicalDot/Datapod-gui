
from cx_Freeze import setup, Executable 
import sys
setup(name = "Datapod-desktop" , 
      version = "0.1" , 
      description = "" , 
      executables = [Executable("UserInterface/latest.py")]) 

