:; # ------------------------------------------------------------------
:; # FOR LINUX AND MACOS (BASH)
:; # ------------------------------------------------------------------
:;
:; # 1. Verify if script is executed with `source`.
:; if [[ "${BASH_SOURCE}" == "${0}" ]]; then
:;     echo "ERROR: On Linux/macOS you must run:"
:;     echo "\tsource setup.cmd"
:;     exit 1
:; fi
:;
:; # 2. Create virtual environment.
:; echo "Initializing python virtual environment."
:; echo ""
:; echo ""
:; python3 -m venv .venv || python -m venv .venv
:;
:; # 3. Activate virtual environment.
:; echo ""
:; echo ""
:; echo "Activating python virtual environment."
:; echo ""
:; echo ""
:; source .venv/bin/activate
:;
:; # 4. Upgrade pip.
:; echo ""
:; echo ""
:; echo "Upgrading pip"
:; echo ""
:; echo ""
:; pip install --upgrade pip
:;
:; # 5. Install dependencies.
:; echo ""
:; echo ""
:; echo "Installing dependencies"
:; echo ""
:; echo ""
:; [ -f requirements-dev.txt ] && pip install -r requirements-dev.txt
:; echo ""
:; echo ""
:; echo "Environment setup successful!"
:; return 0

@echo off
:: ------------------------------------------------------------------
:: FOR WINDOWS (CMD / POWERSHELL)
:: ------------------------------------------------------------------

:: 1. Verify if script is running on PowerShell or pure CMD
echo $PSVersionTable >nul 2>&1
if %errorlevel% equ 0 (
    set "TAB=    "
    echo ERROR: On PowerShell you must run:
    echo %TAB%. .\setup.cmd
    exit /b 1
)

:: 2. Create virtual environment.
echo Initializing python virtual environment.
echo.
echo.
python -m venv .venv

:: 3. Activate virtual environment.
echo Activating python virtual environment.
echo.
echo.
call .venv\Scripts\activate.bat

:: 4. Upgrade pip.
echo.
echo.
echo Upgrading pip
echo.
echo.
python -m pip install --upgrade pip

:: 5. Install dependencies.
echo.
echo.
echo Installing dependencies
echo.
echo.
if exist requirements-dev.txt pip install -r requirements-dev.txt

echo.
echo.
echo Environment setup successful!

exit /b 0
