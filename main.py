import discord
import os
from discord.ext import commands

TOKEN = os.environ.get("BOT_TOKEN")
PREFIX = "!PN"
WELCOME_CHANNEL_ID = int(os.environ.get("WELCOME_ID"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Добро пожаловать!",
            description=f"Привет {member.mention}, подайте заявку и ожидайте её рассмотрения!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=""):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} был кикнут.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=""):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} был забанен. Причина: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 100):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Удалено {amount} сообщений.", delete_after=3)

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, *, reason=""):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)
    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} замьючен. По причине {reason}")

@bot.event
async def on_ready():
    print(f"Клан бот {bot.user} запущен")

bot.run(TOKEN)
