import base64
import datetime
import json
import tkinter as tk
import webbrowser
from io import BytesIO
from tkinter import filedialog, simpledialog, messagebox, colorchooser, scrolledtext
from tkinter import ttk

from PIL import Image, ImageTk
from pygame import mixer

# Initialize mixer
mixer.init()

# Language dictionaries
LANGUAGES = {
    "en": {
        "title": "🎧 Mini Telegram",
        "date": "Date",
        "change_date": "📅 Change Date",
        "chat": "💬 Chat",
        "send": "📨 Send",
        "audio": "🎵 Audio",
        "add_track": "➕ Add Track",
        "play": "▶️ Play",
        "stop": "⏸️ Stop",
        "prev": "⏮️ Prev",
        "next": "⏭️ Next",
        "volume": "🔊 Volume",
        "duration": "Duration: 0:00",
        "now_playing": "Now Playing: -",
        "repeat": "🔁 Repeat",
        "playlist": "📂 Playlist",
        "new_playlist": "➕ New",
        "delete_track": "🗑️ Delete Track",
        "change_bg": "🎨 Change Background",
        "clear_chat": "🧹 Clear Chat",
        "toggle_theme": "🌗 Toggle Theme",
        "settings": "⚙️ Settings",
        "edit_code": "💻 Edit Code",
        "username": "Username:",
        "password": "Password:",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "change_avatar": "Change Avatar"
    },
    "uk": {
        "title": "🎧 Mini Telegram",
        "date": "Дата",
        "change_date": "📅 Змінити дату",
        "chat": "💬 Чат",
        "send": "📨 Надіслати",
        "audio": "🎵 Аудіо",
        "add_track": "➕ Додати трек",
        "play": "▶️ Відтворити",
        "stop": "⏸️ Зупинити",
        "prev": "⏮️ Назад",
        "next": "⏭️ Вперед",
        "volume": "🔊 Гучність",
        "duration": "Тривалість: 0:00",
        "now_playing": "Зараз грає: -",
        "repeat": "🔁 Повтор",
        "playlist": "📂 Плейлист",
        "new_playlist": "➕ Новий",
        "delete_track": "🗑️ Видалити трек",
        "change_bg": "🎨 Змінити фон",
        "clear_chat": "🧹 Очистити чат",
        "toggle_theme": "🌗 Змінити тему",
        "settings": "⚙️ Налаштування",
        "edit_code": "💻 Редагувати код",
        "username": "Ім'я користувача:",
        "password": "Пароль:",
        "login": "Увійти",
        "register": "Зареєструватися",
        "logout": "Вийти",
        "change_avatar": "Змінити аватар"
    },
    "ru": {
        "title": "🎧 Mini Telegram",
        "date": "Дата",
        "change_date": "📅 Изменить дату",
        "chat": "💬 Чат",
        "send": "📨 Отправить",
        "audio": "🎵 Аудио",
        "add_track": "➕ Добавить трек",
        "play": "▶️ Воспроизвести",
        "stop": "⏸️ Остановить",
        "prev": "⏮️ Назад",
        "next": "⏭️ Вперед",
        "volume": "🔊 Громкость",
        "duration": "Длительность: 0:00",
        "now_playing": "Сейчас играет: -",
        "repeat": "🔁 Повтор",
        "playlist": "📂 Плейлист",
        "new_playlist": "➕ Новый",
        "delete_track": "🗑️ Удалить трек",
        "change_bg": "🎨 Изменить фон",
        "clear_chat": "🧹 Очистить чат",
        "toggle_theme": "🌗 Сменить тему",
        "settings": "⚙️ Настройки",
        "edit_code": "💻 Редактировать код",
        "username": "Имя пользователя:",
        "password": "Пароль:",
        "login": "Войти",
        "register": "Зарегистрироваться",
        "logout": "Выйти",
        "change_avatar": "Сменить аватар"
    }
}

# Default settings
DEFAULT_SETTINGS = {
    "theme": {
        "bg_main": "#1e1e2e",
        "bg_box": "#2a2a40",
        "fg_text": "#ffffff",
        "btn_color": "#3b82f6",
        "btn_danger": "#ef4444",
        "btn_ok": "#10b981"
    },
    "user": {
        "username": "Guest",
        "avatar": None,
        "language": "en"
    },
    "users": {}
}


def stop_music():
    mixer.music.stop()


def change_volume(val):
    mixer.music.set_volume(float(val))


