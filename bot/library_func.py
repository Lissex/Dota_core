import requests
from constants import *
import datetime
from base import *
from datetime import datetime, timezone, timedelta

def find_item_name_by_id(item_id):
  for item in itemss["data"]["constants"]["items"]:
      if item["id"] == item_id:
          return item["displayName"]
  return None

def id_hero_by_name(name):
    for hero in datah["constants"]["heroes"]: 
        if isinstance(hero, dict):
            if hero["name"].lower() == name.lower():
                return hero["id"]
    return None  

def name_hero_by_id(hero_id):
    heroes_list = datah["constants"]["heroes"]
    for element in heroes_list:
        if isinstance(element, dict) and "id" in element:
            if element["id"] == hero_id:
                return element["name"]
    return None 

def timegame(timestamp):
  utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
  moscow_time = utc_time.astimezone(timezone(timedelta(hours=3)))  # Часовой пояс UTC+3
  return moscow_time.strftime("%d.%m.%Y")


#Проверка айди 
def check_id(ip_pl):
  query = """{player(steamAccountId:"""+str(ip_pl)+""") {
  steamAccountId
}
}"""
  response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query})
  if response.status_code == 200:
    return True 
  else:
    return False


#Краткая статистика про игрока
def info_player(id_pl):
  query= """{
    player(steamAccountId:"""+ str(id_pl)+""") {
      names {
        name
        lastSeenDateTime
      }
      activity {
        activity
      } 
      matchCount
      winCount
      lastMatchDate
      firstMatchDate

    }
  }
  """

  response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
  try:
    act = response["data"]["player"]["activity"]
    res = {"Никнейм" : response["data"]["player"]["names"][0]["name"],"Активность" : acvivity_data[act["activity"]],
          "Винрейт" : f"{round(response["data"]["player"]["winCount"] * 100 / response["data"]["player"]["matchCount"], 2)}%", "Количество игр" : response["data"]["player"]["matchCount"],
          "Количество игр" : response["data"]["player"]["matchCount"], "Количество побед" : response["data"]["player"]["winCount"]}
        
    result = "" 
    for keys, items in res.items():
      result += str(keys)
      result += ":"
      result += str(items)
      result += "\n"
    
    return result
  except Exception as error:
     print(error)
     return "⚠️ Аккаунт скрыт или вы ввели некорректное ID"


# Краткая статистика игроков в матче
def player_pars(player_stat):
    if player_stat["isRadiant"] == True:
      team = "🌕Силы Света"
    else:
      team = "🌑Силы Тьмы"

    num_hero = player_stat["heroId"]
    result = {"🆔 игрока и сторона" : f"{str(player_stat["steamAccountId"])}|{team}","Герой и лвл" : f" {datah["constants"]["heroes"][num_hero]["name"]} {player_stat["level"]}",
          "💰Нетворс/Роль" :f"{player_stat["networth"]}|Pos.{player_stat["position"][-1]}", "📊KDA" : f" {player_stat['kills']}|{player_stat['deaths']}|{player_stat["assists"]}"}
    return result


def player_pars_extented(player_stat):
    if player_stat["isRadiant"] == True:
      team = "🌕Силы Света"
    else:
      team = "🌑Силы Тьмы"
    if player_stat["isVictory"] == True:
       victory = "Победа"
    else:
       victory = "Поражение"
       

    num_hero = player_stat["heroId"]
    result = {"Результат матча" : victory, "🆔 игрока и сторона" : f"{str(player_stat["steamAccountId"])}|{team}","Герой и лвл" : f" {datah["constants"]["heroes"][num_hero]["name"]} {player_stat["level"]}",
          "💰Нетворс/Роль" :f"{player_stat["networth"]}|Pos.{player_stat["position"][-1]}", "📊KDA" : f" {player_stat['kills']}|{player_stat['deaths']}|{player_stat["assists"]}"}
    return result




