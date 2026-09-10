import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime
import logging

# Logging ayarı
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot'u başlat
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dosya yolları
BANNED_URLS_FILE = "banned_urls.json"
CHECKED_URLS_FILE = "checked_urls.json"

class URLBot:
    def __init__(self):
        self.banned_urls = self.load_banned_urls()
        self.checked_urls = self.load_checked_urls()
    
    def load_banned_urls(self):
        """Banlı URL'leri yükle"""
        if os.path.exists(BANNED_URLS_FILE):
            try:
                with open(BANNED_URLS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_banned_urls(self):
        """Banlı URL'leri kaydet"""
        with open(BANNED_URLS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.banned_urls, f, indent=4, ensure_ascii=False)
    
    def load_checked_urls(self):
        """Kontrol edilen URL'leri yükle"""
        if os.path.exists(CHECKED_URLS_FILE):
            try:
                with open(CHECKED_URLS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_checked_urls(self):
        """Kontrol edilen URL'leri kaydet"""
        with open(CHECKED_URLS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.checked_urls, f, indent=4, ensure_ascii=False)
    
    def is_url_banned(self, url):
        """URL banlı mı kontrol et"""
        return url in self.banned_urls
    
    def extract_urls(self, content):
        """Metinden URL'leri çıkar"""
        urls = []
        words = content.split()
        for word in words:
            if word.startswith(("http://", "https://")):
                urls.append(word)
        return urls
    
    def add_to_checked(self, url, guild_id, channel_id, author_id, status):
        """Kontrol edilen URL'leri kaydet"""
        self.checked_urls.append({
            "url": url,
            "guild_id": guild_id,
            "channel_id": channel_id,
            "author_id": author_id,
            "timestamp": datetime.now().isoformat(),
            "status": status
        })
        self.save_checked_urls()

url_bot = URLBot()

@bot.event
async def on_ready():
    print(f"✅ Bot başladı: {bot.user}")
    print(f"📊 Banlı URL sayısı: {len(url_bot.banned_urls)}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="URL'leri 👀"))

@bot.event
async def on_message(message):
    """Mesajları kontrol et"""
    if message.author == bot.user:
        return
    
    # URL var mı kontrol et
    urls = url_bot.extract_urls(message.content)
    
    if urls:
        for url in urls:
            if url_bot.is_url_banned(url):
                # Mesajı sil
                try:
                    await message.delete()
                    url_bot.add_to_checked(url, message.guild.id, message.channel.id, message.author.id, "BANNED")
                    
                    # Embed oluştur
                    embed = discord.Embed(
                        title="🚫 BANLI URL TESPİT EDİLDİ",
                        description=f"**URL:** `{url}`\n**Kullanıcı:** {message.author.mention}\n**Mesaj silinmiştir.**",
                        color=discord.Color.red(),
                        timestamp=datetime.now()
                    )
                    embed.set_footer(text="Ruby Studios URL Ban Bot")
                    await message.channel.send(embed=embed, delete_after=10)
                    logger.info(f"🚫 Banlı URL engellendi: {url} - Kullanıcı: {message.author}")
                except Exception as e:
                    logger.error(f"Hata: {e}")
                break
            else:
                url_bot.add_to_checked(url, message.guild.id, message.channel.id, message.author.id, "ALLOWED")
    
    await bot.process_commands(message)

@bot.command()
async def banlı_ekle(ctx, url: str):
    """URL'yi banlı listesine ekle"""
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Yetki Hatası",
            description="Bunu yapmak için **yönetici** olman gerekir!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    if url in url_bot.banned_urls:
        embed = discord.Embed(
            title="⚠️ URL Zaten Banlı",
            description=f"`{url}` zaten banlı listesinde!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    url_bot.banned_urls.append(url)
    url_bot.save_banned_urls()
    
    embed = discord.Embed(
        title="✅ URL Banlı Listesine Eklendi",
        description=f"`{url}` artık banlı.\n📊 Toplam banlı URL: {len(url_bot.banned_urls)}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    logger.info(f"✅ Banlı URL eklendi: {url} - Admin: {ctx.author}")

@bot.command()
async def banlı_çıkar(ctx, url: str):
    """URL'yi banlı listesinden çıkar"""
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Yetki Hatası",
            description="Bunu yapmak için **yönetici** olman gerekir!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    if url not in url_bot.banned_urls:
        embed = discord.Embed(
            title="⚠️ URL Banlı Değil",
            description=f"`{url}` banlı listesinde değil!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    url_bot.banned_urls.remove(url)
    url_bot.save_banned_urls()
    
    embed = discord.Embed(
        title="✅ URL Banlı Listesinden Çıkarıldı",
        description=f"`{url}` artık banlı değil.\n📊 Toplam banlı URL: {len(url_bot.banned_urls)}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    logger.info(f"✅ Banlı URL çıkarıldı: {url} - Admin: {ctx.author}")

@bot.command()
async def banlı_listesi(ctx):
    """Banlı URL'lerin listesini göster"""
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Yetki Hatası",
            description="Bunu yapmak için **yönetici** olman gerekir!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    if not url_bot.banned_urls:
        embed = discord.Embed(
            title="📋 Banlı URL Listesi",
            description="Banlı URL yoktur.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return
    
    # Sayfa sayısı hesapla
    urls_per_page = 10
    pages = [url_bot.banned_urls[i:i + urls_per_page] for i in range(0, len(url_bot.banned_urls), urls_per_page)]
    
    embed = discord.Embed(
        title="📋 Banlı URL Listesi",
        color=discord.Color.blue()
    )
    
    url_list = "\n".join(f"• `{url}`" for url in pages[0])
    embed.description = url_list
    embed.set_footer(text=f"Sayfa 1/{len(pages)} | Toplam: {len(url_bot.banned_urls)} URL")
    
    await ctx.send(embed=embed)

@bot.command()
async def url_istatistikleri(ctx):
    """URL kontrol istatistiklerini göster"""
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title="❌ Yetki Hatası",
            description="Bunu yapmak için **yönetici** olman gerekir!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    total = len(url_bot.checked_urls)
    banned = sum(1 for u in url_bot.checked_urls if u["status"] == "BANNED")
    allowed = total - banned
    
    embed = discord.Embed(
        title="📊 URL İstatistikleri",
        color=discord.Color.gold()
    )
    embed.add_field(name="✅ İzin Verilen", value=str(allowed), inline=True)
    embed.add_field(name="🚫 Engellenen", value=str(banned), inline=True)
    embed.add_field(name="📈 Toplam Kontrol Edilen", value=str(total), inline=True)
    embed.add_field(name="🔒 Banlı URL Sayısı", value=str(len(url_bot.banned_urls)), inline=True)
    embed.set_footer(text="Ruby Studios URL Ban Bot")
    
    await ctx.send(embed=embed)

@bot.command()
async def yardım(ctx):
    """Bot komutlarını göster"""
    embed = discord.Embed(
        title="🤖 Ruby Studios URL Ban Bot - Yardım",
        color=discord.Color.blurple(),
        description="Banlı URL'leri otomatik olarak tespit eden ve silen bot."
    )
    
    embed.add_field(
        name="📝 Komutlar",
        value="""
`!banlı_ekle <url>` - URL'yi banlı listesine ekle
`!banlı_çıkar <url>` - URL'yi banlı listesinden çıkar
`!banlı_listesi` - Banlı URL'lerin listesini göster
`!url_istatistikleri` - URL istatistiklerini göster
`!yardım` - Bu mesajı göster
        """,
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Özellikler",
        value="""
✅ 7/24 otomatik URL kontrolü
✅ Banlı URL otomatik tespit ve silme
✅ Detaylı istatistikler
✅ Yönetici komutları
        """,
        inline=False
    )
    
    embed.set_footer(text="Ruby Studios | discord-url-çekecek-bot")
    await ctx.send(embed=embed)

# Bot'u başlat
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN", "BURAYA_TOKEN_YAP")
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Bot başlatılamadı: {e}")