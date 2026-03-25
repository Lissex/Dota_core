from aiogram.fsm.state import StatesGroup, State



class SteamId(StatesGroup):
    waiting_for_steam_id = State()

class playerr(StatesGroup):
    play = State()

class ma_ch(StatesGroup):
    match = State()

class hero_matchup(StatesGroup):
    hero = State()