#Статистика матча (Доработка по времени)
def info_match(id):

    query = """{match(id:""" + str(id) + """) {
    didRadiantWin
    firstBloodTime
    direKills
    radiantKills
    startDateTime
    endDateTime
    players {
      isRadiant
      steamAccountId
      isVictory
      heroId
      kills
      deaths
      assists
      numLastHits
      numDenies
      goldPerMinute
      networth
      experiencePerMinute
      level
      goldSpent
      heroDamage
      towerDamage
      heroHealing
      lane
      position
      imp
      award
      item0Id
      item1Id
      item2Id
      item3Id
      item4Id
      item5Id
      backpack0Id
      backpack1Id
      backpack2Id
      neutral0Id
    }
    id
  }
  }"""
    response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
    time = f"{(int(response["data"]["match"]["endDateTime"]) - int(response["data"]["match"]["startDateTime"])) // 60} : {(int(response["data"]["match"]["endDateTime"]) - int(response["data"]["match"]["startDateTime"])) % 60}" 
    try:
      response["data"]["match"]["players"] = sorted(response["data"]["match"]["players"], key= lambda x: (x["isRadiant"], x["position"][-1] ))
      if response["data"]["match"]["didRadiantWin"] == True:
        win = "Победа сил Света"
      else: 
        win = "Победа сил Тьмы"
      result_match = {"🕐Дата | Длительность матча" : str(timegame(response["data"]["match"]["endDateTime"]))+" | " + str(time),"🥇": win, "Первое убийство" : f"🩸{response["data"]["match"]["firstBloodTime"] // 3600}:{response["data"]["match"]["firstBloodTime"] // 60}:{response["data"]["match"]["firstBloodTime"] % 60}",
            "🌑Убийства сил Тьмы" : f"{sum(response["data"]["match"]["direKills"])}⚔️{sum(response["data"]["match"]["radiantKills"])} : Убийства сил Света🌕" }

      result = ""
      for key, item in result_match.items():
        result += str(key)
        result += ": "
        result += str(item)
        result += "\n"
      result += "\n"
      for player in response["data"]["match"]["players"]:
        for key, item in player_pars(player).items():
          result += str(key)
          result += ": "
          result += str(item)
          result += "\n"
        result += "\n"
      return result
    except Exception as error:
      print(error)
      return "Некорретное айди"



