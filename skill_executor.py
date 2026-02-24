def executar_skill(command):

    try:
        print("Executando:", command)

        # CUIDADO: sandbox depois
        exec(command)

        return "Comando executado com sucesso."

    except Exception as e:
        return f"Erro ao executar comando: {e}"