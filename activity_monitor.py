from pynput import keyboard, mouse
import time

last_activity = time.time()

def on_press(key):
    global last_activity
    last_activity = time.time()

def on_move(x, y):
    global last_activity
    last_activity = time.time()

def on_click(x, y, button, pressed):
    global last_activity
    last_activity = time.time()

def start_monitor():

    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_move=on_move,on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

def get_idle_time():

    return time.time() - last_activity
