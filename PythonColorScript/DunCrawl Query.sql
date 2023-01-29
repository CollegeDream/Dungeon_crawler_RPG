use bbb61uemtrivmf5uyaub;

CREATE TABLE `Player` (
  `PlayerInventoryID` int,
  `Health` int,
  `Food` int,
  `Experience` int,
  `PlayerPosRoom` int,
  `PlayerPosX` int,
  `PlayerPosY` int,
  PRIMARY KEY (`PlayerInventoryID`),
  UNIQUE KEY `PlayerInventoryID_UNIQUE` (`PlayerInventoryID`)
  );
INSERT INTO `Player` VALUES (1,100,10,0,0,16,14);

CREATE TABLE `Inventory` (
	`InventorySlot` int,
	`InventoryItem` int,
	PRIMARY KEY (`InventorySlot`), UNIQUE KEY `InventorySlot_UNIQUE` (`InventorySlot`)
);
INSERT INTO `Inventory` VALUES (0,20);

CREATE TABLE `Item` (
	`ItemID` int,
	`ItemName` varchar(255),
	`ItemUses` int,
	`ItemType` varchar(255),
	`ItemValue` int,
	PRIMARY KEY (`ItemID`),	UNIQUE KEY `ItemID_UNIQUE` (`ItemID`)
);
INSERT INTO `Item` VALUES
(0, 'Leaves', 1, 'Material', 0),
(1, 'Blueberries', 1, 'Food', 3),
(2, 'Mushroom', 1, 'Food', 2),
(3, 'Gunpowder', 1, 'Material', 0),
(4, 'Iron chunk', 1, 'Material', 0),
(5, 'Coal chunk', 1, 'Material', 0),
(6, 'Titanium chunk', 1, 'Material', 0),
(7, 'Datte Fruit', 1, 'Food', 3),
(8, 'Apples', 1, 'Health', 15),
(9, 'Obsidian', 1, 'Material', 0),
(10, 'WoodenRapier', 20, 'Damage', 13),
(11, 'WoodenBroadsword', 40, 'Damage', 9),
(12, 'IronRapier', 35, 'Damage', 19),
(13, 'IronBroadsword', 55, 'Damage', 15),
(14, 'Pistol', 10, 'Damage', 25),
(15, 'Titanium Grade Cutlass', 50, 'Damage', 40),
(16, 'CloseRangedShotgun', 7, 'Damage', 50),
(17, 'Health Kit', 3, 'Health', 35),
(18, 'Enhanced Health Kit', 5, 'Health', 55),
(19, 'Wool', 2, 'Material', 0),
(20, 'fists', -1, 'Damage', 2) # -1==infinite uses?
;

CREATE TABLE `MaterialNode` (
	`MaterialNodeID` int,
	`MaterialName` varchar(255),
	`MaterialDrop` int,
	`ExpDrop` int,
	PRIMARY KEY (`MaterialNodeID`),	UNIQUE KEY `MaterialNodeID_UNIQUE` (`MaterialNodeID`)
);
INSERT INTO `MaterialNode` VALUES
(0,'Bush', 0, 10),
(1,'Fruit Plant', 1, 15),
(2,'Mushrooms', 2, 20),
(3,'Sulfer Deposit', 3, 20),
(4,'Iron Deposit', 4, 30),
(5,'Titanium Deposit', 5, 50),
(6,'Oasis Tree', 6, 25),
(7,'Molten Rock', 7, 50)
;

CREATE TABLE `Chest` (
	`ChestRarityID` int,
	`ChestCommonItems` int,
	`ChestUncommonItems` int,
	`ChestRareItems` int,
	`ChestEpicItems` int,
	PRIMARY KEY (`ChestRarityID`), UNIQUE KEY `ChestRarityID_UNIQUE` (`ChestRarityID`)
);
INSERT INTO `Chest` VALUES
(0, 1, 0, 0, 0),
(1, 2, 0, 0, 0),
(2, 0, 1, 0, 0),
(3, 0, 2, 0, 0),
(4, 1, 0, 1, 0),
(5, 0, 2, 1, 0),
(6, 0, 1, 2, 0),
(7, 0, 1, 1, 1)
;

CREATE TABLE `Creature` (
	`CreatureType` int, 
	`CreatureName` varchar(255),
	`CreatureHealth` int,
	`CreatureDamage` int,
	PRIMARY KEY (`CreatureType`), UNIQUE KEY `CreatureType_UNIQUE` (`CreatureType`)
);
INSERT INTO `Creature` VALUES
(0, "Sheep", 5, 1),
(1, "Boar", 25, 10),
(2, "Bear", 40, 15),
(3, "Bandit", 50, 25),
(4, "Crocodile", 65, 20),
(5, "Undead Miner", 85, 30),
(6, "Pirate", 120, 45),
(7, "Dragon", 200, 50),
(8, "Nobel Knight", 180, 75)
;

