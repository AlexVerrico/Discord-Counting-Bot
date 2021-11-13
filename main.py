<<<<<<< Updated upstream
import sqlite3
import os
from dotenv import load_dotenv
from discord.ext import commands
# import discord
# from queue import Queue
# import threading
# import time

# dbOperations = Queue(maxsize=0)

load_dotenv()
TOKEN = os.getenv('THE_COUNT_DISCORD_TOKEN')
PREFIX = "".join((os.getenv('THE_COUNT_PREFIX'), ' '))

bot = commands.Bot(command_prefix=PREFIX)
# client = discord.Client()

DbName = 'count.sqlite'
count_info_headers = ['guild_id', 'current_count', 'number_of_resets', 'last_user', 'message', 'channel_id', 'log_channel_id', 'greedy_message']

connection = sqlite3.connect(DbName)
cursor = connection.cursor()


# -- Begin SQL Helper Functions --
def create_table(dbname, tablename, tableheader):
    try:
        # connection = sqlite3.connect(dbname)
        # cursor = connection.cursor()
        cursor.execute("CREATE TABLE %s%s" % (tablename, tuple(tableheader)))
        connection.commit()
        # connection.close()
        return
    except sqlite3.OperationalError:
        return


def insert_values_into_table(dbname, tablename, values):
    if os.path.exists(dbname) is True:
        # connection = sqlite3.connect(dbname)
        # cursor = connection.cursor()
        cursor.execute("INSERT INTO %s VALUES %s" % (tablename, tuple(values)))
        connection.commit()
        # connection.close()


def check_if_table_exists(dbname, tablename, tableheaders):
    try:
        # connection = sqlite3.connect(dbname)
        # cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % tablename)
        # connection.close()
    except sqlite3.OperationalError:
        create_table(dbname, tablename, tableheaders)


def create_new_entry(guild_id,
                     count=str(0),
                     number_of_resets=str(0),
                     last_user=str(0),
                     guild_message=str("{{{user}}} typed the wrong number"),
                     count_channel_id=str(''),
                     log_channel_id=str(''),
                     greedy_message=str("{{{user}}} was too greedy")):
    # dbOperations.put(['create',
    temp1 = [
        str(guild_id), str(count),
        str(number_of_resets),
        str(last_user),
        str(guild_message),
        str(count_channel_id),
        str(log_channel_id),
        str(greedy_message)]
    # ])

    cursor.execute("INSERT INTO count_info %s VALUES %s" % (tuple(count_info_headers), tuple(temp1)))
    connection.commit()
    return

# -- End SQL Helper Functions --


# -- Begin Count Master Commands --
bot.remove_command('help')


@bot.command(name='help')
async def count_help(ctx):
    response = """See https://github.com/AlexVerrico/Discord-Counting-Bot for detailed help info"""
    await ctx.send(response)
    return


@bot.command(name='wrong_message')
@commands.has_role("count master")
async def wrong_message(ctx, *args):
    _message = " ".join(args)
    if _message == 'help':
        response = """
        Set the message to be sent when someone types the wrong number
{{{user}}} will be replaced by the name of whoever typed the wrong number
        """
        await ctx.send(response)
        return
    # print('%s, %s' % (_message, ctx.guild.id))
    # connection = sqlite3.connect(DbName)
    # cursor = connection.cursor()
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    # connection.close()
    # print(test)
    if test is None:
        # dbOperations.put(['create', [str(ctx.guild.id), str('0'), str('0'), str(''), str(_message), str(ctx.channel.id), str(ctx.channel.id), str('{{{user}}} was too greedy')]])
        create_new_entry(ctx.guild.id,
                         count_channel_id=ctx.channel.id,
                         log_channel_id=ctx.channel.id,
                         guild_message=_message)
    else:
        guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message = test
        # dbOperations.put(['update',
        temp1 = [guild_id, count, number_of_resets, last_user, _message, channel_id, log_channel_id, greedy_message]
        # ])
        cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
        connection.commit()
    # print(bot.get_user(ctx.message.author.id))
    # await ctx.send("<@%s>" % ctx.message.author.id)
    return


@wrong_message.error
async def wrong_message_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need the role "count master" to run that command')
    else:
        raise error


@bot.command(name='greedy_message')
@commands.has_role("count master")
async def greedy_message(ctx, *args):
    _message = " ".join(args)
    if _message == 'help':
        response = """
        Set the message to be sent when someone types 2 messages in a row
{{{user}}} will be replaced by the name of whoever typed the 2 messages
        """
        await ctx.send(response)
        return
    # print('%s, %s' % (_message, ctx.guild.id))
    # connection = sqlite3.connect(DbName)
    # cursor = connection.cursor()
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    # connection.close()
    # print(test)
    if test is None:
        # dbOperations.put(['create', [str(ctx.guild.id), str('0'), str('0'), str(''), str(_message), str(ctx.channel.id), str(ctx.channel.id), str('{{{user}}} was too greedy')]])
        create_new_entry(ctx.guild.id,
                         count_channel_id=ctx.channel.id,
                         log_channel_id=ctx.channel.id,
                         greedy_message=_message)
    else:
        guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, old_greedy_message = test
        # dbOperations.put(['update',
        temp1 = [guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, _message]
        # ])

        cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
        connection.commit()
    # print(bot.get_user(ctx.message.author.id))
    # await ctx.send("<@%s>" % ctx.message.author.id)
    return


