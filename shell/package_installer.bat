start /wait %~dp0executables\python.exe
call %~dp0ws_backend\set_py_deps.bat True %~dp0dependencies\py_requirements.txt
call %~dp0ws_backend\set_py_ws.bat POOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP App1 App2 App3 App4 App5 App6 App7 App8 App9 App10
start /wait %~dp0executables\node.msi
start %~dp0ws_frontend\set_npm_react.bat  %~dp0dependencies\package.json reactjs
start /wait %~dp0executables\java.exe
start /wait %~dp0executables\psql.exe
start /wait %~dp0executables\vs_code.exe
start /wait %~dp0executables\docker.exe
start /wait powershell -Command "&{ Start-Process powershell -ArgumentList '-executionpolicy remotesigned','-File %~dp0pshel\wsl_install.ps1' -Verb RunAs}"
start /wait %~dp0executables\psql.exe
exit




