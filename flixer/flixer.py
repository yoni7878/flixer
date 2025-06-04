import subprocess
import sys
import time
import os
import threading

# ─── Auto-install missing pip packages ────────────────────────────────────────────
def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Map “pip name” → “import name”
packages = {
    "rich": "rich",
    "selenium": "selenium",
    "bs4": "bs4",
    "keyboard": "keyboard",
    "pyautogui": "pyautogui",
    "webdriver-manager": "webdriver_manager",
    "datetime": "datetime",
    "pygame": "pygame"
}

for pkg_name, import_name in packages.items():
    install_if_missing(import_name)

print("✅ All required packages installed.")

# ─── Imports (after auto-install) ────────────────────────────────────────────────
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import json
import random
from datetime import datetime
import pygame

console = Console()
page = 1  # Needed to avoid NameError when referencing 'page' in main_menu


def play(name: str):
    pygame.mixer.init()
    pygame.mixer.music.load(f"sounds/{name}")
    pygame.mixer.music.play()

# ─── Rich menu functions ─────────────────────────────────────────────────────────
def show_command_list():
    play("notif.wav")

    help_width = 60
    help_top = "┌" + "─" * help_width + "┐"
    help_bottom = "└" + "─" * help_width + "┘"
    help_lines = [
        "│Command list:                                               │",
        "│--------------------------------------------------          │",
        "│1, 2, 3 - Launch respective typing games.                   │",
        "│help    - Show menu explanation.                            │",
        "│clist/commands - Show this command list.                    │",
        "│exit    - Quit the program.                                 │",
        "│clear   - Clear the console screen.                         │",
        "│version - Show program version info.                        │",
        "│next - Show next page.                                      │",
        "│prev - Show previous page.                                  │",
        "│speed - Set typing speed.                                   │",
        "│restart - Self explanatory.                                 │",
        "│                                                            │",
        "│Use the number or command to navigate quickly!              │"
    ]

    full_output = [help_top] + help_lines + [help_bottom]
    for line in full_output:
        console.print(Align.center(Text(line, style="green" if "─" not in line else "dim green")))

