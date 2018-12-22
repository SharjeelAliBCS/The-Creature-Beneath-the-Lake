#An adventure game where the player 
#must prove the existence of a fabled creature

#1. Make dictonary for gameworld
#2. Make dictonary for player
#3. Make protoype that only uses movement
#4. Add take/drop items. 
import csv
def load_text(file_name):
    file_data = []
    file_hndl = open(file_name, "r")
    for file_line in file_hndl.readlines():
        file_data.append(file_line)
        file_hndl.close()
    return file_data

def interact_npc(game_data, name):
    for npc in game_data["player"]["location"]["npc"]:
        npc_name = npc["name"].lower()
   
        if npc_name == name or npc_name.split()[0] == name or npc_name.split()[1] == name:
            #dialog_npc(game_data, npc)
            
            if npc["talk"]:
                dialog_npc(game_data, npc)
            else:
                print(npc_name, "is unavailable.")
            
            return
    print("NPC not found")
    return

def init_dialog(game_data, file_name):
    row_data = readCSV(file_name, False)
    return row_data


def dialog_npc(game_data, npc):
    dialog = npc["dialog"]
    talk = True
    name = npc["name"] +":"
    
    print("You are talking to", npc["name"])
    
    while talk:
        found_input = False

        dialog_input = input()
        
        for row in dialog:
  
            if row[0] == dialog_input:
                print(name, row[1])
                found_input = True

                if npc["name"]=="Father" and row[0] =="what did you see" and game_data["objectives"]["num"]==1:
                    add_objective(game_data)
                    game_data["npc"]["Crydus Averoth"]["dialog"] = readCSV("Assets/dialog/Crydus_Averoth_1.csv", False)
                    game_data["npc"]["Crydus Averoth"]["talk"] = True

                if npc["name"]=="Father" and row[0] =="where to go" and game_data["objectives"]["num"]==6:
                    add_objective(game_data)
                
                if npc["name"]=="Crydus Averoth" and row[0] =="how's life" and game_data["objectives"]["num"]==2:
                    add_objective(game_data)

                if npc["name"]=="Renaila Scoran" and (row[0] =="where's son" or row[0] == "what did you see") and game_data["objectives"]["num"]==4:
                    add_objective(game_data)
                    print("Crydus Averoth: Wait!", game_data["player"]["name"], "let me help you. Renaila, don't worry. We'll find him. Come on, I'll meet you at the lake.")
                break

        if not found_input:
            if dialog_input =="who are you" or dialog_input =="who are you?":
                print(name, npc["who are you"])
            
            elif dialog_input == "help":
                help(game_data, "dialog")

            elif dialog_input =='0':
                return

            else:
                print("Wrong dialog option. Try again.")

def add_objective(game_data):
    
    objective = game_data["objectives"]["list"][game_data["objectives"]["num"]]
    journal = game_data["journal"]["list"][game_data["objectives"]["num"]]
    
    if game_data["objectives"]["num"]>0:
        game_data["objectives"]["previous"].append(game_data["objectives"]["current"])
        game_data["journal"]["previous"].append(game_data["journal"]["current"])

    game_data["journal"]["current"] = journal
    game_data["objectives"]["current"] = objective
    print("NEW OBJECTIVE")
    game_data["score"]+=100
    game_data["objectives"]["num"] +=1

    if game_data["objectives"]["num"]==4:
        game_data["npc"]["Renaila Scoran"]["talk"] = True
        game_data["npc"]["Renaila Scoran"]["dialog"] = readCSV("Assets/dialog/Renaila_dialog1.csv", False)
        game_data["npc"]["Yorla Margrani"]["dialog"] = readCSV("Assets/dialog/Yorla_dialog1.csv", False)
        game_data["npc"]["Yorla Margrani"]["talk"] = True

        game_data["region"]["town"]["npc"].append(game_data["npc"]["Renaila Scoran"])
        game_data["region"]["town"]["npc"].remove(game_data["npc"]["Crydus Averoth"])
        update_player_region(game_data)

    elif game_data["objectives"]["num"]==5:
        game_data["region"]["lakeside"]["npc"].append(game_data["npc"]["Crydus Averoth"])
        game_data["npc"]["Crydus Averoth"]["dialog"] = readCSV("Assets/dialog/Crydus_Averoth_2.csv", False)
        game_data["npc"]["Crydus Averoth"]["talk"] = True

    elif game_data["objectives"]["num"]==6:
        game_data["npc"]["Father"]["talk"] = True
        game_data["npc"]["Father"]["dialog"] = readCSV("Assets/dialog/father_dialog2.csv", False)
        
    return game_data