CREATE TABLE `Biome` (
	`BiomeID` int,
	`EnviormentName` VARCHAR(255),
	`MaterialDepositType` int,
	`LootRarity` int,
	`DifficultyScale` int,
	PRIMARY KEY (`BiomeID`), UNIQUE KEY `BiomeID_UNIQUE` (`BiomeID`)
);
INSERT INTO `Biome` VALUES
(0, "Spawn", 0, 2, 0),
(1, "Meadows", 0, 0, 1),
(2, "Plains", 1, 3, 2),
(3, "Desert", 6, 4, 3),
(4, "Swamp", 2, 3, 2),
(5, "Mountains", 4, 5, 3),
(6, "Beach", 3, 4, 1),
(7, "Volcanic Edge", 7, 7, 5),
(8, "Castle", 5, 6, 4)
;

CREATE TABLE `Room` (
	`RoomID` int,
	`RoomTileLenX` int,
	`RoomTileLenY` int,
	`RoomsBiomeID` int,
	PRIMARY KEY (`RoomID`),	UNIQUE KEY `RoomID_UNIQUE` (`RoomID`)
);
INSERT INTO `Room` VALUES
(0, 40, 30, 0),
(1, 51, 31, -1),
(2, 70, 40, -1),
(3, 24, 60, -1),
(4, 51, 31, -1),
(5, 70, 38, -1),
(6, 40, 20, -1),
(7, 45, 30, -1),
(8, 50, 40, -1)
;

CREATE TABLE `MapTile` (
	TileRoomID int,
	TileX int,
	TileY int,
	TileContents int,
	TileInteracted bool
);
INSERT INTO `MapTile` VALUES
#room0 loot tiles
(0, 6, 3, 2, FALSE),
(0, 6, 18, 2, FALSE),
(0, 3, 25, 2, FALSE),
(0, 35, 25, 2, FALSE),
#room0 spawn space
(0, 16, 14, 0, FALSE),
#room0 doors
(0, 33, 0, 4, FALSE), #top
(0, 0, 5, 4, FALSE), #left
(0, 16, 29, 4, FALSE) #bottom
;

