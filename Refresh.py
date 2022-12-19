# -*- coding: utf-8 -*-
"""
Developed on Python 3.6.4
Created on 2022-09-10

Only tested with Bluestacks 5. Results may vary and not guaranteed. Batteries not included.
"""

from datetime import datetime, timedelta
from time import sleep
import keyboard
import pyautogui
import win32gui
import win32api


class UserSettings:
    def __init__(self):
        self.img_checker_flag = False  # Runs
        self.start_btn = "["
        self.pause_btn = "]"
        self.bs_height = 1280  # Window height you want your bluestacks at when refreshing, the bot will resize to this
        self.bs_width = 720  # Window width you want your bluestacks at when refreshing, the bot will resize to this
        self.max_rolls = 300  # Set number of refreshes you stop at
        self.print_at_roll = 50  # If set at 50, it will print how many refreshes/bms you've gotten every 50 rolls


class FileNames:
    """
    The class values may need to be tweaked according to the user's needs depending if they want to change anything
    such as the resolution for example. The images will need to be recreated depending on their BlueStacks 5 settings.
    """
    def __init__(self):
        self.cov_icon = "covenant1280x720.png"
        self.mys_icon = "mystic1280x720.png"
        self.cov_buy_btn = "buy_button_cov1280x720.png"
        self.mys_buy_btn = "buy_button_mys1280x720.png"
        self.confirm_btn = "confirm_button1280x720.png"
        self.garo = "garo1280x720.png"


class Keys:
    """
    Hot keys set by the user in bluestacks key mapping.
    See: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
    """
    def __init__(self):
        self.icon_1_buy = 0x41          # key: A
        self.icon_2_buy = 0x42          # key: B
        self.icon_3_buy = 0x43          # key: C
        self.icon_4_buy = 0x44          # key: D
        self.icon_5_buy = 0x45          # key: E
        self.icon_6_buy = 0x46          # key: F
        self.confirm_buy = 0x52         # key: R
        self.scroll = 0x53              # key: S
        self.refresh = 0x59             # key: Y
        self.refresh_confirm = 0x5A     # key: Z
        self.initial_test = 0x54        # key: T


class Icon:
    """
    The class sets the positions of the icons based on the height of the bluestacks windows.
    There should be no need to adjust.
    """
    def __init__(self, bs_height):
        self.pos1 = bs_height * .22
        self.pos2 = bs_height * .42
        self.pos3 = bs_height * .62
        self.pos4 = bs_height * .82
        self.pos5 = bs_height * .72
        self.pos6 = bs_height * .92

    @property
    def pixel_diff(self):
        return (self.pos2 - self.pos1) / 2


class Count:
    # Counter class for printing counts
    def __init__(self):
        self.mys = 0
        self.cov = 0
        self.screens_checked = 0
        self.scan = 0
        self.cov_buy_btn = 0
        self.mys_buy_btn = 0
        self.confirm_btn = 0
        self.garo = 0

    @property
    def skystones(self):
        return (self.screens_checked - 1) * 3

    def print_all(self):
        print("------Count------"
              "\nCovenant Bookmarks = ", self.cov, " | Rate = ",
              round(self.cov / self.screens_checked * 100, 1), "% (Avg = 4.41%)",
              "\nMystic Medals = ", self.mys, " | Rate = ",
              round(self.mys / self.screens_checked * 100, 1), "% (Avg = 1.26%)",
              "\nTotal Screens Checked = ", self.screens_checked,
              "\nSkystones = ", self.skystones,
              "\n------vs Expected Avg------"
              "\nAverage for reference: 68ss per cov, 237ss per mys"
              "\nCovenant Bookmarks = ", round(self.skystones / 68, 1),
              "\nMystic Bookmarks = ", round(self.skystones / 238, 1),
              "\n----------------")

    def print_bm_checker(self):
        print("------Count------"
              "\nCovenant Bookmarks = ", self.cov, "/100 found"
              "\nMystic Medals = ", self.mys, "/100 found"
              "\nCovenant buy button = ", self.cov_buy_btn, "/100 found"
              "\nMystic Medals = ", self.mys_buy_btn, "/100 found"
              "\nRefresh confirm button = ", self.confirm_btn, "/100 found"
              "\nGaro = ", self.garo, "/100 found"
              "\n----------------")


