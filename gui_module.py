import tkinter as tk
import customtkinter as ctk
import math
import time
import threading

from PIL import Image, ImageTk
import mss
import numpy as np
import cv2
import pyautogui


class HologramAgentGUI(ctk.CTk):

    def __init__(self, on_send_callback,
                 on_voice_callback,
                 on_file_callback,
                 on_vision_callback=None):

        super().__init__()

        # =============================
        # CONFIG BASE
        # =============================

        self.title("JARVIS OS - SouzaLink Terminal")
        self.geometry("1000x950")
        self.configure(fg_color="#000000")
        ctk.set_appearance_mode("dark")

        self.on_send_callback = on_send_callback
        self.on_voice_callback = on_voice_callback
        self.on_file_callback = on_file_callback
        self.on_vision_toggle = on_vision_callback

        self.screen_running = False
        self.preview_ref = None
        self.intelligent_mode = True

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)

        # =============================
        # 🔵 HOLOGRAMA
        # =============================

        self.canvas = tk.Canvas(self, bg="#000000", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew", pady=20)

        self.angle = 0
        self.pulse_val = 0

        # =============================
        # 👁️ MONITOR VISÃO
        # =============================

        self.monitor_frame = ctk.CTkFrame(
            self,
            fg_color="#050505",
            border_color="#00ffff",
            border_width=1
        )
        self.monitor_frame.grid(row=1, column=0, padx=80, pady=10, sticky="nsew")

        self.monitor_label = ctk.CTkLabel(
            self.monitor_frame,
            text="VISÃO DO SISTEMA: DESATIVADA",
            font=("Consolas", 11, "bold"),
            text_color="#00ffff"
        )
        self.monitor_label.pack(side="top", pady=5)

        self.preview_canvas = tk.Canvas(
            self.monitor_frame,
            bg="#000000",
            height=250,
            highlightthickness=0
        )
        self.preview_canvas.pack(fill="both", expand=True, padx=10, pady=5)

        self.toggle_button = ctk.CTkButton(
            self.monitor_frame,
            text="ATIVAR VISÃO",
            command=self.toggle_visao
        )
        self.toggle_button.pack(pady=5)

        # =============================
        # 💬 CHAT
        # =============================

        self.chat_display = ctk.CTkTextbox(
            self,
            height=80,
            font=("Consolas", 14),
            fg_color="#000000",
            text_color="#00ffff"
        )
        self.chat_display.grid(row=2, column=0, padx=80, pady=(0, 10), sticky="ew")
        self.chat_display.configure(state="disabled")

        # =============================
        # INPUT
        # =============================

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=3, column=0, padx=80, pady=(0, 40), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(
            self.input_frame,
            height=45,
            placeholder_text="Comando para o JARVIS..."
        )
        self.user_input.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.user_input.bind("<Return>", lambda e: self.send_message())

        ctk.CTkButton(
            self.input_frame,
            text="ENVIAR",
            command=self.send_message
        ).grid(row=0, column=1)

        ctk.CTkButton(
            self.input_frame,
            text="🎤",
            command=self.on_voice_callback
        ).grid(row=0, column=2)

        self.draw_hologram()

    # ==========================================================
    # 👁️ VISÃO INTELIGENTE
    # ==========================================================

    def toggle_visao(self):
        if not self.screen_running:
            self.screen_running = True
            self.monitor_label.configure(text="VISÃO DO SISTEMA: ATIVA")
            self.toggle_button.configure(text="DESATIVAR VISÃO")
            threading.Thread(target=self._capturar_tela_loop, daemon=True).start()
        else:
            self.screen_running = False
            self.monitor_label.configure(text="VISÃO DO SISTEMA: DESATIVADA")
            self.toggle_button.configure(text="ATIVAR VISÃO")
            self.preview_canvas.delete("all")

    def _capturar_tela_loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]

            while self.screen_running:
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)

                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

                # 🎯 Marca posição do mouse
                mouse_x, mouse_y = pyautogui.position()
                cv2.circle(frame, (mouse_x, mouse_y), 15, (0, 255, 255), 3)

                # 🧠 Detecta bordas (elementos)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours[:25]:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if w > 60 and h > 40:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Redimensiona preview
                frame = cv2.resize(frame, (600, 250))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                img_pil = Image.fromarray(frame)
                self.preview_ref = ImageTk.PhotoImage(img_pil)

                self.preview_canvas.after(
                    0,
                    lambda: self.preview_canvas.create_image(
                        300, 125,
                        image=self.preview_ref
                    )
                )

                time.sleep(0.03)

    # ==========================================================
    # 🔵 HOLOGRAMA
    # ==========================================================

    def draw_hologram(self):
        self.canvas.delete("energy")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width > 1:
            cx, cy = width / 2, height / 2
            self.pulse_val += 0.1
            radius = 110 + (math.sin(self.pulse_val) * 4)

            for i in range(0, 360, 15):
                rad = math.radians(i + self.angle)
                x = cx + (radius + 25) * math.cos(rad)
                y = cy + (radius + 25) * math.sin(rad)

                self.canvas.create_oval(
                    x - 1, y - 1,
                    x + 1, y + 1,
                    fill="#00ffff",
                    outline="",
                    tags="energy"
                )

            self.angle += 0.6

        self.after(30, self.draw_hologram)

    # ==========================================================
    # 💬 CHAT
    # ==========================================================

    def send_message(self):
        msg = self.user_input.get()
        if msg.strip():
            self.display_message("VOCÊ", msg)
            self.user_input.delete(0, tk.END)
            self.on_send_callback(msg)

    def display_message(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.delete("0.0", tk.END)
        self.chat_display.insert(tk.END, f"> {sender.upper()}: {message}")
        self.chat_display.configure(state="disabled")