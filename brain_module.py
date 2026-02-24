import requests
import os
import time
import re
import json
import subprocess
import traceback
import threading
import memory_module

SKILLS_FILE = "skills_memory.json"


# ======================================================
# IMPORTS OPCIONAIS (não quebra se faltar)
# ======================================================

try:
    from memory_module import MemoryManager
except:
    class MemoryManager:
        def salvar_interacao(self, *a, **k): pass
        def obter_historico(self, limite=6): return []

try:
    from stark_mode import StarkMode
except:
    class StarkMode:
        enabled = False
        def process(self, t): return t


# ======================================================
# LIMPEZA TEXTO
# ======================================================

def clean_text_for_output(text: str):
    if not text:
        return ""

    text = re.sub(r"[*_#`~]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def limit_response(text, max_sentences=3):
    parts = re.split(r"[.!?]", text)
    parts = [p.strip() for p in parts if p.strip()]
    return ". ".join(parts[:max_sentences]) + "." if parts else text


def format_final_response(text):
    return limit_response(clean_text_for_output(text))


# ======================================================
# SKILLS (CÓDIGOS SALVOS)
# ======================================================

class SkillManager:

    def __init__(self):
        self.skills = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(SKILLS_FILE):
                with open(SKILLS_FILE, "r", encoding="utf-8") as f:
                    self.skills = json.load(f)
        except:
            self.skills = {}

    def save(self):
        with open(SKILLS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.skills, f, indent=2)

    def create(self, name, code):
        self.skills[name] = code
        self.save()

    def delete(self, name):
        if name in self.skills:
            del self.skills[name]
            self.save()

    def run(self, name):

        if name not in self.skills:
            return "Skill não encontrada."

        try:
            # sandbox simples
            safe_globals = {"__builtins__": {}}
            exec(self.skills[name], safe_globals)
            return "Skill executada com sucesso."
        except Exception as e:
            return f"Erro executando skill: {e}"


# ======================================================
# AGENT BRAIN
# ======================================================

class AgentBrain:

    def __init__(self, api_key=None, model="llama-3.3-70b-versatile"):

        # APIs
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        self.api_keys = []
        if api_key:
            self.api_keys = [k.strip() for k in api_key.split(",") if k.strip()]

        self.current_key_index = 0
        self.model = model
        self.url_groq = "https://api.groq.com/openai/v1/chat/completions"

        # módulos
        self.memory = MemoryManager()
        self.stark = StarkMode()
        self.skills = SkillManager()

        # estado
        self.mood = "neutral"

        self.system_prompt = (
            "Você é JARVIS. Respostas curtas. Máximo 3 frases. "
            "Chame o usuário de Chefe."
        )

    # ======================================================
    # INTENT LOCAL
    # ======================================================

    def detect_local_intent(self, text):

        t = text.lower()

        if "abrir camera" in t or "abrir câmera" in t:
            return "open_camera"

        if "criar pdf" in t:
            return "create_pdf"

        if "guardar codigo" in t or "salvar codigo" in t:
            return "save_code"

        if "executar skill" in t:
            return "run_skill"

        return None

    # ======================================================
    # AÇÕES LOCAIS
    # ======================================================

    def execute_local_action(self, intent, text):

        try:

            if intent == "open_camera":
                subprocess.Popen("start microsoft.windows.camera:", shell=True)
                return "Abrindo câmera."

            if intent == "create_pdf":
                try:
                    from reportlab.pdfgen import canvas
                except:
                    return "Biblioteca reportlab não instalada."

                c = canvas.Canvas("relatorio.pdf")
                c.drawString(100, 750, f"Relatório criado: {time.ctime()}")
                c.save()
                return "PDF criado."

            if intent == "save_code":
                code_match = re.search(r"```(.*?)```", text, re.DOTALL)

                if code_match:
                    code = code_match.group(1)
                else:
                    code = text

                name = f"skill_{int(time.time())}"
                self.skills.create(name, code)

                return f"Código salvo como {name}"

            if intent == "run_skill":
                match = re.search(r"skill (\w+)", text.lower())
                if match:
                    return self.skills.run(match.group(1))
                return "Nome da skill não informado."

        except Exception as e:
            return f"Erro local: {e}"

        return None

    # ======================================================
    # IA — GROQ
    # ======================================================

    def _call_groq(self, messages):

        if not self.api_keys:
            return None

        # rotação de key
        for _ in range(len(self.api_keys)):

            key = self.api_keys[self.current_key_index]

            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.4
            }

            try:
                r = requests.post(self.url_groq, headers=headers, json=payload, timeout=20)

                if r.status_code == 200:
                    return r.json()["choices"][0]["message"]["content"]

            except:
                pass

            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

        return None

    # ======================================================
    # HUMOR
    # ======================================================

    def update_mood(self, text):

        t = text.lower()

        if any(w in t for w in ["erro", "falha", "problema"]):
            self.mood = "sad"
        elif any(w in t for w in ["bom", "sucesso", "feito"]):
            self.mood = "happy"
        else:
            self.mood = "neutral"

    # ======================================================
    # PROCESSAMENTO PRINCIPAL
    # ======================================================

    def process_input(self, user_text, hardware_context="", software_context=""):

        try:

            # salva memória
            self.memory.salvar_interacao("user", user_text)

            # intenção local
            intent = self.detect_local_intent(user_text)

            if intent:
                resposta = self.execute_local_action(intent, user_text)
                self.update_mood(resposta)
                return resposta

            # histórico
            historico = self.memory.obter_historico(limite=6) or []

            contexto = f"{hardware_context}\n{software_context}"

            messages = [
                {"role": "system", "content": self.system_prompt + "\n" + contexto}
            ] + historico + [
                {"role": "user", "content": user_text}
            ]

            resposta = self._call_groq(messages)

            if not resposta:
                resposta = "Chefe, sistemas offline no momento."

            # modo stark
            if getattr(self.stark, "enabled", False):
                resposta = self.stark.process(resposta)

            self.update_mood(resposta)

            resposta = format_final_response(resposta)

            self.memory.salvar_interacao("assistant", resposta)

            return resposta

        except Exception as e:
            print("Erro brain:", traceback.format_exc())
            return "Erro interno no núcleo cognitivo."