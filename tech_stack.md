# Tecnologias Selecionadas para o Agente de IA (100% Grátis)

## 1. Interface Gráfica (GUI)
- **Biblioteca:** `CustomTkinter` ou `PyQt6` com `QML/QtQuick`.
- **Visual:** Para a esfera holográfica animada (estilo JARVIS/Cortana), usaremos um GIF animado ou sequências de imagens em um canvas transparente. `CustomTkinter` é mais simples para o chat, mas `PyQt6` permite transparências e animações mais fluidas para a esfera.
- **Decisão:** `CustomTkinter` para a estrutura principal (chat e botões) e um `Label` ou `Canvas` para a animação da esfera.

## 2. Núcleo de Inteligência (LLM)
- **Provedor:** **Groq** (API extremamente rápida e com plano gratuito generoso) ou **SiliconFlow** / **OpenRouter** (acesso a modelos como Llama 3, Mixtral).
- **Modelo:** `Llama-3-70b` ou `Gemma-7b` (via Groq para latência mínima).

## 3. Voz (STT e TTS)
- **STT (Speech-to-Text):** Biblioteca `SpeechRecognition` com o motor `Google Web Speech API` (grátis e sem chave para uso moderado) ou `Faster-Whisper` (local, 100% grátis e privado).
- **TTS (Text-to-Speech):** `pyttsx3` (funciona offline, usa vozes do Windows) ou `gTTS` (Google TTS, requer internet, voz mais natural).

## 4. Memória de Longo Prazo
- **Abordagem:** Banco de dados vetorial local simples (`ChromaDB` ou `FAISS`) ou apenas um arquivo JSON/SQLite para armazenar o histórico de conversas e fatos importantes.
- **Decisão:** SQLite para histórico de chat e um sistema simples de "tags" ou "resumos" para memória de longo prazo.

## 5. Acesso ao Sistema (Full Access)
- **Biblioteca:** `os`, `subprocess`, `pyautogui` (para automação de interface), `shutil`.
- **Segurança:** O agente terá funções para executar comandos shell e manipular arquivos.

## 6. Upload de Arquivos
- **Implementação:** Botão na interface que abre o explorador de arquivos do Windows e envia o conteúdo (texto ou metadados) para o contexto do LLM.
