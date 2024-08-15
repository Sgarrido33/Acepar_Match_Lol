import pyautogui
import cv2
import numpy as np
import time

template = cv2.imread('PartidaEncontrada.jpg', 0)

while True:

    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    gray_scale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Buscar la imagen en la screenshot
    result = cv2.matchTemplate(gray_scale_screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Umbral para la deteccion
    umbral = 0.7
    loc_coords = np.where(result >= umbral)

    # Si se encuentra la imagen
    if len(loc_coords[0]) > 0:
        # Primer match
        x, y = loc_coords[1][0], loc_coords[0][0]
        # Mover un poco hacia el centro por sea
        x += 80
        y += 30

        pyautogui.moveTo(x, y)
        pyautogui.click()
        # Tiempo para ver si fue aceptada la partida
        time.sleep(11)

        champion_select_template = cv2.imread('PantallaSeleccionCampeon.PNG', 0)
        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        gray_scale_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray_scale_screenshot, champion_select_template, cv2.TM_CCOEFF_NORMED)

        # Salimos del bucle si la partida fue aceptada y estamos en la selección de campeon
        if np.any(result >= umbral):
            break


    time.sleep(0.5)
