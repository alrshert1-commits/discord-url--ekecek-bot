# 🤖 Ruby Studios - Discord URL Ban Bot

7/24 çalışan, banlı URL'leri otomatik olarak tespit eden ve silen Discord bot.

## 📋 Özellikler

✅ **Otomatik URL Tespit** - Mesajlardaki URL'leri otomatik kontrol eder  
✅ **7/24 Çalışma** - Sunucu kapanmadığı sürece sürekli aktif  
✅ **Banlı URL Listesi** - Admin tarafından yönetilen banlı URL veritabanı  
✅ **Otomatik Silme** - Banlı URL içeren mesajları anında siler  
✅ **İstatistikler** - Detaylı URL kontrol istatistikleri  
✅ **Güvenli** - Sadece yöneticiler komut kullanabilir  

## 🚀 Kurulum

### 1. Gerekli Paketleri Yükle

```bash
pip install -r requirements.txt
```

### 2. Discord Bot Token Oluştur

1. [Discord Developer Portal](https://discord.com/developers/applications) ziyaret et
2. "New Application" tıkla
3. Bot'a isim ver: `Ruby Studios URL Bot`
4. "Bot" sekmesine git ve "Add Bot" tıkla
5. Token'ı kopyala

### 3. Token'ı Yapılandır

`.env` dosyası oluştur:

```
DISCORD_TOKEN=your_bot_token_here
```

Yerine senin token'ını yapıştır.

### 4. Bot İzinlerini Ayarla

1. Developer Portal'da "OAuth2" → "URL Generator" git
2. Scopes: `bot` seç
3. Permissions:
   - ✅ Read Messages/View Channels
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Manage Messages (mesajları silme için)
   - ✅ Embed Links

4. Oluşturulan URL'yi kopyala ve tarayıcıda aç → Sunucuna ekle

### 5. Bot'u Çalıştır

```bash
python bot.py
```

Başarılı başladıysa:
```
✅ Bot başladı: Ruby Studios URL Bot#1234
📊 Banlı URL sayısı: 0
```

## 📝 Komutlar

### Admin Komutları

| Komut | Açıklama |
|-------|----------|
| `!banlı_ekle <url>` | URL'yi banlı listesine ekle |
| `!banlı_çıkar <url>` | URL'yi banlı listesinden çıkar |
| `!banlı_listesi` | Banlı URL'lerin listesini göster |
| `!url_istatistikleri` | URL istatistiklerini göster |
| `!yardım` | Komutları göster |

### Kullanım Örneği

```
!banlı_ekle https://malicious-site.com
!banlı_ekle https://spam.example.com
!banlı_listesi
```

## 📊 Nasıl Çalışır?

1. **URL Tespit** - Bot her mesajı tarar ve URL'leri çıkarır
2. **Banlı Kontrol** - Çıkarılan URL'ler banlı listesiyle karşılaştırılır
3. **Otomatik Silme** - Banlı URL bulunursa mesaj silinir
4. **Uyarı** - Kanal'da kırmızı embed ile uyarı gösterilir
5. **Log** - Tüm işlemler `checked_urls.json` dosyasına kaydedilir

## 💾 Veri Dosyaları

- `banned_urls.json` - Banlı URL'ler listesi
- `checked_urls.json` - Kontrol edilen URL'lerin geçmişi ve istatistikleri

## 🔧 Yapılandırma

### Prefix Değiştir

`bot.py` dosyasında:
```python
bot = commands.Bot(command_prefix="!", intents=intents)
```

Yerine:
```python
bot = commands.Bot(command_prefix=".", intents=intents)  # Prefix: .
```

### Silme Süresi

Embed mesajının kaç saniye sonra silineceğini ayarla:
```python
await message.channel.send(embed=embed, delete_after=10)  # 10 saniye
```

## 🚨 Sorun Giderme

### Bot çalışmıyor
- Token'ı doğru yapılandırdığını kontrol et
- Bot'un sunucuda Administrator izni var mı kontrol et
- Konsol hata mesajlarını kontrol et

### Mesajlar silinmiyor
- Bot'un "Manage Messages" izni var mı kontrol et
- URL'nin tam olarak banlı listesinde olduğundan emin ol

### Token hatasından bahsediyor
- `.env` dosyası oluşturduğunu ve TOKEN'ı doğru girdiğini kontrol et
- Aynı dizinde olduğundan emin ol

## 📞 Destek

Problemi varsa:
1. `bot.py` dosyasını kontrol et
2. Konsol çıktısını oku
3. Discord Developer Portal'da bot izinlerini kontrol et

## 📄 Lisans

MIT License - Ruby Studios

---

**Made with ❤️ by Ruby Studios**