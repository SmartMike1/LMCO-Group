import os
import io
import zipfile
import requests
import threading
import subprocess
import sys
import traceback
import os
import tkinter as tk
from tkinter import ttk, messagebox

# ==== Настройки ====
GITHUB_ZIP_URL = "https://github.com/SmartMike1/LMCO-Group/archive/refs/heads/main.zip"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/SmartMike1/LMCO-Group/main/version.txt"
LOCAL_VERSION_FILE = "version.txt"
MAIN_SCRIPT = "Diplom.py"
REPO_SUBDIR = "LMCO-Group-main/"


def get_local_version():
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


def get_remote_version():
    try:
        response = requests.get(REMOTE_VERSION_URL, timeout=10)
        return response.text.strip()
    except Exception:
        return None


def download_and_extract_update(update_log_callback):
    update_log_callback("🔄 Скачивание обновлений...")
    response = requests.get(GITHUB_ZIP_URL)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        for member in zip_ref.namelist():
            if member.startswith(REPO_SUBDIR):
                rel_path = member.replace(REPO_SUBDIR, "")
                if rel_path:
                    full_path = os.path.join(".", rel_path)
                    if member.endswith("/"):
                        os.makedirs(full_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        with open(full_path, "wb") as f:
                            f.write(zip_ref.read(member))
    update_log_callback("✅ Обновление завершено.")


def run_main_script():
    try:
        with open("error.log", "w") as log_file:
            log_file.write("[Запуск Diplom.py]\n")
            subprocess.Popen(
                [sys.executable, MAIN_SCRIPT],
                stdout=log_file,
                stderr=log_file,
                shell=True
            )
            log_file.write("[Diplom.py запущен]\n")
    except Exception as e:
        with open("error.log", "a") as log_file:
            log_file.write(f"\n[Launcher Error] {e}\n")
            log_file.write(traceback.format_exc())

# ==== GUI интерфейс ====
class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMCO-Group – обновление")
        self.geometry("400x150")
        self.resizable(False, False)

        self.label = ttk.Label(self, text="Подготовка к запуску...", font=("Segoe UI", 11))
        self.label.pack(pady=20)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=30)

        self.after(300, self.start_update_thread)

    def log(self, message):
        self.label.config(text=message)
        self.update_idletasks()

    def start_update_thread(self):
        threading.Thread(target=self.update_and_run).start()

    def update_and_run(self):
        try:
            self.progress.start()
            self.log("Проверка версии...")

            local_version = get_local_version()
            remote_version = get_remote_version()

            if remote_version and local_version != remote_version:
                self.log(f"Найдена новая версия: {remote_version}")
                download_and_extract_update(self.log)
                with open(LOCAL_VERSION_FILE, "w") as f:
                    f.write(remote_version)
            else:
                self.log("Обновление не требуется.")

            self.progress.stop()
            self.log("Запуск приложения...")
            self.update_idletasks()
            run_main_script()  # тут subprocess блокирует поток
            self.destroy()

        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Ошибка запуска", f"Произошла ошибка: {e}")
            self.destroy()


if __name__ == "__main__":
    LauncherApp().mainloop()
