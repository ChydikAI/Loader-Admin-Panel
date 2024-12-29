import ctypes
import sys
import time
import platform
import os
import hashlib
import uuid
import random
import requests
import psutil
import socket
from time import sleep
from datetime import datetime, UTC
from colorama import Fore, Style, init
import wmi
import threading

init(autoreset=True)


API_URL = 'http://127.0.0.1:5000/validate'
KEY_PATH = 'C:\\key.txt'

def random_console_title():
    while True:
        title = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=12))
        if platform.system() == 'Windows':
            os.system(f'title {title}')
        elif platform.system() in ['Linux', 'Darwin']:
            sys.stdout.write(f"\033]0;{title}\007")
            sys.stdout.flush()
        time.sleep(0.1)

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Darwin':
        os.system("clear && printf '\033[3J'")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_with_admin_rights():
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
    except Exception as e:
        print(Fore.RED + f"Не удалось запросить права администратора: {e}")
        sys.exit(1)
def loading_animation(text, duration=3):
    print(Fore.CYAN + text, end="", flush=True)
    for _ in range(duration):
        for dot in "...":
            print(dot, end="", flush=True)
            time.sleep(0.5)
    print(Style.RESET_ALL + "\n")

def get_hwid():
    c = wmi.WMI()
    try:
        cpu = c.Win32_Processor()[0].Name.strip()
        motherboard_model = c.Win32_BaseBoard()[0].Product.strip()
        motherboard_serial = c.Win32_BaseBoard()[0].SerialNumber.strip()
        motherboard = f"{motherboard_model} (S/N: {motherboard_serial})"
        bios_version = c.Win32_BIOS()[0].Version[0].strip()
        bios_date = c.Win32_BIOS()[0].ReleaseDate.strip()
        disk = c.Win32_DiskDrive()[0].SerialNumber.strip()
        gpu = c.Win32_VideoController()[0].Name.strip()
        ram = sum(int(mem.Capacity) for mem in c.Win32_PhysicalMemory()) // (1024 ** 3)
        monitor = c.Win32_DesktopMonitor()[0].Caption.strip()
        os_name = platform.system() + " " + platform.release()
        arch = platform.architecture()[0]
        mac_address = ":".join([f"{(uuid.getnode() >> ele) & 0xff:02x}" for ele in range(0, 8 * 6, 8)][::-1])

        hwid_raw = f"Процессор:{cpu}-Материнская плата:{motherboard}-Версия BIOS:{bios_version}-Дата BIOS:{bios_date}-Диск:{disk}-Видеокарта:{gpu}-ОЗУ:{ram}ГБ-Монитор:{monitor}-ОС:{os_name}-Архитектура:{arch}-MAC-адрес:{mac_address}"
        hwid = hashlib.sha256(hwid_raw.encode('utf-8')).hexdigest()
        return hwid, cpu, motherboard, bios_version, bios_date, disk, gpu, ram, monitor, os_name, arch, mac_address
    except Exception as e:
        print(Fore.RED + f"Ошибка при получении HWID: {e}")
        return ("неизвестно",) * 12

def get_ip():
    try:
        external_ip = requests.get('https://api.ipify.org').text
        return external_ip
    except Exception as e:
        print(Fore.RED + f"Ошибка получения IP-адреса: {e}")
        return "неизвестно"

def validate_key(key, hwid, cpu, motherboard, bios_version, bios_date, disk, gpu, ram, monitor, os_name, arch, mac_address, ip, loader_version="1.0.0"):
    system_info = {
        'hwid': hwid,
        'processor': cpu,
        'motherboard': motherboard,
        'bios_version': bios_version,
        'bios_date': bios_date,
        'disk': disk,
        'gpu': gpu,
        'ram': ram,
        'monitor': monitor,
        'os_name': os_name,
        'arch': arch,
        'mac_address': mac_address,
        'ip': ip,
    }
    data = {
        'key': key,
        'hwid': hwid,
        'loader_version': loader_version,
        'system_info': system_info
    }
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('valid', False):
                print(Fore.GREEN + "Ключ валиден!")
                return True
            else:
                error_message = response_data.get('error', 'Ошибка проверки ключа.')
                print(Fore.RED + f"Ошибка: {error_message}")
                if os.path.exists(KEY_PATH):
                    os.remove(KEY_PATH)
                    print(Fore.YELLOW + "Сохраненный ключ удален.")
                return False
        else:
            error_message = response.json().get('error', 'Неизвестная ошибка')
            print(Fore.RED + f"Ошибка API: {error_message}")
            if os.path.exists(KEY_PATH):
                os.remove(KEY_PATH)
                print(Fore.YELLOW + "Сохраненный ключ удален.")
            return False
    except Exception as e:
        print(Fore.RED + f"Ошибка подключения к API: {e}")
        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
            print(Fore.YELLOW + "Сохраненный ключ удален.")
        return False