@wrong_message.error
async def wrong_message_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need the role "count master" to run that command')
    else:
        raise error


@bot.command(name='counting_channel')
@commands.has_role("count master")
async def counting_channel(ctx, arg1):
    print("counting_channel")
    channel_id = arg1
    if channel_id == 'help':
        response = """
            Set the id of the channel that you want to count in
use `!count counting_channel this_channel` to use the channel that you are typing in
            """
        await ctx.send(response)
        return
    if channel_id == 'this_channel':
        channel_id = ctx.channel.id
        # print(channel_id)
    # print('%s, %s' % (_message, ctx.guild.id))
    # connection = sqlite3.connect(DbName)
    # cursor = connection.cursor()
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    # connection.close()
    # print(test)
    if test is None:
        # dbOperations.put(['create', [str(ctx.guild.id), str('0'), str('0'), str(''), str('{{{user}}} typed the wrong number'), str(channel_id),
        #                              str(channel_id), str('{{{user}}} was too greedy')]])
        create_new_entry(ctx.guild.id,
                         count_channel_id=channel_id,
                         log_channel_id=channel_id,)
    else:
        # print("test is not None")
        guild_id, count, number_of_resets, last_user, guild_message, old_channel_id, log_channel_id, greedy_message = test
        # dbOperations.put(['update',
        temp1 = [guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message]
        # ])

        cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
        connection.commit()
    return


@counting_channel.error
async def counting_channel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need the role "count master" to run that command')
    else:
        raise error


@bot.command(name='log_channel')
@commands.has_role("count master")
async def log_channel(ctx, arg1):
    print("log_channel")
    channel_id = arg1
    if channel_id == 'help':
        response = """
            Set the id of the channel that you want to log mistakes too
use `!count log_channel this_channel` to use the channel that you are typing in
            """
        await ctx.send(response)
        return
    if channel_id == 'this_channel':
        channel_id = ctx.channel.id
        # print(channel_id)
    # print('%s, %s' % (_message, ctx.guild.id))
    # connection = sqlite3.connect(DbName)
    # cursor = connection.cursor()
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    # connection.close()
    # print(test)
    if test is None:
        # dbOperations.put(['create', [str(ctx.guild.id), str('0'), str('0'), str(''), str('{{{user}}} typed the wrong number'), str(channel_id),
        #                              str(channel_id), str('{{{user}}} was too greedy')]])
        create_new_entry(ctx.guild.id,
                         count_channel_id=channel_id,
                         log_channel_id=channel_id,)
    else:
        # print("test is not None")
        guild_id, count, number_of_resets, last_user, guild_message, old_channel_id, old_log_channel_id, greedy_message = test
        # dbOperations.put(['update',
        temp1 = [guild_id, count, number_of_resets, last_user, guild_message, old_channel_id, channel_id, greedy_message]
        # ])

        cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
        connection.commit()
    return


@counting_channel.error
async def counting_channel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need the role "count master" to run that command')
    else:
        raise error

# -- End Count Master Commands --


# -- Begin counting detection --
@bot.event
async def on_message(_message):
    ctx = await bot.get_context(_message)
    if ctx.message.author.bot:
        return
    if str(_message.content).startswith(str(PREFIX)):
        await bot.invoke(ctx)
        return
    # connection = sqlite3.connect(DbName)
    # cursor = connection.cursor()
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % _message.guild.id)
    temp = cursor.fetchone()
    # connection.close()
    if temp is None:
        print("ln 143")
        return
    else:
        print(temp[5])
        print(_message.channel.id)
        if str(temp[5]) != str(ctx.channel.id):
            print("ln 147")
            return
        else:
            print("ln 150")
            try:
                current_count, trash = _message.content.split(' ', 1)
            except ValueError:
                current_count = _message.content
            current_count = int(current_count)
            print(current_count)
            old_count = int(temp[1])
            print(old_count)
            if str(ctx.message.author.id) == str(temp[3]):
                print("greedy")
                guild_id, old_count, old_number_of_resets, old_last_user, guild_message, channel_id, log_channel_id, greedy_message = temp
                count = str(0)
                number_of_resets = str(int(old_number_of_resets) + 1)
                last_user = str('')
                # dbOperations.put(['update',
                temp1 = [guild_id, count, number_of_resets, last_user, guild_message, channel_id,
                         log_channel_id, greedy_message]
                # ])

                cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
                connection.commit()

                await ctx.send(str(temp[7]).replace("{{{user}}}", '<@%s>' % str(ctx.message.author.id)))
                channel = bot.get_channel(int(temp[6]))
                await channel.send('<@%s> lost the count when it was at %s' % (ctx.message.author.id, old_count))
                return
            if old_count + 1 != current_count:
                guild_id, old_count, old_number_of_resets, old_last_user, guild_message, channel_id, log_channel_id, greedy_message = temp
                count = str(0)
                number_of_resets = str(int(old_number_of_resets) + 1)
                last_user = str('')
                # dbOperations.put(['update',
                temp1 = [guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message]
                # ])

                cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
                connection.commit()

                await ctx.send(str(temp[4]).replace("{{{user}}}", '<@%s>' % str(ctx.message.author.id)))
                # await bot.send_message(bot.get_channel(temp[6]), 'test')
                channel = bot.get_channel(int(temp[6]))
                await channel.send('<@%s> lost the count when it was at %s' % (ctx.message.author.id, old_count))
                return
            if old_count + 1 == current_count:
                guild_id, old_count, number_of_resets, old_last_user, guild_message, channel_id, log_channel_id, greedy_message = temp
                count = str(current_count)
                last_user = str(ctx.message.author.id)
                # dbOperations.put(['update',
                temp1 = [guild_id, count, number_of_resets, last_user, guild_message, channel_id,
                         log_channel_id, greedy_message]
                # ])

                cursor.execute("UPDATE count_info SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ? WHERE guild_id = '%s'" % temp1[0], (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7],))
                connection.commit()

                return
            return


