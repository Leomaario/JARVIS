import re
from skill_executor import executar_skill


def parse_and_execute(text):

    match = re.search(r"\[CMD:(.*?)\]", text)

    if not match:
        return None

    command = match.group(1).strip()

    return executar_skill(command)