from colorama import Back, Fore, Style
import os
import json
from requests import post, Session, get
from random import choice
import random
import threading
from discord.ext import commands
import requests as ru
import discord
from discord import ui
import time
import platform
from datetime import datetime
import pytz
import asyncio
import socket
from discord import app_commands
from discord.ext.commands import Bot
import aiohttp
import uuid
from typing import Literal
import json
from bs4 import BeautifulSoup as bs
from pystyle import Colors, Colorate
import itertools
from discord import SyncWebhook
import requests
from re import match
import sys
import subprocess
import qrcode  # assuming this is a general-purpose QR code library
try:
    from promptpay import qrcode as promptpay_qrcode
except Exception:
    # promptpay depends on a compiled extension (libscrc) that may fail to build
    # on systems without a C compiler / build tools. Provide a safe fallback.
    promptpay_qrcode = None
import itertools
from discord import Activity, ActivityType, Status
from datetime import datetime, timedelta
import datetime
import urllib.parse
import ipaddress
# Python 3.14 removed the old `cgi` module APIs that some older packages (like
# googletrans) rely on. Provide a minimal runtime shim for the few functions
# googletrans expects so it can import without requiring changes to the
# third-party package.
try:
    import cgi
except Exception:
    # minimal shim for cgi.parse_qs and cgi.escape used by googletrans
    import types
    import urllib.parse as _urllib_parse
    import importlib

    # Create a real module object so Python import machinery treats it like a module
    cgi_mod = types.ModuleType('cgi')

    def _escape(s):
        import html
        return html.escape(s)

    def _parse_qs(qs, keep_blank_values=False, strict_parsing=False):
        return _urllib_parse.parse_qs(qs, keep_blank_values=keep_blank_values, strict_parsing=strict_parsing)

    cgi_mod.escape = _escape
    cgi_mod.parse_qs = _parse_qs

    import sys as _sys
    _sys.modules['cgi'] = cgi_mod

from googletrans import Translator
from io import BytesIO


try:
	from PIL import Image, ImageDraw, ImageFont
except:
    # Avoid running pip directly via os.system during import time.
    # Instead, provide a clear error and try a safe subprocess install if desired.
    try:
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        raise ImportError("Pillow is required but couldn't be installed automatically. Please run: python -m pip install Pillow")




TOKEN = ".ใส่ที่นี่" # TOKEN BOT





with open('settings.json', 'r') as json_file:
    data = json.load(json_file)
IDROLE = data["IDROLE"] # ไอดียศ
LOGROLE = data["LOGROLE"] # ไอดีแจ้งเตือนเช่ายศ
TIMEROLE = data["TIMEROLE"]  # วินาที่เช้ายศ
# ตั่งค่าใน setting.json นะครับ



avatarbot = "https://media.discordapp.net/attachments/1173589548152926228/1201018181876199564/standard.gif?ex=65ed3458&is=65dabf58&hm=aa24e70748780055628579df8a28f2953a3df22ba14c1e993182974fd2cc78b8&=&width=288&height=288"
Alert = "> ⚠️  คุณไม่มีสิทธิ์ หรือ การอนุณาติที่สามารถใช้คำสั่งนี้ได้คะ "










class roletime(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.value = None

    async def remove_role_task(self, member, role_id):
        await asyncio.sleep(TIMEROLE)  # Wait for 1 minute
        try:
            role = member.guild.get_role(role_id)
            if role:
                await member.remove_roles(role)
        except discord.Forbidden:
            pass  # Handle Forbidden error if bot doesn't have permission to remove roles

    @discord.ui.button(label="・ ยืนยันตัวตน",emoji="✅", style=discord.ButtonStyle.green, custom_id="verifysuccess1")
    async def verifysuccess(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id_to_add = IDROLE  


        member = interaction.guild.get_member(interaction.user.id)


        if discord.utils.get(member.roles, id=role_id_to_add):
            await interaction.response.send_message(content="```คุณเคยรับบทบาทแล้ว```", ephemeral=True)
        else:
            try:

                await member.add_roles(discord.Object(id=role_id_to_add))
                embed = discord.Embed(title="ได้รับบทบาทแล้ว", description=f"__รายละเอียด__ \n\n⏲️ ระยะเวลา : {TIMEROLE} \n\n🗽 ยศที่ได้รับ : <@&{role_id_to_add}>")
                embed.set_footer(text="© 2025 ViSA Shops All rights reserved")
                embed.set_author(name=f"{interaction.guild.name}", url="", icon_url=avatarbot)  
                await interaction.response.send_message(embed=embed, ephemeral=True)
                channel = client.get_channel(LOGROLE)
                embed=discord.Embed(title="🟢 มีบทบาทอยู่", 
                                    description=f"__ข้อมูลการรับยศ__ \n\n👤 คุณ : {interaction.user.mention} \n🗽 ยศที่ได้รับ : <@&{role_id_to_add}> \n⏲️ อายุการใช้งานยศ : {TIMEROLE}", 
                                    color=0x00ff0a)

                embed.set_author(name=f"{interaction.guild.name}", url="", icon_url=avatarbot) 
                embed.set_footer(text="© 2025 ViSA Shops All rights reserved")
                message1 = await channel.send(embed=embed)

                # Start task to remove role after 1 minute
                asyncio.create_task(self.remove_role_task(member, role_id_to_add))
                channel = client.get_channel(LOGROLE)
                embed=discord.Embed(title="🔴 หมดเวลาแล้ว",description=f"{interaction.user.mention} หมดเวลาแล้ว",color=0xffff00)
                embed.set_footer(text="© 2025 ViSA Shops All rights reserved")
                await asyncio.sleep(TIMEROLE)
                await message1.edit(embed=embed)
            except discord.Forbidden:
                await interaction.response.send_message(content="ไม่สามารถเพิ่มบทบาทได้ กรุณาตรวจสอบการตั้งค่าสิทธิ์", ephemeral=True)


        
class aclient(commands.Bot):    
    def __init__(self): 
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
        self.role = None

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        activity = discord.Streaming(name="SlashCommands", url="https://www.twitch.tv/yanglarkdeveloper")
        await client.change_presence(status=discord.Status.idle, activity=activity)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")

        self.add_view(roletime())


client = aclient()




@client.tree.command(name='setuprole', description='ใส่ ID CHANNEL (ADMINONLY)')
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(channel_id='ตัวอย่าง 1193256543974592574')
async def bot(interaction: commands.Context, channel_id: str): 
      embed=discord.Embed(title="ระบบยศชั่วคราว", description="__ระบบยศชั่วคราว__ \n\n ระบบยศชั่วคราว", color=0xff2c2c)
      embed.add_field(name="", value="```diff\n-  เช่ายศ \n```", inline=True)
      embed.set_author(name="𝐕𝐢𝐬𝐀▸𝐒𝐡𝐨𝐩", url="", icon_url=avatarbot)
      embed.set_image(url="https://cdn.discordapp.com/attachments/1085210102992228494/1093902302739443782/f567aaa36d88fde1faf381a30bde00a5.png?ex=68ec6128&is=68eb0fa8&hm=79e20891bbe72292d661e697e0af8db9fdb22ff12ee95f33e7f067030e90b153&")
      embed.set_footer(text=f"© 2024 Planaria Shops All rights reserved")
      channel = client.get_channel(int(channel_id))
      await interaction.response.send_message(f'ได้สร้างคำสั่งบนห้อง <#{channel_id}>', ephemeral=True)
      await channel.send(embed=embed,view=roletime())
@bot.error
async def bot_error(interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"{Alert}", ephemeral=True)



client.run(TOKEN)
