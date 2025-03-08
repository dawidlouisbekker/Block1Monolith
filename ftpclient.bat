@echo off
echo Changing to bankserver directory...
cd bankserver || exit /b
echo Current directory: %cd%

echo Deactivating Conda environment...
conda deactivate

echo Activating virtual environment...
call .\.venv\Scripts\activate.bat
echo Virtual environment activated

echo Starting FTP client...
@echo on
python startftp.py --user dawid


