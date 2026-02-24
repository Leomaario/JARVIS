import re

class IntentRouter:

    def __init__(self, system_controller):
        self.system = system_controller

    def handle(self, text: str):
        text = text.lower()

        # ===== ABRIR CAMERA =====
        if "abrir camera" in text or "abra a camera" in text:
            self.system.open_camera_second_monitor()
            return "Câmera aberta no segundo monitor."

        # ===== CRIAR PDF =====
        if "crie um pdf" in text:
            assunto = self._extrair_assunto(text)
            self.system.create_pdf_report(assunto)
            return f"PDF criado sobre {assunto}."

        return None

    def _extrair_assunto(self, text):
        match = re.search(r"pdf sobre (.*)", text)
        return match.group(1) if match else "relatório"