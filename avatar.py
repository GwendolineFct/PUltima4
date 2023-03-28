import random
import pygame
from constants import *
import globals
from globals import load_avatar_exe
from file_io import DosFile
import graphics
from pygame import Surface
from event import Event, KeyEvent
from graphics import gfx_load_rle_image
from map import Map, TownMap, WorldMap
from party import Party
from ui import Console
from util import rnd, sign

class Avatar:
    _elapsed_time: int
    background: Surface
    console: Console
    party: Party
    map: Map
    world_map: WorldMap

    def __init__(self) -> None:
        self._elapsed_time = 0
        self.party = Party()
        self.world_map = WorldMap()
        self.map = self.world_map
        self.console = Console(16,12)
        self.background = gfx_load_rle_image("START")
        self.console.print("   Welcome to\n   Ultima IV\nPython port by\n   Blackfich\n")
        self.console.prompt()
        load_avatar_exe()

    def update(self, elapsed_time):
        self._elapsed_time += elapsed_time
        while self._elapsed_time >= 250:
            self.console.animate()
            self._animate_mobiles()
            self._elapsed_time -= 250


    def _animate_mobiles(self):
        if self.map is None or self.map.mobiles is None:
            return
        for mobile in self.map.mobiles:
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

        self.console.render(surface, 192, 96)

    def _render_view(self, surface: Surface, x: int, y: int):
        x_range = range(self.party.x-5,self.party.x+6)
        y_range = range(self.party.y-5,self.party.y+6)

        for vy, my in enumerate(y_range):
            for vx, mx in enumerate(x_range):
                tile = self.map[(mx, my, self.party.z)]
                surface.blit(graphics.shapes[tile], (x + vx * graphics.shapes.tile_width, y + vy * graphics.shapes.tile_height))

        for mobile in self.map.mobiles:
            if mobile.x in x_range and mobile.y in y_range:
                vx = mobile.x - x_range.start
                vy = mobile.y - y_range.start
                surface.blit(graphics.shapes[mobile.tile], (x + vx * graphics.shapes.tile_width, y + vy * graphics.shapes.tile_height))

        if isinstance(self.map, (WorldMap, TownMap)):
            surface.blit(graphics.shapes[self.party.transportation],(x + 5 * graphics.shapes.tile_width, y + 5 * graphics.shapes.tile_height))


    def handle_event(self, event: Event):

        if isinstance(event, KeyEvent):
            if event.key == pygame.K_q:
                if (event.modifiers & (pygame.K_LALT | pygame.K_RALT)) != 0:
                    return None
                return self.do_pass()
            elif event.key == pygame.K_SPACE:
                return self.do_pass()
            elif event.key == pygame.K_UP:
                return self.do_north()
            elif event.key == pygame.K_DOWN:
                return self.do_south()
            elif event.key == pygame.K_RIGHT:
                return self.do_east()
            elif event.key == pygame.K_LEFT:
                return self.do_west()
            elif event.key == pygame.K_e:
                return self.do_enter()
            else:
                return self.do_what()

    def end_turn(self):
        self.idle_count = 0

        self.handle_mobiles()

        self.console.prompt()
        return self

    def do_what(self):
        self.console.print("What ?\n")
        return self.end_turn()

    def do_pass(self):
        self.console.print("Pass\n")
        return self.end_turn()

    def do_move(self, dx: int, dy: int, dir: str):
        self.console.print(dir).newline()
        dir = DIR_WEST if dx == -1 else DIR_NORTH if dy == -1 else DIR_SOUTH if dy == 1 else DIR_EAST
        current = self.map[(self.party.x, self.party.y, self.party.z)]
        dest = self.map[(self.party.x + dx, self.party.y + dy, self.party.z)]

        if self.party.transportation == TILE_BALLOON:
            self.console.print("Drift only!").newline()
        elif TILE_SHIP_WEST <= self.party.transportation <= TILE_SHIP_SOUTH and \
            self.party.transportation - TILE_SHIP_WEST != dir:
            # ship must turn before moving
            self.party.transportation = self.party.transportation - TILE_SHIP_WEST + dir
        elif not self.can_move(dx, dy):
            self.console.print("Blocked").newline()
        elif self.move_slowed():
            self.console.print("Slow progress!").newline()
        else:
            self.party.x += dx
            self.party.y += dy
            if self.map.wraps:
                self.party.x %= self.map.width
                self.party.y %= self.map.height
            elif (self.party.x, self.party.y) not in self.map:
                self.console.print("Leaving").newline()
                self.map = self.world_map
                self.party.x = globals.avatar_exe.locations_x[self.party.location]
                self.party.y = globals.avatar_exe.locations_y[self.party.location]

        return self.end_turn()

    def move_slowed(self) -> bool:
        current_tile = self.map[(self.party.x, self.party.y, self.party.z)]

        if self.party.transportation == TILE_AVATAR:
            if current_tile == TILE_SWAMPS:
                return rnd(8) == 0
            elif current_tile == TILE_BRUSH:
                return rnd(4) == 0
            elif current_tile == TILE_HILLS or current_tile == TILE_FIRE_FIELD:
                return rnd(2) == 0
        elif TILE_SHIP_WEST <= self.party.transportation <= TILE_SHIP_SOUTH:
            ship_dir = self.party.transportation - TILE_SHIP_WEST
            if ship_dir == self.wind_dir:
                return rnd(4) == 0
            elif ship_dir == self.wind_dir ^ 0b10:
                return rnd(4) != 0
        return False

    def can_move(self, dx: int, dy: int) -> bool:
        current_tile = self.map[(self.party.x, self.party.y, self.party.z)]
        dest_tile = self.map[(self.party.x + dx, self.party.y + dy, self.party.z)]
        if self.party.transportation == TILE_AVATAR or self.party.transportation == TILE_HORSE_EAST or self.party.transportation == TILE_HORSE_WEST:
            if dest_tile == TILE_LCB_ENTRANCE:
                return dy == -1
            if current_tile == TILE_LCB_ENTRANCE:
                return dy == 1
            if dest_tile in globals.avatar_exe.walkable_tiles:
                return True
            return False
        elif self.party.transportation == TILE_BALLOON:
            return dest_tile != TILE_MOUNTAINS
        elif TILE_SHIP_WEST <= self.party.transportation <= TILE_SHIP_SOUTH:
            return dest_tile in (TILE_DEEP_WATER, TILE_MEDIUM_WATER, TILE_WHIRLPOOL_1, TILE_WHIRLPOOL_2)
        return False

    def do_north(self):
        return self.do_move(0, -1, "North")

    def do_south(self):
        return self.do_move(0, 1, "South")

    def do_east(self):
        return self.do_move(1, 0, "East")

    def do_west(self):
        return self.do_move(-1, 0, "West")

    def do_enter(self):
        self.console.print("Enter").newline()
        p = -1
        if self.party.location == 0:
            for n in range(32):
                if globals.avatar_exe.locations_x[n] == self.party.x and globals.avatar_exe.locations_y[n] == self.party.y:
                    p = n
                    break
        if p >= 16:
            p = -1

        if p == -1:
            return self.cant()

        self.console.print(f" {globals.avatar_exe.location_names[p]}").newline()
        self.map = TownMap(globals.avatar_exe.ult_filenames[p])
        self.party.location = p
        if self.party.location < 4:
            self.party.x = 15
            self.party.y = 31
        else:
            self.party.x = 0
            self.party.y = 15
        return self.end_turn()

    def handle_mobiles(self):
        party_pos = [(self.party.x, self.party.y, self.party.z)]
        for mobile in self.map.mobiles:
            if mobile.behaviour == 0:
                continue
            elif mobile.behaviour == 1:
                if rnd(100) < 50:
                    continue
                dirs = [(0,1),(0,-1),(1,0),(-1,0)]
                random.shuffle(dirs)
                for dir in dirs:
                    if mobile.can_move(dir[0], dir[1], self.map, party_pos):
                        mobile.x += dir[0]
                        mobile.y += dir[1]
                        break
            elif mobile.behaviour == 80 or mobile.behaviour == 255:
                dx = self.party.x - mobile.x
                dy = self.party.y - mobile.y
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
