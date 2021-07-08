import pyautogui
import os
import sys
import cv2
import requests
import yaml
import keyboard
import fake_useragent
import numpy as np
from mss import mss
from time import sleep, time
from math import radians, cos, sin, asin, sqrt


prev = None
user_agent = fake_useragent.UserAgent()['google chrome']
headers = {'user-agent': user_agent, 'if-none-match': "2979-3kcziSj429jfGMhljZ/o5eCq/7E", 'referer': 'https://nycpokemap.com/', 'authority': 'nycpokemap.com', 'x-requested-with': 'XMLHttpRequest'}
url = 'https://nycpokemap.com/pokestop.php?time='
needed, already = [24, 25, 12, 13, 16, 17], []


class MainAction():
    def __init__(self):
        with open('config.yaml', "r") as f:
            self.config = yaml.load(f)
        
    def click(self, location: list):
        pyautogui.moveTo(location)
        sleep(0.5)
        pyautogui.click(location)
        
    def click_back(self):
        pyautogui.click(button='right')

    def gotcha(self):
        self.click(self.config['teleport_plus_gotcha_locations']['open_teleport'])
        sleep(1)
        self.click(self.config['teleport_plus_gotcha_locations']['paste_cords'])
        sleep(1)
        self.click(self.config['teleport_plus_gotcha_locations']['teleport'])
        sleep(1)
        pyautogui.moveTo(self.config['teleport_plus_gotcha_locations']['pre_throw'])
        sleep(0.5)
        pyautogui.dragTo(self.config['teleport_plus_gotcha_locations']['throw'])
        sleep(1.5)
    
    def reopen(self):
        keyboard.press_and_release('alt+h')
        sleep(2)
        self.click(self.config['reopen_locations']['hal_icon'])
        sleep(2)
        self.click(self.config['reopen_locations']['start_service_button'])
        sleep(1)
        self.click(self.config['reopen_locations']['start_service_button'])
        sleep(40)
        self.click(self.config['reopen_locations']['close_all_trashnews'])
        sleep(0.5)
        self.click(self.config['reopen_locations']['close_all_trashnews'])
        sleep(0.5)
        pyautogui.moveTo(self.config['reopen_locations']['close_all_trashnews'][0], self.config['reopen_locations']['close_all_trashnews'][1] + 50)
        sleep(0.5)
        pyautogui.click()
        pyautogui.dragTo(self.config['reopen_locations']['close_all_trashnews'])

    def open_backpack(self):
        self.click(self.config['locations']['backpack_icon'])
        sleep(1)
        self.click(self.config['locations']['close_backpack_icon'])
        sleep(1)
        self.click(self.config['locations']['close_backpack_icon'])

    def open_stop(self):
        self.click(self.config['locations']['open_pokestop'])
    
action = MainAction()
stop_detect = {
    'left': action.config['locations']['open_pokestop_area'][0],
    'top': action.config['locations']['open_pokestop_area'][1],
    'width': action.config['locations']['open_pokestop_area'][2],
    'height': action.config['locations']['open_pokestop_area'][3]
}
exit_detect = {
    'left': action.config['locations']['berry_encounter_area'][0],
    'top': action.config['locations']['berry_encounter_area'][1],
    'width': action.config['locations']['berry_encounter_area'][2],
    'height': action.config['locations']['berry_encounter_area'][3]
}
close_stop_detect = {
    'left': action.config['locations']['pokestop_more_button_area'][0],
    'top': action.config['locations']['pokestop_more_button_area'][1],
    'width': action.config['locations']['pokestop_more_button_area'][2],
    'height': action.config['locations']['pokestop_more_button_area'][3]
}
battle_detect = {
    'left': action.config['locations']['use_this_party_area'][0],
    'top': action.config['locations']['use_this_party_area'][1],
    'width': action.config['locations']['use_this_party_area'][2],
    'height': action.config['locations']['use_this_party_area'][3]
}
feed_detect = {
    'left': action.config['locations']['feed_in_gym_area'][0],
    'top': action.config['locations']['feed_in_gym_area'][1],
    'width': action.config['locations']['feed_in_gym_area'][2],
    'height': action.config['locations']['feed_in_gym_area'][3]
}


class MainDetector:
    def __init__(self):
        self.path = 'r_photo/'
        self.team_r = cv2.imread(self.path + 'r_detect.png', cv2.IMREAD_GRAYSCALE)
        self.team_r_2 = cv2.imread(self.path + 'r_detect_2.png', cv2.IMREAD_GRAYSCALE)
        self.stop = cv2.imread(self.path + 'stop.png', cv2.IMREAD_GRAYSCALE)
        self.conf = cv2.imread(self.path + 'confirm.png', cv2.IMREAD_GRAYSCALE)
        self.poke = cv2.imread(self.path + 'poke.png', cv2.IMREAD_GRAYSCALE)
        self.lead = cv2.imread(self.path + 'leader.png', cv2.IMREAD_GRAYSCALE)
        self.feed = cv2.imread(self.path + 'feed.png', cv2.IMREAD_GRAYSCALE)
        self.sct = mss()

    def detect_stop(self):
        stop_img = np.array(self.sct.grab(stop_detect))

        capture = cv2.cvtColor(stop_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(capture, self.team_r, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.35)

        if loc[::-1][1].size > 0:
            return True

        stop_img = np.array(self.sct.grab(stop_detect))

        capture = cv2.cvtColor(stop_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(capture, self.team_r_2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.35)

        if loc[::-1][1].size > 0:
            return True
        return False

    def detect_close_stop(self):
        close_img = np.array(self.sct.grab(close_stop_detect))

        capture = cv2.cvtColor(close_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(capture, self.stop, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.75)

        if loc[::-1][1].size > 0:
            return True
        return False

    def detect_battle_screen(self):
        battle_img = np.array(self.sct.grab(battle_detect))

        capture = cv2.cvtColor(battle_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(capture, self.conf, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.65)

        if loc[::-1][1].size > 0:
            return True
        return False

    def detect_poke(self):
        exit_img = np.array(self.sct.grab(exit_detect))

        capture = cv2.cvtColor(exit_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(capture, self.poke, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.75)

        if loc[::-1][1].size > 0:
            return True
        return False

    def detect_feed(self):
        feed_img = np.array(self.sct.grab(feed_detect))

        capture = cv2.cvtColor(feed_img, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(capture, self.feed, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.75)

        if loc[::-1][1].size > 0:
            return True
        return False


def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def get_invasion():
    global prev
    cords = []
    ans = []
    data = requests.get(url=url, headers=headers).json()
    for i in range(len(data['invasions'])):
        if int(data['invasions'][i]['invasion_end']) - data['meta']['time'] > 300 and int(data['invasions'][i]['character']) in needed and (data['invasions'][i]['lat'], data['invasions'][i]['lng']) not in already:
            cords.append(((data['invasions'][i]['lat'], data['invasions'][i]['lng']), int(data['invasions'][i]['character'])))

    if prev == None:
        coordinates = f'{cords[0][0][0]},{cords[0][0][1]}'
        prev = (cords[0][0][0], cords[0][0][1])
    else:
        for i in cords:
            dist = haversine(float(prev[0]), float(prev[1]), float(i[0][0]), float(i[0][1]))
            ans.append((dist, i[0][0], i[0][1], i[1]))
        
        ans.sort(key=lambda x: x[0])
        ans = ans[:1][0]
        coordinates = f'{ans[1]},{ans[2]}'
        prev = (ans[1], ans[2])

    os.system(f'adb shell am start -a android.intent.action.VIEW -d "https://pk.md/{coordinates}"')
    already.append(prev)
