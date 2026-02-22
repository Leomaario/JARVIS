# Arquitetura do Agente de IA "Holograma"

O agente será estruturado em módulos independentes para facilitar a manutenção e garantir que cada funcionalidade (voz, visão, inteligência e memória) opere de forma síncrona com a interface do usuário. A arquitetura segue um modelo de **Event Loop** centralizado na interface gráfica (GUI), que coordena as chamadas para os outros serviços.

## Componentes Principais

O sistema será dividido em cinco módulos fundamentais, cada um com uma responsabilidade clara e bem definida:

| Módulo | Responsabilidade | Tecnologias Utilizadas |
| :--- | :--- | :--- |
| **Interface (GUI)** | Exibir a esfera holográfica animada, chat de texto e botões de ação. | `CustomTkinter`, `PIL` (Pillow) |
| **Audição (STT)** | Capturar áudio do microfone e converter para texto em tempo real. | `SpeechRecognition`, `PyAudio` |
| **Fala (TTS)** | Converter as respostas de texto do agente em voz audível. | `pyttsx3` (Offline) ou `gTTS` (Online) |
| **Cérebro (LLM)** | Processar comandos, manter o contexto e decidir ações no sistema. | `Groq API` (Llama 3), `requests` |
| **Memória (DB)** | Armazenar histórico de conversas e fatos importantes para longo prazo. | `SQLite`, `json` |
| **Sistema (OS)** | Executar comandos no Windows, abrir arquivos e controlar o PC. | `os`, `subprocess`, `pyautogui` |

## Fluxo de Execução

O fluxo de trabalho do agente seguirá uma sequência lógica de processamento de informações:

1.  **Entrada:** O usuário fornece um comando via voz (ativado por palavra-chave ou botão) ou digita no chat de texto.
2.  **Processamento de Voz:** Se a entrada for áudio, o módulo de audição converte o som em uma string de texto.
3.  **Consulta à Memória:** O sistema busca no banco de dados SQLite os últimos diálogos e informações relevantes sobre o usuário para compor o prompt.
4.  **Decisão (LLM):** O texto é enviado para a API do Groq. O modelo Llama 3 analisa se o pedido é uma conversa comum ou um comando de sistema (ex: "abra o bloco de notas").
5.  **Ação no Sistema:** Se for um comando, o módulo de sistema executa a tarefa via `subprocess` ou `pyautogui`.
6.  **Resposta:** O agente gera uma resposta textual confirmando a ação ou respondendo à pergunta.
7.  **Saída:** A resposta é exibida no chat e convertida em voz pelo módulo de fala, enquanto a esfera holográfica pulsa na tela.

## Estrutura de Arquivos do Projeto

Para manter o código organizado e fácil de configurar, o projeto será dividido nos seguintes arquivos:

-   `main.py`: Ponto de entrada que inicializa a GUI e coordena os módulos.
-   `gui_module.py`: Contém a classe da interface e a lógica de animação da esfera.
-   `brain_module.py`: Gerencia a comunicação com a API do LLM e a lógica de "ferramentas" (tools).
-   `voice_module.py`: Implementa as funções de `listen()` e `speak()`.
-   `memory_module.py`: Lida com a persistência de dados no banco SQLite.
-   `system_module.py`: Contém as funções de manipulação de arquivos e comandos do Windows.
-   `config.py`: Arquivo central para chaves de API e configurações de personalização.
