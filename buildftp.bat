@echo off
echo Compiling ftpadmin.JavaFX...
javac --module-path "C:\Program Files\Java\javafx-sdk-21.0.6\lib" --add-modules javafx.controls,javafx.swing,javafx.graphics -d . bankadmin/Main.java
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo Running ftpadmin.JavaFX...
java --module-path "C:\Program Files\Java\javafx-sdk-21.0.6\lib" --add-modules javafx.controls,javafx.swing,javafx.graphics bankadmin.Main