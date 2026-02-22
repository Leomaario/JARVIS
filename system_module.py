import os, subprocess, pyautogui, webbrowser, threading, time, mss
import pygetwindow as gw
from screeninfo import get_monitors
from fullacessos import FullAccess
import ast

class SystemController:
    def __init__(self, gui_ref=None):
        self.gui = gui_ref
        # O FullAccess agora recebe a referência da GUI para atualizar o monitor
        self.acesso_total = FullAccess(gui_ref)

    def mapear_ambiente(self):
        """Lista todos os monitores e suas coordenadas para o cérebro."""
        monitores = get_monitors()
        mapa = "RELATÓRIO DE HARDWARE:\n"
        for i, m in enumerate(monitores):
            mapa += f"- Monitor {i+1}: {m.width}x{m.height} em X={m.x}, Y={m.y} (Principal: {m.is_primary})\n"
        return mapa

    def listar_janelas_ativas(self):
        """Retorna os títulos das janelas visíveis para consciência de software."""
        janelas = [w.title for w in gw.getWindowsWithTitle('') if w.visible and w.title.strip()]
        return "JANELAS ABERTAS: " + ", ".join(janelas[:6])

    def take_screenshot(self, filename="visao.png", monitor_index=1):
        """Captura o monitor especificado. Monitor 1 é o padrão."""
        import mss.tools
        with mss.mss() as sct:
            try:
                # Ajuste de índice: sct.monitors[0] é a tela combinada. [1], [2] são as físicas.
                if monitor_index >= len(sct.monitors):
                    monitor_index = 1
                
                monitor = sct.monitors[monitor_index]
                print(f"--- CAPTURANDO MONITOR {monitor_index} ---")
                
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
                
                # Aguarda o IO do Windows finalizar o arquivo
                time.sleep(0.2)
                return filename
            except Exception as e:
                print(f"Erro MSS: {e}. Usando Fallback PyAutoGUI.")
                pyautogui.screenshot(filename)
                return filename

    def execute_command(self, cmd_string):
        def run_it():
            try:
                exec_scope = {
                    "os": os, "pyautogui": pyautogui, "webbrowser": webbrowser,
                    "time": time, "full": self.acesso_total, "sys_ctrl": self
                }
                exec(cmd_string, exec_scope)
            except Exception as e:
                # SE DER ERRO, SALVA NO LOG AUTOMATICAMENTE
                erro_msg = f"Falha ao executar '{cmd_string}': {str(e)}"
                print(f"--- [ERRO DE AUTONOMIA] --- {erro_msg}")
                self.acesso_total.registrar_log("ERRO DE EXECUÇÃO", erro_msg)
                
                if self.gui:
                    self.gui.after(0, self.gui.display_message, "SISTEMA", "Erro na execução. Log gerado.")

        threading.Thread(target=run_it, daemon=True).start()

    def verificar_apis(self):
        """Retorna o status do pool de chaves para o monitor."""
        chaves = os.getenv("GROQ_API_KEYS", "").split(",")
        status = f"Pool de APIs: {len(chaves)} chaves configuradas."
        if self.gui:
            self.gui.atualizar_monitor(status)
        return status

    def execute_command(self, cmd_string):
        def run_it():
            # 1. VALIDAÇÃO DE SINTAXE (A trava de segurança recomendada)
            try:
                # O ast.parse lê o código sem executá-lo. Se tiver erro, ele grita aqui.
                ast.parse(cmd_string)
            except SyntaxError as e:
                erro_sintaxe = f"Comando gerado pela IA tem erro de sintaxe: {e}"
                print(f"--- [BLOQUEADO PELO SISTEMA] --- {erro_sintaxe}")
                self.acesso_total.registrar_log("COMANDO BLOQUEADO", erro_sintaxe)
                
                if self.gui:
                    self.gui.after(0, self.gui.display_message, "SISTEMA", "Comando abortado por segurança (Erro de Sintaxe).")
                return # PARA TUDO. Não deixa o exec() rodar e quebrar o terminal.

            # 2. EXECUÇÃO (Só chega aqui se o código for válido no Python)
            try:
                print(f"--- [EXECUTANDO COMANDO VALIDADO] --- {cmd_string}")
                exec_scope = {
                    "os": os, "pyautogui": pyautogui, "webbrowser": webbrowser,
                    "time": time, "full": self.acesso_total, "sys_ctrl": self
                }
                exec(cmd_string, exec_scope)
            except Exception as e:
                # Se der erro durante a execução (ex: variável não existe)
                erro_msg = f"Falha na execução: {str(e)}"
                print(f"--- [ERRO DE RUNTIME] --- {erro_msg}")
                self.acesso_total.registrar_log("ERRO DE EXECUÇÃO", erro_msg)
                
                if self.gui:
                    self.gui.after(0, self.gui.display_message, "SISTEMA", f"Erro interno: {str(e)}")

        threading.Thread(target=run_it, daemon=True).start()

    def executar_skill(self, nome_skill):
        """Lê e executa o código de uma skill isolada."""
        if nome_skill.endswith(".py"):
            nome_skill = nome_skill.replace(".py", "")
            
        caminho_arquivo = os.path.join("skills", f"{nome_skill}.py")
        
        if not os.path.exists(caminho_arquivo):
            erro = f"A skill '{nome_skill}' não existe na base de dados."
            print(f"--- [SKILL FALHOU] --- {erro}")
            return erro
        
        try:
            # Lê o código do arquivo isolado
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                codigo_skill = f.read()
            
            # Executa o código em um ambiente seguro, dando acesso ao sys_ctrl
            escopo_isolado = {
                "os": os, "time": time, 
                "sys_ctrl": self, "full": self.acesso_total
            }
            exec(codigo_skill, escopo_isolado)
            return f"Skill '{nome_skill}' finalizada."
            
        except Exception as e:
            erro_msg = f"Erro ao rodar a skill {nome_skill}: {str(e)}"
            print(f"--- [ERRO NA SKILL] --- {erro_msg}")
            self.acesso_total.registrar_log("ERRO DE SKILL", erro_msg)
            return erro_msg
        
    def handle_text_input(self, text):
        """Processa uma entrada de texto do usuário."""
        if text.startswith("[CMD:"):
            cmd = text[5:-1].strip()  # Remove os colchetes e espaços extras
            self.execute_command(cmd)
        else:
            self.execute_command(f"full.registrar_log('INPUT USUÁRIO', '{text}')")
    
    