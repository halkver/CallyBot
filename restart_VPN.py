import pyautogui
from time import sleep
from credentials import Credentials
from help_methods import decrypt

pw = decrypt(Credentials().feide[1])


def restart_vpn():  # Server screen is 1366x768
    """Assume no program is above server, and icons in correct position
    All timings can and should be adapted to servers speed. Cordinates must be changed to screen resolution
    """
    pyautogui.moveTo(1201, 748)  # The location of the VPN in the toolbar
    sleep(5)
    pyautogui.click()
    pyautogui.moveTo(1289, 641)  # Location of connect button
    sleep(5)
    pyautogui.click()
    sleep(15)
    pyautogui.click()
    sleep(15)  # Wait of login to open
    pyautogui.typewrite(pw)
    pyautogui.press('enter')
    sleep(15)
