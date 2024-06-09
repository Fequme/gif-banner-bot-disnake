import disnake
from disnake.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import io
from config import * 

intents = disnake.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Зашёл в {bot.user.name}')


    guild_id = GUILD_ID  
    guild = bot.get_guild(guild_id)
    
    if guild:
        banner_loop.start(guild)

@tasks.loop(seconds=10)
async def banner_loop(guild):
    await update_server_banner(guild)

async def update_server_banner(guild):
    if not guild:
        return await print("Invalid guild ID.")

    banner_path = 'banner/banner.gif'
    im = Image.open(banner_path)

    frames = []

    for frame in ImageSequence.Iterator(im):
        width, height = frame.size
        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        total_members = guild.member_count

        voice_members = sum(1 for member in guild.members if member.voice)
        font_path = 'fonts/txt.ttf'
        try:
            font = ImageFont.truetype(font_path, size=40)
            fontr = ImageFont.truetype(font_path, size=60)
        except IOError:
            return await print(f"Ошибка загрузки шрифта: {font_path}")

        text = f"{total_members}"
        draw.text((100, 160), text, fill=COLOR, font=font)
        draw.text((150, 220), f"{voice_members}", fill=COLOR, font=fontr)
        combined_frame = Image.alpha_composite(frame.convert('RGBA'), image)
        frame_bytes = io.BytesIO()
        combined_frame.save(frame_bytes, format="GIF")
        frame = Image.open(frame_bytes)
        frames.append(frame)

    frames[0].save('server_stats.gif', save_all=True, append_images=frames[1:])

    with open('server_stats.gif', 'rb') as file:
        gif_data = file.read()
        await guild.edit(banner=gif_data)



bot.run(TOKEN)
