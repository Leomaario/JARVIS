# Hologram AI Agent - Windows 10 (100% Grátis)

Este é um agente de IA completo desenvolvido em Python para desktop Windows 10, com interface inspirada em esferas holográficas, comandos por voz e texto, upload de arquivos e memória de longo prazo.

## 🚀 Funcionalidades Principais

- **Interface Holográfica:** Esfera animada (estilo JARVIS) que pulsa enquanto você interage.
- **Comandos de Voz (STT):** Clique no ícone do microfone para falar com o agente.
- **Resposta por Voz (TTS):** O agente responde usando as vozes nativas do seu Windows.
- **Chat de Texto:** Interface de chat moderna para comandos escritos.
- **Upload de Arquivos:** Anexe documentos para o agente ler e processar.
- **Acesso ao Sistema:** O agente pode abrir programas, pastas, tirar screenshots e navegar na web.
- **Memória de Longo Prazo:** Banco de dados SQLite que armazena fatos sobre você e o histórico de conversas.

## 🛠️ Requisitos de Instalação

1.  **Python 3.10+** instalado no seu Windows.
2.  Instale as bibliotecas necessárias abrindo o terminal e digitando:
    ```bash
    pip install customtkinter Pillow speechrecognition pyttsx3 requests pyautogui
    ```
    *(Nota: Para suporte a áudio, você pode precisar instalar o `PyAudio`. Se houver erro, use: `pip install pipwin` seguido de `pipwin install pyaudio`)*.

## 🔑 Configuração da API (Grátis)

O cérebro do agente utiliza a **Groq API**, que é extremamente rápida e possui um plano gratuito generoso.

1.  Crie uma conta gratuita em: [https://console.groq.com/](https://console.groq.com/)
2.  Gere uma **API KEY**.
3.  Abra o arquivo `main.py` e substitua `"SUA_CHAVE_AQUI"` pela sua chave real no campo `GROQ_API_KEY`.

## 📁 Estrutura do Projeto

- `main.py`: Arquivo principal que você deve executar.
- `gui_module.py`: Lógica da interface gráfica e animação.
- `voice_module.py`: Reconhecimento de fala e síntese de voz.
- `brain_module.py`: Inteligência artificial (LLM) e conexão com a API.
- `memory_module.py`: Banco de dados SQLite para memória persistente.
- `system_module.py`: Controle de arquivos e comandos do Windows.
- `hologram.gif`: (Opcional) Adicione um GIF de esfera dourada nesta pasta para a animação.

## 💡 Como Usar

1.  Execute o comando: `python main.py`
2.  Digite um comando no chat ou use o microfone.
3.  Para pedir ações no PC, diga algo como: "Abra o bloco de notas", "Pesquise sobre o clima em São Paulo" ou "Crie uma pasta chamada 'Trabalho' na minha área de trabalho".
4.  Para ensinar algo à IA, use: "Lembre que meu aniversário é dia 10 de maio".

---
*Desenvolvido para ser 100% gratuito e extensível.*
