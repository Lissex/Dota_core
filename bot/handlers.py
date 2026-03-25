
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from library_func import *
from aiogram.fsm.context import FSMContext
from state import *
import keyboards as kb
from base import *
import database.requests as rq
router = Router()


# Проверка айди 
@router.message(CommandStart())
async def cmd_start(message : Message, state : FSMContext):
    await state.set_state(SteamId.waiting_for_steam_id)
    await rq.set_user(message.from_user.id)
    await message.answer_animation(animation="https://media1.tenor.com/m/3P9tDl-RZSkAAAAd/demon-slayer-kimetsu-no-yaiba.gif", caption="Привет! Пожалуйста, введи свой Steam ID. \nОбрати внимание что в настройках сообщества должна общедоступная история матчей(Настройки -> Сообщество -> Общедоступная история матчей)\n Айди можно посмотреть во вкладке профиль")

@router.message(SteamId.waiting_for_steam_id)
async def process_steam_id(message: Message, state: FSMContext):
    steam_id = message.text
    if check_id(steam_id):  # Проверка Steam ID
        await rq.set_user(message.from_user.id, steam_id)  # Сохранение Steam ID
        await message.answer("Спасибо! Ваш Steam ID сохранен.", reply_markup=kb.main)
    else:
        await message.answer("Ошибка: введенный Steam ID недействителен. Пожалуйста, попробуйте еще раз.", reply_markup=kb.reg)
    await state.clear()

#Если пользователь ввел  неправильного айди
@router.message(F.text == "Повторить попытку")
async def cmd_start(message : Message, state : FSMContext):
    await state.set_state(SteamId.waiting_for_steam_id)
    await rq.set_user(message.from_user.id)
    await message.answer("Попробуй снова введи свой Steam ID.")



@router.message(F.text == "Указать позже")
async def id_time(message : Message):
    await message.answer("Ты всегда сможешь указать айди позже", reply_markup=kb.main_without_id)

@router.message(F.text == "Указать ID")
async def cmd_start(message : Message, state : FSMContext):
    await state.set_state(SteamId.waiting_for_steam_id)
    await rq.set_user(message.from_user.id)
    await message.answer("Привет! Пожалуйста, введи свой Steam ID.")

@router.message(SteamId.waiting_for_steam_id)
async def process_steam_id(message: Message, state: FSMContext):
    steam_id = message.text
    if check_id(steam_id):  # Проверка Steam ID
        await rq.set_user(message.from_user.id, steam_id)  # Сохранение Steam ID
        await message.answer("Спасибо! Ваш Steam ID сохранен.", reply_markup=kb.main)
    else:
        await message.answer("Ошибка: введенный Steam ID недействителен. Пожалуйста, попробуйте еще раз.", reply_markup=kb.reg)


#команда help

@router.message(Command("help"))
async def get_help(message : Message):
    await message.answer_animation(animation="https://aniyuki.com/wp-content/uploads/2023/09/aniyuki-gojo-satoru-gif-23.gif",caption="Я помогу тебе с аналитикой Доты 2!")

# как дела

@router.message(F.text == "Как дела?")
async def how_are_you(message : Message):
    await message.answer("Я сейчас пиво открою")

#команда player
#команда player

@router.message(F.text == "Статистика аккаунта")
async def player(message : Message, state : FSMContext):
    await state.set_state(playerr.play)
    await message.answer_animation(animation="https://images.steamusercontent.com/ugc/171536664499199589/719B1B73CA6601C65A5919C5567710B53E80D8E9/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false",caption="Введи айди")

@router.message(playerr.play)   
async def player2(message : Message, state : FSMContext):
    await state.update_data(play = message.text)
    bib = await state.get_data()
    await message.answer(info_player(bib["play"]))
    await state.clear()

@router.message(F.text == "Матчапы героя")
async def name_hero(message : Message, state : FSMContext):
    await state.set_state(hero_matchup.hero)
    await message.answer_animation(animation="https://images.steamusercontent.com/ugc/2436887023498214718/D044EF4DA8564D3CD5DA1DC755BF86B222CD70CF/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false",caption="Введи имя героя на английском")

@router.message(hero_matchup.hero)
async def out_hero(message : Message, state : FSMContext):
    await state.update_data(nameh = message.text)
    data = await state.get_data()
    await message.answer(matchup(data["nameh"]))
    await state.clear()


@router.message(F.text == "Мета")
async def meta(message : Message):
    await message.answer_animation(animation="https://i.pinimg.com/originals/af/01/75/af0175972377758820ca5093d18ece93.gif",caption=meta_hero(), reply_markup=kb.meta)

