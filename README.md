# Проект Loader + Admin Panel 🚀

Loader — это мощный инструмент для управления ключами и проверки их валидности через API. Проект позволяет сохранить ключ на диск, проверить его через API и использовать для авторизации.

---

## 📋 Инструкции

### 1. Как использовать проект

1. **Скачайте репозиторий** с GitHub:
   ```bash
   git clone https://github.com/ChydikAI/Loader-Admin-Panel.git
   ```

2. **Убедитесь, что все зависимости установлены:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Запустите скрипт:**
   ```bash
   python main.py
   ```

4. **Введите ключ** при первом запуске. Ключ сохранится на диск `C:\key.txt`. Если ключ недействителен, он будет автоматически удалён.

---

### 2. Как собрать EXE-файл 🔧

Для сборки проекта в EXE-файл используйте `PyInstaller`:

1. Установите `PyInstaller`:
   ```bash
   pip install pyinstaller
   ```

2. Выполните команду для сборки:
   ```bash
   pyinstaller --onefile -i "NONE" main.py
   ```

3. Готовый файл будет находиться в папке `dist`.

---

### 3. Замените значения перед использованием

- **URL API:** Замените `http://127.0.0.1:5000/validate` в файле на реальный адрес вашего API.
- **Путь сохранения ключа:** При необходимости измените путь сохранения ключа `C:\key.txt`.

---

## 🛠️ Технологии

- Python 3.11+
- Библиотеки: `requests`, `wmi`, `colorama`, `pyinstaller`

---

## 💻 Поддержка

Если у вас возникли вопросы, свяжитесь с нами:

- Telegram: https://t.me/lilkitagawas
- GitHub Issues: [Loader-Admin-Pane/issues](https://github.com/ChydikAI/Loader-Admin-Panel/issues)

---

# Loader + Admin Panel Project 🚀

Loader is a powerful tool for managing keys and validating them via an API. The project allows you to save the key to disk, verify it through the API, and use it for authorization.

---

## 📋 Instructions

### 1. How to Use the Project

1. **Clone the repository** from GitHub:
   ```bash
   git clone https://github.com/ChydikAI/Loader-Admin-Panel.git
   ```

2. **Ensure all dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```bash
   python main.py
   ```

4. **Enter the key** on the first run. The key will be saved to `C:\key.txt`. If the key is invalid, it will be automatically deleted.

---

### 2. How to Build an EXE 🔧

To build the project into an EXE file, use `PyInstaller`:

1. Install `PyInstaller`:
   ```bash
   pip install pyinstaller
   ```

2. Execute the build command:
   ```bash
   pyinstaller --onefile -i "NONE" main.py
   ```

3. The final executable will be located in the `dist` folder.

---

### 3. Replace Values Before Use

- **API URL:** Replace `http://127.0.0.1:5000/validate` in the file with the actual URL of your API.
- **Key Save Path:** Modify the key save path `C:\key.txt` if necessary.

---

## 🛠️ Technologies

- Python 3.11+
- Libraries: `requests`, `wmi`, `colorama`, `pyinstaller`

---

## 💻 Support

If you have any questions, contact us:

- Telegram: https://t.me/lilkitagawas
- GitHub Issues: [Loader-Admin-Pane/issues](https://github.com/ChydikAI/Loader-Admin-Panel/issues)