# ─── Path Setup ───────────────────────────────────────────────────────────────
BASE_DIR = "logs"  # You can change this folder name
os.makedirs(BASE_DIR, exist_ok=True)  # Create it if it doesn't exist
BIN_DIR = "config"
os.makedirs(BIN_DIR, exist_ok=True)
SOUND_DIR = "sounds"
os.makedirs(SOUND_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # safe for filenames

LOG_FILE = os.path.join(BASE_DIR, f"{timestamp}.log")
INFO_LOG = os.path.join(BASE_DIR, f"{timestamp}.info")

def send_log(text, color="white", newline=""):
    play("notif.wav")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{newline}[{current_time}] [LOG]: {text}"
    console.print(Text(msg, style=color))
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def send_info(text, color="cyan", newline=""):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{newline}[{current_time}] [INFO]: {text}"
    console.print(Text(msg, style=color))
    with open(INFO_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Config 
TAP_DIR = os.path.join(SOUND_DIR, "tap-effects")

CONFIG_FILE = os.path.join(BIN_DIR, "config.json")

pygame.mixer.init()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def load_config():
    default_config = {"typing_speed": 0.05}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        save_config(default_config)
        return default_config
    
def get_rand_tap():
    if os.path.exists(TAP_DIR):
        files = [f for f in os.listdir(TAP_DIR) if f.endswith(".wav")]
        if files:
            return os.path.join(TAP_DIR, random.choice(files))
    return None

def none(char):

    return char

def play_tap_a(text):
    for char in text:
        time.sleep(typing_speed + 0.002)
        none(char)
        tap_path = get_rand_tap()
        if tap_path:
            sound = pygame.mixer.Sound(tap_path)
            sound.set_volume(0.7)
            sound.play()

def play_tap():
    tap_path = get_rand_tap()
    if tap_path:
        sound = pygame.mixer.Sound(tap_path)
        sound.set_volume(0.7)
        sound.play()

config = load_config()
typing_speed = config.get("typing_speed")

def simulate_checking_tokens():

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Loading...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)

def main_menu():
    console.clear()
    simulate_checking_tokens()
    colors = ["green", "bold green"]

    title_lines = [
        "███████╗██╗     ██╗██╗  ██╗███████╗██████╗ ",
        "██╔════╝██║     ██║╚██╗██╔╝██╔════╝██╔══██╗",
        "█████╗  ██║     ██║ ╚███╔╝ █████╗  ██████╔╝",
        "██╔══╝  ██║     ██║ ██╔██╗ ██╔══╝  ██╔══██╗",
        "██║     ███████╗██║██╔╝ ██╗███████╗██║  ██║",
        "╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
        f"\n\nThe best selenium typing cheat!",
        f"\n Your speed is: {typing_speed}"
    ]

    for line in title_lines:
        st = Text()
        for i, char in enumerate(line):
            st.append(char, style=colors[i % len(colors)])
        console.print(Align.center(st))

    menu_line = Text()

    if page == 1:
        menu_line.append("1: Nitro Type", style="bold green")
        menu_line.append(" │ ")
        menu_line.append("2: Type Racer", style="bold blue")
        menu_line.append(" │ ")
        menu_line.append("3: Key Mash", style="bold magenta")
    elif page == 2:
        menu_line.append("1: Monkey Type", style="bold green")
        menu_line.append(" │ ")
        menu_line.append("2: Human Benchmark", style="bold blue")
        menu_line.append(" │ ")
        menu_line.append("3: Typer.io", style="bold magenta")

    menu_line.append(" │ ")
    menu_line.append("TYPE 'help' for more explanation.", style="bold red")
    menu_line.append(" │ ")
    menu_line.append("TYPE 'clist' for commands.", style="bold yellow")

    box_width = len(menu_line.plain) + 2
    top_bar = "┌" + "─" * box_width + "┐"
    bottom_bar = "└" + "─" * box_width + "┘"
    filler_text = f"Select an option below (Page {page}/2)"
    filler_line = "│" + filler_text.center(box_width) + "│"

    console.print(Align.center(Text(top_bar, style="dim green")))
    console.print(Align.center(Text(filler_line, style="dim green")))
    console.print(
        Align.center(
            Text("│ ", style="dim green") + menu_line + Text(" │", style="dim green")
        )
    )
    console.print(Align.center(Text(bottom_bar, style="dim green")))
    play("start.wav")

def menu_loop():
    global typing_speed
    global page
    typing_speed = config.get("typing_speed") or 0.05 # Default speed
    username = os.getlogin()

    while True:

        token = console.input(f"\n[bold green]{username}@main > [/bold green]").lower()

        # Handle page switching
        if token == "next":
            page = 2 if page == 1 else 1
            play_tap()
            send_info(f"Switched to page {page}.", "green", "\n")
            main_menu()
            play("next.wav")
            continue

        # Handle typing game selections
        if page == 1:
            if token == "1":
                return "nitrotype"
            elif token == "2":
                return "typeracer"
            elif token == "3":
                return "keymash"
        elif page == 2:
            if token == "1":
                return "monkeytype"
            elif token == "2":
                return "humanbenchmark"
            elif token == "3":
                return "typerio"

        # Other commands
        if token == "help":
            play_tap()
            help_text = [
                "Menu explained:",
                "A menu meant for cheating in typing games.",
                "",
                "Options explained (Page 1):",
                "1 - Nitro Type: Online typing racing game.",
                "2 - Type Racer: Compete in typing races.",
                "3 - Key Mash: Quick typing challenge.",
                "",
                "Options explained (Page 2):",
                "1 - MonkeyType: Smooth typing test UI.",
                "2 - HumanBenchmark: Typing test under pressure.",
                "3 - Typer.io: Multiplayer typing battles.",
                "",
                "Type 'next' to switch pages!"
            ]
            play("notif.wav")

            max_len = max(len(line) for line in help_text)
            box_width = max_len + 4  # padding

            top_bar = "┌" + "─" * box_width + "┐"
            bottom_bar = "└" + "─" * box_width + "┘"

            console.print(Align.center(Text(top_bar, style="dim green")))
            for line in help_text:
                padded_line = f"  {line.ljust(max_len)}  "
                console.print(Align.center(Text(f"│{padded_line}│", style="green")))
            console.print(Align.center(Text(bottom_bar, style="dim green")))

        elif token in ["clist", "commands"]:
            show_command_list()
        elif token == "exit":
            console.print("[bold yellow]Exiting program...[/bold yellow]")
            sys.exit()
        elif token.lower() == "prev":
            play_tap()
            page = 1 if page == 2 else 2
            main_menu()
            play("next.wav")
            send_info(f"Switched to page {page}.", "green", "\n")
            continue
        elif token in ["reload", "restart"]:
            script_dir = os.path.dirname(os.path.abspath(__file__))

            batch_file = os.path.join(script_dir, "start.bat")
            subprocess.run(batch_file, shell=True, capture_output=False)

            sys.exit()

        elif token in ["clear", "cls"]:
            main_menu()
        elif token == "version":
            console.print("\n[bold cyan]Flixer V1.2[/bold cyan]")
        elif token == "speed":
            try:
                new_speed = float(Prompt.ask("[bold green]Enter typing speed (seconds per character):[/bold green]"))
                typing_speed = new_speed
                config["typing_speed"] = typing_speed
                save_config(config)
                console.print(f"\n[bold yellow]Typing speed set to {typing_speed} sec/char[/bold yellow]")
            except ValueError:
                console.print("[bold red]Invalid speed. Please enter a decimal number.[/bold red]")
        else:
            send_info("Invalid option! Try again.", "red", "\n")


# ─── Typing game logic ────────────────────────────────────────────────────────────
def get_nitrotype_text(driver):
    dash_copy = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.dash-copy"))
    )
    letters = dash_copy.find_elements(By.CSS_SELECTOR, "span.dash-letter")
    final_text = ""

    for letter in letters:
        classes = letter.get_attribute("class")
        if "is-typed" in classes or letter.find_elements(By.TAG_NAME, "img"):
            continue
        final_text += letter.text.replace('\xa0', ' ')

    return final_text

