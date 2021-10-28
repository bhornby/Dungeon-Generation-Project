from bsp_alg import DungeonGenerator

dungeon = DungeonGenerator(70,50,5,5)
dungeon.generate_map()
dungeon.print_map()