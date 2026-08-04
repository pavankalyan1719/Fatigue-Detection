import time
from pynput import mouse, keyboard

start_time = time.time()
last_activity = time.time()

def on_move(x, y):
    global last_activity
    last_activity = time.time()

def on_click(x, y, button, pressed):
    global last_activity
    last_activity = time.time()

def on_press(key):
    global last_activity
    last_activity = time.time()

def start_tracking():
    mouse.Listener(on_move=on_move, on_click=on_click).start()
    keyboard.Listener(on_press=on_press).start()

    while True:
        screen_time = time.time() - start_time
        idle_time = time.time() - last_activity

        print("Total Screen Time:", round(screen_time/60,2), "minutes")

        if screen_time > 3600:
            print("⚠ Take a break! You used screen for 1 hour")

        time.sleep(60)

start_time = time.time()

def get_screen_time():

    current_time = time.time()

    screen_minutes = (current_time - start_time) / 60

    return round(screen_minutes,2)