# -- Begin General Function Declarations --
# def run_queue():
#     # client.run(TOKEN)
#     while True:
#         if dbOperations.empty() is False:
#             temp = dbOperations.get()
#             # print(temp)
#             # connection = sqlite3.connect(DbName)
#             # cursor = connection.cursor()
#             if temp[0] == 'create':
#                 temp1 = temp[1]
#                 # print("temp1 = %s" % temp1)
#                 cursor.execute("INSERT INTO count_info%s VALUES %s" % (tuple(count_info_headers), tuple(temp1)))
#                 connection.commit()
#                 # connection.close()
#                 del temp
#                 del temp1
#                 continue
#             elif temp[0] == 'update':
#                 # print("temp[0] == update")
#                 temp1 = temp[1]
#                 cursor.execute("UPDATE count_info SET guild_id = '%s', current_count = '%s', number_of_resets = '%s', last_user = '%s', message = '%s', channel_id = '%s', log_channel_id = '%s', greedy_message = '%s' WHERE guild_id = '%s'" % (temp1[0], temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7], temp1[0]))
#                 connection.commit()
#                 # connection.close()
#                 del temp
#                 del temp1
#                 continue
#             else:
#                 time.sleep(0.1)
#                 continue

# -- End General Function Declarations --


# connection = sqlite3.connect(DbName)
# cursor = connection.cursor()
# cursor.execute("UPDATE count_info SET count = count + '1' WHERE last_user = 'AlexV#4999'")
# connection.commit()
# # cursor.execute("SELECT count FROM count_info WHERE guild_id LIKE 'test1'")
# # test = cursor.fetchone()
# connection.close()
# # print(test)


# -- Begin Initialization code --
check_if_table_exists(DbName, 'count_info', count_info_headers)
# t = threading.Timer(0, run_queue)
# t.start()
# print("passed_threading")
bot.run(TOKEN)
# -- End Initialization code --
=======
import sqlite3
import os
from discord.client import Client
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, Embed, Color, guild, message
from discord.utils import get

from datetime import datetime
intents = Intents.default()
intents.guild_messages = True
load_dotenv()
TOKEN = os.getenv('THE_COUNT_DISCORD_TOKEN')
if TOKEN is None:
    print("Please set the TOKEN variable in the Environment")
    exit()
    
#PREFIX = "".join((os.getenv('THE_COUNT_PREFIX'), ' '))
PREFIX = "!count "
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

DbName = 'count.sqlite'
count_info_headers = ['guild_id', 'current_count', 'number_of_resets', 'last_user', 'message', 'channel_id', 'log_channel_id', 'greedy_message', 'record', 'record_user', 'record_timestamp']
stat_headers = ['guild_id', 'user', 'count_correct', 'count_wrong', 'highest_valid_count', 'last_activity', 'drink']
beer_headers = ['guild_id','user', 'owed_user', 'count']
connection = sqlite3.connect(DbName)
cursor = connection.cursor()


# -- Begin SQL Helper Functions --
def create_table(dbname, tablename, tableheader):
    try:
        cursor.execute("CREATE TABLE %s%s" % (tablename, tuple(tableheader)))
        connection.commit()
        return
    except sqlite3.OperationalError:
        return

def time_since(strtime):
    now = datetime.now()
    then = datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S.%f')
    duration = now - then
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds // 60) % 60
    if days > 0:
        return f'{days}d ago'
    elif hours > 0:
        return f'{hours}h ago'
    elif minutes > 0:
        return f'{minutes}m ago'
    else:
        return 'just now'
    

def isrightchannel(ctx):
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    temp = cursor.fetchone()
    if temp is None:
        return
    guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
    if int(log_channel_id) != int(ctx.channel.id):
        return False
    return True

def insert_values_into_table(dbname, tablename, values):
    if os.path.exists(dbname) is True:
        cursor.execute("INSERT INTO %s VALUES %s" % (tablename, tuple(values)))
        connection.commit()


