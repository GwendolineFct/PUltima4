from file_io import DosFile
from handlers import EventHandler

class Dialog:
    question_flag: int
    affects_humility: bool
    turn_away_probability: int
    name: str
    pronoun: str
    look_description: str
    look_description: str
    job_response: str
    health_response: str
    keyword1_response: str
    keyword2_response: str
    yes_no_question: str
    yes_response: str
    no_response: str
    keyword1: str
    keyword2: str

    def __init__(self, filename: str, dialog_index: int) -> None:
        tlk_file = DosFile(filename)
        tlk_file.seek(288 * dialog_index)
        dialog = Dialog()
        dialog.question_flag = tlk_file.read()
        dialog.affects_humility = tlk_file.read()
        dialog.turn_away_probability = tlk_file.read()
        dialog.name = tlk_file.read_asciiz()
        dialog.pronoun = tlk_file.read_asciiz()
        dialog.look_description = tlk_file.read_asciiz()
        dialog.job_response = tlk_file.read_asciiz()
        dialog.job_response = tlk_file.read_asciiz()
        dialog.health_response = tlk_file.read_asciiz()
        dialog.keyword1_response = tlk_file.read_asciiz()
        dialog.keyword2_response = tlk_file.read_asciiz()
        dialog.yes_no_question = tlk_file.read_asciiz()
        dialog.yes_response = tlk_file.read_asciiz()
        dialog.no_response = tlk_file.read_asciiz()
        dialog.keyword1 = tlk_file.read_asciiz()
        dialog.keyword2 = tlk_file.read_asciiz()


class DialogHandler(EventHandler):
    pass
