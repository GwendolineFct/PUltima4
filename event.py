import pygame
from constants import *
from command import *
from ui import Console


class Command():
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

class Event:
    type: str

    def __init__(self, type: str) -> None:
        self.type = type

class TickEvent(Event):
    def __init__(self) -> None:
        super().__init__("tick")

    def __repr__(self) -> str:
        return f"<TickEvent>"

class KeyEvent(Event):
    key: int
    modifiers: int

    def __init__(self, key: int, modifiers: int) -> None:
        super().__init__("key")
        self.key = key
        self.modifiers = modifiers

    def __repr__(self) -> str:
        return f"<KeyEvent key={self.key}, modifiers={'{:016b}'.format(self.modifiers)}>"

class MouseEvent(Event):
    buttons: int
    x: int
    y: int

    def __init__(self, buttons: int, pos: tuple) -> None:
        super().__init__("mouse")
        self.buttons = buttons
        self.x = pos[0]
        self.y = pos[1]

    def __repr__(self) -> str:
        return f"<MouseEvent buttons={self.buttons}, x={self.x}, y={self.y}>"

class DirectionEvent(Event):
    dir: int

    def __init__(self, dir: int) -> None:
        self.dir = dir

    def __repr__(self) -> str:
        return f"<DirectionEvent dir={self.dir}>"

class DigitEvent(Event):
    digit: int

    def __init__(self, digit: str) -> None:
        self.digit = digit

    def __repr__(self) -> str:
        return f"<DigitEvent digit={self.digit}>"

class InputEvent(Event):
    input: str

    def __init__(self, input: str) -> None:
        self.input = input

    def __repr__(self) -> str:
        return f"<InputEvent input={self.input}>"


class EventHandler(): ...

class EventHandler:
    def handle_event(self, event: Event) -> EventHandler:
        pass


INPUT_COMMAND = 0
INPUT_KEY = 1
INPUT_DIR = 2
INPUT_DIGIT = 3
INPUT_YES_NO = 4
INPUT_CHOICE = 5
INPUT_STRING = 6

keys = {
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_0: "0",
    pygame.K_SPACE: " ",
}

class InputEventHandler(EventHandler):
    console: Console
    input: str
    mode: int
    choices: str

    def __init__(self, console: Console) -> None:
        super().__init__()
        self.console = console

    def handle_event(self, event: Event) -> EventHandler:
        if self.mode == INPUT_STRING and isinstance(event, KeyEvent):
            shift = event.modifiers & (pygame.K_LSHIFT | pygame.K_RSHIFT)
            ctrl = event.modifiers & (pygame.K_LCTRL | pygame.K_RCTRL)
            alt = event.modifiers & (pygame.K_LALT | pygame.K_RALT)
            if alt or ctrl:
                return self
            key = event.key
            if key == pygame.K_RETURN:
                self.console.hide_cursor()
                return self.handle_event(InputEvent(self.input))
            if key == pygame.K_BACKSPACE:
                self.console.backspace()
                self.input = self.input[:len(self.input)-1] if len(self.input > 0) else self.input
            if key not in keys or len(self.input) > 16:
                return self
            key = keys[key]
            if shift and "a" < key <= "z":
                key = key.upper()
            self.console.print(key)
            self.input += key
            return self

    def input(self):
        self.mode == INPUT_STRING
        self.input = ""
        self.console.prompt()