def check_if_table_exists(dbname, tablename, tableheaders):
    try:
        cursor.execute("SELECT * FROM %s" % tablename)
    except sqlite3.OperationalError:
        create_table(dbname, tablename, tableheaders)


def create_new_entry(guild_id,
                     count=str(0),
                     number_of_resets=str(0),
                     last_user=str(0),
                     guild_message=str("{{{user}}} typed the wrong number"),
                     count_channel_id=str(''),
                     log_channel_id=str(''),
                     greedy_message=str("{{{user}}} was too greedy")):
    # dbOperations.put(['create',
    temp1 = [
        str(guild_id), str(count),
        str(number_of_resets),
        str(last_user),
        str(guild_message),
        str(count_channel_id),
        str(log_channel_id),
        str(greedy_message),
        str(0),
        str(0),
        str(0)]
    # ])
    
    cursor.execute("INSERT INTO count_info %s VALUES %s" % (tuple(count_info_headers), tuple(temp1)))
    connection.commit()
    return

def update_beertable(guild_id, user, owed_user, count, second_try=False, spend_beer=False):
    cursor.execute(f"SELECT * FROM beers WHERE guild_id = '{guild_id}' AND user = '{user}' AND owed_user = '{owed_user}'")
    temp = cursor.fetchone()
    if temp is None and spend_beer is True:
        return False, 0
    if temp is None:
        if second_try is True:
            cursor.execute(f"INSERT INTO beers (guild_id, user, owed_user, count) VALUES ('{guild_id}', '{owed_user}','{user}', '1')")
            connection.commit()
            return True, 1
        else:
            return update_beertable(guild_id, owed_user, user, -count, second_try=True) #Changed user and owed_user on purpose
        

    else:
        guild_id, user, owed_user, saved_count = temp
        if int(saved_count) + int(count) <= 0:
            cursor.execute(f"DELETE FROM beers WHERE  guild_id = '{guild_id}' AND user = '{user}' AND owed_user = '{owed_user}'")
            connection.commit()
            return True, 0
        cursor.execute(f"UPDATE beers SET count = count + {count} WHERE guild_id = '{guild_id}' AND user = '{user}' AND owed_user = '{owed_user}'")
        connection.commit()

        return True, int(saved_count) + int(count)

def update_stats(guild_id, user, correct_count = True, current_number = 1, drink = ""):
    # stat_headers = ['guild_id', 'user', 'count_correct', 'count_wrong', 'highest_valid_count', 'last_activity']
    
    cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{guild_id}' AND user = '{user}'")
    temp = cursor.fetchone()
    last_activity = datetime.now() 
    
    if temp is None:
        if drink == "":
            drink = "beer"
        if correct_count is True:
            cursor.execute(f"INSERT INTO stats (guild_id, user, count_correct, count_wrong, highest_valid_count, last_activity, drink) VALUES ('{guild_id}', '{user}', '1', '0', '{current_number}', '{last_activity}', '{drink}')")
        else:
            cursor.execute(f"INSERT INTO stats (guild_id, user, count_correct, count_wrong, highest_valid_count, last_activity, drink) VALUES ('{guild_id}', '{user}', '0', '1', '{current_number}', '{last_activity}', '{drink}')")
        connection.commit()
    else:
        highest_valid_count = temp[3]
        if current_number > int(highest_valid_count):
            highest_valid_count = str(current_number)
        if correct_count is True:
            cursor.execute(f"UPDATE stats SET count_correct = count_correct + 1, highest_valid_count = ?, last_activity = ? WHERE guild_id = '{guild_id}' AND user = '{user}'", (highest_valid_count, last_activity,))
        else:
            cursor.execute(f"UPDATE stats SET count_wrong = count_wrong + 1, last_activity = ? WHERE guild_id = '{guild_id}' AND user = '{user}'", (last_activity,))
        connection.commit()
        if drink != "":
            cursor.execute(f"UPDATE stats SET drink = '{drink}' WHERE guild_id = '{guild_id}' AND user = '{user}'")
            connection.commit()
    

def update_info(guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp,  table_name='count_info'):
    cursor.execute(f"UPDATE {table_name} SET guild_id = ?, current_count = ?, number_of_resets = ?, last_user = ?, message = ?, channel_id = ?, log_channel_id = ?, greedy_message = ?, record = ?, record_user = ?, record_timestamp = ? WHERE guild_id = '{guild_id}'", (guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message,record, record_user, record_timestamp, )) 
    connection.commit()
# -- End SQL Helper Functions --


# -- Begin Count Master Commands --
bot.remove_command('help')


