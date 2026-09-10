#!/bin/bash
# Linux/Mac için bot başlatma scripti

echo "🤖 Ruby Studios Discord URL Ban Bot başlatılıyor..."
echo "📦 Gerekli paketler kontrol ediliyor..."

if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 yüklü değil. Lütfen Python3'ü yükle."
    exit 1
fi

echo "✅ Python3 bulundu."

if [ ! -f ".env" ]; then
    echo "❌ .env dosyası bulunamadı!"
    echo "📝 .env dosyası oluşturuluyor..."
    cp .env.example .env
    echo "⚠️ Lütfen .env dosyasında DISCORD_TOKEN değerini değiştir ve tekrar çalıştır."
    exit 1
fi

echo "✅ .env dosyası bulundu."

if [ ! -d "venv" ]; then
    echo "📦 Sanal ortam oluşturuluyor..."
    python3 -m venv venv
fi

echo "✅ Sanal ortam hazırlanıyor..."
source venv/bin/activate

echo "📥 Paketler yükleniyor..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "════════════════════════════════════════"
echo "🚀 BOT BAŞLATILIYOR"
echo "════════════════════════════════════════"
echo ""

python3 bot.py