def round_rectangle(canvas, x1, y1, x2, y2, radius=15, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class LoginDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title(self.app.t("login"))
        self.geometry("300x200")
        self.resizable(False, False)

        tk.Label(self, text=self.app.t("username")).pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text=self.app.t("password")).pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text=self.app.t("login"), command=self.login).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.app.t("register"), command=self.register).pack(side=tk.LEFT, padx=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.app.user_settings["users"]:
            if self.app.user_settings["users"][username]["password"] == password:
                self.app.login_user(username)
                self.destroy()
            else:
                messagebox.showerror("Error", "Invalid password")
        else:
            messagebox.showerror("Error", "User not found")

    def register(self, **kwargs):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.app.user_settings["users"]:
            messagebox.showerror("Error", "Username already exists")
        elif username and password:
            self.app.user_settings["users"][username] = {
                "password": password,
                "avatar": None,
                "settings": {
                    "theme": DEFAULT_SETTINGS["theme"].copy(),
                    "language": "en"
                }
            }
            self.app.save_user_settings()
            self.app.login_user(username)
            self.destroy()
        else:
            messagebox.showerror("Error", "Username and password required")


class UserSettingsDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title(self.app.t("settings"))
        self.geometry("500x400")
        self.resizable(False, False)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # User tab
        self.user_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.user_tab, text=self.app.t("settings"))

        # Avatar
        tk.Label(self.user_tab, text=self.app.t("change_avatar")).pack(pady=5)
        self.avatar_btn = tk.Button(self.user_tab, text=self.app.t("change_avatar"), command=self.select_avatar)
        self.avatar_btn.pack(pady=5)

        # Language
        tk.Label(self.user_tab, text="Language:").pack(pady=5)
        self.lang_var = tk.StringVar(value=self.app.user_settings["user"]["language"])
        lang_menu = ttk.Combobox(self.user_tab, textvariable=self.lang_var, values=list(LANGUAGES.keys()))
        lang_menu.pack(pady=5)
        lang_menu.bind("<>", self.change_language)

        # Theme tab
        self.theme_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.theme_tab, text="Theme")

        colors = [
            ("Main Background", "bg_main"),
            ("Box Background", "bg_box"),
            ("Text Color", "fg_text"),
            ("Primary Button", "btn_color"),
            ("Danger Button", "btn_danger"),
            ("OK Button", "btn_ok")
        ]

        self.color_btns = {}
        for i, (label, key) in enumerate(colors):
            frame = tk.Frame(self.theme_tab)
            frame.pack(fill=tk.X, padx=10, pady=5)

            tk.Label(frame, text=label).pack(side=tk.LEFT)
            btn = tk.Button(frame, text="Change",
                            command=lambda k=key: self.change_color(k))
            btn.pack(side=tk.RIGHT)
            self.color_btns[key] = btn

        # Save button
        tk.Button(self, text="Save", command=self.save_settings).pack(pady=10)

    def select_avatar(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if filepath:
            try:
                with open(filepath, "rb") as f:
                    self.app.user_settings["user"]["avatar"] = base64.b64encode(f.read()).decode('utf-8')
                messagebox.showinfo("Success", "Avatar image selected")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def change_color(self, key):
        color = colorchooser.askcolor(title=f"Select {key} color")[1]
        if color:
            self.app.user_settings["theme"][key] = color

    def change_language(self, event):
        lang = self.lang_var.get()
        self.app.user_settings["user"]["language"] = lang
        self.app.update_language()

    def save_settings(self):
        self.app.save_user_settings()
        self.app.update_ui_theme()
        self.destroy()


class CodeEditorDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title(self.app.t("edit_code"))
        self.geometry("800x600")

        # Text area with scrollbar
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Load current code
        with open(__file__, "r", encoding="utf-8") as f:
            self.code = f.read()
        self.text_area.insert(tk.END, self.code)

        # Button frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="Save", command=self.save_code).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Open in External Editor",
                  command=self.open_external).pack(side=tk.RIGHT, padx=5)

    def save_code(self):
        new_code = self.text_area.get("1.0", tk.END)
        try:
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(new_code)
            messagebox.showinfo("Success", "Code saved. Please restart the application.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save code: {str(e)}")

    def open_external(self):
        try:
            webbrowser.open(__file__)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open editor: {str(e)}")


