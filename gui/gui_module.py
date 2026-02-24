import tkinter as tk
import customtkinter as ctk
import math
import time
import random
import psutil
import cv2
import mss
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageOps
import threading
from collections import deque
import colorsys

ctk.set_appearance_mode("dark")

# =============================
# CORES FUTURISTAS - CORRIGIDAS
# =============================

BG = "#000000"
PRIMARY = "#00ffff"
SECONDARY = "#ff00ff"
ACCENT = "#00ff9d"
PANEL = "#0a0a0f"
TEXT = "#b0f0ff"
WARNING = "#ff3366"
NEON_BLUE = "#00ffff"
NEON_PINK = "#ff00ff"
NEON_GREEN = "#00ffaa"
NEON_PURPLE = "#aa00ff"

# Cores para gradientes (formato RGB)
GRADIENT_START = (0, 255, 255)  # Ciano
GRADIENT_END = (255, 0, 255)    # Magenta

class HologramAgentGUI(ctk.CTk):

    def __init__(self, on_send_callback, on_voice_callback, on_file_callback, on_vision_callback=None):
        super().__init__()

        self.title("JARVIS — STARK SUPREME [NEXUS PROTOCOL]")
        self.geometry("1400x900")
        self.configure(fg_color=BG)
        self.attributes('-alpha', 0.98)

        # callbacks
        self.on_send_callback = on_send_callback
        self.on_voice_callback = on_voice_callback
        self.on_file_callback = on_file_callback
        self.on_vision_toggle = on_vision_callback

        # estados e animações
        self.angle = 0
        self.pulse = 0
        self.glow_pulse = 0
        self.voice_energy = 5
        self.mood = "neutral"
        self.agent_state = "idle"
        self.scan_lines_pos = 0
        self.particle_systems = []
        self.energy_rings = []
        self.quantum_fluctuation = 0
        self.data_stream = deque(maxlen=50)
        self.gradient_offset = 0

        # visão
        self.screen_running = False
        self.preview_ref = None
        self.cap = None
        self.vision_enhanced = False

        # dados simulados
        for _ in range(50):
            self.data_stream.append(random.randint(0, 100))

        self.setup_layout()
        self.init_particle_systems()
        self.start_loops()

    def setup_layout(self):
        """Configura o layout com múltiplos painéis flutuantes"""
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=2)

        # Canvas principal para hologramas e efeitos
        self.main_canvas = tk.Canvas(
            self, 
            bg=BG, 
            highlightthickness=0,
            bd=0
        )
        self.main_canvas.grid(row=0, column=0, columnspan=4, sticky="nsew")

        # Painéis futuristas
        self.setup_system_panel()
        self.setup_quantum_panel()
        self.setup_chat_panel()
        self.setup_control_panel()
        self.setup_radar_panel()

    def setup_system_panel(self):
        """Painel de sistema com efeito holográfico"""
        
        self.sys_panel = ctk.CTkFrame(
            self,
            fg_color="transparent",
            border_width=0,
            corner_radius=20
        )
        self.sys_panel.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Background com glow
        sys_bg = ctk.CTkFrame(
            self.sys_panel,
            fg_color="#0a0a15",
            border_color=NEON_BLUE,
            border_width=2,
            corner_radius=20
        )
        sys_bg.pack(fill="both", expand=True, padx=2, pady=2)

        # Título com efeito neon
        title = ctk.CTkLabel(
            sys_bg,
            text="⚡ SISTEMA ⚡",
            font=("Orbitron", 16, "bold"),
            text_color=NEON_BLUE
        )
        title.pack(pady=10)

        # Barras de progresso
        self.cpu_bar = ctk.CTkProgressBar(sys_bg, height=20, corner_radius=10)
        self.cpu_bar.pack(fill="x", padx=20, pady=10)
        self.cpu_bar.configure(progress_color=NEON_GREEN, border_color=NEON_BLUE, border_width=1)

        self.ram_bar = ctk.CTkProgressBar(sys_bg, height=20, corner_radius=10)
        self.ram_bar.pack(fill="x", padx=20, pady=10)
        self.ram_bar.configure(progress_color=NEON_PINK, border_color=NEON_BLUE, border_width=1)

        # Métricas em tempo real
        self.metrics_frame = ctk.CTkFrame(sys_bg, fg_color="transparent")
        self.metrics_frame.pack(fill="x", padx=20, pady=10)

        self.cpu_label = ctk.CTkLabel(
            self.metrics_frame,
            text="CPU: 0%",
            font=("Consolas", 12),
            text_color=TEXT
        )
        self.cpu_label.pack(side="left", padx=5)

        self.temp_label = ctk.CTkLabel(
            self.metrics_frame,
            text="TEMP: 42°C",
            font=("Consolas", 12),
            text_color=NEON_PINK
        )
        self.temp_label.pack(side="right", padx=5)

    def setup_quantum_panel(self):
        """Painel quântico com efeitos de partículas"""
        
        self.quantum_panel = ctk.CTkFrame(
            self,
            fg_color="transparent",
            border_width=0
        )
        self.quantum_panel.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        quantum_bg = ctk.CTkFrame(
            self.quantum_panel,
            fg_color="#0a0a15",
            border_color=NEON_PURPLE,
            border_width=2,
            corner_radius=20
        )
        quantum_bg.pack(fill="both", expand=True, padx=2, pady=2)

        title = ctk.CTkLabel(
            quantum_bg,
            text="🌀 QUANTUM STATE 🌀",
            font=("Orbitron", 16, "bold"),
            text_color=NEON_PURPLE
        )
        title.pack(pady=10)

        # Canvas para animações quânticas
        self.quantum_canvas = tk.Canvas(
            quantum_bg,
            width=200,
            height=150,
            bg="#0a0a15",
            highlightthickness=0
        )
        self.quantum_canvas.pack(pady=10)

        # Status quântico
        self.quantum_status = ctk.CTkLabel(
            quantum_bg,
            text="ESTADO: SUPERPOSIÇÃO",
            font=("Consolas", 10),
            text_color=NEON_PURPLE
        )
        self.quantum_status.pack(pady=5)

    def setup_chat_panel(self):
        """Painel de chat com efeito terminal"""
        
        self.chat_panel = ctk.CTkFrame(
            self,
            fg_color="transparent",
            border_width=0
        )
        self.chat_panel.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        chat_bg = ctk.CTkFrame(
            self.chat_panel,
            fg_color="#0a0a15",
            border_color=NEON_GREEN,
            border_width=2,
            corner_radius=20
        )
        chat_bg.pack(fill="both", expand=True, padx=2, pady=2)

        title = ctk.CTkLabel(
            chat_bg,
            text="💬 TERMINAL 💬",
            font=("Orbitron", 16, "bold"),
            text_color=NEON_GREEN
        )
        title.pack(pady=10)

        self.chat_display = ctk.CTkTextbox(
            chat_bg,
            font=("Consolas", 12),
            fg_color="#010103",
            text_color=NEON_GREEN,
            border_color=NEON_GREEN,
            border_width=1,
            corner_radius=10
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=10)
        self.chat_display.configure(state="disabled")

        # Configurar tags para cores diferentes no chat
        self.chat_display.tag_config("user", foreground="#ffaa00")
        self.chat_display.tag_config("user_msg", foreground="#ffffff")
        self.chat_display.tag_config("jarvis", foreground=NEON_BLUE)
        self.chat_display.tag_config("jarvis_msg", foreground=NEON_GREEN)

    def setup_control_panel(self):
        """Painel de controle central"""
        
        self.control_panel = ctk.CTkFrame(
            self,
            fg_color="transparent",
            border_width=0
        )
        self.control_panel.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        control_bg = ctk.CTkFrame(
            self.control_panel,
            fg_color="#0a0a15",
            border_color=NEON_PINK,
            border_width=2,
            corner_radius=20
        )
        control_bg.pack(fill="both", expand=True, padx=2, pady=2)

        title = ctk.CTkLabel(
            control_bg,
            text="🎮 CONTROLE 🎮",
            font=("Orbitron", 16, "bold"),
            text_color=NEON_PINK
        )
        title.pack(pady=10)

        # Input
        self.user_input = ctk.CTkEntry(
            control_bg,
            placeholder_text="COMANDO:",
            font=("Consolas", 12),
            fg_color="#010103",
            border_color=NEON_PINK,
            text_color=NEON_GREEN
        )
        self.user_input.pack(pady=10, padx=20, fill="x")
        self.user_input.bind("<Return>", lambda e: self.send_message())

        # Botões
        btn_style = {
            "font": ("Orbitron", 12, "bold"),
            "border_width": 2,
            "corner_radius": 15,
            "hover": True
        }

        self.send_btn = ctk.CTkButton(
            control_bg,
            text="🚀 EXECUTAR",
            command=self.send_message,
            fg_color="#00aa88",
            hover_color=NEON_GREEN,
            border_color=NEON_GREEN,
            **btn_style
        )
        self.send_btn.pack(pady=5, padx=20, fill="x")

        self.voice_btn = ctk.CTkButton(
            control_bg,
            text="🎤 COMANDO DE VOZ",
            command=self.activate_listening,
            fg_color="#8800aa",
            hover_color=NEON_PURPLE,
            border_color=NEON_PURPLE,
            **btn_style
        )
        self.voice_btn.pack(pady=5, padx=20, fill="x")

        self.vision_btn = ctk.CTkButton(
            control_bg,
            text="👁️ VISÃO ENHANCED",
            command=self.toggle_visao,
            fg_color="#aa4400",
            hover_color=NEON_PINK,
            border_color=NEON_PINK,
            **btn_style
        )
        self.vision_btn.pack(pady=5, padx=20, fill="x")

    def setup_radar_panel(self):
        """Mini radar holográfico"""
        
        self.radar_canvas = tk.Canvas(
            self.main_canvas,
            width=150,
            height=150,
            bg=BG,
            highlightthickness=0
        )
        self.radar_canvas.place(relx=0.02, rely=0.02)

    def init_particle_systems(self):
        """Inicializa sistemas de partículas"""
        for _ in range(20):
            self.particle_systems.append({
                'x': random.randint(0, 1400),
                'y': random.randint(0, 900),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'life': random.randint(50, 200),
                'color': random.choice([NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_PURPLE])
            })

    # =====================================================
    # LOOPS DE ANIMAÇÃO
    # =====================================================

    def start_loops(self):
        """Inicia todos os loops de animação"""
        self.update_system_monitor()
        self.animate_hologram()
        self.animate_grid()
        self.animate_particles()
        self.animate_voice_wave()
        self.animate_state_indicator()
        self.animate_quantum_field()
        self.animate_radar()
        self.animate_scan_lines()
        self.animate_data_stream()
        self.start_webcam()

    def update_system_monitor(self):
        """Atualiza métricas do sistema"""
        try:
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
            
            self.cpu_bar.set(cpu_percent / 100)
            self.ram_bar.set(ram_percent / 100)
            
            self.cpu_label.configure(text=f"CPU: {cpu_percent}%")
            self.temp_label.configure(text=f"TEMP: {random.randint(35, 55)}°C")
        except:
            pass
            
        self.after(1000, self.update_system_monitor)

    def animate_hologram(self):
        """Holograma principal com múltiplas camadas"""
        
        self.main_canvas.delete("holo")
        
        w = self.main_canvas.winfo_width()
        h = self.main_canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(30, self.animate_hologram)
            return
            
        cx, cy = w / 2, h / 2 - 50

        self.angle += 2
        self.pulse += 0.1
        self.glow_pulse += 0.05

        # Cores baseadas no humor
        colors = {
            "happy": [NEON_GREEN, NEON_BLUE],
            "sad": [NEON_PURPLE, NEON_PINK],
            "neutral": [NEON_BLUE, NEON_PURPLE]
        }.get(self.mood, [NEON_BLUE, NEON_PURPLE])

        # Múltiplos anéis holográficos
        for i in range(8):
            radius = 120 + i * 25 + math.sin(self.pulse + i) * 15
            
            # Efeito de rotação 3D
            x_offset = math.sin(math.radians(self.angle + i * 45)) * 20
            y_offset = math.cos(math.radians(self.angle + i * 45)) * 10
            
            color = colors[i % 2]
            
            # Anel principal
            self.main_canvas.create_oval(
                cx - radius + x_offset, 
                cy - radius + y_offset,
                cx + radius + x_offset, 
                cy + radius + y_offset,
                outline=color,
                width=2 - i*0.2,
                dash=(20, 5) if i % 2 == 0 else (),
                tags="holo"
            )
            
            # Anel secundário
            self.main_canvas.create_oval(
                cx - radius - x_offset, 
                cy - radius - y_offset,
                cx + radius - x_offset, 
                cy + radius - y_offset,
                outline=color,
                width=1,
                dash=(5, 10),
                tags="holo"
            )

        # Linhas de conexão
        for i in range(0, 360, 30):
            angle_rad = math.radians(i + self.angle)
            x1 = cx + math.cos(angle_rad) * 120
            y1 = cy + math.sin(angle_rad) * 120
            x2 = cx + math.cos(angle_rad + 0.5) * 200
            y2 = cy + math.sin(angle_rad + 0.5) * 200
            
            self.main_canvas.create_line(
                x1, y1, x2, y2,
                fill=NEON_BLUE,
                width=1,
                dash=(5, 3),
                tags="holo"
            )

        # Núcleo pulsante
        core_radius = 40 + math.sin(self.pulse * 2) * 10
        for j in range(3):
            r = core_radius - j * 10
            self.main_canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=colors[0],
                width=3 - j,
                tags="holo"
            )

        self.after(30, self.animate_hologram)

    def animate_grid(self):
        """Grade holográfica animada - CORRIGIDA"""
        
        self.main_canvas.delete("grid")
        
        w = self.main_canvas.winfo_width()
        h = self.main_canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(50, self.animate_grid)
            return
        
        # Grade principal
        spacing = 40
        offset = (self.angle % spacing)
        
        for x in range(-spacing, int(w) + spacing, spacing):
            x_pos = x + offset
            
            # CORRIGIDO: Usar cores hexadecimais de 6 dígitos
            alpha_val = int(100 * (1 - abs(x_pos - w/2) / w))
            # Converter para hexadecimal de 2 dígitos
            alpha_hex = format(min(255, alpha_val * 2), '02x')
            
            self.main_canvas.create_line(
                x_pos, 0, x_pos, h,
                fill=f"#{alpha_hex}00{alpha_hex}",  # Formato #RRGGBB
                width=1,
                tags="grid"
            )

        for y in range(-spacing, int(h) + spacing, spacing):
            y_pos = y + offset
            alpha_val = int(100 * (1 - abs(y_pos - h/2) / h))
            alpha_hex = format(min(255, alpha_val * 2), '02x')
            
            self.main_canvas.create_line(
                0, y_pos, w, y_pos,
                fill=f"#{alpha_hex}00{alpha_hex}",  # Formato #RRGGBB
                width=1,
                tags="grid"
            )

        # Pontos de interseção
        for x in range(0, int(w), spacing):
            for y in range(0, int(h), spacing):
                x_pos = x + offset
                y_pos = y + offset
                
                if 0 <= x_pos <= w and 0 <= y_pos <= h:
                    size = 3 + math.sin(self.pulse + x/10 + y/10) * 2
                    self.main_canvas.create_oval(
                        x_pos - size, y_pos - size,
                        x_pos + size, y_pos + size,
                        fill=NEON_BLUE,
                        outline="",
                        tags="grid"
                    )

        self.after(50, self.animate_grid)

    def animate_particles(self):
        """Sistema de partículas futurista"""
        
        self.main_canvas.delete("particle")
        
        w = self.main_canvas.winfo_width()
        h = self.main_canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(20, self.animate_particles)
            return
        
        # Atualiza partículas existentes
        for particle in self.particle_systems[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if (particle['life'] <= 0 or 
                particle['x'] < 0 or particle['x'] > w or
                particle['y'] < 0 or particle['y'] > h):
                
                # Reset da partícula
                particle['x'] = random.randint(0, w)
                particle['y'] = random.randint(0, h)
                particle['vx'] = random.uniform(-2, 2)
                particle['vy'] = random.uniform(-2, 2)
                particle['life'] = random.randint(50, 200)
                particle['color'] = random.choice([NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_PURPLE])

        # Desenha partículas
        for p in self.particle_systems:
            # Efeito de rastro
            for i in range(3):
                x = p['x'] - p['vx'] * i
                y = p['y'] - p['vy'] * i
                size = 3 - i
                color = p['color']
                
                self.main_canvas.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill=color,
                    outline="",
                    tags="particle"
                )

        self.after(20, self.animate_particles)

    def animate_voice_wave(self):
        """Onda de voz animada"""
        
        self.main_canvas.delete("wave")
        
        w = self.main_canvas.winfo_width()
        h = self.main_canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(30, self.animate_voice_wave)
            return
            
        base_y = h - 150

        # Onda principal
        points = []
        for x in range(0, int(w), 5):
            if self.agent_state == "listening":
                noise = random.random() * self.voice_energy
                y = base_y + math.sin(x/20 + time.time()*10) * 20 * noise
            else:
                y = base_y + math.sin(x/30 + time.time()*5) * 15
            points.append((x, y))

        # Desenha onda
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            self.main_canvas.create_line(
                x1, y1, x2, y2,
                fill=NEON_GREEN,
                width=3,
                tags="wave"
            )

        self.after(30, self.animate_voice_wave)

    def animate_state_indicator(self):
        """Indicador de estado com animação"""
        
        self.main_canvas.delete("state")
        
        w = self.main_canvas.winfo_width()
        
        if w < 100:
            self.after(200, self.animate_state_indicator)
            return
        
        state_colors = {
            "idle": TEXT,
            "listening": NEON_GREEN,
            "thinking": NEON_BLUE,
            "speaking": NEON_PINK
        }
        
        color = state_colors.get(self.agent_state, TEXT)
        
        # Texto com efeito
        self.main_canvas.create_text(
            w - 150,
            50,
            text=self.agent_state.upper(),
            fill=color,
            font=("Orbitron", 16, "bold"),
            tags="state"
        )

        self.after(200, self.animate_state_indicator)

    def animate_quantum_field(self):
        """Campo quântico animado"""
        
        self.quantum_canvas.delete("all")
        
        w = self.quantum_canvas.winfo_width()
        h = self.quantum_canvas.winfo_height()
        
        if w < 50 or h < 50:
            self.after(50, self.animate_quantum_field)
            return
        
        self.quantum_fluctuation += 0.1
        
        # Padrão de ondas quânticas
        for i in range(0, w, 20):
            for j in range(0, h, 20):
                x = i + math.sin(self.quantum_fluctuation + j/10) * 5
                y = j + math.cos(self.quantum_fluctuation + i/10) * 5
                
                if random.random() > 0.5:
                    self.quantum_canvas.create_oval(
                        x-2, y-2, x+2, y+2,
                        fill=NEON_PURPLE,
                        outline=""
                    )
                else:
                    self.quantum_canvas.create_rectangle(
                        x-2, y-2, x+2, y+2,
                        fill=NEON_BLUE,
                        outline=""
                    )

        self.after(50, self.animate_quantum_field)

    def animate_radar(self):
        """Radar holográfico animado"""
        
        self.radar_canvas.delete("all")
        
        w = 150
        h = 150
        cx, cy = w/2, h/2

        # Círculos concêntricos
        for i in range(3, 0, -1):
            radius = i * 25
            self.radar_canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline=NEON_GREEN,
                width=1,
                dash=(5, 3)
            )

        # Linhas de varredura
        angle_rad = math.radians(self.angle * 2)
        x2 = cx + math.cos(angle_rad) * 70
        y2 = cy + math.sin(angle_rad) * 70
        
        self.radar_canvas.create_line(
            cx, cy, x2, y2,
            fill=NEON_GREEN,
            width=2
        )

        # Pontos de "contato"
        for _ in range(3):
            r = random.randint(10, 70)
            a = random.randint(0, 360)
            x = cx + math.cos(math.radians(a)) * r
            y = cy + math.sin(math.radians(a)) * r
            
            self.radar_canvas.create_oval(
                x-3, y-3, x+3, y+3,
                fill=NEON_PINK,
                outline=NEON_GREEN
            )

        self.after(100, self.animate_radar)

    def animate_scan_lines(self):
        """Linhas de scan animadas"""
        
        self.main_canvas.delete("scan")
        
        w = self.main_canvas.winfo_width()
        h = self.main_canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(30, self.animate_scan_lines)
            return
        
        self.scan_lines_pos = (self.scan_lines_pos + 5) % h
        
        # Linha de scan horizontal
        y = self.scan_lines_pos
        self.main_canvas.create_line(
            0, y, w, y,
            fill=NEON_BLUE,
            width=2,
            tags="scan"
        )
        
        # Efeito de glow (CORRIGIDO)
        for i in range(1, 4):
            alpha = int(100 / i)
            alpha_hex = format(alpha, '02x')
            self.main_canvas.create_line(
                0, y - i*2, w, y - i*2,
                fill=f"#{alpha_hex}00{alpha_hex}",  # Formato #RRGGBB
                width=1,
                tags="scan"
            )

        self.after(30, self.animate_scan_lines)

    def animate_data_stream(self):
        """Stream de dados animado"""
        
        self.main_canvas.delete("data")
        
        w = self.main_canvas.winfo_width()
        h = self.main_canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(100, self.animate_data_stream)
            return
        
        # Adiciona novo dado
        self.data_stream.append(random.randint(0, 100))
        
        # Desenha gráfico de dados
        x_step = w / len(self.data_stream) if self.data_stream else 1
        points = []
        
        for i, value in enumerate(self.data_stream):
            x = i * x_step
            y = h - 100 - (value * 2)
            points.append((x, y))

        # Linha de dados
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            self.main_canvas.create_line(
                x1, y1, x2, y2,
                fill=NEON_PURPLE,
                width=2,
                tags="data"
            )

        self.after(100, self.animate_data_stream)

    # =====================================================
    # WEBCAM E VISÃO
    # =====================================================

    def start_webcam(self):
        """Inicia captura da webcam com efeitos"""
        
        try:
            self.cap = cv2.VideoCapture(0)
        except:
            print("Webcam não disponível")
            return

        def loop():
            if self.cap and self.cap.isOpened():
                try:
                    ret, frame = self.cap.read()

                    if ret:
                        frame = cv2.resize(frame, (250, 180))
                        
                        # Efeitos cyberpunk
                        if self.vision_enhanced:
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame = cv2.addWeighted(frame, 0.7, np.zeros_like(frame), 0.3, 0)
                        
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = ImageTk.PhotoImage(Image.fromarray(frame))
                        self.preview_ref = img

                        self.main_canvas.delete("webcam")
                        
                        # Moldura futurista
                        x, y = 100, 80
                        self.main_canvas.create_rectangle(
                            x-5, y-5, x+260, y+190,
                            outline=NEON_BLUE,
                            width=3,
                            tags="webcam"
                        )
                        
                        self.main_canvas.create_image(x, y, image=img, anchor="nw", tags="webcam")
                except:
                    pass

            self.after(30, loop)

        loop()

    def toggle_visao(self):
        """Alterna modo de visão enhanced"""
        self.vision_enhanced = not self.vision_enhanced
        self.screen_running = self.vision_enhanced

        if self.screen_running and self.on_vision_toggle:
            self.on_vision_toggle()

    # =====================================================
    # FUNÇÕES DE INTERFACE
    # =====================================================

    def display_message(self, sender, message):
        """Exibe mensagem no chat"""
        
        try:
            self.chat_display.configure(state="normal")

            timestamp = time.strftime("%H:%M:%S")
            
            if sender == "VOCÊ":
                prefix = f"[{timestamp}] ⚡ {sender}: "
                self.chat_display.insert(tk.END, prefix, "user")
                self.chat_display.insert(tk.END, f"{message}\n", "user_msg")
            else:
                prefix = f"[{timestamp}] 🔮 JARVIS: "
                self.chat_display.insert(tk.END, prefix, "jarvis")
                self.chat_display.insert(tk.END, f"{message}\n", "jarvis_msg")

            self.chat_display.see(tk.END)
            self.chat_display.configure(state="disabled")
        except:
            pass

    def send_message(self):
        """Envia mensagem do usuário"""
        
        msg = self.user_input.get()

        if msg.strip():
            self.display_message("VOCÊ", msg)
            self.user_input.delete(0, tk.END)

            self.set_state("thinking")
            self.after(500, lambda: self.set_state("speaking"))

            if self.on_send_callback:
                self.on_send_callback(msg)

    def activate_listening(self):
        """Ativa modo de escuta"""
        
        self.set_state("listening")
        self.voice_energy = 40
        
        # Efeito visual
        self.voice_btn.configure(fg_color=NEON_GREEN, text="🎤 OUVINDO...")
        self.after(2000, lambda: self.voice_btn.configure(
            fg_color="#8800aa", 
            text="🎤 COMANDO DE VOZ"
        ))
        
        if self.on_voice_callback:
            self.on_voice_callback()

    def set_state(self, state):
        """Define estado do agente"""
        self.agent_state = state
        
        if state == "speaking":
            self.voice_energy = 30
        elif state == "listening":
            self.voice_energy = 40
        else:
            self.voice_energy = 5

    def set_mood(self, mood):
        """Define humor do agente"""
        self.mood = mood

