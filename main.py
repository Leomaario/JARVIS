import tkinter as tk
from tkinter import filedialog
import os
import re
import threading
from dotenv import load_dotenv

# Módulos customizados
from gui_module import HologramAgentGUI
from voice_module import VoiceAssistant
from brain_module import AgentBrain
from system_module import SystemController
from vision_module import VisionEngine

# ============================================================
# 🔧 CONFIG
# ============================================================

load_dotenv()

CHAVES_API = os.getenv("GROQ_API_KEYS")

CONFIG = {
    "GROQ_API_KEYS": CHAVES_API,
    "MODEL": "llama-3.3-70b-versatile"
}

# ============================================================
# 🧠 APP PRINCIPAL
# ============================================================

class HologramApp:

    def __init__(self):

        # 1️⃣ Sistema base primeiro
        self.system = SystemController(gui_ref=None)

        # 2️⃣ Brain
        self.brain = AgentBrain(
            api_key=CONFIG["GROQ_API_KEYS"],
            model=CONFIG["MODEL"]
        )

        # 3️⃣ Voz
        self.voice = VoiceAssistant()

        # 4️⃣ GUI
        self.gui = HologramAgentGUI(
            on_send_callback=self.handle_text_input,
            on_voice_callback=self.handle_voice_input,
            on_file_callback=self.handle_file_upload,
            on_vision_callback=self.toggle_vision_mode
        )

        # 5️⃣ Vincula sistema com GUI
        self.system.gui = self.gui

        # 6️⃣ Vision Engine (AGORA sim pode criar)
        self.vision = VisionEngine(self.system, self.brain, self.gui)

        self.current_file_content = None


    # ============================================================
    # 👁️ VISÃO INTELIGENTE
    # ============================================================

    def toggle_vision_mode(self):
        if not self.vision.intelligent_mode:
            self.vision.start_intelligent_mode()
            self.gui.display_message("SISTEMA", "Modo Visão Inteligente ativado.")
        else:
            self.vision.stop_intelligent_mode()
            self.gui.display_message("SISTEMA", "Modo Visão Inteligente desativado.")


    # ============================================================
    # 💬 TEXTO
    # ============================================================

    def handle_text_input(self, text):

        self.voice.stop_speaking()

        def task():
            try:
                if not CONFIG["GROQ_API_KEYS"]:
                    self.gui.after(
                        0,
                        self.gui.display_message,
                        "AGENTE",
                        "Chaves API não configuradas no .env"
                    )
                    return

                response = self.brain.process_input(
                    user_text=text,
                    hardware_context=self.system.mapear_ambiente(),
                    software_context=self.system.listar_janelas_ativas()
                )

                if not isinstance(response, str):
                    response = "Erro interno no processamento."

                # Detecta comandos invisíveis
                cmd_match = re.search(r"\[CMD:\s*(.*?)\]", response, re.DOTALL)
                clean_res = re.sub(r"\[CMD:\s*.*?\]", "", response, flags=re.DOTALL).strip()

                if cmd_match:
                    self.system.execute_command(cmd_match.group(1))

                if clean_res:
                    self.gui.after(
                        0,
                        self.gui.display_message,
                        "AGENTE",
                        clean_res
                    )

                    self.voice.speak(clean_res)

            except Exception as e:
                print(f"ERRO THREAD: {e}")
                self.gui.after(
                    0,
                    self.gui.display_message,
                    "SISTEMA",
                    "Erro interno detectado."
                )

        threading.Thread(target=task, daemon=True).start()


    # ============================================================
    # 🎤 VOZ
    # ============================================================

    def handle_voice_input(self):
        self.voice.listen(callback=self.handle_text_input)


    # ============================================================
    # 📎 ARQUIVO
    # ============================================================

    def handle_file_upload(self):

        file_path = filedialog.askopenfilename(
            title="Selecionar código",
            filetypes=[
                ("Arquivos Técnicos", "*.py *.js *.java *.json *.txt *.html *.css"),
                ("Todos", "*.*")
            ]
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.current_file_content = f.read()

                filename = os.path.basename(file_path)

                self.gui.display_message(
                    "VOCÊ",
                    f"[Arquivo {filename} anexado]"
                )

                self.voice.speak(
                    f"Arquivo {filename} recebido e analisado."
                )

            except Exception:
                self.voice.speak("Erro ao carregar o arquivo.")


    # ============================================================
    # 🚀 RUN
    # ============================================================

    def run(self):
        self.gui.mainloop()


# ============================================================
# ▶ START
# ============================================================

if __name__ == "__main__":
    app = HologramApp()
    app.run()