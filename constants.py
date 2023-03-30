from enum import Enum

AVATAR_EXE_SHA256 = "84ec144394cb561b047d6ef80b7bd8e8652f0159891ff273a3c051b3f9dfd368"

DIR_WEST = (-1, 0)
DIR_NORTH = (0, -1)
DIR_EAST = (1, 0)
DIR_SOUTH = (0, 1)
DIR_UP = DIR_NORTH
DIR_DOWN = DIR_SOUTH
DIR_LEFT = DIR_WEST
DIR_RIGHT = DIR_EAST

LOC_BRITANNIA = 0
LOC_LCB = 1
LOC_LYCAEUM = 2
LOC_EMPATH_ABBEY = 3
LOC_SERPENTS_HOLD = 4
LOC_MOONGLOW = 5
LOC_BRITAIN = 6
LOC_JHELOM = 7
LOC_YEM = 8
LOC_MINOC = 9
LOC_TRINSIC = 10
LOC_SKARA_BRAE = 11
LOC_MAGINCIA = 12
LOC_PAWS = 13
LOC_BUCCANEERS_DEN = 14
LOC_VESPER = 15
LOC_COVE = 16
LOC_DECEIT = 17
LOC_DESPISE = 18
LOC_DESTARD = 19
LOC_WRONG = 20
LOC_COVETOUS = 21
LOC_SHAME = 22
LOC_HYTHLOTH = 23
LOC_ABBYSS = 24
LOC_SHRINE_HONESTY = 25
LOC_SHRINE_COMPASSION = 26
LOC_SHRINE_VALOR = 27
LOC_SHRINE_JUSTICE = 28
LOC_SHRINE_SACRIFICE = 29
LOC_SHRINE_HONOR = 30
LOC_SHRINE_SPRIRITUALITY = 31
LOC_SHRINE_HUMILITY = 32


