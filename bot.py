import discord
from discord.ext import commands, tasks
import json
import secrets
import string
import os
import random
import pytz
from typing import Union
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='++', intents=intents)
                   
used_keys_path = 'used_keys.json'
available_keys_path = 'available_keys.json'
role_id_to_assign = 851058432881590283 # ID Role 

class CustomHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title='Bot Commands',
            color=0x3498db,  
            description='Here is a list of available commands.'
        )

        for cog, commands in mapping.items():
            if cog is None:
                name = "No Category"
            else:
                name = cog.qualified_name

            command_signatures = [self.get_command_signature(c) for c in commands]
            embed.add_field(name=name, value='\n'.join(command_signatures), inline=False)

        embed.set_footer(text="Bot By Pimsickgirl", icon_url="https://cdn.discordapp.com/avatars/837294095335817226/21150d8c1ff6a2bf1db442d464aea3a4.png?size=1024")
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/977500765943902329/270528bf0e304c301290ce2966b6bc20.png?size=1024")

        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = CustomHelpCommand()

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.lower()
        if 'ดี' in content:
            await self.greet(message)
        elif 'm!p' in content or 'm!play' in content:
            await self.play_music(message)
        elif 'พิมพ์' in content or 'พิม' in content:
            await self.call_member(message, 837294095335817226, "มีคนเรียกคนใต้ครับ !!", "มีคนเรียกไอดำ")
        elif 'เอก' in content or 'ใต้' in content:
            await self.call_member(message, 952987907424133190, "มีคนเรียกคนใต้ครับ !!", "มีคนเรียกไอดำ")
        elif 'เอ็น' in content or 'อ้วน' in content:
            await self.call_member(message, 712274129663033375, "ไอเอ็นมีคนเรียก", "ไอ้อ้วนมีคนเรียกมาตอบเร็วๆ", "ไอ้อีสานมีคนเรียกไอสัส")
        elif 'ภู' in content or 'hannibal' in content:
            await self.call_member(message, 951901025713934376, "ไอ้ภูมีคนเรียกไอสัส", "ไอฮันนิบาลมีคนเรียก")
        elif '55' in content or 'ตลก' in content or 'ขำ' in content:
            await self.respond_to_joke(message)
        elif 'ควย' in content or 'สัส' in content:
            await self.respond_to_profanity(message)
        elif 'ผมรักคิมมี่' in content:
            await self.give_role(message.author, 700539912851816546)
            await message.channel.send(f'{message.author.mention} ได้รับยศ!')

        await self.process_commands(message)
        
    async def give_role(self, member, role_id):
        role = discord.utils.get(member.guild.roles, id=role_id)
        if role:
            await member.add_roles(role)

    async def greet(self, message):
        await message.channel.send(f"สวัสดีครับ {message.author.mention}")

    async def play_music(self, message):
        responses = [
            "เปิดเพลงควยไรครับ",
            "ผมขอละนะเปิดเพลงอื่นเหอะ",
            "เพลงลาวๆอย่าหาเปิด",
            "ให้โอกาศปิดเพลง"
        ]
        response = random.choice(responses)
        await message.channel.send(response)

    async def call_member(self, message, member_id, response1, response2):
        member = message.guild.get_member(member_id)
        if member:
            response = [f"{member.mention} {response1}", f"{member.mention} {response2}"]
            selected_response = random.choice(response)
            await message.channel.send(selected_response)

    async def respond_to_joke(self, message):
        responses = [
            "5555555 พ่อมึงตายหรอขำอะ",
            "5555555 มันตลกแบบนี้หรือ",
            "ตลกตายละไอควาย",
            "5555555 ขำมากครับ"
        ]
        response = random.choice(responses)
        await message.channel.send(response)

    async def respond_to_profanity(self, message):
        responses = ["ควยไรไอสัสดำ", "พ่อมึงดิไอเหี้ยลาว"]
        response = random.choice(responses)
        await message.channel.send(response)

blocked_roles = {686934992152297513}

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel and any(role.id in blocked_roles for role in member.roles):
            embed = discord.Embed(
                title="การเข้าร่วม Voice Channel ถูกบล็อก",
                description=f"คุณไม่ได้รับอนุญาตให้เข้าร่วม Voice Channel `{after.channel.name}!`\n กรุณาติดต่อแอดมิน: **Pimsickgirl**",
                color=discord.Color.red()
            )
            await member.send(embed=embed)
            await member.move_to(None)

        embed = discord.Embed()
        targeted_server_id = 687301737274540090 
        if member.guild.id != targeted_server_id:
            return
        thailand_timezone = pytz.timezone('Asia/Bangkok')
        timestamp = datetime.now(thailand_timezone).strftime('%Y-%m-%d %H:%M:%S')

        if before.channel is None:
            user = member if isinstance(member, discord.User) else member
            embed.set_author(name=user.name, icon_url=user.avatar)
            embed.description = f'{member.mention} เข้า Voice Channel: {after.channel.name}'
            embed.color = discord.Color.green()
            embed.set_footer(text=f'{timestamp}')
        elif after.channel is None:
            user = member if isinstance(member, discord.User) else member
            embed.set_author(name=user.name, icon_url=user.avatar)
            embed.description = f'{member.mention} ออกจาก Voice Channel: {before.channel.name}'
            embed.color = discord.Color.red()
            embed.set_footer(text=f'{timestamp}')
        else:
            user = member if isinstance(member, discord.User) else member
            embed.set_author(name=user.name, icon_url=user.avatar)
            embed.description = f'{member.mention} ย้ายจาก {before.channel.name} ไป {after.channel.name}'
            embed.color = discord.Color.blue()
            embed.set_footer(text=f'{timestamp}')

        channel = bot.get_channel(1184110223296831508)
        await channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    change_activity.start()

