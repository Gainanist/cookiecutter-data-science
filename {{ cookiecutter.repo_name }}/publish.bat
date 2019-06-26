@echo off
setlocal enabledelayedexpansion

set "ORIGIN_DIR=%CD%"

for /f %%i in ('git rev-parse --show-toplevel') do set "ROOT_DIR=%%~dpni"

set "REPORTS_DIR=%ROOT_DIR%\reports"

set "referencePath=%ROOT_DIR%"
set "absolutePath=%CD%\%~1"
FOR /F "delims=" %%a IN ("%absolutepath%") DO FOR %%r IN ("%referencepath%") DO (
  SET "abspath=%%~pna"
  SET "relativepath=!abspath:%%~pnr=!"
)
set "NOTEBOOK_NAME_PATH=%relativePath%"

set "HTML_PATH=%REPORTS_DIR%%NOTEBOOK_NAME_PATH%.html"
for /f "delims=" %%c in ("%HTML_PATH%") do (
  set "HTML_DIR=%%~dpc"
  set "HTML_NAME=%%~nxc"
)

IF EXIST "%HTML_PATH%.dvc" dvc remove "%HTML_PATH%.dvc"
jupyter nbconvert %1 --to html --output "%HTML_PATH%"

cd "%HTML_DIR%"
dvc add "%HTML_NAME%"
git add "%HTML_NAME%.dvc"
IF EXIST .gitignore git add .gitignore

cd "%ROOT_DIR%\docs"
make html
cd "%ORIGIN_DIR%"

:END