@router.callback_query(F.data == "pos_1")
async def meta1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(meta_hero_pos(1),reply_markup=kb.meta)  # Отправляем сообщение в чат

@router.callback_query(F.data == "pos_2")
async def meta1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(meta_hero_pos(2),reply_markup=kb.meta)  # Отправляем сообщение в чат

@router.callback_query(F.data == "pos_3")
async def meta1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(meta_hero_pos(3),reply_markup=kb.meta)  # Отправляем сообщение в чат

@router.callback_query(F.data == "pos_4")
async def meta1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(meta_hero_pos(4),reply_markup=kb.meta)  # Отправляем сообщение в чат

@router.callback_query(F.data == "pos_5")
async def meta1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(meta_hero_pos(5),reply_markup=kb.meta)  # Отправляем сообщение в чат

@router.callback_query(F.data == "end")
async def meta1(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Теперь ты готов поднимать ммры")



@router.message(F.text == "Статистика матча")
async def match(message: Message, state: FSMContext):
    await state.set_state(ma_ch.match)
    await message.answer_animation(animation="https://i.imgur.com/FnbRKc2.gif?noredirect",caption="Введи айди матча")

@router.message(ma_ch.match)
async def match2(message: Message, state: FSMContext):
    await state.update_data(match=message.text)
    bib = await state.get_data()
    await message.answer(info_match(bib["match"]), reply_markup=kb.players)

@router.callback_query(F.data == "0")
async def pos_1di(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "0")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message,0),reply_markup=kb.players)  # Отправляем сообщение в чат

@router.callback_query(F.data == "1")
async def pos_2di(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "1")
    await callback.answer()
    await callback.message.answer_photo(id_p,caption = extended_player_pars(response_message, 1), reply_markup=kb.players)

@router.callback_query(F.data == "2")
async def pos_3di(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "2")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 2), reply_markup=kb.players)

@router.callback_query(F.data == "3")
async def pos_4di(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "3")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 3), reply_markup=kb.players)

@router.callback_query(F.data == "4")
async def pos_5di(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "4")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 4), reply_markup=kb.players)

@router.callback_query(F.data == "5")
async def pos_1ra(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "5")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 5), reply_markup=kb.players)

@router.callback_query(F.data == "6")
async def pos_2ra(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "6")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 6), reply_markup=kb.players)

@router.callback_query(F.data == "7")
async def pos_3ra(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "7")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 7), reply_markup=kb.players)

@router.callback_query(F.data == "8")
async def pos_4ra(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "8")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 8), reply_markup=kb.players)

@router.callback_query(F.data == "9")
async def pos_5ra(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    id_p = photo(response_message, "9")
    await callback.answer()
    await callback.message.answer_photo(id_p, caption = extended_player_pars(response_message, 9), reply_markup=kb.players)

@router.callback_query(F.data == "10")
async def close(callback: CallbackQuery, state: FSMContext):
    bib = await state.get_data()
    response_message = bib['match']
    await callback.answer()
    await callback.message.answer("Обращайся еще")
    await state.clear()


@router.message(F.text == "Помощь")
async def help(message : Message):
    await message.answer("Связь с автором: https://t.me/ewooni")

@router.message(F.text == "Мой аккаунт")
async def my_acc(message: Message):
    tg_id = message.from_user.id
    steam_id = await rq.get_steam_id(tg_id)
        
    if steam_id:
        response = info_player(steam_id)
        await message.answer(response, reply_markup=kb.my_account)
    else:
        await message.answer(
            "❌ Аккаунт не найден!\n"
            "Пожалуйста, зарегистрируйтесь через кнопку ниже",
            reply_markup=kb.registration
        )
            

@router.callback_query(F.data == "best_heroes_myac")
async def check_account(callback: CallbackQuery):
    tg_id = callback.from_user.id
    steam_id = await rq.get_steam_id(tg_id)   
    await callback.answer()       
    if steam_id:
        await callback.message.answer(
            test_wr(steam_id),
            reply_markup=kb.my_account
            )
    else:
        await callback.message.answer(
            "Ваш аккаунт не зарегистрирован. Пожалуйста, зарегистрируйтесь."
        )

@router.callback_query(F.data == "last_matches")
async def check_account(callback: CallbackQuery):
    tg_id = callback.from_user.id
    steam_id = await rq.get_steam_id(tg_id)   
    await callback.answer()       
    if steam_id:
        await callback.message.answer(
            last_matches_by_id_player(steam_id),
            reply_markup=kb.my_account
            )
    else:
        await callback.message.answer(
            "Ваш аккаунт не зарегистрирован. Пожалуйста, зарегистрируйтесь."
        )








