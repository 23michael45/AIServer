set PrePath=%CD%
echo The current directory is %~dp0
set CurrentPath=%~dp0
cd %CurrentPath%

rem From tensorflow/models/research/
rem FOR %%i IN (*) DO ECHO %%i


for /f %%i in ('dir /b object_detection\protos\*.proto') do D:/DevelopProj/ProtocolBuffers/Releases/protobuf-cpp-3.6.1/protobuf-3.6.1/build_x64/Release/protoc  .\object_detection\protos\%%i --python_out=.