def get_typerio_text(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Gameboard_container__DtBpp"))
        )

        # Get all word wrappers
        word_wrappers = driver.find_elements(By.CSS_SELECTOR, "div.Gameboard_wrapper__R_X8I")
        text_to_type = []

        for wrapper in word_wrappers:
            # Find the word element which could be either a div or span with class Gameboard_word__IDrpz
            word_element = wrapper.find_element(By.CSS_SELECTOR, ".Gameboard_word__IDrpz")
            letter_spans = word_element.find_elements(By.CSS_SELECTOR, "span.Gameboard_letter__QiDmD")
            word_text = "".join(letter.text for letter in letter_spans)
            text_to_type.append(word_text)

        return " ".join(text_to_type)

    except Exception as e:
        console.print(f"[bold red]Error getting Typer.io text:[/bold red] {e}")
        return ""

def get_keymash_text(driver):
    try:
        # Wait for the container
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.match--text.match--mono"))
        )
    except:
        console.print("[bold red][ERROR] Timed out waiting for KeyMASH text container[/bold red]")
        return ""

    # Grab the container's full HTML
    container = driver.find_element(By.CSS_SELECTOR, "div.match--text.match--mono")
    html = container.get_attribute("innerHTML")

    soup = BeautifulSoup(html, "html.parser")
    upcoming = []

    # Find all spans with class match--letter
    for span in soup.find_all("span", class_="match--letter"):
        classes = span.get("class", [])
        text = span.get_text(strip=True)

        # Skip typed or highlighted letters
        if any(c in classes for c in ["match--correct", "bg-red-600", "bg-green-600"]):
            continue

        # Collect gray text (adjust if your gray class differs)
        if any(c.startswith("text-gray") for c in classes) and text:
            upcoming.append(text)

    raw = "".join(upcoming).strip()  # changed here, no split and no space
    if not raw:
        return ""
    return raw

def get_typeracer_text(driver):
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    spans = soup.find_all("span")
    text = ""

    for span in spans:
        if "unselectable" in str(span):
            text += span.text

    if not text:
        console.print("[bold red]No text found on TypeRacer![/bold red]")
        return None
    else:
        console.print(f"[bold green]Text to type:[/bold green] {text}")
    return text


def get_monkeytype_text(driver):
    # Find the container with words by id "words"
    try:
        container = driver.find_element(By.ID, "words")
    except:
        return ""

    # Find all word divs inside container
    words = container.find_elements(By.CLASS_NAME, "word")

    text_to_type = []

    for word in words:
        classes = word.get_attribute("class").split()
        # Skip typed or active words
        if "typed" in classes:
            continue
        
        # Each word is made up of letter elements, usually <letter> tags or spans
        # Let's try to get all child elements that represent letters
        letters = word.find_elements(By.TAG_NAME, "letter")
        if not letters:
            # fallback if <letter> tags don't exist, get text directly
            word_text = word.text
        else:
            # Join all letter texts
            word_text = "".join(letter.text for letter in letters)
        text_to_type.append(word_text)

    return " ".join(text_to_type)

def get_humanbenchmark_text(driver):
    try:
        letters_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.letters"))
        )

        spans = letters_div.find_elements(By.TAG_NAME, "span")

        text_to_type = []
        for span in spans:
            classes = span.get_attribute("class").split()
            if "incomplete" in classes:
                char = span.text
                # If it's visually blank but present, treat it as a space
                if char == "":
                    text_to_type.append(" ")
                else:
                    text_to_type.append(char)
        
        return "".join(text_to_type)

    except Exception as e:
        print(f"Error getting HumanBenchmark text: {e}")
        return ""


import threading
from pygame import mixer

import threading