def update_player_region(game_data):
    region_name = game_data["player"]["location"]["name"]
    game_data["player"]["location"] = game_data["region"][region_name]
    return game_data    

def view_objectives(game_data):
    if game_data["objectives"]["num"] ==  0:
        print("No objectives found.")

    else:
        print("CURRENT OBJECTIVE: "+ game_data["objectives"]["current"])
        print(game_data["journal"]["current"])

        if(len(game_data["objectives"]["previous"])>0):
            print("PREVIOUS OBJECTIVES:")
            
            journal_reversed= game_data["journal"]["previous"][::-1]
            objective_reversed= game_data["objectives"]["previous"][::-1]

            for index in range(len(game_data["objectives"]["previous"])):
                print(str(index+1)+" - "+ objective_reversed[index])
                print(journal_reversed[index])
            
def readCSV(csv_file_name, is_map):

	with open(csv_file_name) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		row_data = []
		i = 0       
		for row in readCSV:
           
			if is_map:
				row_data.append(row)
			if i >0 and not is_map:	
				row_data.append(row)
			i+=1	
	return row_data

def view_inventory(game_data):

    while(True):

        print(game_data["coins"], "coins")
        print("You currently have "+str(len(game_data["inventory"])) +" items in your inventory")
        for item in game_data["inventory"]:
            print("\t"+item["name"])

        action = input()

        if action.split()[0] == 'drop':
            drop_item(game_data, action.split('drop ')[1])
        elif action.split()[0] == 'view':
            view_item(game_data, action.split('view ')[1])
        elif action =="help":
            help(game_data, "inventory")
        elif action == '0':
            break
        else:
            print("Error 02: Wrong input. Try again.")
        print("")

def view_item(game_data, item):

    if item == "coin" or item == "coins":
        print("Cannot examine this.")
        return

    for inventory_item in game_data["inventory"]:
        if item.lower()==inventory_item["name"].lower():
            print(inventory_item["type"]+": "+inventory_item["name"])
            print(inventory_item["info"])

            if(inventory_item["type"] == "Weapon"):
                print("damage: "+ str(inventory_item["damage"]) )

            elif(inventory_item["type"] == "Book"):
                for line in inventory_item["text"]:
                    print(line)
            return
    print("Item not found.")
    return

def drop_item(game_data, item):

    if(item == "coins" or item == "coin"):
        if game_data["coins"]==0:
            print("You cannot drop any more coins.")
            return
        amount = int(input("how many?: "))
        
        if amount>=game_data["coins"]:
            amount = game_data["coins"]

        game_data["coins"]-=amount
        game_data["region"][game_data["player"]["location"]["name"]]["coins"]+=amount
        game_data["player"]["location"] = game_data["region"][game_data["player"]["location"]["name"]]

        print(amount, "coins dropped.")
        return

    for location_item in game_data["inventory"]:

        if item.lower()==location_item["name"].lower():

            game_data["inventory"].remove(location_item)
            game_data["region"][game_data["player"]["location"]["name"]]["items"].append(location_item)
            game_data["player"]["location"] = game_data["region"][game_data["player"]["location"]["name"]]

            print("item removed")
            return game_data
    print("Item not found.")
    return game_data

def pickup_item(game_data, item):

    if(item == "coins" or item == "coin"):
        if game_data["region"][game_data["player"]["location"]["name"]]["coins"]==0:
            print("No coins to pickup.")
            return

        amount = int(input("how many?: "))
        
        if amount>=game_data["region"][game_data["player"]["location"]["name"]]["coins"]:
            amount = game_data["region"][game_data["player"]["location"]["name"]]["coins"]
        
        game_data["coins"]+= amount

        game_data["region"][game_data["player"]["location"]["name"]]["coins"]-= amount
        game_data["player"]["location"] = game_data["region"][game_data["player"]["location"]["name"]]

        print(amount, "coins picked up.")
        return

    for location_item in game_data["player"]["location"]["items"]:

        if item==location_item["name"].lower():

            if location_item["pickup"]:
                game_data["inventory"].append(location_item)
                game_data["region"][ game_data["player"]["location"]["name"] ]["items"].remove(location_item)
                game_data["player"]["location"] = game_data["region"][game_data["player"]["location"]["name"]]
                print("%s picked up" % location_item["name"])

                if item=="Father's letter".lower() and game_data["objectives"]["num"]==0:
                    add_objective(game_data)
                    game_data["npc"]["Father"]["talk"] = True
            else:
                print("Cannot pick this up.")

                
            return game_data
    print("Item not found.")
    return game_data
            
