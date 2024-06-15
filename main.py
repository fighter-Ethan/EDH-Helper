import random
import tkinter as tk
import json
from pyedhrec import EDHRec
from guizero import App, Text, TextBox, PushButton, Slider, Combo
from requests.exceptions import HTTPError
import re

eapi = EDHRec()

def dict_to_str(dictionary):
    name = dictionary.get('name', 'No Name')
    synergy = dictionary.get('synergy', 'No Synergy')
    header = dictionary.get('header', 'No Header')
    return f"{name} (Synergy: {synergy}, {header})"


def list_to_str(list_of_items, limit=100):
    str_items = []
    if len(list_of_items) > limit:
        selected_items = random.sample(list_of_items, limit)
    else:
        selected_items = list_of_items
    
    for item in selected_items:  # Use `selected_items` here
        if isinstance(item, list):
            str_items.append(list_to_str(item, limit))
        elif isinstance(item, dict):
            str_items.append(dict_to_str(item))
        else:
            str_items.append(item)
    return "\n".join(str_items)



def get_synergy_cards():
    try:
      commander_name = commander.value
      details = eapi.get_card_details(commander_name)
      synergy_get = eapi.get_high_synergy_cards(commander_name)
      synergy_data = synergy_get['High Synergy Cards']
      limit_value = int(display_amt.value)
      formatted_string = list_to_str(synergy_data, limit_value)
      cards_rec.value = "High-Synergy Cards" + "\n\u200b" + "Remember: The closer to 1.0, the better the synergy." + "\n\u200b" + "\n\u200b" + formatted_string
    except HTTPError:
        cards_rec.value = "I don't think that's a commander. Please try again!"

def get_associated_cards():
    try:
        commander_name = commander.value
        details = eapi.get_card_details(commander_name)
        good_get = eapi.get_commander_cards(commander_name)
        good_data = good_get['New Cards']
        limit_value = int(display_amt.value)
        formatted_string = list_to_str(good_data, limit_value)
        cards_rec.value = "Commonly Associated Cards" + "\n\u200b" + "Remember: The closer to 1.0, the better the synergy." + "\n\u200b" + "\n\u200b" + formatted_string
    except HTTPError:
        cards_rec.value = "I don't think that's a commander. Please try again."

def get_top_cards():
    try:
        commander_name = commander.value
        details = eapi.get_card_details(commander_name)
        top_get = eapi.get_top_cards(commander_name)
        top_data = top_get['Top Cards']
        limit_value = int(display_amt.value)
        formatted_string = list_to_str(top_data, limit_value)
        cards_rec.value = "Top Cards" + "\n\u200b" + "Remember: The closer to 1.0, the better the synergy." + "\n\u200b" + "\n\u200b" + formatted_string
    except HTTPError:
        cards_rec.value = "I don't think that's a commander. Please try again."

def get_combos():
  commander_name = commander.value
  details = eapi.get_card_details(commander_name)
  combo_get = eapi.get_card_combos(commander_name)
  combo_data = combo_get.get('cardlist')
  headers = [cardlist.get("header", "No Header") for cardlists in combo_data]
  print(headers)
  limit_value = int(display_amt.value)
  formatted_string = list_to_str(headers, limit_value)
  cards_rec.value = "Top Cards" + "\n\u200b" + "Remember: The closer to 1.0, the better the synergy." + "\n\u200b" + "\n\u200b" + formatted_string


def determine_action():
    if mode.value == "Synergy":
        get_synergy_cards()
    elif mode.value == "Commonly Used Cards":
        get_associated_cards()
    elif mode.value == "Top Cards":
        get_top_cards()
    elif mode.value == "Card Combos":
        get_combos()
    


#Actual executed script
app = App(title="EDHelp", width=570, height=449)
welcome_message = Text(app, text="Welcome to EDHelp - EDH Deck Helper!", size=30, font="Times New Roman", color="white")
welcome_subheader = Text(app, text="Put your Commander below.", size=20, font="Times New Roman", color="white")
commander = TextBox(app)
mode = Combo(app, options=["Synergy", "Commonly Used Cards", "Top Cards", "Card Combos"])
display_amt = Slider(app, start=1, end=10)
get_cards_button = PushButton(app, command=determine_action, text="Get Cards")
cards_rec = Text(app, text="",size=15, font="Times New Roman", color="white")


app.display()
