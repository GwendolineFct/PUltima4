from pygame import Surface


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

class EventHandler:
    pass

class EventHandler:

    def init(self): ...

    def handle_event(self, event: Event) -> EventHandler: ...

    def render(self, surface: Surface): ...
    
    def dispose(self): ...