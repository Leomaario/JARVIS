import tkinter as tk
import customtkinter as ctk
import math
import time
import threading
import random
import psutil
import cv2
from PIL import Image, ImageTk
import mss
import numpy as np

ctk.set_appearance_mode("dark")

BG = "#020308"
PRIMARY = "#00F0FF"
ACCENT = "#00FFD0"
PANEL = "#060B18"
TEXT = "#9FEFFF"
WARNING = "#FF3B3B"


class HologramAgentGUI(ctk.CTk):

    def __init__(self, on_send_callback, on_voice_callback, on_file_callback, on_vision_callback=None):
        super().__init__()

        self.title("JARVIS — STARK SUPREME")
        self.geometry("1400x900")
        self.configure(fg_color=BG)

        # callbacks
        self.on_send_callback = on_send_callback
        self.on_voice_callback = on_voice_callback
        self.on_file_callback = on_file_callback
        self.on_vision_toggle = on_vision_callback

        # estados internos
        self.angle = 0
        self.pulse = 0
        self.voice_energy = 5
        self.mood = "neutral"

        # ⚠️ NUNCA usar self.state (bug do tkinter)
        self.agent_state = "idle"

        self.screen_running = False
        self.preview_ref = None
        self.cap = None

        self.setup_layout()
        self.start_animations()
        self.iniciar_monitor_sistema()
        self.start_webcam()

    # =====================================================
    # LAYOUT
    # =====================================================

    def setup_layout(self):

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # painel sistema
        self.sys_panel = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            border_color=PRIMARY,
            border_width=1,
            corner_radius=20
        )
        self.sys_panel.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.cpu_bar = ctk.CTkProgressBar(self.sys_panel)
        self.cpu_bar.pack(fill="x", padx=10, pady=5)

        self.ram_bar = ctk.CTkProgressBar(self.sys_panel)
        self.ram_bar.pack(fill="x", padx=10, pady=5)

        # terminal
        self.chat_display = ctk.CTkTextbox(
            self,
            font=("Consolas", 13),
            fg_color="#010203",
            text_color=TEXT,
            border_color=PRIMARY,
            border_width=1
        )
        self.chat_display.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.chat_display.configure(state="disabled")

        # input
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=2, sticky="nsew")

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Comando...")
        self.user_input.pack(pady=10, padx=20, fill="x")
        self.user_input.bind("<Return>", lambda e: self.send_message())

        ctk.CTkButton(self.input_frame, text="ENVIAR", command=self.send_message).pack(pady=5)
        ctk.CTkButton(self.input_frame, text="🎤 VOZ", command=self.activate_listening).pack(pady=5)
        ctk.CTkButton(self.input_frame, text="VISÃO", command=self.toggle_visao).pack(pady=5)

    # =====================================================
    # MONITOR CPU / RAM
    # =====================================================

    def iniciar_monitor_sistema(self):

        def update():
            try:
                cpu = psutil.cpu_percent() / 100
                ram = psutil.virtual_memory().percent / 100

                self.cpu_bar.set(cpu)
                self.ram_bar.set(ram)

            except Exception as e:
                print("Erro monitor sistema:", e)

            self.after(1000, update)

        update()

    # =====================================================
    # ANIMAÇÕES
    # =====================================================

    def start_animations(self):
        self.animate_grid()
        self.animate_hologram()
        self.animate_particles()
        self.animate_voice_wave()
        self.animate_state_indicator()

    def animate_grid(self):
        self.canvas.delete("grid")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for x in range(0, int(w), 60):
            self.canvas.create_line(x, 0, x, h, fill="#031420", tags="grid")

        for y in range(0, int(h), 60):
            self.canvas.create_line(0, y, w, y, fill="#031420", tags="grid")

        self.after(300, self.animate_grid)

    def animate_hologram(self):

        self.canvas.delete("holo")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx, cy = w / 2, h / 2

        self.angle += 1
        self.pulse += 0.08

        r = 130 + math.sin(self.pulse) * 10

        color = {
            "happy": ACCENT,
            "sad": WARNING,
            "neutral": PRIMARY
        }[self.mood]

        for i in range(4):
            size = r + i * 25
            self.canvas.create_oval(
                cx-size, cy-size, cx+size, cy+size,
                outline=color, width=1, tags="holo"
            )

        rad = math.radians(self.angle)
        x = cx + r * math.cos(rad)
        y = cy + r * math.sin(rad)

        self.canvas.create_line(cx, cy, x, y, fill=color, width=2, tags="holo")

        energy = 15 + math.sin(self.pulse) * 6
        self.canvas.create_oval(
            cx-energy, cy-energy, cx+energy, cy+energy,
            fill=color, outline="", tags="holo"
        )

        if self.agent_state == "thinking":
            self.canvas.create_rectangle(
                0, cy-5, w, cy+5,
                fill=color, stipple="gray25", tags="holo"
            )

        self.after(30, self.animate_hologram)

    def animate_particles(self):

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for _ in range(6):
            x = random.randint(0, int(w))
            y = random.randint(0, int(h))
            self.canvas.create_oval(x, y, x+2, y+2, fill=PRIMARY, tags="particle")

        self.canvas.after(800, lambda: self.canvas.delete("particle"))
        self.after(400, self.animate_particles)

    def animate_voice_wave(self):

        self.canvas.delete("wave")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        base_y = h - 100

        for x in range(0, int(w), 10):
            height = random.randint(5, 20 + self.voice_energy)
            self.canvas.create_line(
                x, base_y-height, x, base_y+height,
                fill=ACCENT, tags="wave"
            )

        self.after(80, self.animate_voice_wave)

    def animate_state_indicator(self):

        self.canvas.delete("state")
        w = self.canvas.winfo_width()

        color = {
            "idle": TEXT,
            "listening": "yellow",
            "thinking": PRIMARY,
            "speaking": ACCENT
        }[self.agent_state]

        self.canvas.create_text(
            w-120, 40,
            text=self.agent_state.upper(),
            fill=color,
            font=("Consolas", 14),
            tags="state"
        )

        self.after(200, self.animate_state_indicator)

    # =====================================================
    # WEBCAM
    # =====================================================

    def start_webcam(self):

        self.cap = cv2.VideoCapture(0)

        def loop():
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()

                if ret:
                    frame = cv2.resize(frame, (200, 140))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    img = ImageTk.PhotoImage(Image.fromarray(frame))
                    self.preview_ref = img

                    self.canvas.delete("webcam")
                    self.canvas.create_image(140, 90, image=img, tags="webcam")

            self.after(30, loop)

        loop()

    # =====================================================
    # SCREEN CAPTURE
    # =====================================================

    def toggle_visao(self):

        self.screen_running = not self.screen_running

        if self.screen_running:
            threading.Thread(target=self.capture_loop, daemon=True).start()

    def capture_loop(self):

        with mss.mss() as sct:
            monitor = sct.monitors[1]

            while self.screen_running:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
                frame = cv2.resize(frame, (320, 180))

                tk_img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.after(0, lambda im=tk_img: self.show_screen(im))

                time.sleep(0.05)

    def show_screen(self, img):
        self.preview_ref = img
        self.canvas.delete("screen")
        self.canvas.create_image(250, 150, image=img, tags="screen")

    # =====================================================
    # CHAT
    # =====================================================

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        t = time.strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"\n[{t}] {sender}: {message}")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state="disabled")

    def send_message(self):

        msg = self.user_input.get()

        if msg.strip():
            self.display_message("VOCÊ", msg)
            self.user_input.delete(0, tk.END)

            self.set_state("thinking")
            self.after(500, lambda: self.set_state("speaking"))

            self.on_send_callback(msg)

    # =====================================================
    # ESTADOS
    # =====================================================

    def activate_listening(self):
        self.set_state("listening")
        self.voice_energy = 40
        self.on_voice_callback()

    def set_state(self, state):
        self.agent_state = state
        self.voice_energy = 30 if state == "speaking" else 5

    def set_mood(self, mood):
        self.mood = mood