from constants import *
from map import TownMap
from state import State
from util import rnd
from event import INPUT_STRING, Event, EventHandler, InputEvent
import binaries

class Command():
    def __init__(self) -> None:
        pass

    def do_cant(self, state: State):
        state.console.print("Can't").newline()

    def do_what(self, state: State):
        state.console.print("What ?").newline()


    def not_here(self, state: State):
        self.console.print("Not here").newline()
        return self

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"

class CommandEvent(Event):
    command: Command

    def __init__(self, command: Command) -> None:
        self.command = command

    def handle_event(self, event: Event, handler: EventHandler):
        pass

    def __repr__(self) -> str:
        return f"<CommandEvent command={self.command}>"

class ImmediateCommand(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, handler: EventHandler) -> EventHandler: ...

class InteractiveCommand(Command):
    def __init__(self) -> None:
        super().__init__()

    def init(self, handler: EventHandler): ...

    def handle_event(event: Event, handler: EventHandler) -> EventHandler: ...

class PassCommand(ImmediateCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, handler: EventHandler) -> EventHandler:
        handler.state.console.print("Pass").newline()
        return handler

class EchoCommand(InteractiveCommand):
    def __init__(self) -> None:
        super().__init__()

    def init(self, handler: EventHandler) -> EventHandler:
        handler.state.console.print("Echo:").prompt()
        handler.mode = INPUT_STRING
        return self

    def handle_event(event: Event, handler: EventHandler) -> EventHandler:
        if isinstance(event, InputEvent):
            handler.state.console.print(f"<{event.input}>")




class MoveCommand(ImmediateCommand):
    dir: tuple

    def __init__(self, dir: tuple) -> None:
        super().__init__()
        self.dir = dir

    def __repr__(self) -> str:
        return f"<{type(self).__name__} dir={self.dir}>"


    def execute(self, state: State, handler: EventHandler) -> EventHandler:
        console = state.console
        map = state.map
        party = state.party
        dir = self.dir

        if dir == DIR_WEST:
            console.print("West").newline()
        elif dir == DIR_EAST:
            console.print("East").newline()
        elif dir == DIR_NORTH:
            console.print("North").newline()
        elif dir == DIR_SOUTH:
            console.print("South").newline()

        if party.transportation == TILE_BALLOON:
            console.print("Drift only!").newline()
        elif TILE_SHIP_WEST <= party.transportation <= TILE_SHIP_SOUTH \
            and party.transportation - TILE_SHIP_WEST != dir:
            # ship must turn before moving
            party.transportation = party.transportation - TILE_SHIP_WEST + dir
        elif not self.can_move(state, dir):
            console.print("Blocked").newline()
        elif self.move_slowed(state):
            console.print("Slow progress!").newline()
        else:
            party.x += dir[0]
            party.y += dir[1]
            if map.wraps:
                party.x %= map.width
                party.y %= map.height
            elif (party.x, party.y) not in map:
                console.print("Leaving...").newline()
                state.map = state.world_map
                party.x = binaries.avatar_exe.locations_x[party.location]
                party.y = binaries.avatar_exe.locations_y[party.location]
                party.location = LOC_BRITANNIA

        return self

    def move_slowed(self, state: State) -> bool:
        map = state.map
        party = state.party
        current_tile = map[(party.x, party.y, party.z)]

        if party.transportation == TILE_AVATAR:
            if current_tile == TILE_SWAMPS:
                return rnd(8) == 0
            elif current_tile == TILE_BRUSH:
                return rnd(4) == 0
            elif current_tile == TILE_HILLS or current_tile == TILE_FIRE_FIELD:
                return rnd(2) == 0
        elif TILE_SHIP_WEST <= party.transportation <= TILE_SHIP_SOUTH:
            ship_dir = party.transportation - TILE_SHIP_WEST
            if ship_dir == state.wind_dir:
                return rnd(4) == 0
            elif ship_dir == state.wind_dir ^ 0b10:
                return rnd(4) != 0
        return False

    def can_move(self, state: State, dir: tuple) -> bool:
        party = state.party
        current_tile = state.map[(party.x, party.y, party.z)]
        dest_tile = state.map[(party.x + dir[0], party.y + dir[1], party.z)]
        if party.transportation == TILE_AVATAR or party.transportation == TILE_HORSE_EAST or party.transportation == TILE_HORSE_WEST:
            if dest_tile == TILE_LCB_ENTRANCE:
                return dir[1] == -1
            if current_tile == TILE_LCB_ENTRANCE:
                return dir[1] == 1
            if dest_tile in binaries.avatar_exe.walkable_tiles:
                return True
            return False
        elif party.transportation == TILE_BALLOON:
            return dest_tile != TILE_MOUNTAINS
        elif TILE_SHIP_WEST <= party.transportation <= TILE_SHIP_SOUTH:
            return dest_tile in (TILE_DEEP_WATER, TILE_MEDIUM_WATER, TILE_WHIRLPOOL_1, TILE_WHIRLPOOL_2)
        return False

class NorthCommand(MoveCommand):
    def __init__(self) -> None:
        super().__init__(DIR_NORTH)

class SouthCommand(MoveCommand):
    def __init__(self) -> None:
        super().__init__(DIR_SOUTH)

class WestCommand(MoveCommand):
    def __init__(self) -> None:
        super().__init__(DIR_WEST)

class EastCommand(MoveCommand):
    def __init__(self) -> None:
        super().__init__(DIR_EAST)


class EnterCommand(ImmediateCommand):
    def __init__(self) -> None:
        super().__init__()

    def execute(self, state: State, handler: EventHandler) -> bool:
        state.console.print("Enter ")
        p = -1
        if state.party.location == 0:
            for n in range(32):
                if binaries.avatar_exe.locations_x[n] == state.party.x and binaries.avatar_exe.locations_y[n] == state.party.y:
                    p = n
                    break
        if p >= 16:
            p = -1

        if p == -1:
            return self.do_what(state)

        if p <= LOC_SERPENTS_HOLD:
            state.console.print(binaries.avatar_exe.location_types[2])
        elif p <= LOC_SKARA_BRAE:
            state.console.print(binaries.avatar_exe.location_types[3])
        elif p <= LOC_MAGINCIA:
            state.console.print(binaries.avatar_exe.location_types[4])
        elif p <= LOC_COVE:
            state.console.print(binaries.avatar_exe.location_types[1])
        elif p <= LOC_ABBYSS:
            state.console.print(binaries.avatar_exe.location_types[0])
        else:
            state.console.print(binaries.avatar_exe.location_types[5])

        state.console.print(binaries.avatar_exe.location_names[p]).newline().newline()

        state.map = TownMap(binaries.avatar_exe.ult_filenames[p])
        state.party.location = p
        if state.party.location < 4:
            state.party.x = 15
            state.party.y = 31
        else:
            state.party.x = 0
            state.party.y = 15

        return self
