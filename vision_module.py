import cv2
import numpy as np
import pytesseract
import pyautogui
import mss
import time
import threading


class VisionEngine:
    def __init__(self, system_controller, brain, gui=None):
        self.sys = system_controller
        self.brain = brain
        self.gui = gui

        self.intelligent_mode = False
        self.running = False

    # ======================================================
    # 📸 CAPTURA DE TELA
    # ======================================================

    def capture_screen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img

    # ======================================================
    # 🎯 POSIÇÃO DO MOUSE
    # ======================================================

    def get_mouse_position(self):
        return pyautogui.position()

    # ======================================================
    # 🔍 OCR
    # ======================================================

    def extract_text(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()

    # ======================================================
    # 🎨 DESENHAR OVERLAY DO MOUSE
    # ======================================================

    def draw_mouse_overlay(self, image):
        x, y = self.get_mouse_position()

        # círculo vermelho
        cv2.circle(image, (x, y), 20, (0, 0, 255), 3)
        cv2.putText(
            image,
            f"Mouse: {x},{y}",
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

        return image

    # ======================================================
    # 🧠 ANÁLISE VISUAL
    # ======================================================

    def analyze_scene(self):

        img = self.capture_screen()

        # Marca mouse
        img = self.draw_mouse_overlay(img)

        text_detectado = self.extract_text(img)

        contexto_visual = f"""
        CONTEXTO VISUAL DETECTADO:
        Texto visível na tela:
        {text_detectado[:1500]}

        """

        resposta = self.brain.process_input(
            user_text="Analise o que estou vendo na tela.",
            hardware_context=contexto_visual,
            software_context=""
        )

        return resposta, img

    # ======================================================
    # 🔥 LOOP INTELIGENTE
    # ======================================================

    def start_intelligent_mode(self):
        if self.running:
            return

        self.running = True
        self.intelligent_mode = True

        def loop():
            while self.running:
                try:
                    resposta, frame = self.analyze_scene()

                    # salva imagem temporária
                    cv2.imwrite("vision_preview.png", frame)

                    if self.gui:
                        self.gui.after(0, self.gui.display_message, "👁️ VISÃO", resposta)

                        # Atualiza monitor com imagem
                        if hasattr(self.gui, "atualizar_monitor"):
                            self.gui.after(
                                0,
                                self.gui.atualizar_monitor,
                                "VISÃO INTELIGENTE",
                                "vision_preview.png"
                            )

                except Exception as e:
                    print("Erro visão:", e)

                time.sleep(5)

        threading.Thread(target=loop, daemon=True).start()

    def stop_intelligent_mode(self):
        self.running = False
        self.intelligent_mode = False