class MiniTelegramApp:
    def __init__(self, master):
        self.master = master
        self.load_user_settings()

        # Initialize fonts
        self.FONT_TITLE = ("Segoe UI", 14, "bold")
        self.FONT_TEXT = ("Segoe UI", 11)

        # Setup UI
        self.setup_ui()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def t(self, key):
        """Translate text based on current language"""
        lang = self.user_settings["user"]["language"]
        return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key)

    def load_user_settings(self):
        try:
            with open("user_settings.json", "r", encoding="utf-8") as f:
                self.user_settings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.user_settings = DEFAULT_SETTINGS.copy()
            self.save_user_settings()

    def save_user_settings(self):
        try:
            with open("user_settings.json", "w", encoding="utf-8") as f:
                json.dump(self.user_settings, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            return False

    def login_user(self, username):
        self.user_settings["user"] = {
            "username": username,
            "avatar": self.user_settings["users"][username].get("avatar"),
            "language": self.user_settings["users"][username]["settings"].get("language", "en")
        }
        self.user_settings["theme"] = self.user_settings["users"][username]["settings"]["theme"]
        self.save_user_settings()
        self.update_ui_theme()
        self.update_language()

    def logout_user(self):
        self.user_settings["user"] = DEFAULT_SETTINGS["user"].copy()
        self.user_settings["theme"] = DEFAULT_SETTINGS["theme"].copy()
        self.save_user_settings()
        self.update_ui_theme()
        self.update_language()

    def update_language(self):
        self.master.title(self.t("title"))
        # Need to update all UI elements with translated text
        # This is a simplified version - in a full implementation,
        # you would need to update all text elements in the UI

    def update_ui_theme(self):
        theme = self.user_settings["theme"]
        self.master.config(bg=theme["bg_main"])

        # Update widgets that need manual updating
        if hasattr(self, 'main_canvas'):
            self.main_canvas.config(bg=theme["bg_main"])
            self.main_frame.config(bg=theme["bg_main"])

    def setup_ui(self):
        theme = self.user_settings["theme"]

        # Main canvas and scrollbar
        self.main_canvas = tk.Canvas(self.master, bg=theme["bg_main"], highlightthickness=0)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.main_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        self.main_frame = tk.Frame(self.main_canvas, bg=theme["bg_main"])
        self.main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.main_frame.bind("",
                             lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.bind_all("", self._on_mousewheel)

        # Top frame with user info
        top_frame = tk.Frame(self.main_frame, bg=theme["bg_main"])
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # User avatar
        if self.user_settings["user"]["avatar"]:
            try:
                avatar_data = base64.b64decode(self.user_settings["user"]["avatar"])
                image = Image.open(BytesIO(avatar_data))
                image = image.resize((40, 40), Image.LANCZOS)
                self.avatar_img = ImageTk.PhotoImage(image)
                self.avatar_label = tk.Label(top_frame, image=self.avatar_img, bg=theme["bg_main"])
                self.avatar_label.pack(side=tk.LEFT)
            except Exception as e:
                print(f"Error loading avatar: {str(e)}")

        # Date label
        self.date_label = tk.Label(top_frame, text=datetime.date.today().strftime("%d.%m.%Y"),
                                   font=self.FONT_TEXT, bg=theme["bg_main"], fg=theme["fg_text"])
        self.date_label.pack(side=tk.LEFT)

        # Buttons
        btn_frame = tk.Frame(top_frame, bg=theme["bg_main"])
        btn_frame.pack(side=tk.RIGHT)

        tk.Button(btn_frame, text=self.t("settings"), font=self.FONT_TEXT, command=self.open_settings,
                  bg=theme["btn_color"], fg="white", relief=tk.FLAT, bd=0).pack(side=tk.RIGHT, padx=5)

        tk.Button(btn_frame, text=self.t("edit_code"), font=self.FONT_TEXT, command=self.open_code_editor,
                  bg=theme["btn_color"], fg="white", relief=tk.FLAT, bd=0).pack(side=tk.RIGHT, padx=5)

        tk.Button(btn_frame, text=self.t("change_date"), font=self.FONT_TEXT, command=self.change_date,
                  bg=theme["btn_color"], fg="white", relief=tk.FLAT, bd=0).pack(side=tk.RIGHT, padx=5)

        # Rest of the UI setup would continue here...
        # (Chat frame, audio controls, playlist, etc.)

    def open_settings(self):
        UserSettingsDialog(self.master, self)

    def open_code_editor(self):
        CodeEditorDialog(self.master, self)

    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def change_date(self):
        date = simpledialog.askstring(self.t("change_date"), "Enter new date (dd.mm.yyyy):")
        if date:
            self.date_label.config(text=date)

    def on_close(self):
        if self.save_user_settings():
            self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniTelegramApp(root)

    # Show login dialog if not logged in
    if app.user_settings["user"]["username"] == "Guest":
        login_dialog = LoginDialog(root, app)
        root.wait_window(login_dialog)