def update_region(game_data, region):
    return
def init_game_data():

    game_data ={}
  
    game_data["score"] = 0
    game_data["game_over"] = False

    game_data["info"] ="You are in a ...."

    game_data["coins"] = 100
    game_data["player"] ={}
    game_data["inventory"] = []
    
    game_data["objectives"] = {}

    game_data["objectives"]["list"] = []
    game_data["journal"] = {}
    game_data["journal"]["current"] =None
    game_data["journal"]["previous"] = []
    game_data["journal"]["list"] = []

    row_data = readCSV("Assets/objectives.csv", False)
    for objective in row_data:   
        game_data["objectives"]["list"].append(objective[0])

    row_data = readCSV("Assets/journal.csv", False)
    for objective in row_data:   
        game_data["journal"]["list"].append(objective[0])

    game_data["objectives"]["current"] = None
    game_data["objectives"]["num"] = 0
    game_data["objectives"]["previous"] = []

    game_data["region"] ={}
    row_data = readCSV("Assets/regions.csv", False)

    for region_data in row_data:
        game_data["region"][region_data[0]] = {}
        game_data["region"][region_data[0]]["name"] = region_data[0]
        game_data["region"][region_data[0]]["info"] = region_data[1]
        game_data["region"][region_data[0]]["look"] = region_data[2]
        game_data["region"][region_data[0]]["access"] = []
        game_data["region"][region_data[0]]["items"] = [] 
        game_data["region"][region_data[0]]["npc"] = []
        game_data["region"][region_data[0]]["coins"] = 0

        access = region_data[3].split(", ")
        for access_area in access:
            game_data["region"][region_data[0]]["access"].append(access_area)

    game_data["region"]["bedroom"]["coins"] = 40

    game_data["items"] = {}
    row_data = readCSV("Assets/Items.csv", False)

    for item in row_data:
        game_data["items"][item[0]] = {}
        game_data["items"][item[0]]["name"] = item[0]
        game_data["items"][item[0]]["info"] = item[1]
        game_data["items"][item[0]]["type"] = item[2]

        if item[5] =="TRUE":
            game_data["items"][item[0]]["pickup"] = True
        else:
            game_data["items"][item[0]]["pickup"] = False

        if item[2]=="Book" or item[2] == "Text":
            game_data["items"][item[0]]["text"] = load_text(item[3])
        elif item[2] == "Weapon":
            game_data["items"][item[0]]["damage"] = item[3]

        if not item[4]=="None":
            game_data["region"][item[4]]["items"].append(game_data["items"][item[0]])

    game_data["enemies"] ={}
    
    
    game_data["npc"] ={}
    row_data = readCSV("Assets/npc.csv", False)

    for npc_data in row_data:
        game_data["npc"][npc_data[0]] = {}
        game_data["npc"][npc_data[0]]["name"] = npc_data[0]
        game_data["npc"][npc_data[0]]["region"] = npc_data[1]
        game_data["npc"][npc_data[0]]["who are you"] = npc_data[2]
        game_data["npc"][npc_data[0]]["access"] = npc_data[3]
        game_data["npc"][npc_data[0]]["encounter"] = 1
        game_data["npc"][npc_data[0]]["talk"] = False 
        if not npc_data[1] =="None":
            game_data["region"][npc_data[1]]["npc"].append(game_data["npc"][npc_data[0]])

    game_data["npc"]["Father"]["dialog"] = init_dialog(game_data,"Assets/dialog/father_dialog1.csv")

    #print(game_data["npc"]["Father"]["dialog"])
        
    game_data["player"]["location"] = game_data["region"]["bedroom"]
    
    return game_data

def help(game_data, mode):
    if mode =="default":
        print("Type '0' to quit.")
        print("Type 'inventory' to access inventory")
        print("Type 'pickup' followed by the item name to pickup the item")
        print("Type 'drop' followed by the item name to drop the item")
        print("Type 'examine' followed by the item name to examine an item in the room.")
        print("Type 'look' to get a detailed look around your enviroment")
        print("Type 'move' followed by a location to move")
        print("Type 'objective' to view current objective.")
        print("Type 'talk' followed by the NPC's name to talk to them.")
        print("Type 'help' when in inventory, dialog mode to get help.")

    elif mode == "inventory":
        print("Type '0' to exit inventory.")
        print("Type 'drop' followed by the item name to drop an item.")
        print("Type 'view' followed by the item name to view an item.")
        print("Type 'equip' followed by the item name to equip a weapon.")
    
    elif mode == "dialog":
        print("Type 'ask about' followed by a noun to ask about a certain event, thing, or person.")
        print("Type 'who killed' followed by a person's name to find out who the killer was.")
        print("Type 'what did you see'/'what do you see' to ask about what the person saw.")
        print("Type 'what happened' to know more about an event that occured.")
        print("Type 'How's life' to get some current insight into the person's day to day life.")
        print("Type 'where's' followed by a person's name to find out where they are")
        print("Type 'Found something' to ask about what the person has found.")
        print("Type 'Where to go' to get advice about where you should go.")
        
