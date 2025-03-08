@echo off
echo Compiling serverview...

javac --module-path "C:\Program Files\Java\javafx-sdk-21.0.6\lib" ^
      --add-modules javafx.controls,javafx.swing,javafx.graphics ^
      -cp "C:\Users\Louis\projects\year2\ITPNA\Block1\oracleWorkbench\lib\ojdbc17.jar" ^
      -d . oracleworkbench\*.java

if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo Running serverview...

java --module-path "C:\Program Files\Java\javafx-sdk-21.0.6\lib" ^
     --add-modules javafx.controls,javafx.swing,javafx.graphics ^
     -cp ".;C:\Users\Louis\projects\year2\ITPNA\Block1\oracleWorkbench\lib\ojdbc17.jar" ^
     oracleworkbench.Main


