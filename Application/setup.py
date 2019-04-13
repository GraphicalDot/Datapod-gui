
import sys

from cx_Freeze import setup, Executable 


base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    "packages": [
        "kivy", "kivymd", "asyncio", "aiohttp", "idna"
    ]
}

setup(
    name = "Datapod-desktop" , 
      version = "0.1" , 
      description = "" , 
      executables=[Executable("latest.py", base=base)],
    options={"build_exe": build_exe_options}
)

