# main.py

import json
import csv
import os
import json
import requests
import logging
# import datetime

from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta as td


from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from pathlib import Path
from kivy.utils import platform

from multiprocessing import Process


from time import sleep
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

from telebot import TeleBot


__version__ = '0.0.1'

def main_process():
    while True:
        try:
            with open(Path(Path.cwd(), "config.json"), "r") as file:
                config = json.load(file)
            bot = TeleBot(config['telegram_bot_api_key'])
            create_time = dt.now().strftime('%d-%m-%Y %H:%M:%S')
            if config['is_parse_1xstavka']:
                data = parse_1xstavka()
                keys = []
                for d in data:
                    for key in d:
                        if not key in keys:
                            keys.append(key)
                with open(f"1xstavka_{create_time}.csv", 'w') as file:
                    file_writer = csv.DictWriter(file, fieldnames=keys)
                    file_writer.writeheader()
                    file_writer.writerows(data)
                with open(f"1xstavka_{create_time}.csv", 'rb') as file:
                    bot.send_document(config['telegram_id_for_send_data'], document=file)
            if config['is_parse_24score_pro']:
                data = parse_24score_pro(dt.now() - td(days=1))
                keys = []
                for d in data:
                    for key in d:
                        if not key in keys:
                            keys.append(key)
                with open(f"24scorePro_{create_time}.csv", 'w') as file:
                    file_writer = csv.DictWriter(file, fieldnames=keys)
                    file_writer.writeheader()
                    file_writer.writerows(data)
                with open(f"24scorePro_{create_time}.csv", 'rb') as file:
                    bot.send_document(config['telegram_id_for_send_data'], document=file)
            if config['is_parse_flashscorekz']:
                data = parse_flashscore()
                keys = []
                for d in data:
                    for key in d:
                        if not key in keys:
                            keys.append(key)
                with open(f"FlashCoreKZ_{create_time}.csv", 'w') as file:
                    file_writer = csv.DictWriter(file, fieldnames=keys)
                    file_writer.writeheader()
                    file_writer.writerows(data)
                with open(f"FlashCoreKZ_{create_time}.csv", 'rb') as file:
                    bot.send_document(config['telegram_id_for_send_data'], document=file)
        except:
            pass
        sleep(config['sleep_time_seconds'])

