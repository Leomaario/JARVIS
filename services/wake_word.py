import speech_recognition as sr


def listen(timeout=5, phrase_time_limit=10):

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Ouvindo...")

            # reduz ruído ambiente
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        # Google Speech
        text = recognizer.recognize_google(audio, language="pt-BR")
        print("Você disse:", text)

        return text

    except sr.WaitTimeoutError:
        return None

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        print("Erro no serviço de reconhecimento.")
        return None

    except Exception as e:
        print("Erro microfone:", e)
        return None