TILE_DEEP_WATER = 0
TILE_MEDIUM_WATER = 1
TILE_SHALLOW_WATER = 2
TILE_SWAMPS = 3
TILE_GRASSLANDS = 4
TILE_BRUSH = 5
TILE_FOREST = 6
TILE_HILLS = 7
TILE_MOUNTAINS = 8
TILE_DUNGEON_ENTRANCE = 9
TILE_TOWN = 10
TILE_CASTLE = 11
TILE_VILLAGE = 12
TILE_LCB_WEST = 13
TILE_LCB_ENTRANCE = 14
TILE_LCB_EAST = 15
TILE_SHIP_WEST = 16
TILE_SHIP_NORTH = 17
TILE_SHIP_EAST = 18
TILE_SHIP_SOUTH = 19
TILE_HORSE_WEST = 20
TILE_HORSE_EAST = 21
TILE_FLOOR = 22
TILE_BRIDGE = 23
TILE_BALLOON = 24
TILE_BRIDGE_NORTH = 25
TILE_BRIDGE_SOUTH = 26
TILE_LADDER_UP = 27
TILE_LADDER_DOWN = 28
TILE_RUINS = 29
TILE_SHRINE = 30
TILE_AVATAR = 31
TILE_MAGE_1 = 32
TILE_MAGE_2 = 33
TILE_BARD_1 = 34
TILE_BARD_2 = 35
TILE_FIGHTER_1 = 36
TILE_FIGHTER_2 = 37
TILE_DRUID_1 = 38
TILE_DRUID_2 = 39
TILE_TINKER_1 = 40
TILE_TINKER_2 = 41
TILE_PALADIN_1 = 42
TILE_PALADIN_2 = 43
TILE_RANGER_1 = 44
TILE_RANGER_2 = 45
TILE_SHEPHERD_1 = 46
TILE_SHEPHERD_2 = 47
TILE_COLUMN = 48
TILE_WHITE_SW = 49
TILE_WHITE_SE = 50
TILE_WHITE_NW = 51
TILE_WHITE_NE = 52
TILE_SHIP_MAST = 53
TILE_SHIP_WHEEL = 54
TILE_ROCKS = 55
TILE_CORPSE = 56
TILE_STONE_WALL = 57
TILE_LOCKED_DOOR = 58
TILE_DOOR = 59
TILE_CHEST = 60
TILE_ANKH = 61
TILE_BRICK_FLOOR = 62
TILE_WOODEN_PLANKS = 63
TILE_MOONGATE_1 = 64
TILE_MOONGATE_2 = 65
TILE_MOONGATE_3 = 66
TILE_MOONGATE_4 = 67
TILE_POISON_FIELD = 68
TILE_ENERGY_FIELD = 69
TILE_FIRE_FIELD = 80
TILE_SLEEP_FIELD = 71
TILE_SOLID_BARRIER = 72
TILE_HIDDEN_PASSAGE = 73
TILE_ALTAR = 74
TILE_BBQ = 75
TILE_LAVA = 76
TILE_MISSILE = 77
TILE_MAGIC_SPHERE = 78
TILE_ATTACK_FLASH = 79
TILE_GUARD_1 = 80
TILE_GUARD_2 = 81
TILE_CITIZEN_1 = 82
TILE_CITIZEN_2 = 83
TILE_SINGING_BARD_1 = 84
TILE_SINGING_BARD_2 = 85
TILE_JESTER_1 = 86
TILE_JESTER_2 = 87
TILE_BEGGAR_1 = 88
TILE_BEGGAR_2 = 89
TILE_CHILD_1 = 90
TILE_CHILD_2 = 91
TILE_BULL_1 = 92
TILE_BULL_2 = 93
TILE_LCB_1 = 94
TILE_LCB_2 = 95
TILE_A = 96
TILE_Z = 121
TILE_SPACE = 122
TILE_RIGHT = 123
TILE_LEFT = 124
TILE_WINDOW = 125
TILE_BLANK = 126
TILE_BRICK_WALL = 127
TILE_PIRATE_SHIP_WEST = 128
TILE_PIRATE_SHIP_NORTH = 129
TILE_PIRATE_SHIP_EAST = 130
TILE_PIRATE_SHIP_SOUTH = 131
TILE_NIXIE_1 = 132
TILE_NIXIE_2 = 133
TILE_SQUID_1 = 134
TILE_SQUID_2 = 135
TILE_SEASERPENT_1 = 136
TILE_SEASERPENT_2 = 137
TILE_SEAHORSE_1 = 138
TILE_SEAHORSE_2 = 139
TILE_WHIRLPOOL_1 = 140
TILE_WHIRLPOOL_2 = 141
TILE_STORM_1 = 142
TILE_STORM_2 = 143
TILE_RAT_1 = 144
TILE_RAT_2 = 145
TILE_RAT_3 = 146
TILE_RAT_4 = 147
TILE_BAT_1 = 148
TILE_BAT_2 = 149
TILE_BAT_3 = 150
TILE_BAT_4 = 151
TILE_GIANT_SPIDER_1 = 152
TILE_GIANT_SPIDER_2 = 153
TILE_GIANT_SPIDER_3 = 154
TILE_GIANT_SPIDER_4 = 155
TILE_GHOST_1 = 156
TILE_GHOST_2 = 157
TILE_GHOST_3 = 158
TILE_GHOST_4 = 159
TILE_SLIME_1 = 160
TILE_SLIME_2 = 161
TILE_SLIME_3 = 162
TILE_SLIME_4 = 163
TILE_TROLL_1 = 164
TILE_TROLL_2 = 165
TILE_TROLL_3 = 166
TILE_TROLL_4 = 167
TILE_GREMLIN_1 = 168
TILE_GREMLIN_2 = 169
TILE_GREMLIN_3 = 170
TILE_GREMLIN_4 = 171
TILE_MIMIC_1 = 172
TILE_MIMIC_2 = 173
TILE_MIMIC_3 = 174
TILE_MIMIC_4 = 175
TILE_REAPER_1 = 176
TILE_REAPER_2 = 177
TILE_REAPER_3 = 178
TILE_REAPER_4 = 179
TILE_INSECT_SWARM_1 = 180
TILE_INSECT_SWARM_2 = 181
TILE_INSECT_SWARM_3 = 182
TILE_INSECT_SWARM_4 = 183
TILE_GAZER_1 = 184
TILE_GAZER_2 = 185
TILE_GAZER_3 = 186
TILE_GAZER_4 = 187
TILE_PHANTOM_1 = 188
TILE_PHANTOM_2 = 189
TILE_PHANTOM_3 = 190
TILE_PHANTOM_4 = 191
TILE_ORC_1 = 192
TILE_ORC_2 = 193
TILE_ORC_3 = 194
TILE_ORC_4 = 195
TILE_SKELETON_1 = 196
TILE_SKELETON_2 = 197
TILE_SKELETON_3 = 198
TILE_SKELETON_4 = 199
TILE_ROGUE_1 = 200
TILE_ROGUE_2 = 201
TILE_ROGUE_3 = 202
TILE_ROGUE_4 = 203
TILE_PYTHON_1 = 204
TILE_PYTHON_2 = 205
TILE_PYTHON_3 = 206
TILE_PYTHON_4 = 207
TILE_ETTIN_1 = 208
TILE_ETTIN_2 = 209
TILE_ETTIN_3 = 210
TILE_ETTIN_4 = 211
TILE_HEADLESS_1 = 212
TILE_HEADLESS_2 = 213
TILE_HEADLESS_3 = 214
TILE_HEADLESS_4 = 215
TILE_CYCLOPS_1 = 216
TILE_CYCLOPS_2 = 217
TILE_CYCLOPS_3 = 218
TILE_CYCLOPS_4 = 219
TILE_WISP_1 = 220
TILE_WISP_2 = 221
TILE_WISP_3 = 222
TILE_WISP_4 = 223
TILE_EVIL_MAGE_1 = 224
TILE_EVIL_MAGE_2 = 225
TILE_EVIL_MAGE_3 = 226
TILE_EVIL_MAGE_4 = 227
TILE_LICH_1 = 228
TILE_LICH_2 = 229
TILE_LICH_3 = 230
TILE_LICH_4 = 231
TILE_LAVA_LIZARD_1 = 232
TILE_LAVA_LIZARD_2 = 233
TILE_LAVA_LIZARD_3 = 234
TILE_LAVA_LIZARD_4 = 235
TILE_ZORN_1 = 236
TILE_ZORN_2 = 237
TILE_ZORN_3 = 238
TILE_ZORN_4 = 239
TILE_DAEMON_1 = 240
TILE_DAEMON_2 = 241
TILE_DAEMON_3 = 242
TILE_DAEMON_4 = 243
TILE_HYDRA_1 = 244
TILE_HYDRA_2 = 245
TILE_HYDRA_3 = 246
TILE_HYDRA_4 = 247
TILE_DRAGON_1 = 248
TILE_DRAGON_2 = 249
TILE_DRAGON_3 = 250
TILE_DRAGON_4 = 251
TILE_BALRON_1 = 252
TILE_BALRON_2 = 253
TILE_BALRON_3 = 254
TILE_BALRON_4 = 255

