# 1174448383394590790
import config
import random
import discord # Подключаем библиотеку
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import asyncio
import re

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()  # Синхронизация слэш-команд с Discord


# Отправка сообщения в канал от лица бота
@bot.tree.command(name="сообщение_в_канал", description='Отправка сообщения в канал')
@app_commands.describe(
    url='Ссылка на канал',
    players='Список игроков для пинга',
    message='Текст сообщения'
)
async def message_send(interaction: discord.Interaction, url: str, players: str, message: str):
    # Деферим ответ, чтобы сообщить пользователю, что бот работает
    await interaction.response.defer()
    user_id = interaction.user.id
    if user_id not in config.PLAYERS_ADMIN_ID:
        await interaction.followup.send(f"Ну и куда мы лезем?")
    else:
        # Обрабатываем переносы строк
        message = message.replace("\\n", "\n")

        # Получаем текст сообщения, который идет после ссылки на канал
        message_text = message

        # Пытаемся извлечь ID канала из ссылки
        channel_id_match = re.search(r"discord(?:app)?\.com/channels/(\d+)/(\d+)", url)

        if channel_id_match:
            guild_id = int(channel_id_match.group(1))  # ID сервера
            channel_id = int(channel_id_match.group(2))  # ID канала

            # Находим сервер
            guild = bot.get_guild(guild_id)
            if guild:
                # Находим канал по ID
                channel = guild.get_channel(channel_id)
                if channel:
                    # Добавляем пинг игроков в конец сообщения
                    if players != '-':
                        message_text += '\n'
                        players = players.split()
                        for player in players:
                            if player not in ['everyone', 'here']:
                                user = discord.utils.get(guild.members, name=player)
                                if user:
                                    player_id = user.id
                                    message_text += f"<@{player_id}> "
                            else:
                                message_text += f"@{player} "
                    # Отправляем сообщение в канал
                    await channel.send(message_text)
                    await interaction.followup.send(f"Сообщение отправлено в канал {channel.mention}.")
                else:
                    await interaction.followup.send("Не удалось найти канал с таким ID.")
            else:
                await interaction.followup.send("Не удалось найти сервер с таким ID.")
        else:
            await interaction.followup.send("Некорректная ссылка на канал.")


# Отображение меню таверны
async def generate_menu_and_respond(interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send("О, ты с Риверфорджа? Ну и славно. Я там знаю одного стража, он тебе "
                                                "быстро объяснит, почему НЕ НАДО НАПИСЫВАТЬ НЕЗНАКОМЫМ БОТАМ!")
    elif interaction.channel.id in config.TAVERN_ID:
        # Список имен файлов картинок
        images = [
            config.MENU_PATH + r'\Меню1.jpg',
            config.MENU_PATH + r'\Меню2.jpg',
        ]

        # Создайте список файлов
        files = [discord.File(image) for image in images]

        await interaction.followup.send(files=files)
    elif interaction.guild_id in config.GUILD_ID:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***Люди, что находились рядом, посмотрели на <@{user_id}> как на '
                                                f'идиота. Не каждый день встретишь умника, что пытается попросить '
                                                f'меню в случайном месте, а не в '
                                                f'https://discord.com/channels/{interaction.guild_id}/{config.TAVERN_ID[config.GUILD_ID.index(interaction.guild_id)]}'
                                                f'***')
    else:
        await interaction.followup.send(f'Так... А сюда я как попал?')


# Отображение меню таверны
@bot.tree.command(name='меню')
async def menu_send(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_menu_and_respond(interaction))  # Создаем фоновую задачу



# Блюда-----------------------------------------------------------------------------------------------------------------
# Сэндвич с мясом бубуйвола (/бубуйвол)
async def generate_bubuivol_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Сэндвич с мясом бубуйвола.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='бубуйвол')
async def bubuivol(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_bubuivol_and_respond(interaction))  # Создаем фоновую задачу


# Суп из семи видов мяса (/суп-семь)
async def generate_soup_seven_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Суп из семи видов мяса.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='суп-семь')
async def soup_seven(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_soup_seven_and_respond(interaction))  # Создаем фоновую задачу


