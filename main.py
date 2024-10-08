import tkinter as tk
import pyautogui
import cv2
import numpy as np
import time
import threading
import psutil
import pyttsx3
import win32gui

script_running = False
script_thread = None
engine = pyttsx3.init()
window_title = "League of Legends"

def is_window_on_screen(window_title):
    try:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd == 0:
            return False


        is_visible = win32gui.IsWindowVisible(hwnd)
        is_foreground = (hwnd == win32gui.GetForegroundWindow())

        return is_visible and is_foreground
    except Exception as e:
        print(f"Error: {e}")
    return False


def script_logic():
    template = cv2.imread('PartidaEncontrada.jpg', 0)
    while script_running:
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
            if is_window_on_screen(window_title):
                # Primer match
                x, y = loc_coords[1][0], loc_coords[0][0]
                # Mover un poco hacia el centro por sea
                x += 80
                y += 30

                pyautogui.moveTo(x, y)
                pyautogui.click()

                engine.say("Partida Encontrada")
                engine.runAndWait()

                # Tiempo para ver si fue aceptada la partida
                time.sleep(10)

        if check_lol_process():
            wait_end_match()
            break

        time.sleep(2)


def start_script():
    global script_running, script_thread
    if not script_running:
        script_running = True
        script_thread = threading.Thread(target=script_logic)
        script_thread.start()
        update_status()

def stop_script():
    global script_running
    script_running = False
    update_status()

def check_lol_process():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "League of Legends.exe":
            return True
    return False


def wait_end_match():
    while True:
        if check_lol_process():
            stop_script()

            while check_lol_process():
                time.sleep(20)

            start_script()
            break


def update_status():
    if script_running:
        status_indicator.config(bg="green", text="Activo")
    else:
        status_indicator.config(bg="red", text="Detenido")

def change_language(lang):
    print(f"Idioma cambiado a: {lang}")

def open_language_menu():
    language_button.config(relief="sunken")
    language_menu = tk.Menu(root, tearoff=0)
    languages = ["Japonés","Chino","Taiwanés","Español","Inglés","Coreano","Francés","Alemán","Italiano","Polaco","Rumano","Griego","Portugués","Húngaro","Ruso","Turco"]

    for lang in languages:
        language_menu.add_command(label=lang, command=lambda l=lang: change_language(l))

    x = language_button.winfo_rootx()
    y = language_button.winfo_rooty() + language_button.winfo_height()
    language_menu.tk_popup(x, y)

    language_button.config(relief="raised")

def close_language_menu(event=None):
    language_button.config(relief="raised")


# Ventana principal
root = tk.Tk()
root.title("AAP")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.125)
window_height = int(screen_height * 0.12)
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

icon = tk.PhotoImage(file="lol_icon.png")
root.iconphoto(False, icon)

# Botones de control
start_button = tk.Button(root, text="Empezar", command=start_script)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Detener", command=stop_script)
stop_button.pack(pady=5)

language_button = tk.Button(root, text="⚙", width=3, height=1, command=open_language_menu)
language_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

# Indicador visual de estado
status_indicator = tk.Label(root, text="Detenido", bg="red", fg="white", width=20)
status_indicator.pack(pady=10)

# Ventana Abierta
root.mainloop()

