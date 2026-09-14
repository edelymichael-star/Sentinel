import discord
from discord import app_commands
import aiohttp
import random

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Track active channels for the Nitro section only
ACTIVE_NITRO_PFP_CHANNEL = None
ACTIVE_NITRO_USR_CHANNEL = None
ACTIVE_NITRO_BIO_CHANNEL = None

nitro_pfp_running = True
nitro_usr_running = True
nitro_bio_running = True

# Elite Nitro Asset pools (Animated styles, custom formatting)
NITRO_USERNAMES = ["vortex", "savage", "lunar", "eclipse", "numb", "hollow", "bliss", "phantom", "valour", "cynical"]
NITRO_BIOS = [
    "✦  building worlds in the dark.\n✦  moving in silence.",
    "─────────────────\nlost in translation.\n─────────────────",
    "> silent executioner.\n> seek clarity, find peace.",
    "• digital ghost\n• out of service"
]

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} - AuraCore NITRO Section Streamer Active")
    client.loop.create_task(nitro_pfp_background_loop())
    client.loop.create_task(nitro_usr_background_loop())
    client.loop.create_task(nitro_bio_background_loop())

# --- NITRO SETUP COMMANDS ---
@tree.command(name="setupnitropfp", description="Start the elite Nitro animated PFP/Banner stream.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_nitro_pfp(interaction: discord.Interaction):
    global ACTIVE_NITRO_PFP_CHANNEL, nitro_pfp_running
    ACTIVE_NITRO_PFP_CHANNEL = interaction.channel
    nitro_pfp_running = True
    await interaction.response.send_message("✨ Nitro PFP & Banner channel initialized!", ephemeral=True)
    await send_nitro_pfp(interaction.channel)

@tree.command(name="setupnitrousr", description="Start the elite Nitro username stream.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_nitro_usr(interaction: discord.Interaction):
    global ACTIVE_NITRO_USR_CHANNEL, nitro_usr_running
    ACTIVE_NITRO_USR_CHANNEL = interaction.channel
    nitro_usr_running = True
    await interaction.response.send_message("💎 Nitro Username channel initialized!", ephemeral=True)
    await send_nitro_usr(interaction.channel)

@tree.command(name="setupnitrobio", description="Start the elite Nitro formatted bio stream.")
@app_commands.checks.has_permissions(administrator=True)
async def setup_nitro_bio(interaction: discord.Interaction):
    global ACTIVE_NITRO_BIO_CHANNEL, nitro_bio_running
    ACTIVE_NITRO_BIO_CHANNEL = interaction.channel
    nitro_bio_running = True
    await interaction.response.send_message("📝 Nitro Bio channel initialized!", ephemeral=True)
    await send_nitro_bio(interaction.channel)

# --- NITRO STOP COMMAND ---
@tree.command(name="stopnitro", description="Stop the Nitro automated streams.")
@app_commands.choices(target=[
    app_commands.Choice(name="all", value="all"),
    app_commands.Choice(name="pfp", value="pfp"),
    app_commands.Choice(name="usernames", value="usernames"),
    app_commands.Choice(name="bios", value="bios")
])
@app_commands.checks.has_permissions(administrator=True)
async def stop_nitro(interaction: discord.Interaction, target: str):
    global nitro_pfp_running, nitro_usr_running, nitro_bio_running
    if target == "all":
        nitro_pfp_running = nitro_usr_running = nitro_bio_running = False
        await interaction.response.send_message("🛑 All Nitro streams paused.", ephemeral=True)
    elif target == "pfp":
        nitro_pfp_running = False
        await interaction.response.send_message("🛑 Nitro PFP stream paused.", ephemeral=True)
    elif target == "usernames":
        nitro_usr_running = False
        await interaction.response.send_message("🛑 Nitro Username stream paused.", ephemeral=True)
    elif target == "bios":
        nitro_bio_running = False
        await interaction.response.send_message("🛑 Nitro Bio stream paused.", ephemeral=True)

# --- NITRO HELPERS ---
async def send_nitro_pfp(channel):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.best/api/v2/waifu") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    embed = discord.Embed(
                        title="✨ • NITRO PROFILE ASSET",
                        description="*Optimized for Animated Avatars & Banners*",
                        color=0x2b2d31
                    )
                    embed.set_image(url=data["results"][0]["url"])
                    embed.set_footer(text="AuraCore • Nitro Exclusive")
                    await channel.send(embed=embed)
    except Exception as e:
        print(f"Nitro PFP Error: {e}")

async def send_nitro_usr(channel):
    try:
        chosen = random.choice(NITRO_USERNAMES)
        embed = discord.Embed(
            title="💎 • NITRO USERNAME TAG",
            description=f"```ansi\n\u001b[1;35m{chosen}\u001b[0m```",
            color=0x2b2d31
        )
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Nitro Username Error: {e}")

async def send_nitro_bio(channel):
    try:
        chosen = random.choice(NITRO_BIOS)
        embed = discord.Embed(
            title="📝 • NITRO BIO LAYOUT",
            description=f"```\n{chosen}\n```",
            color=0x2b2d31
        )
        embed.set_footer(text="AuraCore • Advanced Profile Showcase")
        await channel.send(embed=embed)
    except Exception as e:
        print(f"Nitro Bio Error: {e}")

# --- NITRO LOOPS ---
async def nitro_pfp_background_loop():
    await client.wait_until_ready()
    while not client.is_closed():
        if nitro_pfp_running and ACTIVE_NITRO_PFP_CHANNEL:
            await send_nitro_pfp(ACTIVE_NITRO_PFP_CHANNEL)
        import asyncio
        await asyncio.sleep(35.0)

async def nitro_usr_background_loop():
    await client.wait_until_ready()
    while not client.is_closed():
        if nitro_usr_running and ACTIVE_NITRO_USR_CHANNEL:
            await send_nitro_usr(ACTIVE_NITRO_USR_CHANNEL)
        import asyncio
        await asyncio.sleep(25.0)

async def nitro_bio_background_loop():
    await client.wait_until_ready()
    while not client.is_closed():
        if nitro_bio_running and ACTIVE_NITRO_BIO_CHANNEL:
            await send_nitro_bio(ACTIVE_NITRO_BIO_CHANNEL)
        import asyncio
        await asyncio.sleep(28.0)

@setup_nitro_pfp.error
@setup_nitro_usr.error
@setup_nitro_bio.error
@stop_nitro.error
async def setup_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Admin permissions required.", ephemeral=True)

# Replace YOUR_BOT_TOKEN_HERE with your bot's token
client.run("YOUR_BOT_TOKEN_HERE")
      
