import tkinter as tk
from tkinter import filedialog
import os
import re
import threading
from dotenv import load_dotenv

# módulos do sistema
from gui_module import HologramAgentGUI
from voice_module import VoiceAssistant
from brain_module import AgentBrain
from system_module import SystemController
from vision_module import VisionEngine


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

CHAVES_API = os.getenv("GROQ_API_KEYS")

CONFIG = {
    "GROQ_API_KEYS": CHAVES_API,
    "MODEL": "llama-3.3-70b-versatile"
}


# ============================================================
# APP PRINCIPAL
# ============================================================

class HologramApp:

    def __init__(self):

        print("Inicializando sistema...")

        # ===============================
        # SISTEMA BASE
        # ===============================
        self.system = SystemController(gui_ref=None)

        # ===============================
        # CÉREBRO IA
        # ===============================
        self.brain = AgentBrain(
            api_key=CONFIG["GROQ_API_KEYS"],
            model=CONFIG["MODEL"]
        )

        # ===============================
        # VOZ
        # ===============================
        self.voice = VoiceAssistant()

        # ===============================
        # GUI
        # ===============================
        self.gui = HologramAgentGUI(
            on_send_callback=self.handle_text_input,
            on_voice_callback=self.handle_voice_input,
            on_file_callback=self.handle_file_upload,
            on_vision_callback=self.toggle_vision_mode
        )

        # conecta GUI no sistema
        self.system.gui = self.gui

        # ===============================
        # VISÃO
        # ===============================
        self.vision = VisionEngine(self.system, self.brain, self.gui)

        self.current_file_content = None

        print("Sistema pronto.")

    # ============================================================
    # VISÃO
    # ============================================================

    def toggle_vision_mode(self):

        if not self.vision.intelligent_mode:
            self.vision.start_intelligent_mode()
            self.gui.display_message("SISTEMA", "Modo visão ativado.")
        else:
            self.vision.stop_intelligent_mode()
            self.gui.display_message("SISTEMA", "Modo visão desativado.")

    # ============================================================
    # PROCESSAMENTO IA
    # ============================================================

    def process_agent_response(self, text):

        try:
            extra_context = ""

            # adiciona arquivo como contexto se existir
            if self.current_file_content:
                extra_context = f"\nArquivo carregado:\n{self.current_file_content[:2000]}"

            response = self.brain.process_input(
                user_text=text + extra_context,
                hardware_context=self.system.mapear_ambiente(),
                software_context=self.system.listar_janelas_ativas()
            )

            if not isinstance(response, str):
                return "Erro interno."

            return response

        except Exception as e:
            print("Erro processamento:", e)
            return "Erro interno detectado."

    # ============================================================
    # TEXTO
    # ============================================================

    def handle_text_input(self, text):

        # para qualquer fala atual
        self.voice.stop_speaking()

        def task():

            try:
                # verifica API
                if not CONFIG["GROQ_API_KEYS"]:
                    self.gui.after(
                        0,
                        self.gui.display_message,
                        "SISTEMA",
                        "Chaves API não configuradas no .env"
                    )
                    return

                # chama IA
                response = self.process_agent_response(text)

                # mostra na GUI
                self.gui.after(0, self.gui.display_message, "AGENTE", response)

                # fala limpa
                fala = self.clean_voice_text(response)
                self.voice.speak(fala)

            except Exception as e:
                print("Erro thread:", e)
                self.gui.after(
                    0,
                    self.gui.display_message,
                    "SISTEMA",
                    "Erro interno detectado."
                )

        threading.Thread(target=task, daemon=True).start()

    # ============================================================
    # LIMPEZA DE TEXTO PARA VOZ
    # ============================================================

    def clean_voice_text(self, text):

        if not text:
            return ""

        text = re.sub(r"\[CMD:.*?\]", "", text)
        text = text.replace("*", "")
        text = text.replace("`", "")
        text = re.sub(r"[^\w\s.,!?áéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ-]", "", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ============================================================
    # VOZ
    # ============================================================

    def handle_voice_input(self):
        self.voice.listen(callback=self.handle_text_input)

    

    # ============================================================
    # UPLOAD DE ARQUIVO
    # ============================================================

    def handle_file_upload(self):

        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo",
            filetypes=[
                ("Arquivos Técnicos", "*.py *.js *.java *.json *.txt *.html *.css"),
                ("Todos", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.current_file_content = f.read()

            filename = os.path.basename(file_path)

            self.gui.display_message("VOCÊ", f"[Arquivo {filename} anexado]")
            self.voice.speak(f"Arquivo {filename} recebido.")

        except Exception:
            self.voice.speak("Erro ao carregar arquivo.")

    # ============================================================
    # RUN
    # ============================================================

    def run(self):
        self.gui.mainloop()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    app = HologramApp()
    app.run()