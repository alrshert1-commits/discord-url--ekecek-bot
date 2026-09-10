@echo off
REM Windows için bot başlatma scripti

echo 🤖 Ruby Studios Discord URL Ban Bot baslatiliyor...
echo 📦 Gerekli paketler kontrol ediliyor...

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python yuklü degil. Lütfen Python'u indir: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python bulundu.

if not exist ".env" (
    echo ❌ .env dosyası bulunamadı!
    echo 📝 .env dosyası oluşturuluyor...
    copy .env.example .env
    echo ⚠️ Lütfen .env dosyasında DISCORD_TOKEN değerini değiştir ve tekrar çalıştır.
    pause
    exit /b 1
)

echo ✅ .env dosyası bulundu.

if not exist "venv" (
    echo 📦 Sanal ortam oluşturuluyor...
    python -m venv venv
)

echo ✅ Sanal ortam hazırlanıyor...
call venv\Scripts\activate.bat

echo 📥 Paketler yükleniyor...
pip install -r requirements.txt >nul 2>&1

echo.
echo ════════════════════════════════════════
echo 🚀 BOT BAŞLATILIYOR
echo ════════════════════════════════════════
echo.

python bot.py
pause
