import pygame
# Import the code from the other files
from sprites import *
from config import *

# Create Room
def createRoom(self, tileMap, biome):
    # i == row of the tilemap, row == the str content of that row
    for i, row in enumerate(tileMap):
        # each index for the contents in each row
        for j, column in enumerate(row):
            if column == "A": # A = PATH 9-Tile UpperLeft
                DecoTile(self, j, i, PATH_9T_UL[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_4T_UL[biome], GROUND_LAYER2)
            if column == "B": # B = PATH 9-Tile Upper
                DecoTile(self, j, i, PATH_9T_U[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_B[biome], GROUND_LAYER2)
            if column == "C": # C = PATH 9-Tile UpperRight
                DecoTile(self, j, i, PATH_9T_UR[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_4T_UR[biome], GROUND_LAYER2)
            if column == "D": # D = PATH 9-Tile Left
                DecoTile(self, j, i, PATH_9T_L[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_R[biome], GROUND_LAYER2)
            if column == "E": # E = PATH 9-Tile Center
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER3)
            if column == "F": # F = PATH 9-Tile Right
                DecoTile(self, j, i, PATH_9T_R[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_L[biome], GROUND_LAYER2)
            if column == "G": # G = PATH 9-Tile BottomLeft
                DecoTile(self, j, i, PATH_9T_BL[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_4T_BL[biome], GROUND_LAYER2)
            if column == "H": # H = PATH 9-Tile Bottom
                DecoTile(self, j, i, PATH_9T_B[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_U[biome], GROUND_LAYER2)
            if column == "I": # I = PATH 9-Tile BottomRight
                DecoTile(self, j, i, PATH_9T_BR[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_4T_BR[biome], GROUND_LAYER2)
            if column == "J": # J = PATH 4-Tile UpperLeft
                DecoTile(self, j, i, PATH_4T_UL[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_UL[biome], GROUND_LAYER2)
            if column == "K": # K = PATH 4-Tile UpperRight
                DecoTile(self, j, i, PATH_4T_UR[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_UR[biome], GROUND_LAYER2)
            if column == "L": # L = PATH 4-Tile BottomLeft
                DecoTile(self, j, i, PATH_4T_BL[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_BL[biome], GROUND_LAYER2)
            if column == "M": # M = PATH 4-Tile BottomRight
                DecoTile(self, j, i, PATH_4T_BR[biome], GROUND_LAYER3)
                DecoTile(self, j, i, DETAIL_9T_BR[biome], GROUND_LAYER2)
            if column == "N": # N = PATH Excess Tile 1
                PathTile(self, j, i, PATH_ET_1[biome], GROUND_LAYER3)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER2)
            if column == "O": # O = PATH Excess Tile 2
                PathTile(self, j, i, PATH_ET_2[biome], GROUND_LAYER3)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER2)
            if column == "P": # P = PATH Excess Tile 3
                PathTile(self, j, i, PATH_ET_3[biome], GROUND_LAYER3)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER2)
            if column == "Q": # Q = PATH Excess Deco 1
                PathTile(self, j, i, PATH_ED_1[biome], GROUND_LAYER3)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER2)
            if column == "R": # R = PATH Excess Deco 2
                PathTile(self, j, i, PATH_ED_2[biome], GROUND_LAYER3)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER2)

            if column == "S": # A = DETAIL 9-Tile UpperLeft
                DecoTile(self, j, i, DETAIL_9T_UL[biome], GROUND_LAYER2)
            if column == "T": # B = DETAIL 9-Tile Upper
                DecoTile(self, j, i, DETAIL_9T_U[biome], GROUND_LAYER2)
            if column == "U": # C = DETAIL 9-Tile UpperRight
                DecoTile(self, j, i, DETAIL_9T_UR[biome], GROUND_LAYER2)
            if column == "V": # D = DETAIL 9-Tile Left
                DecoTile(self, j, i, DETAIL_9T_L[biome], GROUND_LAYER2)
            if column == ".": # E = DETAIL 9-Tile Center
                DecoTile(self, j, i, DETAIL_9T_C[biome], GROUND_LAYER2)
            if column == "X": # F = DETAIL 9-Tile Right
                DecoTile(self, j, i, DETAIL_9T_R[biome], GROUND_LAYER2)
            if column == "Y": # G = DETAIL 9-Tile BottomLeft
                DecoTile(self, j, i, DETAIL_9T_BL[biome], GROUND_LAYER2)
            if column == "Z": # H = DETAIL 9-Tile Bottom
                DecoTile(self, j, i, DETAIL_9T_B[biome], GROUND_LAYER2)
            if column == "0": # I = DETAIL 9-Tile BottomRight
                DecoTile(self, j, i, DETAIL_9T_BR[biome], GROUND_LAYER2)
            if column == "1": # J = DETAIL 4-Tile UpperLeft
                DecoTile(self, j, i, DETAIL_4T_UL[biome], GROUND_LAYER2)
            if column == "2": # K = DETAIL 4-Tile UpperRight
                DecoTile(self, j, i, DETAIL_4T_UR[biome], GROUND_LAYER2)
            if column == "3": # L = DETAIL 4-Tile BottomLeft
                DecoTile(self, j, i, DETAIL_4T_BL[biome], GROUND_LAYER2)
            if column == "4": # M = DETAIL 4-Tile BottomRight
                DecoTile(self, j, i, DETAIL_4T_BR[biome], GROUND_LAYER2)
            if column == "5": # N = DETAIL Excess Tile 1
                DecoTile(self, j, i, DETAIL_ET_1[biome], GROUND_LAYER2)
                DecoTile(self, j, i, DETAIL_9T_C[biome], GROUND_LAYER1)
            if column == "6": # O = DETAIL Excess Tile 2
                DecoTile(self, j, i, DETAIL_ET_2[biome], GROUND_LAYER2)
                DecoTile(self, j, i, DETAIL_9T_C[biome], GROUND_LAYER1)
            if column == "7": # P = DETAIL Excess Tile 3
                DecoTile(self, j, i, DETAIL_ET_3[biome], GROUND_LAYER2)
                DecoTile(self, j, i, DETAIL_9T_C[biome], GROUND_LAYER1)
            if column == "8": # Q = DETAIL Excess Deco 1
                DecoTile(self, j, i, DETAIL_ED_1[biome], GROUND_LAYER2)
                DecoTile(self, j, i, DETAIL_9T_C[biome], GROUND_LAYER1)
            if column == "9": # R = DETAIL Excess Deco 2
                DecoTile(self, j, i, DETAIL_ED_2[biome], GROUND_LAYER2)
                DecoTile(self, j, i, DETAIL_9T_C[biome], GROUND_LAYER1)

            if column == "$": # Loot Chest
                InteractableTile(self, j, i, CHEST, GROUND_LAYER4)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER3)
            if column == "!": # Enemy
                Enemy(self, j, i, GROUND_LAYER4)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER3)
            if column == "@": # Door
                InteractableTile(self, j, i, DOOR, GROUND_LAYER4)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER3)
            if column == "*": # Material Node
                InteractableTile(self, j, i, OUTCROP, GROUND_LAYER4)
                PathTile(self, j, i, PATH_9T_C[biome], GROUND_LAYER3)