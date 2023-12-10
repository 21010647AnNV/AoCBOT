import discord
from discord.ext.commands import *
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    intents = discord.Intents.all()
    intents.members = True

    bot = Bot(command_prefix='!', intents=intents)

    leaderboard_url = 'https://adventofcode.com/2023/leaderboard/private/view/1763801.json'
    session_id = os.getenv('SESSION_ID')

    @bot.event
    async def on_ready():
        print(f'Bot đã kết nối thành công: {bot.user.name}')

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            detailMessage = 'Chao mung {0.mention} den voi {1.name}!'.format(member, guild)
            await guild.system_channel.send(detailMessage)

    @bot.command(name='hello')
    async def hello(ctx):
        author = ctx.message.author
        await ctx.send(f'Xin chào, {author.mention}!')

    @bot.command(name='info')
    async def info(ctx):
        embed = discord.Embed(title="Thông tin về Bot",
                          description="AoC BOT",
                          color=0x00ff00)
        embed.add_field(name="Tác giả", value="Nguyen Van An")
        embed.add_field(name="Ngôn ngữ", value="Python")
        embed.set_footer(text="© 2023 AoCBOT")
        await ctx.send(embed=embed)
    
    @bot.command(name='ping')
    async def ping(ctx):
        latency = round(bot.latency * 1000)  
        await ctx.send(f'Độ trễ hiện tại của bot là {latency} ms.')

    @bot.command(name='leaderboard')
    async def leaderboard(ctx):
        headers = {'Cookie': f'session={session_id}'}
        response = requests.get(leaderboard_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            members = data['members']

            sorted_members = sorted(members.items(), key=lambda x: x[1]['local_score'], reverse=True)

            embed = discord.Embed(title="Leaderboard", color=0x00ff00)

            leaderboard_info = "Leaderboard:\n"
            for member_id, member_data in sorted_members:
                member_name = member_data['name']
                local_score = member_data['local_score']
                embed.add_field(name=member_name, value=f"Score: {local_score}★", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Failed to fetch leaderboard. Status code: {response.status_code}")

    @bot.command(name='menu')
    async def menu(ctx):
        help_message = """
    Danh sách câu lệnh:
    `!menu`: Hiển thị danh sách câu lệnh
    `!leaderboard`: Flex nhẹ cái điểm
    `!hello`: Tự kỷ
    `!ping`: Ping mạng
    """
        await ctx.send(help_message)



    bot.run(os.getenv('TOKEN'))

