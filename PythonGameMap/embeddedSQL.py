'''
    This file will contain all (or most) of the embeddedSQL querys
    in the form of functions to interact, change, and store variables
    in the classes and on the database.
'''
# Import the embedded mySQL library
import pymysql
import random
from config import TILESIZE

# Connect to the database
db = pymysql.connect(host='bbb61uemtrivmf5uyaub-mysql.services.clever-cloud.com', 
                     user='u0s0smkg4a9n1fgi', password='eRuqzZnbfDQoW5JS10ev', database='bbb61uemtrivmf5uyaub')

# GAME START DATABASE RESET ACTIONS
def sqlDatabaseReset(biomelist, biomeScaler):
    # Reset interacted tiles and enemies
    cursor = db.cursor()
    sql = "CALL resetAllInteracted();"
    cursor.execute(sql)
    db.commit()

    # Randomly set each room's biome (beyond spawn - room 0)
    for i in range(1,9):
        sqlbiomeassignment = "UPDATE Room SET RoomsBiomeID = "+str(biomelist[i])+" WHERE RoomID = "+str(i)
        cursor.execute(sqlbiomeassignment)
        db.commit()
    print(sqlbiomeassignment)

    # get the difficulty scale for each biome
    sql = "\
    SELECT DifficultyScale\
    FROM Biome"
    cursor.execute(sql)
    biomeScaler.clear()
    for i in range(len(cursor._rows)):
        biomeScaler.append(cursor._rows[biomelist[i]][0])
    # Determine the highest ItemValue for purposes of loot rolling below
    sql = "\
    SELECT Max(ItemValue)\
    FROM Item \
    "
    cursor.execute(sql)
    global maxItemValue #declare global scope
    for row in cursor:
        maxItemValue = row[0]
#    CALL resetInventory();"    # STORED PROCEDURE CURRENTLY UNCREATED
    # reset the inventory
    sql = "DELETE FROM Inventory WHERE Inventory.InventorySlot != 1"
    cursor.execute(sql)
    db.commit()
    
# Below is a list of ALL mySQL QUERY FUNCTIONS we must make to interact with the game
def sqlGetInteractableTiles(room):
    cursor = db.cursor()
    sql = "SELECT *\
           FROM MapTile MP\
           WHERE MP.`TileRoomID`="+str(room)+" AND MP.`TileContents` != 0"
    cursor.execute(sql)

    results = [ [] for i in range(len(cursor._rows)) ] 
    for i in range(len(cursor._rows)):
        results[i].append(cursor._rows[i][0])
        results[i].append(cursor._rows[i][1])
        results[i].append(cursor._rows[i][2])
        results[i].append(cursor._rows[i][3])
        results[i].append(cursor._rows[i][4])
    return results

def sqlCheckInventory():
    cursor = db.cursor()
    sql = "SELECT T.ItemName, T.ItemUses, T.ItemType, T.ItemValue\
    FROM Inventory I JOIN Item T\
        ON I.InventoryItem=T.ItemID\
        "
    cursor.execute(sql)
    itemList = cursor.fetchall()

    print("Name,    Uses, Type, Value")
#    results = [ [] for i in range(len(cursor._rows)) ] 
    for i in range(len(itemList)):
        print(itemList[i])
    
    return itemList

# Check and return BOOL if tile player has been interacted with
def sqlTileInteracted(player):
    cursor = db.cursor()
    sql = "\
    SELECT M.TileInteracted \
    FROM MapTile M \
    WHERE M.TileRoomID="+str(player.room)+"\
        AND M.TileX="+str(player.tileX)+"\
        AND M.TileY="+str(player.tileY)
    cursor.execute(sql)
    for row in cursor:
        TileInteracted = row[0]
    return TileInteracted

