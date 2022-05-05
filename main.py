import vkbottle
import os
import tracemalloc
import connection_for_db
import time
import random

from config import token
from vkbottle import BaseStateGroup, Keyboard, OpenLink,Text, GroupEventType, GroupTypes, KeyboardButtonColor, EMPTY_KEYBOARD, VKAPIError
from vkbottle.bot import Bot, Message
from list import list_words

tracemalloc.start()

bot = Bot(token=token)

class MenuState(BaseStateGroup):
    state_start = 1
    state_menu = 2
    state_amba = 3
    state_event = 4
    state_city = 5
    state_city_db = 6
    state_number = 7
    state_number_db = 8
    state_all_event = 9
    state_category = 10
    state_online = 11
    state_offline = 12
    state_type = 13
    state_type_db = 14
    state_reg_1 = 15
    state_reg_2 = 16
    state_reg_final = 17
    state_all_guid = 18
    state_reg_final_all = 19
    state_online_offline = 20


async def check_month(id):
    current_month = time.strftime('%m')
    tempt_ = await connection_for_db.bd_check_id(id)
    try:
        tempt_id = int(str(tempt_).replace("(", '').replace(")", '').replace(",", ''))
        if int(id) == tempt_id:
            return 1
        else:
            return 0
    except:
        if current_month < '06' or current_month > '08':
            return 1
        else:
            return 0

async def number():
    current_year = time.strftime('%Y')
    first_number = 2018
    current_number = int(current_year)-first_number
    return int(current_number)



#----------------JOIN GROUP
# @bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
# async def group_join_handler(event: GroupTypes.GroupJoin):
#     try:
#         await bot.api.messages.send(
#             peer_id=event.object.user_id,
#             message="👋Привет! \n \n Говорят, что в этой группе самые лучшие люди, которые стали амбассадорами ВК! \n \n Пришли мне любое сообщение и мы начнем)",
#             random_id=0,
#             keyboard=(EMPTY_KEYBOARD)
#         )
#     except VKAPIError(901):
#         pass



#----------------START
@bot.on.private_message(state = None)
async def start_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        user = await bot.api.users.get(message.from_id)
        id = user[0].id
        first = user[0].first_name
        last =user[0].last_name
        name = first + ' ' + last
        name_gem = '🔹' + first + ' ' + last
        link_name = '@' + 'id' + str(id) + '(' + name_gem + ')'
        result = await message.ctx_api.users.get(message.from_id, fields=["bdate"])
        bdate = str(result[0].bdate)
        city = await bot.api.users.get(message.from_id, fields=["city"])
        city_1 = str(city[0].city).replace("=", '').replace("'", '').partition("e")[2]
        f = 'https://vk.com/id'
        link = f + str(id)
        num = await number()
        temp = await connection_for_db.bd_registration(id, name, link_name, link, num, bdate, city_1)
        if (temp == 1):
            await message.answer(
                f"👋Привет, {user[0].first_name}! \n \n Ты попал в группу амбассадоров! Я буду помогать тебе с амбассадорством.\n \n Прежде чем пройти дальше, давай закончим регистрацию",
                keyboard=(
                    Keyboard()
                        .add(Text("Закончить регистрацию", {"cmd": "next_reg"}))
                        .get_json()
                ),
            )
        elif (temp == 0):
            await message.answer(
                "Бот был перезагружен, но уже снова все работает",
                keyboard = (
                              Keyboard()
                                  .add(Text("Меню", {"cmd": "next_1"}),color=KeyboardButtonColor.POSITIVE)
                                  .get_json()
                          ),
            )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_start)



@bot.on.private_message(state=[
    MenuState.state_start],
    payload={"cmd": "next_reg"})
async def city_handler(message: Message):
    await message.answer(
         f"Вводи данные аккуратно. Исправить их будет нельзя! \n \n Введи город, в которым ты являешься амбассадором",
        keyboard=(EMPTY_KEYBOARD))
    await bot.state_dispenser.set(message.peer_id, MenuState.state_reg_1)

@bot.on.private_message(state =
    MenuState.state_reg_1,
    text='<msg>')
async def start_handler(message: Message, msg):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    temp = await connection_for_db.bd_registration_continue(id, msg)
    if (temp == 1):
        await message.answer(
            f"Город записан! \n \n Теперь введи название своего университета",
            keyboard=(EMPTY_KEYBOARD))
    else:
        await message.answer(
            f"Попробуй еще раз")
    await bot.state_dispenser.set(message.peer_id, MenuState.state_reg_2)

@bot.on.private_message(state =
    MenuState.state_reg_2,
    text='<msg>')