# Стейк из оленины под голубичным соусом (/стейк-оленина)
async def generate_deer_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Стейк из оленины под голубичным соусом.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='стейк-оленина')
async def deer(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_deer_and_respond(interaction))  # Создаем фоновую задачу


# Овсяная каша (/каша)
async def generate_porridge_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Овсяная каша.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='каша')
async def porridge(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_porridge_and_respond(interaction))  # Создаем фоновую задачу


# Овсяная каша с ягодами и орехами (/каша-доп)
async def generate_porridge_dop_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Овсяная каша с ягодами и орехами.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='каша-доп')
async def porridge_dop(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_porridge_dop_and_respond(interaction))  # Создаем фоновую задачу


# Сырный крем суп (/крем-суп)
async def generate_cream_soup_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Сырный крем суп.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='крем-суп')
async def cream_soup(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_cream_soup_and_respond(interaction))  # Создаем фоновую задачу


# Сэндвич из копчёного мяса доу-доу (/доу-доу)
async def generate_doe_doe_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Сэндвич из копчёного мяса доу-доу.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='доу-доу')
async def doe_doe(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_doe_doe_and_respond(interaction))  # Создаем фоновую задачу


# Суп из весёлых грибов (/суп-грибной)
async def generate_mushroom_soup_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Суп из весёлых грибов.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='суп-грибной')
async def mushroom_soup(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_mushroom_soup_and_respond(interaction))  # Создаем фоновую задачу


# Драконий стейк (/стейк-дракон)
async def generate_dragon_steak_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Драконий стейк.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='стейк-дракон')
async def dragon_steak(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_dragon_steak_and_respond(interaction))  # Создаем фоновую задачу


# Салат с мясом лазурного краба (/салат-краб)
async def generate_crab_salad_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Салат с мясом лазурного краба.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='салат-краб')
async def crab_salad(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_crab_salad_and_respond(interaction))  # Создаем фоновую задачу


# Пельмени из щуки с салом (/пельмени)
async def generate_dumplings_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Пельмени из щуки с салом.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='пельмени')
async def dumplings(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_dumplings_and_respond(interaction))  # Создаем фоновую задачу


# Кровяная колбаса с салом (/колбаса)
async def generate_sausage_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DISHES_PATH + r'\Кровяная колбаса с салом.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='колбаса')
async def sausage(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_sausage_and_respond(interaction))  # Создаем фоновую задачу


# Напитки---------------------------------------------------------------------------------------------------------------
# Зеленый чай (/зеленый-чай)
async def generate_green_tea_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Зеленый чай.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='зеленый-чай')
async def green_tea(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_green_tea_and_respond(interaction))  # Создаем фоновую задачу


# Черный чай (/черный-чай)
async def generate_black_tea_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Черный чай.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='черный-чай')
async def black_tea(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_black_tea_and_respond(interaction))  # Создаем фоновую задачу


# Молочный коктейль (/коктейль)
async def generate_cocktail_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Молочный коктейль.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='коктейль')
async def cocktail(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_cocktail_and_respond(interaction))  # Создаем фоновую задачу


# Горячий шоколад (/горячий-шоколад)
async def generate_hot_chocolate_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Горячий шоколад.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='горячий-шоколад')
async def hot_chocolate(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_hot_chocolate_and_respond(interaction))  # Создаем фоновую задачу


# СВЕТлое пиво (/свет)
async def generate_light_beer_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\СВЕТлое пиво.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='свет')
async def light_beer(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_light_beer_and_respond(interaction))  # Создаем фоновую задачу


# ТЕМНое пиво (/тьма)
async def generate_dark_beer_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\ТЕМНое пиво.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='тьма')
async def dark_beer(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_dark_beer_and_respond(interaction))  # Создаем фоновую задачу


# Грушевый кальвадос (/груша)
async def generate_pear_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Грушевый кальвадос.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='груша')
async def pear(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_pear_and_respond(interaction))  # Создаем фоновую задачу


