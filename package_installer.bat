start /wait %~dp0executables\python.exe
call %~dp0shell\ws_backend\set_py_deps.bat True %~dp0dependencies\py_requirements.txt
call %~dp0shell\ws_backend\set_py_ws.bat server_01 app_01 app_02 app_03 app_04 app_05 app_06 app_07 app_08 app_09 app_10
start /wait %~dp0executables\node.msi
start %~dp0shell\ws_frontend\set_npm_react.bat  %~dp0dependencies\package.json reactjs
start /wait %~dp0executables\java.exe
start /wait %~dp0executables\psql.exe
start /wait %~dp0executables\vs_code.exe
start /wait %~dp0executables\docker.exe
start /wait powershell -Command "&{ Start-Process powershell -ArgumentList '-executionpolicy remotesigned','-File %~dp0shell\pshel\wsl_install.ps1' -Verb RunAs}"
exit