def type_text(driver, site):
    global typing_speed
    play("start.wav")
    send_info(f"Starting typing for {site} with speed {typing_speed} sec/char.", "cyan", "\n")

    # Get text and selector based on site
    if site == "nitrotype":
        text = get_nitrotype_text(driver)
        selector = "input.dash-copy-input"
    elif site == "keymash":
        text = get_keymash_text(driver)
        selector = "input.match--input"
    elif site == "typeracer":
        text = get_typeracer_text(driver)
        selector = "input.txtInput"
    elif site == "monkeytype":
        text = get_monkeytype_text(driver)
        selector = "input#wordsInput"
    elif site == "humanbenchmark":
        text = get_humanbenchmark_text(driver)
        selector = "div.letters"
    elif site == "typerio":
        text = get_typerio_text(driver)
        selector = "input#input"
    else:
        send_log("Invalid site for typing.", "red", "\n")
        return

    if not text:
        console.print("[bold red]Nothing to type![/bold red]")
        return

    try:
        # Typing logic
        def typing_job():
            if site == "typeracer":
                input_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                input_box.click()
                input_box.clear()
                for char in text:
                    input_box.send_keys(char)
                    time.sleep(typing_speed)

            elif site == "keymash":
                input_box = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                input_box.click()
                time.sleep(0.3)
                input_box.clear()
                for char in text:
                    input_box.send_keys(char)
                    time.sleep(typing_speed)

            elif site == "monkeytype":
                driver.execute_script(f"document.querySelector('{selector}').focus()")
                pyautogui.typewrite(text, interval=typing_speed)

            elif site == "humanbenchmark":
                typing_area = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                typing_area.click()
                pyautogui.typewrite(text, interval=typing_speed)

            elif site == "typerio":
                input_div = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="button"].Editor_container__DN_YS'))
                )
                input_div.click()
                time.sleep(0.3)
                input_box = input_div.find_element(By.CSS_SELECTOR, 'input')
                input_box.clear()
                for char in text:
                    input_box.send_keys(char)
                    time.sleep(typing_speed)

            else:  # Default (e.g. nitrotype)
                driver.execute_script(f"document.querySelector('{selector}').focus()")
                pyautogui.typewrite(text, interval=typing_speed)

        # Sound logic
        def sound_job():
            if site in ["typeracer", "keymash", "typerio"]:
                for char in text:
                    if char.strip():
                        play_tap()
                    time.sleep(typing_speed)
            else:
                play_tap_a(text)  # Assume this handles the full string as one sound flow

        # Start typing and sound in parallel
        typing_thread = threading.Thread(target=typing_job)
        sound_thread = threading.Thread(target=sound_job)

        typing_thread.start()
        sound_thread.start()

        typing_thread.join()
        sound_thread.join()

        send_log("Finished typing text.", "green", "\n")

    except Exception as e:
        console.print(f"[bold red]Typing error:[/bold red] {e}")


def start_response():
    response = Prompt.ask("\n[bold green]Do you want to run the bot again? (y = same game, r = just repeat, n = main menu, q = quit)[/bold green]").lower()
    return response


def launch_typing_bot(site):
    send_info(f"Preparing to launch typing bot for site: {site}", "cyan", "\n")
    url_map = {
    "nitrotype": "https://www.nitrotype.com/race",
    "keymash": "https://keymash.io",
    "typeracer": "https://play.typeracer.com",
    "monkeytype": "https://monkeytype.com",
    "humanbenchmark": "https://humanbenchmark.com/tests/typing",
    "typerio": "https://typer.io"  # Add this line
    }

    url = url_map.get(site)
    if not url:
        send_log("Invalid site selected!", "red", "\n")
        return

    send_log(f"Opening browser to URL: {url}", "yellow", "\n")

    global chrome_options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    global service
    service = Service(ChromeDriverManager().install())
    global driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    if site == "typeracer":
        try:
            time.sleep(3)
            if not driver.find_elements(By.CSS_SELECTOR, "input.txtInput"):
                try:
                    WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cc-btn.cc-dismiss"))
                    ).click()
                except:
                    pass
        except Exception as e:
            console.print(f"[bold red]Error handling Typeracer popup:[/bold red] {e}")

    send_info("Waiting 2 seconds for game to load...", "cyan", "\n")
    time.sleep(2)

    def run_typing_session():
        send_info("Press CTRL + ALT + P to start typing...", "yellow", "\n")
        keyboard.wait("ctrl+alt+p")
        type_text(driver, site)
        send_info("Done with this typing bot session!", "cyan", "\n")

    # Run the first typing session
    run_typing_session()

    while True:
        response = Prompt.ask("\n[bold green]Do you want to run the bot again? (y = just repeat, n = main menu, q = quit)[/bold green]").lower()

        if response == 'y':
            # Just repeat the typing on the same page
            run_typing_session()
        elif response == 'n':
            main_menu
            driver.quit()
            break
        elif response == 'q':
            # Quit completely
            driver.quit()
            sys.exit()
        else:
            send_log("Invalid input. Please try again.", "red")

def main():
    continue_running = True
    while continue_running:
        main_menu()
        send_log("Waiting for user to select a site...", "yellow", "\n")
        selected_site = menu_loop()

        launch_typing_bot(selected_site)


if __name__ == "__main__":
    main()