def look(game_data):

    if game_data["objectives"]["num"]==3:
        print("It's night now. The sky is turning pitch black. You better hurry and get home.")

    if game_data["objectives"]["num"] ==4 and game_data["player"]["location"]["name"]=="traven":
        print("This is odd. You look around the building and see dozens of men all scampering around. You gaze at their faces and all you see is shock. Even some of the town guards are here. Something is wrong. You decide to ask Yorla about it. ")
    
    print(game_data["player"]["location"]["look"])

    if(len(game_data["player"]["location"]["items"])>0):
        print("List of items found:")
        for item in game_data["player"]["location"]["items"]:
            if  item["pickup"]:
                print(item["name"]+"    ", end='')
        
    if game_data["player"]["location"]["coins"]>0:
        print(str(game_data["player"]["location"]["coins"]), "coins")  

    if len(game_data["player"]["location"]["items"])<=0 and game_data["player"]["location"]["coins"]==0:
        print("No items found")
        


    for npc in game_data["player"]["location"]["npc"]:
        print(npc["access"])

def examine(game_data, item):
    if(item =="coin" or item =="coins"):
        print("Cannot examine this.")
        return

    for location_item in game_data["player"]["location"]["items"]:
        if item.lower() == location_item["name"].lower():

            if location_item["name"]=="footprint" and game_data["objectives"]["num"]==5:
                print(location_item["info"])
                print("Crydus Averoth: This... This is a horse footprint. But it doesn't make sense... What's a horse doing out here, and why is it walking out of a lake?")
                print("You know what this is. You rise up from the wet ground, your back soaked, and you tell Crydus that the horse is actually going towards the water instead. His face lights up in shock and disbelief. You suddenly realize: Your father was telling the truth.")
                add_objective(game_data)

            elif location_item["type"]=="text":
                print(location_item["name"])
                print(location_item["text"])
            else:
                print(location_item["info"])
            return

    print("Item not found.")
    return

def move_region(game_data, region_name):

    for region in game_data["player"]["location"]["access"]:

        if region.split('_')[0]==region_name:
            game_data["player"]["location"] = game_data["region"][region.split('_')[1]]
            
            if region_name=="bedroom" and game_data["objectives"]["num"]:
                add_objective(game_data)
                print("You wake up, fresh as ever.")
            return game_data
    print("Invalid move location.")
    return game_data

def main():
    
    game_quit = False
    while(not game_quit):
        game_data = init_game_data()
        
        
        print("The Creature beneath the lake")
        player_input = input("Press any key to start, or '0' to quit: ")

        if player_input =='0':
            game_quit = True

        else:
            game_data["player"]["name"] = "Servius"
            #game_data["player"]["name"] = input("Type your character's name: ")
            print("Type 'help' for help.")
            
            print("You lie still on your wool bed. Suddenly, you wake up. You look outside to see the sun shining a warm, bright light into your eyes.")
            while(not game_data["game_over"]):
                print("SCORE: " + str(game_data["score"]))
                print(game_data["player"]["location"]["info"]+"\n")
                
                player_input = input().lower()

                if player_input =='0':
                    game_data["game_over"] = True

                elif player_input== "help":
                    help(game_data, "default")
                elif player_input.split()[0] == 'move':
                    move_region(game_data, player_input.split('move ')[1])
                
                elif player_input.split()[0] == 'examine':
                    examine(game_data, player_input.split('examine ')[1])
                elif player_input=="look":
                    look(game_data)

                elif player_input =='inventory':
                    view_inventory(game_data)
                    
                elif player_input.split()[0] == 'drop':
                    drop_item(game_data, player_input.split('drop ')[1])

                elif player_input.split()[0] =='pickup':
                    pickup_item(game_data, player_input.split('pickup ')[1])

                elif player_input== "objective":
                    view_objectives(game_data)

                elif player_input.split()[0] =="talk":
                    interact_npc(game_data, player_input.split('talk ')[1])
                   
                else:
                    print("Error 01: Wrong input. Try again")

                print("")

if __name__ == "__main__":
    main()

