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
