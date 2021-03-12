import psycopg2
import discord
import requests
import random
from datetime import *
from discord.ext import commands
client=commands.Bot(command_prefix="!")

#--------------connecting to the database---------------------------------------

connection = psycopg2.connect(
    host="",
    database="",
    user="",
    password=""

)

#-------------------------Initializing the date object-----------------------
now=datetime.now()
#cursor
cursor=connection.cursor()

#----------------fetching all the data------------------------------
cursor.execute("select * from birthdays.bdays;")
rows = cursor.fetchall()

#-----------------Confirmation that the bot has logged in----------------
@client.event
async def on_ready():
    print("Logged in as Giga-Zeus")
    await client.change_presence(activity=discord.Game(name="!plshelp"))
    for guild in client.guilds:
        if str(guild.id) == "your server id":
            for channel in guild.channels:
                if str(channel.id) == "your channel id":
                    bdays=checkBirthday(rows, now)
                    if len(bdays)==0:
                        pass
                    else:
                        for bday in bdays:
                            embed = discord.Embed(title="Happy Birthday "+bday,
                                          description="Are you blind? Deploy the Birthday Wishes!!!",
                                          color=discord.Colour.red())
                            await channel.send(embed=embed)
                        await channel.send("@here")

@client.command()
async def hello(ctx):
    await ctx.send("```Konichiwa {}! ```".format(ctx.author))

#--------------------A function that gives the server information-----------------------
@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    memberCount = str(ctx.guild.member_count)

    embed = discord.Embed(title=name+" Server Information",
                        description=description,
                        color=discord.Colour.red()
                        )
    embed.add_field(name="Owner :",value=owner,inline=True)
    embed.add_field(name="Description :", value=description, inline=True)
    embed.add_field(name="Server Id :", value=id, inline=True)
    embed.add_field(name="Member Count :", value=memberCount, inline=True)

    await ctx.send(embed=embed)

#inserting birthdays into the birthday table
@client.command()
async def setbd(ctx,bd):
    cursor.execute("INSERT INTO birthdays.bdays(id,name,born_day) VALUES('{0}','{1}','{2}') ON CONFLICT (id) DO UPDATE SET born_day='{2}',name ='{1}';".format(ctx.author.id,ctx.author.name,bd))
    embed = discord.Embed(title="Your Birthday has been noted.",
                        description="You will be wished when your day comes.",
                        color=discord.Colour.red())
    connection.commit()
    await ctx.send(embed=embed)






@client.command()
async def plshelp(ctx):
    embed= discord.Embed(title="Commands list",
                         description="A big dum dum bot",
                         color=discord.Colour.red())
    embed.add_field(name="!hello :", value="Giga-Zeus will greet you.", inline=True)
    embed.add_field(name="!server:", value="To display server information", inline=True)
    embed.add_field(name="!setbd DD/MM/YY", value="To record your birthday.", inline=True)

    await ctx.send(embed=embed)


#-------------------------------To check if the current day is a  birthday---------------------------------
def checkBirthday(data,today):
    bdaylist=[]
    day=str(today.day)
    month=str(today.month)
    if len(day)==1:
        day= "0"+day
    if len (month)==1:
        month="0"+month

    for bday in data:
        checkDay=bday[2][0:2]
        checkMonth=bday[2][3:5]


        if checkDay==day and checkMonth==month:
            bdaylist.append(bday[1])

    return bdaylist


client.run('ADD YOUR OWN BOT TOKEN HERE')


