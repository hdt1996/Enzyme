set package_json=%1
set react_name=%2
if not exist "C:\IT\Front_End" mkdir C:\IT\Front_End
npm install create-react-app -g & cd C:\IT\Front_End & npx create-react-app %react_name% & xcopy %package_json% C:\IT\Front_End\package.json* & cd C:\IT\Front_End\%package_json% & npm install & exit