@tasks.loop(seconds=60)
async def change_activity():
    await bot.change_presence(activity=discord.Game(name=f"with {len(bot.guilds)} servers | ++help "))

@bot.command()
@commands.is_owner()
async def getkey(ctx, num_keys: int = 1):
    keys_generated = []

    for _ in range(num_keys):
        redeem_code = generate_random_key()

        if not is_key_used(redeem_code):
            keys_generated.append(redeem_code)
            mark_key_as_available(redeem_code)

    if keys_generated:
        keys_str = '\n'.join(keys_generated)
        embed = discord.Embed(
            title='Keys Generated', 
            description=f'The keys are:\n```{keys_str}```', 
            color=0x00ff00)
        await ctx.send(embed=embed)
        print(f'key gen: \n{keys_str}')
    else:
        embed = discord.Embed(
            title='Error', 
            description='There is an issue in generating the keys. Please try again.', 
            color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def redeemkey(ctx, redeem_code: str):
    if is_key_available(redeem_code):
        embed = discord.Embed(
            title='Key Redeemed',
            description=f'The key `{redeem_code}` has been redeemed!',
            color=0x00ff00)
        await ctx.send(embed=embed)
        mark_key_as_used(redeem_code)
        remove_key_from_available(redeem_code)

        member = ctx.author
        role = ctx.guild.get_role(role_id_to_assign)
        await member.add_roles(role)
        
        embed = discord.Embed(
            title='Role Assigned', 
            description=f'You have been assigned the role `{role.name}`!',
            color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Error', 
            description=f'Invalid key: `{redeem_code}`',
            color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def purge(ctx, amount: int = 5):
    if 1 <= amount <= 100:
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title='Messages Cleared',
            description=f'{amount} messages have been cleared by {ctx.author.mention}.',
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='Error',
            description='Please provide a number between 1 and 100 for the amount to clear.',
            color=0xff0000
        )
        await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, user: Union[discord.User, int] = None):
    if user is None:
        user = ctx.author
    elif isinstance(user, int):
        user = bot.get_user(user)

    if user:
        embed = discord.Embed(
            title=f"Picture of {user.name}",
            color=discord.Color.blue()
        )

        embed.set_image(url=user.display_avatar.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found.")

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.BadUnionArgument):
        await ctx.send("User not found.")
    
@bot.command()
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not mute_role:
        mute_role = await ctx.guild.create_role(name='Muted')
        overwrite = discord.PermissionOverwrite(send_messages=False)
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, overwrite=overwrite)

    await member.add_roles(mute_role)

    embed = discord.Embed(
        title='Muted',
        description=f'{member.mention} has been Muted.\nReason: {reason}',
        color=discord.Color.red()
    )

    await ctx.send(embed=embed)

@bot.command()
async def unmute(ctx, member: discord.Member = None):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if not member:
        await ctx.send("Please specify a member to unmute.")
        return

    if not mute_role:
        await ctx.send("Muted role not found. Use the mute command first.")
        return

    await member.remove_roles(mute_role)

    embed = discord.Embed(
        title='Unmuted',
        description=f'{member.mention} has been Unmuted.',
        color=discord.Color.green()
    )

    await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Please tag the user you want to mute.')

@bot.command()
async def limit(ctx, limit: int):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel

        if channel.permissions_for(ctx.guild.me).manage_channels:
            try:
                await channel.edit(user_limit=limit)

                embed = discord.Embed(
                    title="User Limit Updated",
                    description=f"User limit set to {limit} in {channel.name}.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="Error",
                    description="I don't have permission to modify the user limit in this channel.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="I don't have permission to manage channels.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="You need to be in a voice channel to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@limit.error
async def limit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error",
            description="Please provide a user limit.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Error",
            description="Please provide a valid integer for the user limit.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)

        embed = discord.Embed(
            title=f"{member.name}#{member.discriminator} Banned",
            description=f"The user {member.mention} has been banned, \n Reason: {reason}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to ban member")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason="NO reason priveded"):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title=f"{member.name}#{member.discriminator} Kicked",
            description=f"The user {member.mention} has been kicked.\nReason: {reason}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have permission to kick members.")