# Поцелуй дриады (/дриада)
async def generate_dryad_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Поцелуй дриады.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='дриада')
async def dryad(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_dryad_and_respond(interaction))  # Создаем фоновую задачу


# Золотой грааль (/грааль)
async def generate_grail_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Золотой грааль.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='грааль')
async def grail(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_grail_and_respond(interaction))  # Создаем фоновую задачу


# Лимонный твист (/твист)
async def generate_limon_twist_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DRINK_PATH + r'\Лимонный твист.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках поднос с напитком, после чего поставил его перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам времопровождения!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='твист')
async def limon_twist(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_limon_twist_and_respond(interaction))  # Создаем фоновую задачу


# Десерты---------------------------------------------------------------------------------------------------------------
# Драконий фрукт (/дракон)
async def generate_dragon_fruit_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Драконий фрукт.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='дракон')
async def dragon_fruit(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_dragon_fruit_and_respond(interaction))  # Создаем фоновую задачу


# Лунная апельсиновая дыня (/дыня)
async def generate_melon_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Лунная апельсиновая дыня.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='дыня')
async def melon(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_melon_and_respond(interaction))  # Создаем фоновую задачу


# Космическая звездочка (/звездочка)
async def generate_star_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Космическая звездочка.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='звездочка')
async def star(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_star_and_respond(interaction))  # Создаем фоновую задачу


# Лимонный сорбет (/сорбет)
async def generate_sorbet_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Лимонный сорбет.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='сорбет')
async def sorbet(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_sorbet_and_respond(interaction))  # Создаем фоновую задачу


# Единорогова блевота (/единорог)
async def generate_unicorn_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Единорогова блевота.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='единорог')
async def unicorn(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_unicorn_and_respond(interaction))  # Создаем фоновую задачу


# Брауни (/брауни)
async def generate_brownie_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Брауни.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='брауни')
async def brownie(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_brownie_and_respond(interaction))  # Создаем фоновую задачу


# Яблочное суфле с грушей (/суфле)
async def generate_souffle_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Яблочное суфле с грушей.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='суфле')
async def souffle(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_souffle_and_respond(interaction))  # Создаем фоновую задачу


# Желе из медового пива (/желе)
async def generate_jelly_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Желе из медового пива.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='желе')
async def jelly(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_jelly_and_respond(interaction))  # Создаем фоновую задачу


# Синяя бездна: небесный вкус (/бездна)
async def generate_abyss_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Синяя бездна небесный вкус.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='бездна')
async def abyss(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_abyss_and_respond(interaction))  # Создаем фоновую задачу


# Красный рубин: вкус страсти (/рубин)
async def generate_ruby_and_respond(interaction: discord.Interaction):
    # Проверяем, является ли сообщение личным сообщением
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.followup.send(config.DMCHANNEL_MSG)
    elif interaction.channel.id in config.TAVERN_ID:
        user_id = interaction.user.id  # ID пользователя
        file_menu = discord.File(config.DESSERT_PATH + r'\Красный рубин вкус страсти.jpg', filename="image.jpg")
        await interaction.followup.send('***Подбижал мальчишка, неся в руках заказ, после чего поставил тарелку перед '
                                                f'<@{user_id}> и протораторил***\n- Прошу, приятного вам аппетита!\n'
                                                '***После чего сразу убежал дальше работать***', file=file_menu)
    else:
        user_id = interaction.user.id  # ID пользователя
        await interaction.followup.send(f'***<@{user_id}> получил от воображаемого официанта свой воображаемый '
                                                f'заказ... А вот если бы заказ был сделан в нужном месте '
                                                f'то тут не попахивало бы дуркой... Или запрещеннымы веществами... '
                                                f'***')


@bot.tree.command(name='рубин')
async def ruby(interaction: discord.Interaction):
    await interaction.response.defer()  # Откладываем ответ
    asyncio.create_task(generate_ruby_and_respond(interaction))  # Создаем фоновую задачу


bot.run(config.TOKEN)