def download_and_execute():

    random_filename = f"{uuid.uuid4().hex}.exe"
    temp_path = os.path.join(os.getenv('TEMP'), random_filename)
    url = 'http://http://127.0.0.1:5000/hack.exe'  # Замените на ваш external cheat

    print(Fore.YELLOW + "Запуск чита...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(response.content)

        print(Fore.GREEN + f"Файл загружен ")
        os.startfile(temp_path)

        sleep(10)
        print(Fore.RED + "Spoofing...")
    except requests.RequestException as e:
        print(Fore.RED + f"Ошибка загрузки файла: {e}")
    except Exception as e:
        print(Fore.RED + f"Ошибка выполнения: {e}")
def display_system_info(hwid, cpu, motherboard, bios_version, bios_date, disk, gpu, ram, monitor, os_name, arch, mac_address, ip):
    print(Fore.MAGENTA + "[Системная информация]")
    print(Fore.CYAN + f"HWID: {Fore.GREEN}{hwid}")
    print(Fore.CYAN + f"Процессор: {Fore.GREEN}{cpu}")
    print(Fore.CYAN + f"Материнская плата: {Fore.GREEN}{motherboard}")
    print(Fore.CYAN + f"Версия BIOS: {Fore.GREEN}{bios_version}")
    print(Fore.CYAN + f"Дата BIOS: {Fore.GREEN}{bios_date}")
    print(Fore.CYAN + f"Диск: {Fore.GREEN}{disk}")
    print(Fore.CYAN + f"Видеокарта: {Fore.GREEN}{gpu}")
    print(Fore.CYAN + f"ОЗУ: {Fore.GREEN}{ram}ГБ")
    print(Fore.CYAN + f"Монитор: {Fore.GREEN}{monitor}")
    print(Fore.CYAN + f"Операционная система: {Fore.GREEN}{os_name}")
    print(Fore.CYAN + f"Архитектура: {Fore.GREEN}{arch}")
    print(Fore.CYAN + f"MAC-адрес: {Fore.GREEN}{mac_address}")
    print(Fore.CYAN + f"Внешний IP: {Fore.GREEN}{ip}")

def save_key_to_temp(key):
    try:
        with open(KEY_PATH, 'w') as file:
            file.write(key)
    except Exception as e:
        print(Fore.RED + f"Ошибка сохранения ключа: {e}")

def load_key_from_temp():
    if os.path.exists(KEY_PATH):
        try:
            with open(KEY_PATH, 'r') as file:
                return file.read().strip()
        except Exception as e:
            print(Fore.RED + f"Ошибка чтения ключа: {e}")
    return None

def main_menu():
    try:

        if not is_admin():
            print(Fore.RED + "Эта программа требует запуска с правами администратора.")
            print(Fore.YELLOW + "Перезапуск программы с запросом прав администратора...")
            restart_with_admin_rights()
            sys.exit(0)


        key = load_key_from_temp()
        if key:
            print(Fore.CYAN + "Найден сохраненный ключ. Используем его для проверки...")
        else:
            key = input(Fore.CYAN + 'Введите ключ: ' + Style.RESET_ALL)
            save_key_to_temp(key)

        hwid, cpu, motherboard, bios_version, bios_date, disk, gpu, ram, monitor, os_name, arch, mac_address = get_hwid()
        ip = get_ip()

        loading_animation("Проверка системы", 5)
        display_system_info(hwid, cpu, motherboard, bios_version, bios_date, disk, gpu, ram, monitor, os_name, arch, mac_address, ip)

        loader_version = "1.1"

        if validate_key(key, hwid, cpu, motherboard, bios_version, bios_date, disk, gpu, ram, monitor, os_name, arch, mac_address, ip, loader_version):
            print(Fore.GREEN + "Авторизация успешна!")
            download_and_execute()
        else:
            sleep(5)
            os._exit(1)

        sleep(1)
        clear()
        os._exit(1)

    except KeyboardInterrupt:
        print(Fore.RED + "\nПрограмма завершена.")
        os._exit(1)


threading.Thread(target=random_console_title, daemon=True).start()
clear()
loading_animation("BootStarting", 3)
main_menu()