@bot.command(name='help')
async def count_help(ctx):
    embed=Embed(title="Counting Bot", url="https://github.com/bloedboemmel/Discord-Counting-Bot",
     description="All commands",
    color=Color.purple())
    embed.set_thumbnail(url="https://pbs.twimg.com/media/D9x2dXnWsAgrqN7.jpg")
    message = f"`{PREFIX}counting_channel this_channel` to check the counting in this channel\n"
    message += f"`{PREFIX}counting_channel @other_channel` to set the counting channel to another one\n"
    message += f"`{PREFIX}log_channel this_channel` to set the log channel\n"
    embed.add_field(name="Admin-Commands", value=message, inline=False)
    message = f"`{PREFIX}server` - Shows stats for the server\n"
    message += f"`{PREFIX}highscore` - Shows the top 10 users with the most correctly counted numbers\n"
    message += f"`{PREFIX}highcount` - Shows the top 10 users with the highest counted numbers\n"
    message += f"`{PREFIX}user` - Shows stats for yourself\n"
    message += f"`{PREFIX}user @user` - Shows stats for different user\n"
    message += f"`{PREFIX}beer_count` - Gets the current beer-debt-table for this guild\n"
    message += f"`{PREFIX}beer_count me` - Gets the current beer-debt-table for this guild, where you are involved\n"
    message += f"`{PREFIX}spend_beer @user` - Notify the bot that the other user has paid for your beer and updates the debts\n"
    message += f"`{PREFIX}set_drink` - Your favorite drink is not beer? No problem, weirdo!\n"
    message += f"`{PREFIX}copy_data message_id` - Copies data from the original counting bot\n"
    message += f"`{PREFIX}delete_me` Deletes yourself from the stats"
    embed.add_field(name="User-Commands", value=message, inline=False)
    embed.set_footer(text= f"{PREFIX} help")
    await ctx.send(embed=embed)
    return


@bot.command(name='wrong_message')
@commands.has_permissions(administrator=True)
async def wrong_message(ctx, *args):
    _message = " ".join(args)
    if _message == 'help':
        response = """
        Set the message to be sent when someone types the wrong number
{{{user}}} will be replaced by the name of whoever typed the wrong number
        """
        await ctx.send(response)
        return
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()

    
    if test is None:
        create_new_entry(ctx.guild.id,
                         count_channel_id=ctx.channel.id,
                         log_channel_id=ctx.channel.id,
                         guild_message=_message)
    else:
        guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = test
        update_info(guild_id, count, number_of_resets, last_user, _message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp)
    return


@wrong_message.error
async def wrong_message_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need Admin Permissions to do that command')
    else:
        raise error



@bot.command(name='greedy_message')
@commands.has_permissions(administrator=True)
async def greedy_message(ctx, *args):
    _message = " ".join(args)
    if _message == 'help':
        response = """
        Set the message to be sent when someone types 2 messages in a row
{{{user}}} will be replaced by the name of whoever typed the 2 messages
        """
        await ctx.send(response)
        return
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    if test is None:
        create_new_entry(ctx.guild.id,
                         count_channel_id=ctx.channel.id,
                         log_channel_id=ctx.channel.id,
                         greedy_message=_message)
        
    else:
        guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, old_greedy_message, record, record_user, record_timestamp = test
        update_info(guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, _message, record, record_user, record_timestamp)
    return


@wrong_message.error
async def wrong_message_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need Admin rights to run that command')
    else:
        raise error


@bot.command(name='counting_channel')
@commands.has_permissions(administrator=True)
async def counting_channel(ctx, arg1):
    #print("counting_channel")
    channel_id = arg1
    if channel_id == 'help':
        response = f"""
            Set the id of the channel that you want to count in
use `{PREFIX}counting_channel this_channel` to use the channel that you are typing in
            """
        await ctx.send(response)
        return
    if channel_id == 'this_channel':
        channel_id = ctx.channel.id
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    
    
    if test is None:
        create_new_entry(ctx.guild.id,
                         count_channel_id=channel_id,
                         log_channel_id=channel_id,)
    else:
        guild_id, count, number_of_resets, last_user, guild_message, old_channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = test
        update_info(guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp)
    return


@counting_channel.error
async def counting_channel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need Admin rights to run that command')
    else:
        raise error

# temp: Hardcode solution bis Datenbank es unterstuetzt
PRO_ROLE_ID = 909158530039300126
PRO_ROLE_THRESHOLD = 50
# TODO: Admin-only Command um pro_role zu setzen
# TODO: Admin-only Command um pro_role_thresh zu setzen



@bot.command(name='log_channel')
@commands.has_permissions(administrator=True)
async def log_channel(ctx, arg1):
    #print("log_channel")
    channel_id = arg1
    if channel_id == 'help':
        response = f"""
            Set the id of the channel that you want to log mistakes too
use `{PREFIX}log_channel this_channel` to use the channel that you are typing in
            """
        await ctx.send(response)
        return
    if channel_id == 'this_channel':
        channel_id = ctx.channel.id
        
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    test = cursor.fetchone()
    if test is None:
        create_new_entry(ctx.guild.id,
                         count_channel_id=channel_id,
                         log_channel_id=channel_id,)
    else:
        guild_id, count, number_of_resets, last_user, guild_message, old_channel_id, old_log_channel_id, greedy_message, record, record_user, record_timestamp = test
        update_info(guild_id, count, number_of_resets, last_user, guild_message, old_channel_id, channel_id, greedy_message, record, record_user, record_timestamp)
    return


@counting_channel.error
async def counting_channel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You need the Admin rights to run that command')
    else:
        raise error