@bot.command()
async def lock(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(
            title="Channel Locked",
            description=f"This channel has been locked by {ctx.author.mention}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Permission",
            description="You don't have permission to locked channel",
            color=discord.Color.dark_orange()
        )
        await ctx.send(embed=embed)

@bot.command()
async def unlock(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(
            title='Channel Unlock',
            description=f'This Channel has been unlocked by {ctx.author.mention}',
            color=discord.Color.dark_orange()
        )
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="U CAN DO IT BRO",
            description="You don't have permission to unlocked channel",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command()
async def credit(ctx):
    creator_name = "Pimlisy"
    creation_data = "21 May 2022"
    creator_image_url = "https://images-ext-1.discordapp.net/external/GQVGnIhEioj6DNGFhsDIdJmTTx8Ksab8qpYM0ppoFXs/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/837294095335817226/d7b4e097db59a6b301815294c2f0134c.png"
    discord_contact = "https://discord.gg/t5WBnbfZS2"
    
    embed = discord.Embed(
        title="Bot Credits",
        color=0x00ff00
    )
    embed.add_field(name="Creator", value=creator_name, inline=False)
    embed.add_field(name="Creation Data", value=creation_data, inline=False)
    embed.add_field(name="Discord Contact", value=discord_contact, inline=False)
    embed.set_thumbnail(url=creator_image_url)
    embed.set_footer(text=f"requested by {ctx.author.name} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    await ctx.send(embed=embed)

@bot.command()
async def warning(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title=f"Warning to {member.name}",
        description=f"{ctx.author.name} has issued a warning",
        color=discord.Color.red()
    )

    if reason:
        embed.add_field(name='Reason', value=reason, inline=False)

    try:
        await member.send(embed=embed)
        await ctx.send(f'Warning sent to {member.mention} successfully.')
    except discord.Forbidden:
        await ctx.send(f'Unable to send a warning to {member.mention} via DM.')

@bot.command()
async def slowmode(ctx, seconds: int):
    embed = discord.Embed(
        title='Slow Mode Set',
        description=f'Slow mode has been set to {seconds} seconds in this channel',
        color=discord.Color.blue()
    )

    try: 
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed.description = 'I do not have permission to set slow mode in this channel.'

        await ctx.send(embed=embed
                       )
@bot.command()
@commands.is_owner()
async def kickallvc(ctx):
    embed = discord.Embed(
        title="Kick All Members from Voice Channels",
        description="The bot has kicked all members from all voice channels.",
        color=discord.Color.red()
    )
    for voice_channel in ctx.guild.voice_channels:
        for member in voice_channel.members:
            await member.move_to(None)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def muteallvc(ctx):
    if ctx.author.guild_permissions.administrator:
        if ctx.guild.me.guild_permissions.mute_members:
            for channel in ctx.guild.voice_channels:
                for member in channel.members:
                    await member.edit(mute=True)
            await ctx.send("Everyone was server muted on every voice channel.")
        else:
            await ctx.send("Bot does not have rights to Server Mute members.")
    else:
        await ctx.send("You do not have permission to use this command.")

def generate_random_key():
    characters = string.ascii_letters + string.digits
    key_length = 12
    return ''.join(secrets.choice(characters) for i in range(key_length))

def remove_key_from_available(key):
    try:
        with open(available_keys_path, 'r') as f:
            available_keys = json.load(f)
    except json.decoder.JSONDecodeError:
        available_keys = []

    if key in available_keys:
        available_keys.remove(key)

        with open(available_keys_path, 'w') as f:
            json.dump(available_keys, f)

def is_key_used(key):
    if not os.path.exists(used_keys_path):
        with open(used_keys_path, 'w') as f:
            json.dump([], f)
    with open(used_keys_path, 'r') as f:
        used_keys = json.load(f)
    return key in used_keys

def is_key_available(key):
    if not os.path.exists(available_keys_path):
        with open(available_keys_path, 'w') as f:
            json.dump([], f)

    try:
        with open(available_keys_path, 'r') as f:
            available_keys = json.load(f)
    except json.decoder.JSONDecodeError:
        available_keys = []

    return key in available_keys

def mark_key_as_used(key):
    with open(used_keys_path, 'r') as f:
        used_keys = json.load(f)
    used_keys.append(key)
    with open(used_keys_path, 'w') as f:
        json.dump(used_keys, f)

def mark_key_as_available(key):
    if not os.path.exists(available_keys_path):
        with open(available_keys_path, 'w') as f:
            json.dump([], f)

    try:
        with open(available_keys_path, 'r') as f:
            available_keys = json.load(f)
    except json.decoder.JSONDecodeError:
        available_keys = []

    available_keys.append(key)

    with open(available_keys_path, 'w') as f:
        json.dump(available_keys, f)
    
bot.run(os.getenv('DISCORD_TOKEN'))