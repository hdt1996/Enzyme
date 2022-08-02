setlocal enableDelayedExpansion
set server_name=%1
set args=%*
set num_args=0

for %%x in (%*) do (
   set /A num_args+=1
   set "argVec[!num_args!]=%%~x"
)
echo Number of processed arguments: %num_args%

if not exist "C:\IT\" mkdir C:\IT
if not exist "C:\IT\Back_End" mkdir C:\IT\Back_End
call django-admin startproject %server_name% C:\IT\Back_End

for /L %%i in (2,1,%num_args%) do (
    if not exist "C:\IT\Back_End\!argVec[%%i]!" mkdir C:\IT\Back_End\!argVec[%%i]!
    call django-admin startapp !argVec[%%i]! C:\IT\Back_End\!argVec[%%i]!
)