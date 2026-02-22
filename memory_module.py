import sqlite3
import os

class MemoryManager:
    def __init__(self, db_name="agent_memory.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Cria a tabela se for a primeira vez rodando
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memoria 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)''')
        self.conn.commit()

    def salvar_interacao(self, role, content):
        """Salva a nova mensagem no banco de dados."""
        self.cursor.execute("INSERT INTO memoria (role, content) VALUES (?, ?)", (role, content))
        self.conn.commit()

    def obter_historico(self, limite=6):
        """
        Pega apenas as últimas X mensagens. 
        Isso é o que impede o erro 429 de limite de tokens da Groq!
        """
        self.cursor.execute("SELECT role, content FROM memoria ORDER BY id DESC LIMIT ?", (limite,))
        linhas = self.cursor.fetchall()
        
        # Retorna na ordem cronológica correta (do mais antigo para o mais novo)
        return [{"role": l[0], "content": l[1]} for l in reversed(linhas)]
        
    def limpar_memoria(self):
        """Reseta a memória se o sistema travar."""
        self.cursor.execute("DELETE FROM memoria")
        self.conn.commit()