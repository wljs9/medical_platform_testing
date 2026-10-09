@echo off
cd /d %~dp0
echo ============================================
echo  Medical Platform - JMeter Performance Test
echo  (non-GUI / command-line mode)
echo ============================================

REM --- threads: usage: run-performance [50|100|200], default 100 ---
set THREADS=%1
if "%THREADS%"=="" set THREADS=100

REM --- cleanup old artifacts to avoid JMeter "file exists" errors ---
if exist perf_runner.jmx del /q perf_runner.jmx
if exist perf_result.jtl del /q perf_result.jtl
if exist report_perf_%THREADS%t rmdir /s /q report_perf_%THREADS%t

REM --- copy newest *.jmx to an ASCII name (avoids CJK filename issues in cmd) ---
for /f "delims=" %%f in ('dir /b *.jmx') do copy /y "%%f" perf_runner.jmx >nul

REM --- replace thread count in the temp jmx via PowerShell (ASCII script) ---
powershell -NoProfile -Command "$p='perf_runner.jmx'; $t='<intProp name=\"ThreadGroup.num_threads\">\d+</intProp>'; $r='<intProp name=\"ThreadGroup.num_threads\">%THREADS%</intProp>'; (Get-Content $p -Raw -Encoding UTF8) -replace $t,$r | Set-Content $p -Encoding UTF8"

echo.
echo Testing with %THREADS% threads, please keep backend running ...
jmeter -n -t perf_runner.jmx -l perf_result.jtl -e -o report_perf_%THREADS%t
if errorlevel 1 goto :fail

echo.
echo ============================================
echo  DONE. Report: report_perf_%THREADS%t\index.html
echo  Open it in a browser. Raw log: perf_result.jtl
echo ============================================
goto :end

:fail
echo.
echo  FAILED - check that jmeter is on PATH and backend is running.
:end
pause