# -- End Count Master Commands --
# -- Begin Beer Count Commands --
@bot.command(name='beer_count', aliases=['drink_count', 'drinks'])
async def beer_count(ctx, args1 = ""):
    if not isrightchannel(ctx):
        return
    #print("beer_count")
    if args1 == 'me':
        cursor.execute(f"SELECT * FROM beers WHERE guild_id = '{ctx.guild.id}' AND user = '{ctx.message.author.id}' ORDER BY count DESC")
        db_results = cursor.fetchall()
    else:
        cursor.execute(f"SELECT * FROM beers WHERE guild_id = '{ctx.guild.id}' ORDER BY count DESC")
        db_results = cursor.fetchall()
    if db_results == [] and args1 == 'me':
        await ctx.send(f"{ctx.message.author.mention} has not won any drinks yet")
        return
    if db_results == []:
        await ctx.send("No one has won any drinks yet")
        return
    
    str = ""
    for result in db_results:
        guild_id, user1, user2, count = result
        if user1 == '' or user2 == '':
            continue
        cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}' AND user = '{user1}'")
        temp = cursor.fetchone()
        if temp is None:
            drink = "beer"
        else:
            guild_id, user, count_correct, count_wrong, highest_valid_count, last_activity, drink = temp

        str +=  f"<@{user2}> ows <@{user1}> {count} {drink}s\n"
    
    if str != "":
        embed = Embed(title=f"Drink Table for {ctx.guild.name}", description=str, color=Color.dark_gold())
        embed.set_footer(text=f"{PREFIX}help")
        await ctx.send(embed=embed)
    

@bot.command(name= 'spend_beer')
async def spend_beer(ctx, args1 = ""):
    if not isrightchannel(ctx):
        return
    owing_user = args1[args1.find("<@&")+3:args1.find(">")]
    owing_user = int(owing_user.replace("!", ""))
    if args1 == 'help' or args1 == "" or owing_user == "":
        await ctx.send(f"""
        `{PREFIX}spend_beer @user` to register a done forfeit. Make sure to really tag the person
        """)
        return
    if args1 == 'me':
        await ctx.send("Funny you! I won't count your own drinkung habits")
        return
    user = ctx.message.author.id
    #update_beertable(guild_id, user, owed_user, count, second_try=False, spend_beer=False):
   
    Changed, new_count = update_beertable(ctx.guild.id, user, owing_user, -1, second_try=False, spend_beer=True)
    if Changed == False:
        await ctx.send(f"<@{owing_user}> didn't owe you a beer, but it's still great you met up")
        return
    if new_count == 0:
        await ctx.send(f"<@{owing_user}> and you are now all made up!")
        return
    await ctx.send(f"Thanks for the info!, <@{owing_user}> now owes <@{user}> {new_count} beers")

@bot.command(name='server')
async def server(ctx):
    if not isrightchannel(ctx):
        return
    #print("server")
    # count_info_headers = ['guild_id', 'current_count', 'number_of_resets', 'last_user', 'message', 'channel_id', 'log_channel_id', 'greedy_message', 'record', 'record_user', 'record_timestamp']
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % ctx.guild.id)
    temp = cursor.fetchone()
    if temp is None:
        return
    
    guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
    timestr = time_since(record_timestamp)
    if last_user == '':
        last_user = 'None'
    else:
        last_user = f"<@{last_user}>"
    message = f"`Current count:` {count}\n"
    message += f"`Last counted by` {last_user}\n"
    message += f"`High Score:` {record} ({timestr})\n"
    message += f"`Counted by` <@{record_user}>\n"
    embed=Embed(title=f"Stats for {ctx.guild.name}", 
                description=message)    
    embed.set_footer(text=f"{PREFIX}help")
    await ctx.send(embed=embed)
    
@bot.command(name='user')
async def user(ctx, arg1 = ""):
    if not isrightchannel(ctx):
        return
    if arg1 == "":
        user = ctx.message.author.id
        username = ctx.message.author.name
        message =""
        title = f"Stats for {username}"
    else:
        user = arg1[arg1.find("<@&")+3:arg1.find(">")]
        user = int(user.replace("!", ""))
        title = "User-Stats"
        message = f"Are you even there? <@{user}>\n"
    cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}' AND user = '{user}'")
    temp = cursor.fetchone()
    if temp is None:
        if arg1 == "":
            await ctx.send(f"<@{user}, you should try counting first!")
        else:
            await ctx.send(f"<@{user}> has to learn counting first and is revisiting school")
        return
    else:
     #stat_headers = ['user', 'count_correct', 'count_wrong', 'highest_valid_count', 'last_activity']
        guild_id, user, count_correct, count_wrong, highest_valid_count, last_activity, drink = temp
        percent_correct = round(int(count_correct) / (int(count_correct) + int(count_wrong)) * 100, 2)
        message += f"`Count Correct:` {count_correct}\n"
        message += f"`Count Wrong:` {count_wrong}\n"
        message += f"`Percentage Correct:` {percent_correct} %\n"
        message += f"`Highest Valid Count:` {highest_valid_count}\n"
        message += f"`Last Activity:` {time_since(last_activity)}\n"
        message += f"`Favorite Drink:` {drink}\n"
        embed = Embed(title=title, 
                      description=message)
        embed.set_footer(text=f"{PREFIX}help")
        await ctx.send(embed=embed)
       

    
