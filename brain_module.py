import requests
import os
import time
from memory_module import MemoryManager


class AgentBrain:
    def __init__(self, api_key, model="llama-3.3-70b-versatile"):

        # ===== GROQ (ÚLTIMO RECURSO) =====
        self.api_keys = [k.strip() for k in api_key.split(",") if k.strip()] if api_key else []
        self.current_key_index = 0
        self.model = model
        self.url_groq = "https://api.groq.com/openai/v1/chat/completions"

        self.memory = MemoryManager()

        # ===== OUTRAS APIs =====
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.cohere_key = os.getenv("COHERE_API_KEY", "").strip()

        self.system_prompt = (
            "Você é o JARVIS. Administrador: Leo (SouzaLink). "
            "Se o chefe pedir para criar uma função nova, use EXATAMENTE: "
            "[CMD: full.criar_skill('nome_da_skill', 'codigo_python')]"
        )

    # ======================================================
    # UTIL
    # ======================================================

    def get_active_key(self):
        if not self.api_keys:
            return None
        return self.api_keys[self.current_key_index]

    def rotate_key(self):
        if self.api_keys:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            print(f"--- [RODÍZIO] Groq chave {self.current_key_index + 1} ---")

    # ======================================================
    # 1️⃣ OPENROUTER (PRINCIPAL)
    # ======================================================

    def _call_openrouter(self, messages):
        print("--- [MOTOR PRINCIPAL] OpenRouter ---")

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Jarvis"
        }

        payload = {
            # MODELO VÁLIDO (SEM :free)
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": messages,
            "temperature": 0.4
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)

        if response.status_code != 200:
            print("OpenRouter erro:", response.status_code)
            print(response.text)
            return None

        return response.json()["choices"][0]["message"]["content"]

    # ======================================================
    # 2️⃣ GEMINI (FALLBACK 1)
    # ======================================================

    def _call_gemini(self, messages):
        print("--- [FALLBACK 1] Gemini ---")

        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/gemini-1.5-flash-latest:generateContent?key={self.gemini_key}"
        )

        contents = []

        for msg in messages:
            role = "user" if msg["role"] != "assistant" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        payload = {"contents": contents}

        response = requests.post(url, json=payload, timeout=20)

        if response.status_code != 200:
            print("Gemini erro:", response.status_code)
            print(response.text)
            return None

        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    # ======================================================
    # 3️⃣ COHERE (FALLBACK 2)
    # ======================================================

    def _call_cohere(self, messages):
        print("--- [FALLBACK 2] Cohere ---")

        url = "https://api.cohere.ai/v2/chat"

        headers = {
            "Authorization": f"Bearer {self.cohere_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "command-r",
            "messages": [
                {"role": msg["role"], "content": msg["content"]}
                for msg in messages
            ]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)

        if response.status_code != 200:
            print("Cohere erro:", response.status_code)
            print(response.text)
            return None

        return response.json()["message"]["content"][0]["text"]

    # ======================================================
    # 4️⃣ GROQ (ÚLTIMA DEFESA)
    # ======================================================

    def _call_groq(self, messages):
        if not self.api_keys:
            return None

        print("--- [FALLBACK 3] Groq Pool ---")

        for _ in range(len(self.api_keys)):

            headers = {
                "Authorization": f"Bearer {self.get_active_key()}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.4
            }

            response = requests.post(self.url_groq, headers=headers, json=payload, timeout=15)

            if response.status_code == 429:
                print("Groq 429 - aguardando 3s...")
                time.sleep(3)
                self.rotate_key()
                continue

            if response.status_code == 401:
                print("Groq 401 - chave inválida.")
                self.rotate_key()
                continue

            if response.status_code != 200:
                print("Groq erro:", response.status_code)
                print(response.text)
                return None

            return response.json()["choices"][0]["message"]["content"]

        return None

    # ======================================================
    # PROCESSAMENTO PRINCIPAL
    # ======================================================

    def process_input(self, user_text, hardware_context="", software_context=""):

        self.memory.salvar_interacao("user", user_text)
        historico = self.memory.obter_historico(limite=6)

        contexto_extra = f"\n{hardware_context}\n{software_context}"

        messages = [
            {"role": "system", "content": self.system_prompt + contexto_extra}
        ] + historico

        # 1️⃣ OpenRouter
        if self.openrouter_key:
            resposta = self._call_openrouter(messages)
            if resposta:
                self.memory.salvar_interacao("assistant", resposta)
                return resposta

        # 2️⃣ Gemini
        if self.gemini_key:
            resposta = self._call_gemini(messages)
            if resposta:
                self.memory.salvar_interacao("assistant", resposta)
                return resposta

        # 3️⃣ Cohere
        if self.cohere_key:
            resposta = self._call_cohere(messages)
            if resposta:
                self.memory.salvar_interacao("assistant", resposta)
                return resposta

        # 4️⃣ Groq
        resposta = self._call_groq(messages)
        if resposta:
            self.memory.salvar_interacao("assistant", resposta)
            return resposta

        return "Chefe, todos os motores estão indisponíveis no momento."