def sqlCheckTileContents(player, list):
    contents = list[3] # Determine contents
    if(contents != 0 and (list[4] == 0)):
        cursor = db.cursor()
        if(contents == 1):
            print("This is a Material Deposit")
            # The player is currently on the tile with the node
            # If not depleted (TileInteracted=1): then add that material to the persons inventory
            if(sqlTileInteracted(player) == 0):   # unmined node
                # Cross-reference player.room to biome, to materialnode-drop, to ItemName and ItemID
                # Select the item name and item's ID from Item table
                # We check the biome of the room, the biome will decide the material deposit
                # Material deposit type contains the foreign key to material node table
                # Material node table contains details about the material
                sql = "\
                SELECT ItemName, ItemID\
                FROM MaterialNode M, Biome B, Room R, Item I\
                WHERE M.MaterialNodeID=B.MaterialDepositType \
                    AND B.BiomeID=R.RoomsBiomeID\
                    AND I.ItemID=M.MaterialDrop\
                    AND R.RoomID=\
                "+str(player.room)
                cursor.execute(sql)
                for row in cursor:
                    MaterialDropName = row[0]
                    ItemID = row[1]
                    print("MaterialDrop ItemName is: "+str(MaterialDropName))
                    print("ItemID is: "+str(ItemID))
                # stepping on the deposit will mine it
                # https://www.mysqltutorial.org/mysql-if-statement/ for stored procedures
                # room,tileX,tileY
                # Set tile to show it's been interacted with
                sql = "CALL setInteracted("\
                    +str(player.room)+","\
                    +str(player.tileX)+","\
                    +str(player.tileY)+");"
                cursor.execute(sql) # push the update
                db.commit() # DON'T FORGET TO COMMIT THE CHANGES!

                # Check and notify interaction complete
                for row in cursor:
                    TileInteracted = row[0]
                if(TileInteracted): #tileInteracted=1
                    print("You mined "+str(MaterialDropName)+" - adding it to your inventory")   # E.g. "Leaves"
                
                # Update/add to inventory table (the InventorySlot key DB column is set to auto_increment (AI))
                sql = "\
                INSERT INTO Inventory (InventoryItem) \
                VALUES ("+str(ItemID)+"); \
                "
                cursor.execute(sql) # push the update
                db.commit() # DON'T FORGET TO COMMIT THE CHANGES!
            else:
                print("Tile is already mined") # and nothing else happens

        if(contents == 2):
            '''
            Do what we need to do for Treasire Chests
            - Get the biome of the room you are in
            - Get the loot rareity accociated with that biome
            - pull the chest tuple from the treasure chest table and then roll for a random
            item from the itemlist of the same rarity and then append it to the player inventory
            - update the inventory in the database
            - set the chest interacted boolean to true
            '''
            print("This is a Treasure Chest")
            # Has chest been looted already?
            if(sqlTileInteracted(player) == 0):   # unlooted chest
                
                # Cross-reference player.room to biome, to biome loot rarity, to chest
                # Check room's biome
                # Each biome has a rarity value which determines loot drop
                sql = "\
                SELECT ChestCommonItems, ChestUncommonItems, ChestRareItems, ChestEpicItems\
                FROM Biome B, Room R, Chest C\
                WHERE C.ChestRarityID=B.LootRarity\
                    AND B.BiomeID=R.RoomsBiomeID\
                    AND R.RoomID=\
                "+str(player.room)
                cursor.execute(sql)
                loot = cursor.fetchall()[0]
                print("Loot rolls: "+str(loot))
                
                # Roll for the different categories of loot
                # Odds for reference: % of DB.`item`.`ItemValues` 
                # Commmon: Lower 40%  
                # Uncommon: Next 30%
                # Rare:     Next 20%
                # Epic:  Highest 10%
                rbound=[0,40,70,90,100]   #rarity percentage boundaries
                rcategory=["common","uncommon","rare","epic"]

                for rarityCat in range(len(loot)): # rarity is 0-3 (4 categories or elements returned in loot just above)
                    print("For rarity category "+rcategory[rarityCat]+"...")
                    for rollnum in range(loot[rarityCat]):
                    # SQL: pick an item of said rarity and add it to inventory
                        sql_items_in_rarity = "\
                        SELECT * \
                        FROM Item I \
                        WHERE I.ItemValue > "+str(maxItemValue*rbound[rarityCat]/100)+"\
                            AND I.ItemValue <= "+str(maxItemValue*rbound[rarityCat+1]/100)+"\
                        "
                        print("Item value range: "+str(maxItemValue*rbound[rarityCat]/100)+"-"+str(maxItemValue*rbound[rarityCat+1]/100))
                        cursor.execute(sql_items_in_rarity)
                        result = cursor.fetchall()
                        count=len(result) # # of rows/items
                        print(str(count)+" items of "+rcategory[rarityCat]+" rarity")

                        # rng select one row from that list
                        roll = random.randint(1,count) # roll for loot in each category of rarity
                        selected=result[roll-1] # keep selection index within range
                        print(selected[1]+" GET!")
                        ItemID = selected[0]
                        # After the player rolls for each item, copy the item into his inventory
                        store_sql = "\
                        INSERT INTO Inventory (InventoryItem) \
                        VALUES ("+str(ItemID)+"); \
                        "
                        cursor.execute(store_sql)
                        db.commit()
                        sql = "CALL setInteracted("\
                            +str(player.room)+","\
                            +str(player.tileX)+","\
                            +str(player.tileY)+");"
                        cursor.execute(sql) # push the update
                        db.commit() # DON'T FORGET TO COMMIT THE CHANGES!
            
            else:
                print("This chest has been looted")

        if(contents == 3):
            '''
            Do what we need to do for Enemies (TBD)
            '''
            print("This is an enemy!")
        if(contents == 4):
            '''
            Do what we need to do for Doors
            - Find the door at the same coordinates of the specified location
            - Find the linking door tile from the door table
            - Clear the current room and generate the new room, updating the player location at
            the tile transported to by the door
            '''
            # The door table contains the combination of connecting doors
            # Entering a door will teleport the player to the coordinate that it is linked to
            # in the other room
            cursor = db.cursor()
            sql =  "SELECT *\
                    FROM Door AS D\
                    WHERE (D.`Room1`="+str(player.room)+" AND \
                           D.`Door1PosX`="+str(player.tileX)+" AND \
                           D.`Door1PosY`="+str(player.tileY)+") \
                       OR (D.`Room2`="+str(player.room)+" AND \
                           D.`Door2PosX`="+str(player.tileX)+" AND \
                           D.`Door2PosY`="+str(player.tileY)+")"
            cursor.execute(sql)
            results = []
            for i in range(len(cursor._rows[0])):
                results.append(cursor._rows[0][i])

            print(results)
            ''' Find which values to return '''
            # If coordinates match 1st half, set new coordinates to 2nd half
            if(player.room == results[0] and player.tileX == results[1] and player.tileY == results[2]):
                player.room = results[3]
                player.tileX = results[4]
                player.tileY = results[5]
                player.game.genRoom = True
                print("Door is 1st half!")
                print("Entering room: "+str(player.room)+"...")
                return
            # if coordinates match 2nd half, set new coordinates to 1st half 
            if(player.room == results[3] and player.tileX == results[4] and player.tileY == results[5]):
                player.room = results[0]
                player.tileX = results[1]
                player.tileY = results[2]
                player.game.genRoom = True
                print("Door is 2nd half!")
                print("Entering room: "+str(player.room)+"...")
                return
            
#endfunc