class MainApp(MDApp):
    def on_stop(self):
        self.parser_process.terminate()
        self.parser_process.join()

    def build(self):
        logging.info(f"Test print")
        if not Path(Path.cwd(), "config.json").is_file():
            with open(Path(Path.cwd(), "config.json"), "w") as file:
                json.dump({
                    "telegram_bot_api_key": "5884657861:AAG3XQApsUS4ViELJJZ2z6AJ2roapnyKvnY",
                    "telegram_id_for_send_data": "778261480",
                    "is_parse_1xstavka": True,
                    "is_parse_24score_pro": True,
                    "is_parse_flashscorekz": True,
                    "sleep_time_seconds": 60
                }, file, indent=4)
        with open(Path(Path.cwd(), "config.json"), "r") as file:
            data = json.load(file)
        self.parser_process = Process(target=main_process)
        self.parser_process.start()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        main_box_layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            padding=dp(20),
            spacing=dp(30),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        self.telegram_api_key_field = MDTextField(
                hint_text="Telegram Bot Api key",
                pos_hint={"center_x": .5, "center_y": .5},
            text=data['telegram_bot_api_key']
            )
        main_box_layout.add_widget(
            self.telegram_api_key_field
        )

        self.telegram_api_admin_id_field = MDTextField(
                hint_text="Telegram Admin ID",
                pos_hint={"center_x": .5, "center_y": .5},
        text = data['telegram_id_for_send_data']
            )
        main_box_layout.add_widget(
            self.telegram_api_admin_id_field
        )

        is_parse_1xstavka_box_layout = MDBoxLayout(
            adaptive_height=True,
            spacing=dp(30),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        self.is_parse_1xstavka_switch = MDSwitch(
            active=data['is_parse_1xstavka']
            )
        is_parse_1xstavka_box_layout.add_widget(
            self.is_parse_1xstavka_switch
        )
        is_parse_1xstavka_box_layout.add_widget(
            MDLabel(
                text="Parse 1Xstavka"
            )
        )
        main_box_layout.add_widget(is_parse_1xstavka_box_layout)

        is_parse_flashcorekz_box_layout = MDBoxLayout(
            adaptive_height=True,
            spacing=dp(30),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        self.is_parse_flash_core_kz_switch = MDSwitch(
            active=data['is_parse_flashscorekz']
            )
        is_parse_flashcorekz_box_layout.add_widget(
            self.is_parse_flash_core_kz_switch
        )
        is_parse_flashcorekz_box_layout.add_widget(
            MDLabel(
                text="Parse FlashScore KZ"
            )
        )
        main_box_layout.add_widget(is_parse_flashcorekz_box_layout)

        is_parse_24score_box_layout = MDBoxLayout(
            adaptive_height=True,
            spacing=dp(30),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        self.is_parse_24score_switch = MDSwitch(
                active=data['is_parse_24score_pro']
            )
        is_parse_24score_box_layout.add_widget(
            self.is_parse_24score_switch
        )
        is_parse_24score_box_layout.add_widget(
            MDLabel(
                text="Parse 24 Score"
            )
        )
        main_box_layout.add_widget(is_parse_24score_box_layout)

        self.sleep_time_seconds_field = MDTextField(
                hint_text="Sleep time seconds",
                pos_hint={"center_x": .5, "center_y": .5},
            text=str(data['sleep_time_seconds'])
            )
        main_box_layout.add_widget(
            self.sleep_time_seconds_field
        )

        main_box_layout.add_widget(MDRectangleFlatButton(
            text="Update config",
            pos_hint={"center_x": .5, "center_y": .5},
            width=dp(250),
            on_press=self.update_config
        ))
        return main_box_layout

    def update_config(self, button_instance):
        if not self.telegram_api_key_field.text:
            self.telegram_api_key_field.error = True
            return
        if not self.telegram_api_admin_id_field.text:
            self.telegram_api_admin_id_field.error = True
            return
        if not self.sleep_time_seconds_field.text.isdigit():
            self.sleep_time_seconds_field.error = True
            return
        with open("config.json", 'w') as file:
            json.dump({
                "telegram_bot_api_key": self.telegram_api_key_field.text,
                "telegram_id_for_send_data": self.telegram_api_admin_id_field.text,
                "is_parse_1xstavka": self.is_parse_1xstavka_switch.active,
                "is_parse_24score_pro": self.is_parse_24score_switch.active,
                "is_parse_flashscorekz": self.is_parse_flash_core_kz_switch.active,
                "sleep_time_seconds": int(self.sleep_time_seconds_field.text)
            }, file, indent=4)

def parse_1xstavka():
    response = requests.get("https://1xstavka.ru/LineFeed/Get1x2_VZip?sports=1&count=50&lng=en&tf=2200000&tz=3"
                            "&antisports=188&mode=4&country=1&partner=51&getEmpty=true")
    data = response.json()
    events_data = []
    for event in data['Value']:
        event_data = {}
        thead = event['L']
        team_one = event.pop("O1")
        team_two = event.pop("O2")
        event_data.update({
            "Liga": thead,
            "Team one": team_one,
            "Team two": team_two
        })
        handicaps = {}
        try:
            handicaps_data = event["AE"].pop(0)['ME']
            for handicap_data in handicaps_data:
                handicap_team = ""
                if handicap_data.get("P"):
                    if handicap_data.get("P") > 0:
                     handicap_value = f"(+{handicap_data.get('P')})"
                    else:
                        handicap_value = f"({handicap_data.get('P')})"
                else:
                    handicap_value = f"(0)"
                if handicap_data.get("T") == 7:
                    handicap_team = "Team one handicap"
                elif handicap_data.get("T") == 8:
                    handicap_team = "Team two handicap"
                handicaps.update({
                     f"{handicap_team} {handicap_value}": handicap_data.get("C")
                })
        except:
            pass
        for key in handicaps:
            event_data.update({
                key: handicaps[key]
            })
        totals = {}
        try:
            totals_data = event["AE"].pop(0).get("ME")
            for total_data in totals_data:
                total_team = ""
                if total_data.get("P"):
                    if total_data.get("P") > 0:
                     total_value = f"{total_data.get('P')}"
                    else:
                        total_value = f"{total_data.get('P')}"
                else:
                    total_value = f""
                if total_data.get("T") == 9:
                    total_team = "Over"
                elif total_data.get("T") == 10:
                    total_team = "Under"
                totals.update({
                     f"Total {total_team} {total_value}": total_data.get("C")
                })
        except:
            pass
        for key in totals:
            event_data.update({
                key: totals[key]
            })
        x12s_data = event["E"]
        x12 = {
            "1x": 0,
            "Draw": 0,
            "2x": 0
        }
        teams = {
            1: "1x",
            2: "Draw",
            3: "2x"
        }
        for x12_data in x12s_data:
            if x12_data.get("T") in teams:
                x12.update({
                    teams[x12_data.get("T")]: x12_data.get("C")
                })
        event_data.update(x12)
        events_data.append(event_data)
    return events_data

def parse_24score_pro(date: dt):
    response = requests.get(f"https://old.24score.pro/?date={date.strftime('%Y-%m-%d')}")
    with open("test.html", 'w') as file:
        file.write(response.text)
    soup = BeautifulSoup(response.text)
    table = soup.find("table", {"class": "daymatches"})
    tbodies = table.find_all("tbody")
    data = []
    for tbody in tbodies:
        trs = tbody.find_all("tr", )
        main_tr = trs.pop(0)
        thead = main_tr.find("th").find("a").text
        for tr in trs:
            if tr.get("class") is not None:
                if "odd" in tr.get("class") or "even" in tr.get("class"):
                    time = tr.find("td", {"class": "time"}).text.replace("\n", "").strip().split("\t\t\t")[0]
                    team_one = tr.find("td", {"class": "team tm1"}).text.replace("\n", "").strip()
                    team_two = tr.find("td", {"class": "team tm2"}).text.replace("\n", "").strip()
                    odds = tr.find_all("td", {"class": "odds"})
                    team_one_win = odds[0].text.replace("\n", "").replace(" ", "")
                    if team_one_win:
                        team_one_win = float(team_one_win)
                    draw = odds[1].text.replace("\n", "").replace(" ", "")
                    if draw:
                        draw = float(draw)
                    team_two_win = odds[2].text.replace("\n", "").replace(" ", "")
                    if team_two_win:
                        team_two_win = float(team_two_win)
                    data.append({
                        "Liga": thead,
                        "Time": time,
                        "Team one": team_one,
                        "Team two": team_two,
                        "1x": team_one_win,
                        "2x": team_two_win,
                        "Draw": draw,
                        "Series": []
                    })
                else:
                    series_element = tr.find("td", {"class": "series"})
                    if series_element is not None:
                        series_data = series_element.find_all("p")
                        for series_d in series_data:
                            data[-1]['series'].append(series_d.text)
    return data

def parse_flashscore():
    response = requests.get("https://d.flashscorekz.com/x/feed/f_1_-1_3_ru-kz_1", headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                      "Safari/537.36",
        "origin": "https://www.flashscorekz.com",
        "referer": "https://www.flashscorekz.com",
        "x-fsign": "SW9D1eZo"
    }).text
    data = response.split("~")
    result = []
    head = ""
    for row in data:
        tmp_row = row.split("Г·")
        row = []
        for tmp_r in tmp_row:
            row += tmp_r.split("В¬")
        row_dict = {}
        for i in range(0, len(row), 2):
            try:
                key = row[i]
                value = row[i + 1]
                row_dict.update({key: value})
            except:
                pass
        if "ZA" in row_dict:
            head = row_dict["ZA"]
        elif "AE" in row_dict and "AF" in row_dict and "AG" in row_dict and "AH" in row_dict:
            team_one = row_dict['AE']
            team_two = row_dict['AF']
            team_one_result = row_dict['AG']
            team_two_result = row_dict['AH']
            result.append({
                "Liga": head,
                "Team one": team_one,
                "Team two": team_two,
                "Team one score": team_one_result,
                "Team two score": team_two_result
            })
    return result

if __name__ == '__main__':
    app = MainApp()
    app.run()
