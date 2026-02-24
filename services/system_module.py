import os
import subprocess
import pyautogui
import webbrowser
import threading
import time
import mss
import ast
import pygetwindow as gw

from screeninfo import get_monitors
from services.fullacessos import FullAccess
from reportlab.pdfgen import canvas


class SystemController:

    def __init__(self, gui_ref=None):
        self.gui = gui_ref
        self.acesso_total = FullAccess(gui_ref)

    # ======================================================
    # AÇÕES SISTEMA
    # ======================================================

    def open_camera_second_monitor(self):
        print("Abrindo câmera...")
        os.system("start microsoft.windows.camera:")

    def create_pdf_report(self, assunto="Relatório"):
        file_name = "relatorio_jarvis.pdf"

        c = canvas.Canvas(file_name)
        c.drawString(100, 750, "Relatório JARVIS")
        c.drawString(100, 720, f"Assunto: {assunto}")
        c.drawString(100, 690, "Gerado automaticamente.")
        c.save()

        print("PDF criado:", file_name)

    # ======================================================
    # CONTEXTO PARA IA
    # ======================================================

    def mapear_ambiente(self):
        """Lista monitores e coordenadas."""
        monitores = get_monitors()
        mapa = "RELATÓRIO DE HARDWARE:\n"

        for i, m in enumerate(monitores):
            mapa += f"- Monitor {i+1}: {m.width}x{m.height} em X={m.x}, Y={m.y} (Principal: {m.is_primary})\n"

        return mapa

    def listar_janelas_ativas(self):
        """Retorna títulos das janelas abertas."""
        janelas = [w.title for w in gw.getWindowsWithTitle("") if w.visible and w.title.strip()]
        return "JANELAS ABERTAS: " + ", ".join(janelas[:6])

    # ======================================================
    # SCREENSHOT
    # ======================================================

    def take_screenshot(self, filename="visao.png", monitor_index=1):
        """Captura monitor específico."""
        import mss.tools

        with mss.mss() as sct:
            try:
                if monitor_index >= len(sct.monitors):
                    monitor_index = 1

                monitor = sct.monitors[monitor_index]
                print(f"--- CAPTURANDO MONITOR {monitor_index} ---")

                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)

                time.sleep(0.2)
                return filename

            except Exception as e:
                print(f"Erro MSS: {e}. Fallback PyAutoGUI.")
                pyautogui.screenshot(filename)
                return filename

    # ======================================================
    # EXECUÇÃO DE COMANDOS IA (SEGURA)
    # ======================================================

    def execute_command(self, cmd_string):

        def run_it():

            # 1️⃣ valida sintaxe antes de rodar
            try:
                ast.parse(cmd_string)
            except SyntaxError as e:
                erro = f"Erro de sintaxe no comando IA: {e}"
                print("--- [BLOQUEADO] ---", erro)

                self.acesso_total.registrar_log("COMANDO BLOQUEADO", erro)

                if self.gui:
                    self.gui.after(
                        0,
                        self.gui.display_message,
                        "SISTEMA",
                        "Comando abortado por segurança."
                    )
                return

            # 2️⃣ executa comando validado
            try:
                print("--- EXECUTANDO ---", cmd_string)

                exec_scope = {
                    "os": os,
                    "pyautogui": pyautogui,
                    "webbrowser": webbrowser,
                    "time": time,
                    "full": self.acesso_total,
                    "sys_ctrl": self
                }

                exec(cmd_string, exec_scope)

            except Exception as e:
                erro_msg = f"Erro execução: {str(e)}"
                print("--- ERRO ---", erro_msg)

                self.acesso_total.registrar_log("ERRO DE EXECUÇÃO", erro_msg)

                if self.gui:
                    self.gui.after(
                        0,
                        self.gui.display_message,
                        "SISTEMA",
                        f"Erro interno: {str(e)}"
                    )

        threading.Thread(target=run_it, daemon=True).start()

    # ======================================================
    # SKILLS
    # ======================================================

    def executar_skill(self, nome_skill):

        if nome_skill.endswith(".py"):
            nome_skill = nome_skill.replace(".py", "")

        caminho = os.path.join("skills", f"{nome_skill}.py")

        if not os.path.exists(caminho):
            erro = f"Skill '{nome_skill}' não existe."
            print("--- SKILL FALHOU ---", erro)
            return erro

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                codigo = f.read()

            escopo = {
                "os": os,
                "time": time,
                "sys_ctrl": self,
                "full": self.acesso_total
            }

            exec(codigo, escopo)
            return f"Skill '{nome_skill}' executada."

        except Exception as e:
            erro = f"Erro na skill {nome_skill}: {str(e)}"
            print("--- ERRO SKILL ---", erro)
            self.acesso_total.registrar_log("ERRO DE SKILL", erro)
            return erro

    # ======================================================
    # STATUS
    # ======================================================

    def verificar_apis(self):
        chaves = os.getenv("GROQ_API_KEYS", "").split(",")
        status = f"Pool de APIs: {len(chaves)} chaves configuradas."

        if self.gui and hasattr(self.gui, "atualizar_monitor"):
            self.gui.atualizar_monitor(status)

        return status