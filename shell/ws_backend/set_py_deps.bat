set use_container=%1
set py_requirements=%2
if '%use_container%' == 'False' (call pip install -r %py_requirements%) ^
else (call pip install -r %py_requirements%)