INSERT INTO `MapTile` VALUES
#room1 material nodes
(1, 42, 3, 1, FALSE),
(1, 3, 5, 1, FALSE),
(1, 30, 6, 1, FALSE),
(1, 17, 7, 1, FALSE),
(1, 20, 11, 1, FALSE),
(1, 22, 11, 1, FALSE),
(1, 19, 19, 1, FALSE),
(1, 3, 20, 1, FALSE),
(1, 48, 20, 1, FALSE),
(1, 43, 23, 1, FALSE),
#room1 loot tiles
(1, 6, 1, 2, FALSE),
(1, 27, 3, 2, FALSE),
(1, 29, 10, 2, FALSE),
(1, 29, 12, 2, FALSE),
(1, 13, 24, 2, FALSE),
#room1 enemies
(1, 31, 4, 3, FALSE),
(1, 43, 5, 3, FALSE),
(1, 11, 11, 3, FALSE),
(1, 6, 21, 3, FALSE),
(1, 33, 21, 3, FALSE),
(1, 46, 21, 3, FALSE),
#room1 doors
(1, 50, 5, 4, FALSE),
(1, 33, 30, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room2 material nodes
(2, 66, 2, 1, FALSE),
(2, 57, 4, 1, FALSE),
(2, 61, 13, 1, FALSE),
(2, 64, 14, 1, FALSE),
(2, 11, 16, 1, FALSE),
(2, 6, 23, 1, FALSE),
(2, 62, 24, 1, FALSE),
(2, 55, 26, 1, FALSE),
(2, 4, 27, 1, FALSE),
(2, 31, 33, 1, FALSE),
(2, 51, 33, 1, FALSE),
(2, 38, 34, 1, FALSE),
(2, 55, 34, 1, FALSE),
(2, 4, 37, 1, FALSE),
(2, 24, 37, 1, FALSE),
#room2 loot tiles
(2, 32, 1, 2, FALSE),
(2, 43, 5, 2, FALSE),
(2, 15, 8, 2, FALSE),
(2, 44, 12, 2, FALSE),
(2, 25, 15, 2, FALSE),
(2, 3, 17, 2, FALSE),
(2, 51, 22, 2, FALSE),
(2, 37, 24, 2, FALSE),
(2, 3, 34, 2, FALSE),
#room2 enemies
(2, 16, 2, 3, FALSE),
(2, 52, 7, 3, FALSE),
(2, 62, 7, 3, FALSE),
(2, 7, 9, 3, FALSE),
(2, 38, 10, 3, FALSE),
(2, 33, 14, 3, FALSE),
(2, 16, 17, 3, FALSE),
(2, 53, 22, 3, FALSE),
(2, 25, 26, 3, FALSE),
(2, 38, 29, 3, FALSE),
#room2 doors
(2, 0, 4, 4, FALSE),
(2, 69, 22, 4, FALSE),
(2, 15, 39, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room3 material nodes
(3, 4, 5, 1, FALSE),
(3, 19, 16, 1, FALSE),
(3, 7, 22, 1, FALSE),
(3, 19, 22, 1, FALSE),
(3, 22, 23, 1, FALSE),
(3, 6, 25, 1, FALSE),
(3, 22, 36, 1, FALSE),
(3, 19, 38, 1, FALSE),
(3, 15, 40, 1, FALSE),
(3, 1, 45, 1, FALSE),
(3, 14, 45, 1, FALSE),
(3, 15, 47, 1, FALSE),
(3, 12, 58, 1, FALSE),
(3, 22, 58, 1, FALSE),
#room3 loot tiles
(3, 22, 3, 2, FALSE),
(3, 22, 5, 2, FALSE),
(3, 4, 20, 2, FALSE),
(3, 21, 25, 2, FALSE),
(3, 3, 39, 2, FALSE),
(3, 17, 43, 2, FALSE),
(3, 17, 52, 2, FALSE),
(3, 5, 56, 2, FALSE),
#room3 enemies
(3, 9, 2, 3, FALSE),
(3, 19, 5, 3, FALSE),
(3, 6, 12, 3, FALSE),
(3, 15, 20, 3, FALSE),
(3, 4, 24, 3, FALSE),
(3, 20, 32, 3, FALSE),
(3, 17, 35, 3, FALSE),
(3, 5, 46, 3, FALSE),
#room3 doors
(3, 0, 4, 4, FALSE),
(3, 23, 53, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room4 material nodes
(4, 10, 2, 1, FALSE),
(4, 48, 5, 1, FALSE),
(4, 47, 10, 1, FALSE),
(4, 24, 11, 1, FALSE),
(4, 29, 14, 1, FALSE),
(4, 22, 15, 1, FALSE),
(4, 3, 16, 1, FALSE),
(4, 34, 16, 1, FALSE),
(4, 29, 26, 1, FALSE),
(4, 16, 27, 1, FALSE),
(4, 46, 28, 1, FALSE),
#room4 loot tiles
(4, 43, 2, 2, FALSE),
(4, 14, 3, 2, FALSE),
(4, 7, 11, 2, FALSE),
(4, 21, 11, 2, FALSE),
(4, 31, 12, 2, FALSE),
(4, 8, 23, 2, FALSE),
(4, 48, 23, 2, FALSE),
(4, 32, 27, 2, FALSE),
#room4 enemies
(4, 11, 5, 3, FALSE),
(4, 45, 5, 3, FALSE),
(4, 23, 8, 3, FALSE),
(4, 41, 9, 3, FALSE),
(4, 9, 15, 3, FALSE),
(4, 33, 19, 3, FALSE),
(4, 6, 20, 3, FALSE),
(4, 45, 23, 3, FALSE),
(4, 30, 24, 3, FALSE),
#room4 doors
(4, 0, 7, 4, FALSE),
(4, 17, 30, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room5 material nodes
(5, 65, 5, 1, FALSE),
(5, 33, 10, 1, FALSE),
(5, 34, 12, 1, FALSE),
(5, 32, 14, 1, FALSE),
(5, 3, 16, 1, FALSE),
(5, 53, 18, 1, FALSE),
(5, 26, 20, 1, FALSE),
(5, 48, 21, 1, FALSE),
(5, 26, 28, 1, FALSE),
(5, 53, 30, 1, FALSE),
(5, 7, 33, 1, FALSE),
#room5 loot tiles
(5, 38, 3, 2, FALSE),
(5, 46, 3, 2, FALSE),
(5, 38, 6, 2, FALSE),
(5, 38, 9, 2, FALSE),
(5, 46, 9, 2, FALSE),
(5, 14, 17, 2, FALSE),
(5, 17, 17, 2, FALSE),
(5, 61, 21, 2, FALSE),
(5, 33, 30, 2, FALSE),
(5, 48, 30, 2, FALSE),
(5, 14, 31, 2, FALSE),
(5, 17, 31, 2, FALSE),
#room5 enemies
(5, 43, 4, 3, FALSE),
(5, 41, 6, 3, FALSE),
(5, 43, 8, 3, FALSE),
(5, 13, 17, 3, FALSE),
(5, 26, 17, 3, FALSE),
(5, 45, 22, 3, FALSE),
(5, 62, 25, 3, FALSE),
(5, 45, 26, 3, FALSE),
(5, 4, 31, 3, FALSE),
(5, 19, 32, 3, FALSE),
#room5 doors
(5, 58, 0, 4, FALSE),
(5, 0, 24, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room6 material nodes
(6, 16, 5, 1, FALSE),
(6, 10, 8, 1, FALSE),
(6, 12, 10, 1, FALSE),
(6, 26, 11, 1, FALSE),
(6, 22, 17, 1, FALSE),
#room6 loot tiles
(6, 28, 6, 2, FALSE),
(6, 14, 8, 2, FALSE),
(6, 19, 9, 2, FALSE),
(6, 6, 12, 2, FALSE),
(6, 19, 17, 2, FALSE),
#room6 enemies
(6, 12, 6, 3, FALSE),
(6, 5, 7, 3, FALSE),
(6, 25, 13, 3, FALSE),
#room6 doors
(6, 15, 0, 4, FALSE),
(6, 39, 9, 4, FALSE),
(6, 0, 13, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room7 material nodes
(7, 12, 6, 1, FALSE),
(7, 34, 10, 1, FALSE),
(7, 22, 11, 1, FALSE),
(7, 1, 16, 1, FALSE),
(7, 3, 18, 1, FALSE),
(7, 14, 22, 1, FALSE),
(7, 39, 24, 1, FALSE),
#room7 loot tiles
(7, 14, 3, 2, FALSE),
(7, 35, 3, 2, FALSE),
(7, 5, 9, 2, FALSE),
(7, 2, 10, 2, FALSE),
(7, 9, 13, 2, FALSE),
(7, 42, 14, 2, FALSE),
(7, 24, 15, 2, FALSE),
(7, 33, 20, 2, FALSE),
(7, 3, 26, 2, FALSE),
(7, 14, 27, 2, FALSE),
#room7 enemies
(7, 18, 5, 3, FALSE),
(7, 7, 9, 3, FALSE),
(7, 38, 12, 3, FALSE),
(7, 20, 13, 3, FALSE),
(7, 7, 16, 3, FALSE),
(7, 17, 25, 3, FALSE),
#room7 doors
(7, 28, 0, 4, FALSE),
(7, 44, 21, 4, FALSE)
;

INSERT INTO `MapTile` VALUES
#room8 material nodes
(8, 22, 2, 1, FALSE),
(8, 20, 11, 1, FALSE),
(8, 28, 11, 1, FALSE),
(8, 22, 15, 1, FALSE),
(8, 13, 19, 1, FALSE),
(8, 11, 22, 1, FALSE),
(8, 27, 26, 1, FALSE),
(8, 11, 31, 1, FALSE),
#room8 loot tiles
(8, 25, 2, 2, FALSE),
(8, 43, 4, 2, FALSE),
(8, 5, 6, 2, FALSE),
(8, 24, 16, 2, FALSE),
(8, 15, 18, 2, FALSE),
(8, 20, 22, 2, FALSE),
(8, 12, 24, 2, FALSE),
(8, 24, 25, 2, FALSE),
(8, 41, 27, 2, FALSE),
(8, 5, 33, 2, FALSE),
#room8 enemies
(8, 38, 6, 3, FALSE),
(8, 24, 11, 3, FALSE),
(8, 5, 17, 3, FALSE),
(8, 31, 22, 3, FALSE),
(8, 15, 23, 3, FALSE),
(8, 31, 33, 3, FALSE),
#room8 doors
(8, 8, 0, 4, FALSE),
(8, 49, 25, 4, FALSE),
(8, 15, 39, 4, FALSE)
;

CREATE TABLE `Door` (
	`Room1` int,
	`Door1PosX` int,
	`Door1PosY` int,
	`Room2` int,
	`Door2DestPosX` int,
	`Door2DestPosY` int
);
INSERT INTO `Door` VALUES
(0,33,0, 2,15,39), #room0 top <-> room2 bottom 
(0,0,5, 8,49,25), #room0 left <-> room8 right
(0,16,29, 6,15,0), #room0 bottom <-> room6 top
(1,50,5, 2,0,4), #room1 right <-> room2 left
(1,33,30, 8,8,0), #room1 bottom <-> room8 top
(2,69,22, 3,0,4), #room2 right <-> room3 left
(3,23,53, 4,0,7), #room3 right <-> room4 left
(4,17,30, 5,58,0), #room4 bot <-> room5 top
(5,0,24, 6,39,9), #room5 left <-> room6 right
(6,0,13, 7,44,21), #room6 left <-> room7 right
(7,28,0, 8,15,39) #room7 top <-> room8 bot
;

ALTER TABLE `bbb61uemtrivmf5uyaub`.`MapTile`
ORDER BY `TileRoomID` ASC, `TileY` ASC, `TileX` ASC
;

ALTER TABLE `bbb61uemtrivmf5uyaub`.`MapTile`
ADD PRIMARY KEY (`TileRoomID`, `TileY`, `TileX`)
;