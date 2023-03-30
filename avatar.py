import random
import pygame
from command import *
from constants import *
import binaries
from binaries import load_avatar_exe
import graphics
from pygame import Surface
from event import *
from graphics import gfx_load_rle_image
from map import Map, TownMap, WorldMap
from party import Party
from state import State
from ui import Console
from util import rnd, sign


class CommandEventHandler(InputEventHandler):
    state: State
    current_command: Command

    def __init__(self, state: State) -> None:
        super().__init__(state.console)
        self.state = state
        self.mode = INPUT_COMMAND
        self.current_command = None

    def handle_event(self, event: Event) -> EventHandler:
        if self.current_command is not None:
            handler = self.current_command.handle_event(event, self)
            if handler == self:
                return self.end_turn()
            else:
                return handler
        elif isinstance(event, CommandEvent):
            if isinstance(event.command, ImmediateCommand):
                handler = event.command.execute(self)
                if handler == self:
                    return self.end_turn()
                else:
                    return handler
            elif isinstance(event.command, InteractiveCommand):
                handler = event.command.init(self)
                if handler:
                    self.current_command = event.command
                    return handler
                return self
        elif isinstance(event, KeyEvent):
            shift = event.modifiers & (pygame.K_LSHIFT | pygame.K_RSHIFT)
            ctrl = event.modifiers & (pygame.K_LCTRL | pygame.K_RCTRL)
            alt = event.modifiers & (pygame.K_LALT | pygame.K_RALT)
            key = event.key
            command = None
            if not shift and not ctrl and not alt:
                if key == pygame.K_UP:
                    command = NorthCommand()
                elif key == pygame.K_DOWN:
                    command = SouthCommand()
                elif key == pygame.K_RIGHT:
                    command = EastCommand()
                elif key == pygame.K_LEFT:
                    command = WestCommand()
                elif key == pygame.K_SPACE:
                    command = PassCommand()
                elif key == pygame.K_e:
                    command = EnterCommand()
            elif ctrl and not alt and not shift:
                if key == pygame.K_e:
                    command = EchoCommand()

            if command is None:
                self.console.print("What ?").newline()
                return self.end_turn()
            else:
                return self.handle_event(CommandEvent(command))
        return super().handle_event(event)

    def end_turn(self):
        self.current_command = None
        self.console.print(chr(16)).prompt()
        return self

class WorldEventHandler(CommandEventHandler):
    def __init__(self, state: State) -> None:
        super().__init__(state)

    def end_turn(self):
        self.handle_mobiles()
        return super().end_turn()

    def handle_mobiles(self):
        party = self.state.party
        map = self.state.map
        party_pos = [(party.x, party.y, party.z)]
        for mobile in map.mobiles:
            if mobile.behaviour == 0:
                continue
            elif mobile.behaviour == 1:
                if rnd(100) < 50:
                    continue
                dirs = [(0,1),(0,-1),(1,0),(-1,0)]
                random.shuffle(dirs)
                for dir in dirs:
                    if mobile.can_move(dir[0], dir[1], map, party_pos):
                        mobile.x += dir[0]
                        mobile.y += dir[1]
                        break
            elif mobile.behaviour == 80 or mobile.behaviour == 255:
                dx = party.x - mobile.x
                dy = party.y - mobile.y
                adx = abs(dx)
                ady = abs(dy)
                dx = sign(dx)
                dy = sign(dx)
                dx1, dy1, dx2, dy2 = 0, 0, 0, 0
                if adx == ady:
                    if rnd(100) < 50:
                        adx += 1
                    else:
                        adx += 1
                if adx > ady:
                    dx1, dy2 = dx, dy
                else:
                    dy2, dx1 = dy, dx

                if mobile.can_move(dx1, dy1, self.map, party_pos):
                    mobile.x += dx1[0]
                    mobile.y += dy1[1]
                elif mobile.can_move(dx2, dy2, self.map, party_pos):
                    mobile.x += dx2[0]
                    mobile.y += dy2[1]

