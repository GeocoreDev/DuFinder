@echo off
setlocal enabledelayedexpansion

set "python_script_path=C:\Script\main.py"
set "config_file_path=C:\Script\config.txt"

for /L %%y in (1998,1,2023) do (
    echo %%y > %config_file_path%
    start cmd /k "python %python_script_path%"
    timeout /t 10 > nul
)

endlocal
