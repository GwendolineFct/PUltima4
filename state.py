from map import Map
from party import Party
from ui import Console

class State():
    console: Console
    party: Party
    map: Map
    world_map: Map
    wind_dir: int
    idle_count: int
    quit: bool
    in_combat: bool

    def __init__(self) -> None:
        self.console = None
        self.party = None
        self.map = None
        self.world_map = None
        self.wind_dir = None
        self.idle_count = 0
        self.quit = False
        self.in_combat = False