@bot.command(name='highscore')
async def highscore(ctx):
    if not isrightchannel(ctx):
        return
    #print("highscore")
    cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}'  ORDER BY count_correct DESC")
    db_results = cursor.fetchall()
    i = 1
    message = ""
    for result in db_results:
        guild_id, user1, count_correct, count_wrong, highest_valid_count, last_activity, drink = result
        if user1 == '':
            continue
        message += f"<@{user1}>: {count_correct}\n"
        if i == 10:
            break
        i += 1
    if i > 1:
        embed = Embed(title=f"Top 10 for {ctx.guild.name}", 
                      description=message, color=Color.green())
        embed.set_footer(text=f"{PREFIX}help")
        await ctx.send(embed=embed)

@bot.command(name='highcount')
async def highcount(ctx):
    if not isrightchannel(ctx):
        return
    cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}'  ORDER BY highest_valid_count DESC")
    db_results = cursor.fetchall()
    i = 1
    message = ""
    for result in db_results:
        guild_id, user1, count_correct, count_wrong, highest_valid_count, last_activity, drink = result
        if user1 == '':
            continue
        message += f"<@{user1}>: {highest_valid_count}\n"
        if i == 10:
            break
        i += 1
    if i > 1:
        embed = Embed(title=f"10 highest Counters for {ctx.guild.name}", 
                      description=message, color=Color.green())
        embed.set_footer(text=f"{PREFIX}help")
        await ctx.send(embed=embed)

@bot.command(name='set_drink')
async def set_drink(ctx, arg1 = ""):
    if not isrightchannel(ctx):
        return
    if arg1 == "":
        await ctx.send("Please specify a drink")
        return
    cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}' AND user = '{ctx.author.id}'")
    temp = cursor.fetchone()
    if temp is None:
        await ctx.send("You have to count first!")
        return
    else:
        cursor.execute(f"UPDATE stats SET drink = '{arg1}' WHERE guild_id = '{ctx.guild.id}' AND user = '{ctx.author.id}'")
        connection.commit()
        await ctx.send(f"{ctx.author.name}'s favorite drink is now {arg1}")

@bot.command(name='delete_me')
async def delete_me(ctx):
    if not isrightchannel(ctx):
        return
    cursor.execute(f"DELETE FROM stats WHERE guild_id = '{ctx.guild.id}' AND user = '{ctx.author.id}'")
    connection.commit()
    await ctx.message.add_reaction("😞")
    await ctx.send(f"{ctx.author.name} has been deleted from the database")

@bot.command(name='copy_data')
async def copy_data(ctx, arg1 = ""):
    if not isrightchannel(ctx):
        return
    if arg1 == "":
        await ctx.send("Please enter a message id")
        return
    cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}' AND user = '{ctx.author.id}'")
    temp = cursor.fetchone()
    if temp is not None:
        await ctx.send(f"This works only if you delete yourself first with `{PREFIX}delete_me`")
        return
    counting_bot_mssg = await ctx.channel.fetch_message(int(arg1))
    try: 
        counting_bot_mssg_content = counting_bot_mssg.content
        username = counting_bot_mssg.embeds[0].title
        if username != ctx.author.name + "#" + ctx.author.discriminator:
            await ctx.send("Sneaky you! These stats aren't yours!")
            return
        value = counting_bot_mssg.embeds[0].fields[1].value.split("\n")
        # get number from "Total correct: **2**"
        total_correct = int(value[1].split("**")[1].replace("**", ""))
        # get number from "Total wrong: **1**"
        total_wrong = int(value[2].split("**")[1].replace("**", ""))
        # get number from 'Highest Valid Count: **1 (24s ago)**'
        highest_valid_count = int(value[4].split("**")[1].split(" ")[0])
        
        # Insert data into database
        last_activity = datetime.now()
        cursor.execute(f"INSERT INTO stats (guild_id, user, count_correct, count_wrong, highest_valid_count, last_activity, drink) VALUES ('{ctx.guild.id}', '{ctx.author.id}', '{total_correct}', '{total_wrong}', '{highest_valid_count}', '{last_activity}', 'beer')")
        connection.commit()
        await ctx.send(f"{ctx.author.name}, welcome to the Party\n<@{counting_bot_mssg.author.id}> is too stupid to save your favorite drink. Pls set it with `{PREFIX}set_drink`")
    except:
        embed = Embed(title=f"Please help", url="https://github.com/bloedboemmel/Discord-Counting-Bot",
            description="Something went utterly wrong! But a Nerd is fixing it right away. Are you yourself a nerd? Just help at the github-repo!", color=Color.red())
        embed.set_footer(text=f"{PREFIX}help")
        await ctx.send(embed=embed)
        

