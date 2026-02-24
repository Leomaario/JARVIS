import time
import threading

class ConsciousnessEngine:

    def __init__(self, brain, system, gui, webcam):
        self.brain = brain
        self.system = system
        self.gui = gui
        self.webcam = webcam
        self.running = True

    def start(self):
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):

        while self.running:

            activity = self.webcam.last_activity

            if activity == "phone":
                self.gui.display_message("JARVIS","Chefe, evitando distrações aumenta produtividade.")

            if activity == "sleepy":
                self.gui.display_message("JARVIS","Chefe, recomendo pausa.")

            time.sleep(20)