async def start_handler(message: Message, msg):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    temp = await connection_for_db.bd_registration_continue_2(id, msg)
    if (temp == 1):
        await message.answer(
            f"Университет записан! \n \n Теперь введи информацию о себе, чтобы другие амбассадоры могли понимать, что ты можешь сделать. Например: Я дизайнер, работаю в фотошопе и могу нарисовать все что угодно",)
    else:
        await message.answer(
            f"Попробуй еще раз")
    await bot.state_dispenser.set(message.peer_id, MenuState.state_reg_final)


@bot.on.private_message(state = [
    MenuState.state_reg_final],
    text='<msg>')
async def start_handler(message: Message, msg):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    temp = await connection_for_db.bd_registration_continue_info(id, msg)
    if (temp == 1):
        await message.answer(
            f"Информация успешно записана! \n \n Регистрация оконченна",
            keyboard=(
                Keyboard()
                    .add(Text("Амбассадор ВК, Welcome", {"cmd": "final_reg"}))
                    .get_json()
            ),)
    else:
        await message.answer(
            f"Попробуй еще раз")
    await bot.state_dispenser.set(message.peer_id, MenuState.state_reg_final_all)



#----------------MENU
@bot.on.private_message(state = [
    MenuState.state_start,
    MenuState.state_reg_final_all,
    MenuState.state_amba,
    MenuState.state_event,
    MenuState.state_city,
    MenuState.state_city_db,
    MenuState.state_number,
    MenuState.state_number_db,
    MenuState.state_category,
    MenuState.state_type,
    MenuState.state_type_db,
    MenuState.state_all_event,
    MenuState.state_online,
    MenuState.state_offline,
    MenuState.state_online_offline,
    MenuState.state_all_guid],
    payload=[{"cmd": "back_menu"},{"cmd": "back_1"},{"cmd": "next_1"}, {"cmd": "final_reg"}]) #Много статусов
