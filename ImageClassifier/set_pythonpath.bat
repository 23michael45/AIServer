set CurrentPath=%~dp0
rem From tensorflow/models/research/
set PYTHONPATH=%PYTHONPATH%;%CurrentPath%;%CurrentPath%slim

echo %PYTHONPATH%