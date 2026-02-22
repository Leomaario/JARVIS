import speech_recognition as sr
import asyncio, edge_tts, pygame, os, threading, time

class VoiceAssistant:
    def __init__(self):
        pygame.mixer.init()
        self.voice = "pt-BR-AntonioNeural"
        self.temp_audio = "jarvis_temp.mp3"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def stop_speaking(self):
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except: pass

    def speak(self, text, ui_callback=None):
        def run_speak():
            self.stop_speaking()
            time.sleep(0.1)
            if ui_callback: ui_callback(True)
            try:
                communicate = edge_tts.Communicate(text, self.voice)
                asyncio.run(communicate.save(self.temp_audio))
                pygame.mixer.music.load(self.temp_audio)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): time.sleep(0.1)
                pygame.mixer.music.unload()
            except Exception as e: print(f"Erro Voz: {e}")
            if ui_callback: ui_callback(False)
        threading.Thread(target=run_speak, daemon=True).start()

    def listen(self, callback):
        def run_listen():
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    callback(self.recognizer.recognize_google(audio, language="pt-BR"))
                except: pass
        threading.Thread(target=run_listen, daemon=True).start()