class Avatar():

    _elapsed_time: int
    background: Surface
    console: Console
    party: Party
    map: Map
    world_map: WorldMap
    handlers: list
    current_command: Command

    def __init__(self) -> None:
        self._elapsed_time = 0
        self.state = State()
        self.state.party = Party()
        self.state.world_map = WorldMap()
        self.state.map = self.state.world_map
        self.state.console = Console(16,12)
        self.handlers = [WorldEventHandler(self.state)]
        self.background = gfx_load_rle_image("START")
        self.state.console.print("   Welcome to\n   Ultima IV\nPython port by\n   Blackfich\n")
        self.state.console.prompt()
        self.current_command = None
        load_avatar_exe()


    def handle_event(self, event):
        handler: EventHandler = self.handlers[-1]
        new_handler = handler.handle_event(event)
        if not new_handler:
            # we're done with this handler, remove it
            self.handlers.pop()
        elif new_handler != handler:
            self.handlers.append(new_handler)

        return self if self.handlers else None

    def update(self, elapsed_time):
        self._elapsed_time += elapsed_time
        while self._elapsed_time >= 250:
            self.state.console.animate()
            self._animate_mobiles()
            self._elapsed_time -= 250


    def _animate_mobiles(self):
        state = self.state

        if state.map is None or state.map.mobiles is None:
            return
        for mobile in self.state.map.mobiles:
            if mobile is None or mobile.tile < 0:
                continue
            if TILE_MAGE_1 <= mobile.tile <= TILE_SHEPHERD_2 \
                or TILE_GUARD_1 <= mobile.tile <= TILE_LCB_2 \
                or TILE_NIXIE_1 <= mobile.tile <= TILE_STORM_2:
                mobile.tile = mobile.tile - mobile.tile % 2 + rnd(2)
            elif TILE_RAT_1 <= mobile.tile:
                mobile.tile = mobile.tile - mobile.tile % 4 + rnd(4)

    def render(self, surface: Surface):
        surface.blit(self.background, (0,0))

        self._render_view(surface, 8, 8)

        self.state.console.render(surface, 192, 96)

    def _render_view(self, surface: Surface, x: int, y: int):
        x_range = range(self.state.party.x-5, self.state.party.x+6)
        y_range = range(self.state.party.y-5, self.state.party.y+6)

        for vy, my in enumerate(y_range):
            for vx, mx in enumerate(x_range):
                tile = self.state.map[(mx, my, self.state.party.z)]
                surface.blit(graphics.shapes[tile], (x + vx * graphics.shapes.tile_width, y + vy * graphics.shapes.tile_height))

        for mobile in self.state.map.mobiles:
            if mobile.x in x_range and mobile.y in y_range:
                vx = mobile.x - x_range.start
                vy = mobile.y - y_range.start
                surface.blit(graphics.shapes[mobile.tile], (x + vx * graphics.shapes.tile_width, y + vy * graphics.shapes.tile_height))

        if isinstance(self.state.map, (WorldMap, TownMap)):
            surface.blit(graphics.shapes[self.state.party.transportation],(x + 5 * graphics.shapes.tile_width, y + 5 * graphics.shapes.tile_height))


    def handle_command_event(self, event: Event) -> EventHandler:
        if self.current_command is None and isinstance(event, CommandEvent):
            print(event)
            self.current_command == event.command
            if isinstance(self.current_command, ImmediateCommand):
                print("Immediate command")
                self.current_command.execute(self.state)
                return self.end_turn()
            elif isinstance(self.current_command, InteractiveCommand):
                print("Interactive command")
                return self.current_command.init(self.state)
        elif self.current_command is not None:
            if not self.current_command.handle_event(event, self.state):
                return self.end_turn()
            else:
                return self

    def end_turn(self):
        self.state.idle_count = 0

        # self.handle_mobiles()

        self.current_command = None

        self.console.prompt()

        return self


    def do_enter(self):
        self.console.print("Enter ")
        p = -1
        if self.party.location == 0:
            for n in range(32):
                if binaries.avatar_exe.locations_x[n] == self.party.x and binaries.avatar_exe.locations_y[n] == self.party.y:
                    p = n
                    break
        if p >= 16:
            p = -1

        if p == -1:
            return self.do_what()

            self.console.print(binaries.avatar_exe.location_type[0])
        if p <= LOC_SERPENTS_HOLD:
            self.console.print(binaries.avatar_exe.location_types[2])
        elif p <= LOC_SKARA_BRAE:
            self.console.print(binaries.avatar_exe.location_types[3])
        elif p <= LOC_MAGINCIA:
            self.console.print(binaries.avatar_exe.location_types[4])
        elif p <= LOC_COVE:
            self.console.print(binaries.avatar_exe.location_types[1])
        elif p <= LOC_ABBYSS:
            self.console.print(binaries.avatar_exe.location_types[0])
        else:
            self.console.print(binaries.avatar_exe.location_types[5])

        self.console.print(binaries.avatar_exe.location_names[p]).newline().newline()

        self.map = TownMap(binaries.avatar_exe.ult_filenames[p])
        self.party.location = p
        if self.party.location < 4:
            self.party.x = 15
            self.party.y = 31
        else:
            self.party.x = 0
            self.party.y = 15
        return self.end_turn()