async def menu_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Menu'
        await bd_handler(message, text)
        list = random.choice(list_words)
        await message.answer(
            f"🔻–––––––––МЕНЮ–––––––––🔻 \n \n {list} \n \n ➤ Вкладка амбассадоры: \n Здесь хранится информация о \n всех амбассадорах.\n \n ➤ Вкладка мероприятия:\n Здесь хранится информация о \n мероприятиях и о гайдах.\n \n 🔺––––––––––––––––––––––––🔺",
            keyboard=(
                Keyboard()
                .add(Text("Амбассадоры", {"cmd": "ambo"}))
                .add(Text("Мероприятия", {"cmd": "event"}))
                .row()
                .add(OpenLink("https://vk.com/app6013442_-207473867?form_id=1#form_id=1", "Помощь"), color=KeyboardButtonColor.PRIMARY)
                .get_json()
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_menu)



#----------------AMBA
@bot.on.private_message(state=[
    MenuState.state_menu,
    MenuState.state_city,
    MenuState.state_number,
    MenuState.state_number_db,
    MenuState.state_city_db],
    payload=[{"cmd": "ambo"},{"cmd": "back_3"}, {"cmd": "back_1"}, {"cmd": "back_number"},{"cmd": "back_city"}])
async def amba_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Ambassador'
        await bd_handler(message, text)
        await message.answer(
             "Это раздел с амбассадорами. Здесь ты можешь узнать о всех амбассадорах, посмотреть кто находится в твоем городе и найти помощников на мероприятия!",
             keyboard=(
                Keyboard()
                .add(Text("Набор", {"cmd": "number"}))
                .add(Text("Город", {"cmd": "city"}))
                .row()
                .add(Text("Назад", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_amba)



#----------------CITY
@bot.on.private_message(state=[
    MenuState.state_amba],
    payload={"cmd": "city"})
async def city_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'City'
        await bd_handler(message, text)
        await message.answer(
             "Введи город",
             keyboard=(
                Keyboard()
                .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                .add(Text("Назад", {"cmd": "back_city"}),color=KeyboardButtonColor.PRIMARY)
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_city)


@bot.on.private_message(state=[
    MenuState.state_city,
    MenuState.state_city_db],
    text="<msg>")
async def city_item_handler(message: Message, msg):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        table_city = await connection_for_db.bd_city(msg)
        if (table_city != 9999999999):
            await message.answer(
                f"{table_city}",
             keyboard=(
                Keyboard()
                .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                .add(Text("Назад", {"cmd": "back_city"}),color=KeyboardButtonColor.PRIMARY)
            ),)
        else:
            await message.answer(
                "Похоже амбассадора из такого города нет :(")
        await bot.state_dispenser.set(message.peer_id, MenuState.state_city_db)



#----------------NUMBER
@bot.on.private_message(state=[
    MenuState.state_amba],
    payload={"cmd": "number"})
async def number_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Number'
        await bd_handler(message, text)
        await message.answer(
             "Введи число набора",
             keyboard=(
                Keyboard()
                .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                .add(Text("Назад", {"cmd": "back_number"}),color=KeyboardButtonColor.PRIMARY)
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_number)


@bot.on.private_message(state=[
    MenuState.state_number,
    MenuState.state_number_db],
    text="<msg>")
async def number_item_handler(message: Message, msg):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        try:
            if (type(int(msg)) == int):
                table_number = await connection_for_db.bd_number_check(msg)
                if (table_number != 9999999999):
                    await message.answer(
                        f"{table_number}",
                        keyboard = (
                            Keyboard()
                               .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                               .add(Text("Назад", {"cmd": "back_number"}),color=KeyboardButtonColor.PRIMARY)
                                   ),)
                else:
                    await message.answer(
                        "Увы, ничего не найдено")
        except:
            await message.answer(
            "Ой, похоже ты ввел не число :(")
        await bot.state_dispenser.set(message.peer_id, MenuState.state_number_db)



#----------------EVENT
@bot.on.private_message(state=[
    MenuState.state_menu,
    MenuState.state_category,
    MenuState.state_all_event,
    MenuState.state_all_guid],
    payload=[{"cmd": "event"},{"cmd": "back_1"},{"cmd": "back_all"},{"cmd": "back_category"},{"cmd": "back_all_g"}])
async def event_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Event'
        await bd_handler(message, text)
        await message.answer(
             "Это раздел с мероприятиями. Если у тебя закончались идеи, что проводить, то смело бери их отсюда. У каждого мероприятия есть свой гайд :3",
             keyboard=(
                Keyboard()
                .add(Text("Все мероприятия", {"cmd": "all_event"}))
                .add(Text("Категория", {"cmd": "category"}))
                .row()
                .add(Text("Все гайды", {"cmd": "all_guid"}))
                .row()
                .add(Text("Назад", {"cmd": "back_1"}),color=KeyboardButtonColor.PRIMARY)
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_event)



#----------------CATEGORY
@bot.on.private_message(state=[
    MenuState.state_event,
    MenuState.state_type,
    MenuState.state_online,
    MenuState.state_offline,
MenuState.state_online_offline,
    MenuState.state_type_db],
    payload=[{"cmd": "category"}, {"cmd": "back_1"}, {"cmd": "back_type"}, {"cmd": "back_online"}, {"cmd": "back_offline"}, {"cmd": "back_online/offline"}, {"cmd": "back_user_type"}])
async def number_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        await message.answer(
             "Это раздел с категориями мероприятий. Тут ты сможешь выбрать любое мероприятие и получить информацию о нем. \n \n Можно получить мероприятия по типу формата: \n 🔶Онлайн \n 🔷Офлайн \n ♦️Любое \n \n Или перейти во вкладку тип и выбрать конкретное.",
             keyboard=(
                Keyboard()
                .add(Text("Онлайн", {"cmd": "online"}))
                .add(Text("Офлайн", {"cmd": "offline"}))
                .add(Text("Любое", {"cmd": "online/offline"}))
                .row()
                .add(Text("Тип", {"cmd": "type"}))
                .row()
                .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                .add(Text("Назад", {"cmd": "back_category"}),color=KeyboardButtonColor.PRIMARY)
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_category)

#----------------ONLINE
@bot.on.private_message(state=[
    MenuState.state_category,
    MenuState.state_online],
    payload = {"cmd": "online"})
async def number_item_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Online'
        await bd_handler(message, text)
        table_online = await connection_for_db.bd_online()
        await message.answer(
            f"{table_online}",
            keyboard=(
                Keyboard()
                    .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                    .add(Text("Назад", {"cmd": "back_online"}),color=KeyboardButtonColor.PRIMARY)
            ), )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_online)

#----------------OFFLINE
@bot.on.private_message(state=[
    MenuState.state_category,
    MenuState.state_offline],
    payload = {"cmd": "offline"})
async def number_item_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Offline'
        await bd_handler(message, text)
        table_offline = await connection_for_db.bd_offline()
        await message.answer(
            f"{table_offline}",
            keyboard=(
                Keyboard()
                    .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                    .add(Text("Назад", {"cmd": "back_offline"}),color=KeyboardButtonColor.PRIMARY)
            ), )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_offline)

#----------------ONLINE/OFFLINE
@bot.on.private_message(state=[
    MenuState.state_category,
    MenuState.state_online],
    payload = {"cmd": "online/offline"})
async def number_item_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'online/offline'
        await bd_handler(message, text)
        table_online = await connection_for_db.bd_online_offline()
        await message.answer(
            f"{table_online}",
            keyboard=(
                Keyboard()
                    .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                    .add(Text("Назад", {"cmd": "back_online/offline"}),color=KeyboardButtonColor.PRIMARY)
            ), )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_online_offline)

#----------------TYPE
@bot.on.private_message(state=[
    MenuState.state_category,
    MenuState.state_type_db],
    payload={"cmd": "type"})
async def city_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'Type'
        await bd_handler(message, text)
        table_type = await connection_for_db.bd_type()
        await message.answer(
             f"Введи номер типа мероприятия \n \n {table_type}",
             keyboard=(
                Keyboard()
                .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                .add(Text("Назад", {"cmd": "back_type"}),color=KeyboardButtonColor.PRIMARY)
            ),
        )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_type)


@bot.on.private_message(state=[
    MenuState.state_type,
    MenuState.state_type_db],
    text="<msg>")
async def city_item_handler(message: Message, msg):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        if (type(int(msg)) == int):
            table_user_type = await connection_for_db.bd_user_type(msg)
            if (table_user_type != 999999999999):
                await message.answer(
                    f"{table_user_type}",
                    keyboard=(
                        Keyboard()
                            .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                            .add(Text("Назад", {"cmd": "back_user_type"}),color=KeyboardButtonColor.PRIMARY)
                    ),
                )
            else:
                await message.answer(
                    f"Извини, но такого мероприятия еще нет")
        else:
            await message.answer(
                f"Извини, но ты ввел не число :(")
        await bot.state_dispenser.set(message.peer_id, MenuState.state_type_db)



#----------------ALL_EVENT
@bot.on.private_message(state=[
    MenuState.state_event],
    payload={"cmd": "all_event"})
async def number_item_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'All Event'
        await bd_handler(message, text)
        table_all_event = await connection_for_db.bd_all_event()
        await message.answer(
            f"{table_all_event}",
            keyboard = (
                       Keyboard()
                           .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                           .add(Text("Назад", {"cmd": "back_all"}),color=KeyboardButtonColor.PRIMARY)
                       ),
            )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_all_event)



#----------------ALL_GUID
@bot.on.private_message(state=[
    MenuState.state_event],
    payload={"cmd": "all_guid"})
async def number_item_handler(message: Message):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    chk = await check_month(id)
    if chk == 1:
        text = 'All Guid'
        await bd_handler(message, text)
        table_all_event = await connection_for_db.bd_all_guid()
        await message.answer(
            f"{table_all_event}",
            keyboard = (
                       Keyboard()
                           .add(Text("Меню", {"cmd": "back_menu"}),color=KeyboardButtonColor.PRIMARY)
                           .add(Text("Назад", {"cmd": "back_all_g"}),color=KeyboardButtonColor.PRIMARY)
                       ),
            )
        await bot.state_dispenser.set(message.peer_id, MenuState.state_all_guid)


async def bd_handler(message, text):
    user = await bot.api.users.get(message.from_id)
    id = user[0].id
    await connection_for_db.bd_last_visit(id, text)


#----------------SORRY
@bot.on.private_message()
async def sorry_handler(_):
    return "Похоже ты написал что-то, воспользуйся лучше кнопками",



bot.run_forever()

#----------------BDATE
# async def bdate_handler():
#     now_d = time.strftime("%d")
#     now_m = time.strftime("%m")
#     bdate_d = int(str(await connection_for_db.bd_date(now_d)).replace("'",'').replace(',','').replace(')','').replace('(','').replace('[','').replace(']',''))
#     bdate_m = int(str(await connection_for_db.bd_month(now_m)).replace("'", '').replace(',','').replace(')','').replace('(','').replace('[','').replace(']',''))
#     name = str(await connection_for_db.bd_name(bdate_d)).replace("'", '').replace(',','').replace(')','').replace('(','').replace('[','').replace(']','')
#     date_o = int((int(now_d) - int(bdate_d)) * (-1))
#     print(bdate_m, bdate_d, date_o)
#     if (int(bdate_m) == int(now_m)):
#         if (date_o == 7 or date_o == 6 or date_o == 5):
#             return(f"Через {date_o} дней День Рождение у {name}")
#         elif (date_o == 4 or date_o == 3 or date_o == 2):
#             return(f"Через {date_o} дня День Рождение у {name}")
#         elif (date_o == 1):
#             return(f"Через {date_o} день День Рождение у {name}")
#         elif (date_o == 0):
#             return(f"Сегодня День Рождение у {name}")
#         elif (date_o > 8):
#             temp = random.choice(list_words)
#             return(f"{temp}")
#     else:
#         temp = random.choice(list_words)
#         return (f"{temp}")