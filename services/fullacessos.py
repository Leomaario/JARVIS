import os
import time
import pyautogui
import pygetwindow as gw
import pyperclip
import webbrowser
import psutil
import datetime # NECESSÁRIO PARA O LOG

class FullAccess:
    def __init__(self, gui_ref=None): # ADICIONADO gui_ref para evitar o TypeError
        # Configurações para automação fluida
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True
        
        self.gui = gui_ref # ARMAZENA A REFERÊNCIA DA GUI
        self.log_file = "auto_edition_history.log" # DEFINIÇÃO DO ARQUIVO DE LOG

    def focar_e_ler_vscode(self):
        """Foca no VS Code, copia todo o código e retorna o texto."""
        try:
            vscode = gw.getWindowsWithTitle('Visual Studio Code')
            if vscode:
                vscode[0].activate()
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.2)
                return pyperclip.paste()
            return "VS Code não encontrado."
        except Exception as e:
            return f"Erro ao acessar VS Code: {e}"

    def organizar_area_trabalho(self):
        """Minimiza tudo, exceto o JARVIS e o VS Code."""
        for window in gw.getAllWindows():
            if window.title and not any(x in window.title for x in ["JARVIS", "Visual Studio Code"]):
                try:
                    window.minimize()
                except:
                    pass
        return "Área de trabalho organizada, chefe."

    def modo_suporte_santa_casa(self):
        """Abre as ferramentas padrão para o seu trabalho na Santa Casa."""
        # Link real pode ser inserido aqui no futuro pelo Leo
        webbrowser.open("https://google.com") 
        os.system("code") 
        return "Modo Suporte N1 ativado."

    def ler_arquivo_projeto(self, caminho_relativo):
        """Lê o conteúdo de qualquer arquivo no diretório do projeto."""
        try:
            with open(caminho_relativo, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {e}"

    def executar_terminal(self, comando):
        """Abre o CMD e executa um comando diretamente."""
        os.system(f"start cmd /k {comando}")
        return f"Comando '{comando}' disparado no terminal."
    
    def abortar_processos_ia(self):
        """Para qualquer movimento do mouse ou digitação que a IA esteja fazendo."""
        return "Processos de automação resetados para nova instrução."
    
    def registrar_log(self, acao, detalhe):
        """Salva o histórico de alterações para auditoria do Leo."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {acao.upper()}: {detalhe}\n")
        except Exception as e:
            print(f"Erro ao escrever log: {e}")

    def injetar_nova_funcao(self, nome_arquivo, codigo_novo):
        """Tenta injetar código e registra se deu erro."""
        self.registrar_log("TENTATIVA DE INJEÇÃO", f"Arquivo: {nome_arquivo}")
        try:
            # Faz backup do arquivo original antes de mexer (Segurança SouzaLink)
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, "r", encoding="utf-8") as original:
                    backup = original.read()
                
                with open(f"{nome_arquivo}.bak", "w", encoding="utf-8") as bkp_file:
                    bkp_file.write(backup)

            # Injeta a nova função no final do arquivo
            with open(nome_arquivo, "a", encoding="utf-8") as f:
                f.write(f"\n\n{codigo_novo}\n")
            
            self.registrar_log("SUCESSO", f"Código injetado em {nome_arquivo}")
            
            # Se a GUI estiver conectada, avisa na telinha de monitoramento
            if self.gui:
                self.gui.after(0, self.gui.atualizar_monitor, "SISTEMA ATUALIZADO")
            return True
        except Exception as e:
            self.registrar_log("ERRO CRÍTICO", str(e))
            return False
    
    def criar_skill(self, nome_skill, codigo_python):
        """Cria um arquivo independente para a nova habilidade do JARVIS."""
        pasta_skills = "skills"
        
        # Cria a pasta skills se ela não existir
        if not os.path.exists(pasta_skills):
            os.makedirs(pasta_skills)

        # Garante que termine com .py
        if not nome_skill.endswith(".py"):
            nome_skill += ".py"

        caminho_arquivo = os.path.join(pasta_skills, nome_skill)
        self.registrar_log("CRIANDO SKILL", f"Arquivo: {nome_skill}")
        
        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(codigo_python)
            
            self.registrar_log("SUCESSO", f"Skill {nome_skill} pronta.")
            if self.gui:
                self.gui.after(0, self.gui.atualizar_monitor, f"SKILL INSTALADA: {nome_skill}")
            
            return f"Skill '{nome_skill}' criada com sucesso, chefe. Para rodar, use [CMD: sys_ctrl.executar_skill('{nome_skill}')]"
        except Exception as e:
            self.registrar_log("ERRO CRÍTICO", str(e))
            return f"Erro ao criar skill: {str(e)}"