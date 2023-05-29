import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(help_command=None, intents=intents)

# https://github.com/G-eb/

with open("config.json") as f:
    geb = json.load(f)
with open("config.json") as f:
    guildid = int(geb["guild_id"])
    roleid = geb["verified_role_id"]
    bottoken = geb["bot_token"]
    requestschannel = geb["requests_channel_id"]
                  
@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    whitelist = open("whitelist.txt", "r")
    whitelisted = whitelist.read() 
    if(str(member.id) in whitelisted):
        role = discord.utils.get(member.guild.roles, id=int(roleid))
        await member.add_roles(role)
        await member.send(f"You have been whitelisted in `{member.guild.name}`!")
    else:
        await member.send(f"You are not currently whitelisted in `{member.guild.name}`!\nA whitelist request has been sent, please try to join the server again in a few days.")
        await member.ban(reason="Not whitelisted!")
        channel = client.get_channel(int(requestschannel))
        await channel.send(f"{member.mention} has requested to join the server.\n\nRun `/accept id:{member.id}` to accept, or `/deny id:{member.id}` to deny.")
    whitelist.close()

@client.slash_command(guild_ids=[guildid])
async def ping(ctx):
    await ctx.respond(f":ping_pong: {round(client.latency * 1000)}ms")

@client.slash_command(guild_ids=[guildid])
async def accept(ctx, id: str):
    if ctx.author.guild_permissions.administrator:
        f = open("whitelist.txt", "a")
        f.write(id + "\n")
        user = await client.fetch_user(id)
        await ctx.guild.unban(user=user, reason="Whitelisted!")
        await ctx.respond(f"Accepted <@{id}> [`{id}`]!")
    else:
        await ctx.respond("You don't have permission to use this command!", ephemeral=True)

@client.slash_command(guild_ids=[guildid])
async def deny(ctx, id: str):
    if ctx.author.guild_permissions.administrator:
        await ctx.respond(f"Denied <@{id}> [`{id}`]!")
    else:
        await ctx.respond("You don't have permission to use this command!", ephemeral=True)


client.run(bottoken)
