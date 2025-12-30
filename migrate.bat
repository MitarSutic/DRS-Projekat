@REM prvo kreiraj baze dbAvioUsers i dbAvioLetovi u SSMS
@REM zatim
@REM otvori terminal u \server 
@REM i
@REM pokreni .\migrate.bat

@echo off
echo Aktiviram venv...
call venv\Scripts\activate

echo Pokrećem migraciju...
python -m flask db upgrade

echo Migracija završena.
