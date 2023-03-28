from constants import *


class CreatureFlags():
    WALKS = 0b0000_0001
    SWIMS = 0b0000_0010
    SAILS = 0b0000_0100
    FLIES = 0b0000_1000
    GHOST = 0b0001_0000
    HOSTILE = 0b0010_0000
    RANGED = 0b0100_0000

class PartyMember:
    hp: int
    max_hp: int
    xp: int
    strength: int
    dexterity: int
    intelligence: int
    mp: int
    weapon: int
    armor: int
    name: str
    sex: int
    klass: int
    status: int

class Party:
    counter: int
    moves: int
    members: list[PartyMember]
    food: int
    gold: int
    karma: list[int]
    torches: int
    gems: int
    keys: int
    sextants: int
    armors: list[int]
    weapons: list[int]
    reagents: list[int]
    items: int
    x: int
    y: int
    stones: int
    runes: int
    number_of_members: int
    transportation: int
    balloon_status: int
    left_moon_phase: int
    right_moon_phase: int
    hull_integrity: int
    introduced_to_lb: int
    last_camp_time: int
    last_herb_time: int
    last_meditation_time: int
    last_virtue_conversation_time: int
    last_dungeon_location: int
    facing: int
    location: int
    z: int

    def __init__(self) -> None:
        self.counter = 0
        self.moves = 0
        self.members = [PartyMember() for _ in range(8)]
        self.food = 10000
        self.gold = 0
        self.karma = [50, 50, 50, 50, 50, 50, 50, 50]
        self.torches = 3
        self.gems = 0
        self.keys = 0
        self.sextants = 0
        self.armors = [0] * 8
        self.weapons = [0] * 16
        self.reagents = [0] * 8
        self.items = 0
        self.x = 86
        self.y = 108
        self.stones = 0
        self.runes = 0
        self.number_of_members = 0
        self.transportation = TILE_AVATAR
        self.balloon_status = 0
        self.left_moon_phase = 0
        self.right_moon_phase = 0
        self.hull_integrity = 0
        self.introduced_to_lb = 0
        self.last_camp_time = 0
        self.last_herb_time = 0
        self.last_meditation_time = 0
        self.last_virtue_conversation_time = 0
        self.last_dungeon_location = 0
        self.facing = 0
        self.location = 0
        self.z = 0