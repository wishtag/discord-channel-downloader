import discord
import os
import aiohttp
import random
import string

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_unique_filename(directory, original_filename):
    base, ext = os.path.splitext(original_filename)
    print(ext)
    unique_filename = f"{generate_random_string()}{ext}"
    
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = generate_random_string()
    
    return unique_filename


from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

os.makedirs("temp", exist_ok=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.sync_commands()
    print("Commands synced!")

@bot.slash_command(name="save", description="Saves all attachments in a channel to your computer")
async def save(ctx: discord.ApplicationContext):
    if ctx.author.id != 709976218681737277:
        await ctx.respond("You are not authorized to use this command.")
        return
    
    await ctx.respond("Downloading attachments...")
    
    messages = [message async for message in ctx.channel.history(limit=None) if message.author != bot.user]
    
    for message in messages:
        if message.attachments:
            for attachment in message.attachments:
                unique_filename = generate_unique_filename("temp", attachment.filename)
                file_path = os.path.join("temp", unique_filename)
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as resp:
                        if resp.status == 200:
                            with open(file_path, "wb") as f:
                                f.write(await resp.read())
    
    await ctx.send("All attachments have been saved.")

token = os.getenv('bot_token')
bot.run(token)