# -- Begin Edit Detection --
## doesn't work yet...........
@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        cursor.execute(f"SELECT * FROM count_info WHERE guild_id = '{after.guild.id}'")
        temp = cursor.fetchone()
        if temp == None:
            return
        try:
            changed_count, trash = before.content.split(' ', 1)
        except ValueError:
            changed_count = before.content
        try:     
            changed_count = int(changed_count)
        except ValueError:
            return
        
        guild_id, old_count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
        if int(last_user) != int(after.author.id) or changed_count != int(old_count):
            return
        await after.add_reaction('😡')
        await after.reply(f"Wait, <@{after.author.id}> edited this message. Next number is {str(int(old_count) +1)}")

@bot.event
async def on_message_delete(message):
    cursor.execute(f"SELECT * FROM count_info WHERE guild_id = '{message.guild.id}'")
    temp = cursor.fetchone()
    if temp == None:
        return
    try:
        changed_count, trash = message.content.split(' ', 1)
    except ValueError:
        changed_count = message.content
    try:     
        changed_count = int(changed_count)
    except ValueError:
        return
    
    guild_id, old_count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
    if int(last_user) != int(message.author.id) or changed_count != int(old_count):
        return
    await message.channel.send(f"Hold on, <@{message.author.id}> deleted an important message. Next number is {int(old_count) +1}")

# -- Begin counting detection --
@bot.event
async def on_message(_message):
    ctx = await bot.get_context(_message)
    if ctx.message.author.bot:
        return
    if str(_message.content).startswith(str(PREFIX)):
        await bot.invoke(ctx)
        return
    try:
        current_count, trash = _message.content.split(' ', 1)
    except ValueError:
        current_count = _message.content
    try:     
        current_count = int(current_count)
    except ValueError:
        return
    cursor.execute("SELECT * FROM count_info WHERE guild_id = '%s'" % _message.guild.id)
    temp = cursor.fetchone()
    if temp is None:
        return
    else:
        #print(temp[5])
        #print(_message.channel.id)
        if str(temp[5]) != str(ctx.channel.id):
            return
        else:
            old_count = int(temp[1])
            if str(ctx.message.author.id) == str(temp[3]):
                #print("greedy")
                guild_id, old_count, old_number_of_resets, old_last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
                count = str(0)
                number_of_resets = str(int(old_number_of_resets) + 1)
                last_user = str('')
                update_info(guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp)

                await ctx.send(str(greedy_message).replace("{{{user}}}", '<@%s>' % str(ctx.message.author.id)))
                
                
                await ctx.message.add_reaction('🇸')
                await ctx.message.add_reaction('🇭')
                await ctx.message.add_reaction('🇦')
                await ctx.message.add_reaction('🇲')
                await ctx.message.add_reaction('🇪')
                channel = bot.get_channel(int(log_channel_id))
                await channel.send('<@%s> lost the count when it was at %s' % (ctx.message.author.id, old_count))
                
                return
            if old_count + 1 != current_count:
                guild_id, old_count, old_number_of_resets, old_last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
                count = str(0)
                number_of_resets = str(int(old_number_of_resets) + 1)
                last_user = str('')
                beers_last_user = str(ctx.message.author.id)
                update_info(guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp)

                await ctx.send(str(temp[4]).replace("{{{user}}}", '<@%s>' % str(ctx.message.author.id)))
                
                channel = bot.get_channel(int(temp[6]))
                
                await ctx.message.add_reaction('❌')
                if old_count != 0 and old_last_user != '':
                    await channel.send('<@%s> lost the count when it was at %s and has to give <@%s> a beer!' % (ctx.message.author.id, old_count, old_last_user))
                    update_beertable(guild_id, old_last_user, beers_last_user,  +1)
                
                    
                update_stats(guild_id, beers_last_user, correct_count=False)
                # auf PRO_ROLE prüfen
                cursor.execute(f"SELECT * FROM stats WHERE guild_id = '{ctx.guild.id}' AND user = '{ctx.message.author.id}'")
                temp = cursor.fetchone()
                if temp is None:
                    # hat wohl noch nie gezaehlt
                    return
                else:
                    guild_id, msg_user, count_correct, count_wrong, highest_valid_count, last_activity, drink = temp
                    if count_correct >= PRO_ROLE_THRESHOLD:
                        role = get(bot.get_guild(ctx.guild.id).roles, id=PRO_ROLE_ID)
                        await msg_user.add_roles(role)
                return
            if old_count + 1 == current_count:
                guild_id, old_count, number_of_resets, old_last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp = temp
                
                count = str(current_count)
                last_user = str(ctx.message.author.id)
                if int(record) < current_count:
                    record = count
                    record_user = str(ctx.message.author.id)
                    record_timestamp = datetime.now()
                    await ctx.message.add_reaction('☑️')
                else:
                    await ctx.message.add_reaction('✅')

                update_info(guild_id, count, number_of_resets, last_user, guild_message, channel_id, log_channel_id, greedy_message, record, record_user, record_timestamp)
                update_stats(guild_id, ctx.message.author.id, current_number= current_count)
                
                return
            return


# -- Begin Initialization code --
check_if_table_exists(DbName, 'count_info', count_info_headers)
check_if_table_exists(DbName, f'stats', stat_headers)
check_if_table_exists(DbName, f'beers', beer_headers)
bot.run(TOKEN)
# -- End Initialization code --
>>>>>>> Stashed changes
