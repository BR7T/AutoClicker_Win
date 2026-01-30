# 🖱️ AutoClicker for Windows (Multi-Monitor & DPI Fix)

Um **AutoClicker for windows**, builded using **Python + PyQt5**, with visual overlay, complete suport for **multi-screen**, **DPI Scaling**, floating HUD and dinamic click delay

##  Features

-  Visual click point markers (transparent overlay)

-  Automatic numbering of click points

-  Full multi-monitor support

-  DPI scaling correction (Windows)

-  Smart floating HUD interface

-  Sequential autoclick based on a list of positions

-  Real-time adjustable delay (mouse scroll)

-  Editing locked while autoclick is running

-  Safe interruption using the `ESC` key

## Tecnologies
- **Python 3.10+**
- **PyQt5** - GUI
- **pynput** - Keyboard and mouse Capture
- **pyautogui** - Cursor Movement
- **Windows DPI Awarness API** - Scaling Correction

## Controls
| Action | Key/Mouse|
| ----------------- | --------- |
| Add Point   | `Ctrl + Left Click`|
| Remove Point     | `Ctrl + Click on marker`|
| Start autoclick | `Right Shift`|
| Stop autoclick   | `ESC`|
| Ajustar delay     | Mouse scroll |

## How to Run
### 1. Clone the repository
```
git clone https://github.com/BR7T/AutoClicker_Win.git
cd AutoClicker_Win
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the application
```
python main.py
```