class RefreshSecretShop:
    def __init__(self):
        # Initialisation - do not touch
        self.settings = UserSettings()
        self.bs_hwnd = None
        self.count = Count()
        self.filename = FileNames()
        self.icon = Icon(self.find_and_resize_bluestacks(self.settings.bs_height, self.settings.bs_width))
        self.keys = Keys()

        if self.settings.img_checker_flag:
            self.img_checker()
        else:
            self.main()

    def find_and_resize_bluestacks(self, height, width):
        """
        Finds the Bluestacks Screen, sets to a small size then to a higher resolution.
        :param height: desired height resolution
        :param width: designed width resolution
        :return: height
        """
        try:
            self.bs_hwnd = win32gui.FindWindow(None, 'BlueStacks')
            if self.bs_hwnd == 0:
                raise Exception("Bluestacks window not available.")
            win32gui.MoveWindow(self.bs_hwnd, 0, 0, 10, 10, True)
            win32gui.MoveWindow(self.bs_hwnd, 0, 0, height, width, True)
            return win32gui.GetWindowRect(self.bs_hwnd)[3]
        except Exception as e:
            print("Failed to find BlueStacks window or resize.")
            print(e)

    def img_checker(self):
        """
        Scans the screen a hundred times and counts how many times it successfully found it.
        """
        print("Running BM checker.")
        for idx, _ in enumerate(range(0, 100)):
            if pyautogui.locateOnScreen(self.filename.cov_icon, confidence=0.75):
                self.count.cov += 1
            if pyautogui.locateOnScreen(self.filename.cov_icon, confidence=0.75):
                self.count.mys += 1
            if pyautogui.locateOnScreen(self.filename.cov_buy_btn, confidence=0.70):
                self.count.cov_buy_btn += 1
            if pyautogui.locateOnScreen(self.filename.mys_buy_btn, confidence=0.70):
                self.count.mys_buy_btn += 1
            if pyautogui.locateOnScreen(self.filename.confirm_btn, confidence=0.70):
                self.count.confirm_btn += 1
            if pyautogui.locateOnScreen(self.filename.garo, confidence=0.70):
                self.count.garo += 1

            if idx % 10 == 0:
                print("{}/100 locate attempts done so far...".format(idx))
        self.count.print_bm_checker()

    def main(self):
        """
        Handles the refreshing of the secret shop.
        1. Scans the screen twice for covenant and mystic bms per scan.
        2. Scrolls screen if it can't find on first scan.
        3. Refreshes after second scan is done.
        User has two chances of stopping the refresh.
        """
        print("---Secret shop refresh---")
        self.check_bluestacks_focus()
        while self.count.screens_checked <= self.settings.max_rolls:
            if input("To start refreshing, enter the key {}".format(self.settings.start_btn)) == self.settings.start_btn:
                print("Started secret shop refresh.")
                self.count.scan = 0
                while not keyboard.is_pressed(self.settings.pause_btn):
                    # Beginning operations
                    if self.count.scan == 0:
                        self.count.screens_checked += 1
                        print("[", self.count.screens_checked, "] ", end="", flush=True)

                    # Start checking screen
                    self.check_screen()
                    # If someone wants to stop before refresh
                    if keyboard.is_pressed(self.settings.pause_btn):
                        break

                    # After screen is checked
                    if self.count.scan == 0:
                        self.scroll_shop()
                        self.count.scan += 1
                    elif self.count.scan == 1:
                        self.refresh_shop()
                        self.count.scan = 0
                        print("")
                        # Print every N rolls user has set
                        if self.count.screens_checked % self.settings.print_at_roll == 0:
                            self.count.print_all()
                        # Stops refreshing at N rolls user has set
                        if self.count.screens_checked == self.settings.max_rolls:
                            break

                print("\nStopping refresh.")
                self.count.print_all()
                # Wait a little bit so user stops spamming the key if not at max refresh.
                if not self.count.screens_checked == self.settings.max_rolls:
                    sleep(2)
                print("Refresh stopped.")

    def check_bluestacks_focus(self):
        """
        The function checks if it can send a key to bluestacks. If it doesn't, the user must click bluestacks.
        """
        bs_not_clicked, first_message = True, True
        while bs_not_clicked:
            try:
                self.activate_bs_and_click_key(self.keys.initial_test, max_attempts=1)
            except (Exception, ):
                if first_message:
                    print("Please focus Bluestacks window by clicking it.")
                    first_message = False
            else:
                print("\nSuccessfully sent key to Bluestacks --> Bluestacks detected.")
                break

    def refresh_shop(self):
        print("-refresh", end="", flush=True)
        self.click_key_and_wait(self.keys.refresh, self.filename.confirm_btn)
        self.click_key_and_wait(self.keys.refresh_confirm, self.filename.garo)

    def scroll_shop(self):
        print("-scroll", end="", flush=True)
        self.activate_bs_and_click_key(self.keys.scroll)  # Click G Confirm button
        sleep(.5)

    def check_screen(self):
        """
        Checks the screen for a BM. If there is a BM, it will get the respective hot key and click it.
        """
        cov_pos, mys_pos = self.find_bm()
        for pos in cov_pos, mys_pos:
            if pos:
                print("-found:", pos.top, end="", flush=True)
                key = self.get_buy_key(pos)
                if key:
                    print("-buying", end="", flush=True)
                    if cov_pos == pos:
                        self.click_key_and_wait(key, self.filename.cov_buy_btn)
                        self.count.cov += 1
                        print("-cov bought", pos.top, end="", flush=True)
                    elif mys_pos == pos:
                        self.click_key_and_wait(key, self.filename.mys_buy_btn)
                        self.count.mys += 1
                        print("-mys bought", pos.top, end="", flush=True)
                    self.activate_bs_and_click_key(self.keys.confirm_buy)  # Click F Confirm buy button
                    sleep(.5)  # Pause before next action

    def find_bm(self):
        """
        Pyautogui attempts to locate the image on the screen. Confidence = .75 seems to be a decent spot.
        :return: cov position, mys position
        """
        print("-Scan_attempt:", end="", flush=True)
        max_attempts = 10
        for attempt in range(max_attempts):
            print(attempt, end="", flush=True)
            try:
                sleep(1.5)
                return pyautogui.locateOnScreen(self.filename.cov_icon, confidence=0.75), pyautogui.locateOnScreen(
                    self.filename.mys_icon, confidence=0.75)
            except Exception as e:
                if attempt < max_attempts - 1:
                    continue
                else:
                    print(e)
                    raise Exception("Could not locate button.")

    def get_buy_key(self, pos):
        """
        Function returns key if the image located position is found within the top coordinates.
        :param pos: position returned from screen locate
        :return: key
        """
        if self.count.scan == 0:
            if self.icon.pos1 - self.icon.pixel_diff <= pos.top <= self.icon.pos1 + self.icon.pixel_diff:
                return self.keys.icon_1_buy
            elif self.icon.pos2 - self.icon.pixel_diff <= pos.top <= self.icon.pos2 + self.icon.pixel_diff:
                return self.keys.icon_2_buy
            elif self.icon.pos3 - self.icon.pixel_diff <= pos.top <= self.icon.pos3 + self.icon.pixel_diff:
                return self.keys.icon_3_buy
            elif self.icon.pos4 - self.icon.pixel_diff <= pos.top <= self.icon.pos4 + self.icon.pixel_diff:
                return self.keys.icon_4_buy
            else:
                raise Exception("-Could not find within coordinates.")
        elif self.count.scan == 1 and \
                self.icon.pos5 - self.icon.pixel_diff <= pos.top <= self.icon.pos6 + self.icon.pixel_diff:
            if self.icon.pos5 - self.icon.pixel_diff <= pos.top <= self.icon.pos5 + self.icon.pixel_diff:
                return self.keys.icon_5_buy
            elif self.icon.pos6 - self.icon.pixel_diff <= pos.top <= self.icon.pos6 + self.icon.pixel_diff:
                return self.keys.icon_6_buy
            else:
                raise Exception("-Could not find within coordinates.")
        elif self.count.scan == 1:
            print("-Not within coordinates or scan count", end="", flush=True)
        else:
            raise Exception("-Could not find within coordinates.")

    def click_key_and_wait(self, key, filename):
        max_attempts = 3
        for attempt in range(max_attempts):
            self.activate_bs_and_click_key(key)
            if self.wait_for_img_appear(filename):
                return True
        raise Exception("-Exiting process because button could not be found.")

    @staticmethod
    def wait_for_img_appear(filename, confidence_threshhold=0.70):
        """
        Waits for python to find the image on screen.
        :param filename: see class for filenames
        :param confidence_threshhold: 
        :return: boolean button appearing
        """
        try:
            timeout = datetime.now() + timedelta(seconds=10)
            while datetime.now() < timeout:
                if pyautogui.locateOnScreen(filename, confidence=confidence_threshhold):
                    return True
            print("-Could not find: ", filename)
            return False
        except Exception as e:
            print(e)

    def activate_bs_and_click_key(self, key, max_attempts=10):
        """
        Sets bluestacks to focus and sends key input to the window.
        :param key:
        :param max_attempts: how many times it's going to try
        """
        print("_attempt:", end="", flush=True),
        for attempt in range(max_attempts):
            print(attempt, end="", flush=True)
            try:
                # Sends windows key. Don't touch the first sleep timer - but the second one determines how many times
                # it's clicked. Longer = more continuous clicks. Don't set below .3 because then it only clicks once.
                sleep(.3)  # hold button
                win32gui.SetForegroundWindow(self.bs_hwnd)  # activate windows
                win32api.keybd_event(key, 0, 1, 0)
                sleep(.3)  # release button
                win32gui.SetForegroundWindow(self.bs_hwnd)  # activate windows
                win32api.keybd_event(key, 0, 1 | 2, 0)
                break
            except (Exception, ):
                if attempt < max_attempts - 1:
                    sleep(1)
                    continue
                else:
                    raise Exception("-Could not activate or click.")


if __name__ == '__main__':
    main = RefreshSecretShop()
