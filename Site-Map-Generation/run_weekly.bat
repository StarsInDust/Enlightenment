@echo off
cd /d "%~dp0"  REM Switch to the folder where the .bat file lives

echo Running Sitemap Generator and Validator...
echo ------------------------------------------

REM Activate your Python environment if needed
REM call path\to\activate.bat  (optional, if using virtualenv)

REM Run the sitemap generator
python generate_sitemap.py

REM Run the broken link validator
python validate_sitemap_links.py

echo ------------------------------------------
echo All tasks completed.
pause