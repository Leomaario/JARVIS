from brain_module import AgentBrain
from command_parser import parse_and_execute
from tts_engine import speak


class JarvisCore:

    def __init__(self, api_key):
        self.brain = AgentBrain(api_key)

    def handle_input(self, text):

        response = self.brain.process_input(text)

        # executa comandos automáticos
        cmd_result = parse_and_execute(response)

        if cmd_result:
            speak(cmd_result)
            return cmd_result

        speak(response)
        return response