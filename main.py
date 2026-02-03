import sys
if sys.platform.startswith("win"):
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()

from pynput import mouse, keyboard
from pynput.mouse import Controller , Button
from visual import MouseLabel, Overlay
from PyQt5.QtWidgets import QApplication
import sys
import threading
import time
import pyautogui

mouserController = Controller()

class State:
    ctrl_l = False
    shift_r = False
    running = False
    position = []
    click_delay = 0.30

def remove_point_if_hit(x_click, y_click, radius=8):
    if State.running:
        return False
    for i in range(len(State.position) - 1, -1, -1):
        x, y = State.position[i]

        dx = x_click - x
        dy = y_click - y

        if dx * dx + dy * dy <= radius * radius:
            del State.position[i]
            return True
    return False

def save_positions(x, y, button, pressed):
    if State.running:
        return
    
    if button != mouse.Button.left or not pressed:
        return
    
    if State.ctrl_l:
        removed = remove_point_if_hit(x,y)

        if not removed:
            cord = (x,y)
            State.position.append(cord)
        
        overlay.update()


def on_key_press(key):
    if key == keyboard.Key.esc:
        if State.running:
            State.running = False
            print("AutoClick interrompido")
            return
        
        print("Encerrando o programa...")
        mouse_listener.stop()
        QApplication.quit() 
        return False      

    if State.running:
        return
    
    if key == keyboard.Key.ctrl_l:
        State.ctrl_l = True

    if key == keyboard.Key.shift_r:
        if not State.running:
            startAutoClick()

    
          

def on_key_release(key):
    if key == keyboard.Key.ctrl_l:
        State.ctrl_l = False
    if key == keyboard.Key.shift_r:
        State.shift_r = False


def on_Scroll_delay(x,y,button,direction):
    if direction > 0:
        State.click_delay += 0.1
        mouse_label.update()
    else:
        State.click_delay -= 0.1
        if State.click_delay < 0.1:
            State.click_delay = 0.0001
        mouse_label.update()

def startAutoClick():
    if State.running or not State.position:
        return
    
    State.running = True
    t = threading.Thread(target=autoClickLoop , daemon=True).start()
        

user32 = ctypes.windll.user32
def autoClickLoop():
    while State.running:
        for x,y in State.position:
            if not State.running:
                break
            user32.SetCursorPos(int(x+10) , int(y))
            mouserController.click(button=Button.left , count=1)
            time.sleep(State.click_delay)

app = QApplication(sys.argv)

overlay = Overlay(State.position)
overlay.show()

mouse_listener = mouse.Listener(on_click=save_positions , on_scroll=on_Scroll_delay)
keyboard_listener = keyboard.Listener(on_press=on_key_press , on_release=on_key_release)

mouse_label = MouseLabel(State)
mouse_listener.start()
keyboard_listener.start()

sys.exit(app.exec_())