@ECHO OFF

SET /P AREYOUSURE=Did you get an error saying somthing about 'Microsoft Visual C++ 14.0 is required... etc' ( Y / N )?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo. 2>c++_error_help_file.txt
echo Welcome, it seems you got this error.>> c++_error_help_file.txt
echo --> Downloaded Microsoft Visual C++ Build Tools from this link: https://visualstudio.microsoft.com/downloads/>> c++_error_help_file.txt
echo --> Run the installer>> c++_error_help_file.txt
echo --> Select: Workloads → Visual C++ build tools.>> c++_error_help_file.txt
echo --> Install options: select only the “Windows 10 SDK” (assuming the computer is Windows 10)>> c++_error_help_file.txt
echo A file has been created for you called 'c++_error_help_file'.
echo Maybe there you can find a solution.
echo.
PAUSE

:END