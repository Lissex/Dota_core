from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мой аккаунт")],
    [KeyboardButton(text="Статистика аккаунта"), KeyboardButton(text="Статистика матча")],
    [KeyboardButton(text="Мета"), KeyboardButton(text="Матчапы героя")],
    [KeyboardButton(text="Помощь")]
    ], resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню")

main_without_id = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Указать ID")],
    [KeyboardButton(text="Статистика аккаунта"), KeyboardButton(text="Статистика матча")],
    [ KeyboardButton(text="Мета"), KeyboardButton(text="Матчапы героя") ],
    [KeyboardButton(text="Помощь")]
    ], resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню")






players = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="1 🌑", callback_data="0"),
                                                 InlineKeyboardButton(text="2 🌑", callback_data="1"),
                                                 InlineKeyboardButton(text="3 🌑", callback_data="2"),
                                                 InlineKeyboardButton(text="4 🌑", callback_data="3"),
                                                 InlineKeyboardButton(text="5 🌑", callback_data="4")],
                                                [InlineKeyboardButton(text="1 🌕", callback_data="5"),
                                                 InlineKeyboardButton(text="2 🌕", callback_data="6"),
                                                 InlineKeyboardButton(text="3 🌕", callback_data="7"),
                                                 InlineKeyboardButton(text="4 🌕", callback_data="8"),
                                                 InlineKeyboardButton(text="5 🌕", callback_data="9")],
                                                 [InlineKeyboardButton(text="Не нужна дополнительная информация", callback_data="10")]])

my_account = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Лучшие Герои", callback_data="best_heroes_myac")],
                                                    [InlineKeyboardButton(text="Последние 5 игр", callback_data="last_matches")]])

meta = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Pos.1", callback_data="pos_1"),
                                             InlineKeyboardButton(text="Pos.2", callback_data="pos_2"),
                                             InlineKeyboardButton(text="Pos.3", callback_data="pos_3"),
                                             InlineKeyboardButton(text="Pos.4", callback_data="pos_4"),
                                             InlineKeyboardButton(text="Pos.5", callback_data="pos_5")],
                                             [InlineKeyboardButton(text="Завершить",callback_data="end")]])

reg = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Указать позже")], [KeyboardButton(text="Повторить попытку")]],
    resize_keyboard=True, input_field_placeholder="Выбери пункт меню(Регистрация дает дополнительные возможности)")