# Подробная информация про игрока в матче (id матча + номер игрока в ранее отсортированном списке)
def extended_player_pars(id, num):
  query = """{match(id:""" + str(id) +"""){
    players {
    steamAccountId
    isRadiant
    networth
    heroId
    kills
    deaths
    assists
    numLastHits
    numDenies
    goldPerMinute
    experiencePerMinute
    level
    heroDamage
    towerDamage
    position
    item0Id
    item1Id
    item2Id
    item3Id
    item4Id
    item5Id
    backpack0Id
    backpack1Id
    backpack2Id
    neutral0Id
    leaverStatus
  }
}
}"""
  try:
    result = "📊Статиcтика\n"
    response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
    response["data"]["match"]["players"] = sorted(response["data"]["match"]["players"], key= lambda x: (x["isRadiant"], x["position"][-1] ))
    player_stat = response["data"]["match"]["players"][num]
    if player_stat["isRadiant"] == True:
      team = "Силы Света"
    else:
      team = "Силы Тьмы"
    numh = player_stat["heroId"]
    
    player_items = ""
    player_items += find_item_name_by_id(player_stat["item0Id"]).replace("item_", "").replace("_", " ").title() + "|" if player_stat["item0Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["item1Id"]).replace("item_", "").replace("_", " ").title() + "|" if player_stat["item1Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["item2Id"]).replace("item_", "").replace("_", " ").title() + "|" if player_stat["item2Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["item3Id"]).replace("item_", "").replace("_", " ").title() + "|" if player_stat["item3Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["item4Id"]).replace("item_", "").replace("_", " ").title() + "|" if player_stat["item4Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["item5Id"]).replace("item_", "").replace("_", " ").title() + "|" if player_stat["item5Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["backpack0Id"]).replace("item_", "").replace("_", " ").title() + " " if player_stat["backpack0Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["backpack1Id"]).replace("item_", "").replace("_", " ").title() + " " if player_stat["backpack1Id"] != None else ""
    player_items += find_item_name_by_id(player_stat["backpack2Id"]).replace("item_", "").replace("_", " ").title() + " " if player_stat["backpack2Id"] != None else ""
    neutral_items = find_item_name_by_id(player_stat["neutral0Id"]).replace("item_", "").replace("_", " ").title() + " " if player_stat["neutral0Id"] != None else ""


    player_stat = {"ID игрока и сторона" : str(player_stat["steamAccountId"]) + " | " + team,"Герой и лвл" : f" {datah["constants"]["heroes"][numh]["name"]} {player_stat["level"]}",
          "Нетворс/Роль" :f" {player_stat["networth"]}💰|Pos.{player_stat["position"][-1]}", "KDA" : f" {player_stat['kills']}|{player_stat['deaths']}|{player_stat["assists"]}",
          "Ластхиты/Денаи" : f"{player_stat["numLastHits"]}🟢|🔴{player_stat["numDenies"]}", "GPM/XPM" : f"{player_stat["goldPerMinute"]}💵|🌟{player_stat["experiencePerMinute"]}",
          "Урон по героям" : f"{player_stat["heroDamage"]}⚔️", "Урон по постройкам" : f"{player_stat["towerDamage"]}💥", "🎒Предметы" : player_items, "Нейтралка" : neutral_items}
    for key, item in player_stat.items():
      result +="├" + str(key)
      result += ": "
      result += str(item)
      result += "\n"
    return result
  except Exception as error:
    print(error)
    return "Некорретное айди"

  

# Выбор иконки героя из файла base.py
def photo(id_match, num):
    query = """{match(id:"""+str(id_match)+""") {
  id
  players {
    heroId
    isRadiant
    position
  }
}
}"""
    try:
      response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
      response["data"]["match"]["players"] = sorted(response["data"]["match"]["players"], key= lambda x: (x["isRadiant"], x["position"][-1] ))
      player = response["data"]["match"]["players"][int(num)]
      hero_player = player["heroId"]
      result = datah["constants"]["heroes"][hero_player]["photo"]
      
      return result
    except Exception as error:
      print(error)
      return "Некорректное айди"



#Последние 5 игр игрока
def last_matches_by_id_player(id):
  query = """{
  player(steamAccountId: """ + str(id) + """) {
    matches(
      request: { isParsed: true, take: 5, positionIds: [POSITION_4, POSITION_5, POSITION_1, POSITION_2, POSITION_3] }
    ) {
      players(steamAccountId:"""  + str(id) + """) {
        matchId
        steamAccountId
        isRadiant
        kills
        deaths
        assists
        position
        deaths
        kills
        heroId
        networth
        level
        isVictory
      }
    }
  }
}
"""
  try:
    response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
    
    player = response["data"]["player"]["matches"][0]["players"][0]
    result = f"Последние 5 игр \n"
    for i in range(0, 5):
      player = response["data"]["player"]["matches"][i]["players"][0]
      result += f"├🆔 матча : {player["matchId"]} \n"
      for keyi, itemi in player_pars_extented(player).items():
        result += "├" + str(keyi)
        result += ": "
        result += str(itemi)
        result += "\n"
      result += "\n"

    return result
  except Exception as error:
    print(error)
    return "Некорректное айди"



# 5 лучших героев игрока
def test_wr(id):
    query = """{
  player (steamAccountId: """ +str(id) +""") {
    heroesPerformance (request: {
          take: 1000}, take: 1000) {
      heroId
      hero {
        displayName
      }
      matchCount
      winCount
    }
  }
}"""
    try:
      response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
      response["data"]["player"]["heroesPerformance"] = sorted(response["data"]["player"]["heroesPerformance"], key= lambda x: (x["matchCount"], x["winCount"]), reverse= True)
      result = ""
      for i in range(5):
        num_hero = response["data"]["player"]["heroesPerformance"][i]["heroId"]
        all_matches = {"♟Герой" : datah["constants"]["heroes"][num_hero]["name"], "Процент побед" : f"{round(response["data"]["player"]["heroesPerformance"][i]["winCount"] * 100 / response["data"]["player"]["heroesPerformance"][i]["matchCount"], 2)}%"}
        for key, value in all_matches.items():
          result += str(key)
          result += ": "
          result += str(value)
          result += "\n"
      result += "\n"

      return result
    except Exception as error:
       print(error)
       return "Некорректное айди"



# Мета героев
def meta_hero():
    result = ""
    query = """{
  heroStats {
    winWeek(
      gameModeIds: [ALL_PICK_RANKED]
      bracketIds: [IMMORTAL]
      positionIds: [POSITION_1, POSITION_2, POSITION_3, POSITION_4, POSITION_5]
      take: 1
    ) {
  		
      week
      heroId
      winCount
      matchCount
    }
  }
}"""
    data_percent = []
    response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
    for i in response["data"]["heroStats"]["winWeek"]:
        if i["matchCount"] > 8000:
          data_percent.append({"heroId" : i["heroId"], "win_percent" : round(i["winCount"] * 100 / i["matchCount"], 2), "numMatch" : i["matchCount"], })
    data_percent = sorted(data_percent, key= lambda x: (x["win_percent"], x["numMatch"]), reverse = True)

    for i in range(15):
        result += datah["constants"]["heroes"][data_percent[i]["heroId"]]["name"] + f" {str(data_percent[i]["win_percent"])}%"
        result += "\n"
        
    return result


# Мета героев по позиции
def meta_hero_pos(pos_num):
    result = ""
    query = """{
  heroStats {
    winWeek(
      gameModeIds: [ALL_PICK_RANKED]
      bracketIds: [IMMORTAL]
      positionIds: [POSITION_"""+str(pos_num)+"""]
      take: 1
    ) {
  		
      week
      heroId
      winCount
      matchCount
    }
  }
}"""
    data_percent = []
    response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
    for i in response["data"]["heroStats"]["winWeek"]:
      if i["matchCount"] > 6000:   
          data_percent.append({"heroId" : i["heroId"], "win_percent" : round(i["winCount"] * 100 / i["matchCount"], 2), "numMatch" : i["matchCount"], })
    data_percent = sorted(data_percent, key= lambda x: (x["win_percent"], x["numMatch"]), reverse = True)


    if len(data_percent) > 15:
      for i in range(15):
          result += f"├{datah["constants"]["heroes"][data_percent[i]["heroId"]]["name"]}" + f" {str(data_percent[i]["win_percent"])}%"
          result += "\n"
    else:
      for i in range(len(data_percent)):
        result += f"├{datah["constants"]["heroes"][data_percent[i]["heroId"]]["name"]}" + f" {str(data_percent[i]["win_percent"])}%"
        result += "\n"
        
    return result


#Информация против кого пикать героя
def matchup(name):
  query = """{
  heroStats{
    matchUp(heroId: """+str(id_hero_by_name(name))+""", take: 126, bracketBasicIds: DIVINE_IMMORTAL){
      heroId
      with{
        matchCount
        heroId1 
        heroId2
        winsAverage
        synergy
      }
      vs{
        matchCount
        heroId1
        heroId2
        winsAverage
        synergy
      
      }
    }
  }
}"""
  out = f"Лучшие союзники {name.title()}:\n"
  response = requests.post(GRAPHQL_ENDPOINT, headers=HEADERS, json= {"query" : query}).json()
  with_hero = response["data"]["heroStats"]["matchUp"][0]["with"]
  sorted_with_hero_list = []
  vs_hero = response["data"]["heroStats"]["matchUp"][0]["vs"]
  soted_vs_hero_list = []
  for i in with_hero:
    if i["matchCount"] > 100:
      sorted_with_hero_list.append(i)
  sorted_with_hero_list = sorted(sorted_with_hero_list, key=lambda x: x["winsAverage"], reverse=True)
  sorted_with_hero_list = sorted_with_hero_list[1:6]  
  
  for i in vs_hero:
    if i["matchCount"] > 100:
      soted_vs_hero_list.append(i)
  soted_vs_hero_list = sorted(soted_vs_hero_list, key=lambda x: x["winsAverage"], reverse=True)
  soted_vs_hero_list =soted_vs_hero_list[1:6]
  
  for i in sorted_with_hero_list:
    out += f"Винрейт {name.title()} c {name_hero_by_id(i["heroId2"])}: {round(i["winsAverage"] *100, 2)}%\n"
  out += f"В кого лучше всего пикать {name.title()}\n"
  for i in soted_vs_hero_list:
    out += f"Винрейт {name.title()} против {name_hero_by_id(i["heroId2"])}: {round(i["winsAverage"] *100, 2)}%\n"

  return out

