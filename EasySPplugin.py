from phBot import *
import QtBind
import threading
from time import sleep
import json
import struct

eventTeleported = threading.Event()

spawned = False

blocked = False

gui = QtBind.init(__name__, 'Easy SP!')

QtBind.createLabel(gui, 'Written by Midway: https://github.com/joranro1997/phBot-plugins', 10, 10)
QtBind.createLabel(gui, 'Discord: Midway | Sphiria#1225', 10, 260)
QtBind.createLabel(gui, 'PM me in phBot forum: @ratchet2', 10, 235)

QtBind.createLabel(gui, 'Click the button to return or get SP quest!', 265, 130)

button1 = QtBind.createButton(gui, 'button_clicked', 'Go SP!', 325, 160)
    
def button_clicked():
    #Button for testing
    global spawned
    global blocked
    if blocked:
        log('Script is already executing')
        return
    else:
        blocked = True
        spawned = False
        thread = myThread(1, 'SP Quest')
        thread.start()
        return
    
def UseReturnScrollTask():
	# API return success?
	success = use_return_scroll()
	if success:
		teleport()
		global eventTeleported
		eventTeleported.wait()
	return success
    
def teleport():
	global eventTeleported
	global spawned
	aux = False
	while not aux:
		aux = spawned
	eventTeleported.set()
	return
    
def handle_joymax(opcode, data):
    global spawned
    if ((opcode == 12407) and (data == b'\x00\x00')):
        spawned = True
        return True
    else:
        return True    

def GetTown():
    #Check what town we are after spawning
	position = get_position()
	town = ''
	if position['region'] == 25000:
        	town = 'Jangan'
	if position['region'] == 26265:
        	town = 'Donwhang'
	if position['region'] == 23687:
        	town = 'Hotan'
	if position['region'] == 27244:
        	town = 'Samarkand'
	if position['region'] == 26959:
        	town = 'Constantinople'
	return town
    
def checkValidTown():
    town = GetTown()
    valid = False
    if ((town == 'Jangan') or (town == 'Donwhang') or (town == 'Hotan') or (town == 'Samarkand') or (town == 'Constantinople')):
        valid = True
    return valid
    
def unlockExecution():
    global blocked
    blocked = False
    return
        
def GetValidRange():
    #Check if level range is correct for SP quest
    character = get_character_data()
    valid = True
    if ((character['level'] <= 40) or (character['level'] >= 101)):
        valid = False
    return valid
        
def getNPCID():
    npcs = get_npcs()
    for id, npc in npcs.items():
        npc_name = npc['name']
        if npc_name[:5] == 'Daily':
            return id
    return
    
def getQuestID():
    quests = get_quests()
    for id, value in quests.items():
        name = value['name']
        if ((name[:16] == 'Ordinary Essence') or (name[:13] == 'Crude Essence')):
            return id
    return
    
def JanganComplete():
    #Script to walk to NPC and turn in SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(6412.0, 1075.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    quest_id = getQuestID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Turning in quest at NPC')
    inject_joymax(0x7045,p,False)
    sleep(1.0)
    p += struct.pack('B',2)
    sleep(3.0)
    inject_joymax(0x7046,p,False)
    sleep(1.0)
    p = struct.pack('B',5)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(1.0)
    p = struct.pack('I',quest_id)
    p += struct.pack('B',0)
    sleep(3.0)
    inject_joymax(0x7515,p,False)
    log('Quest turned in, going back to town center')
    sleep(3.0)
    move_to(6432.0, 1099.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def DonwhangComplete():
    #Script to walk to NPC and turn in SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(3556.0, 2070.0, 0.0)
    sleep(5.0)
    move_to(3566.0, 2092.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    quest_id = getQuestID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Turning in quest at NPC')
    inject_joymax(0x7045,p,False)
    sleep(1.0)
    p += struct.pack('B',2)
    sleep(3.0)
    inject_joymax(0x7046,p,False)
    sleep(1.0)
    p = struct.pack('B',5)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(1.0)
    p = struct.pack('I',quest_id)
    p += struct.pack('B',0)
    sleep(3.0)
    inject_joymax(0x7515,p,False)
    log('Quest turned in, going back to town center')
    sleep(3.0)
    move_to(3556.0, 2070.0, 0.0)
    sleep(5.0)
    move_to(3551.0, 2070.0, 0.0)
    sleep(3.0)
    start_bot()
    unlockExecution()
    return
    
def HotanComplete():
    #Script to walk to NPC and turn in SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(136.0, 33.0, 0.0)
    sleep(5.0)
    move_to(161.0, 54.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    quest_id = getQuestID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Turning in quest at NPC')
    inject_joymax(0x7045,p,False)
    sleep(1.0)
    p += struct.pack('B',2)
    sleep(3.0)
    inject_joymax(0x7046,p,False)
    sleep(1.0)
    p = struct.pack('B',5)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(1.0)
    p = struct.pack('I',quest_id)
    p += struct.pack('B',0)
    sleep(3.0)
    inject_joymax(0x7515,p,False)
    log('Quest turned in, going back to town center')
    sleep(3.0)
    move_to(136.0, 33.0, 0.0)
    sleep(5.0)
    move_to(115.0, 13.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def SamarkandComplete():
    #Script to walk to NPC and turn in SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(-5159.0, 2858.0, 0.0)
    sleep(5.0)
    move_to(-5158.0, 2899.0, 0.0)
    sleep(7.0)
    npc_id = getNPCID()
    quest_id = getQuestID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Turning in quest at NPC')
    inject_joymax(0x7045,p,False)
    sleep(1.0)
    p += struct.pack('B',2)
    sleep(3.0)
    inject_joymax(0x7046,p,False)
    sleep(1.0)
    p = struct.pack('B',5)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(1.0)
    p = struct.pack('I',quest_id)
    p += struct.pack('B',0)
    sleep(3.0)
    inject_joymax(0x7515,p,False)
    log('Quest turned in, going back to town center')
    sleep(3.0)
    move_to(-5159.0, 2858.0, 0.0)
    sleep(7.0)
    move_to(-5152.0, 2835.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def ConstantinopleComplete():
    #Script to walk to NPC and turn in SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(-10656.0, 2576.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    quest_id = getQuestID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Turning in quest at NPC')
    inject_joymax(0x7045,p,False)
    sleep(1.0)
    p += struct.pack('B',2)
    sleep(3.0)
    inject_joymax(0x7046,p,False)
    sleep(1.0)
    p = struct.pack('B',5)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(1.0)
    p = struct.pack('I',quest_id)
    p += struct.pack('B',0)
    sleep(3.0)
    inject_joymax(0x7515,p,False)
    log('Quest turned in, going back to town center')
    sleep(3.0)
    move_to(-10658.0, 2602.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def JanganGetNew():
    #Script to walk to NPC and get SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(6412.0, 1075.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Getting quest from NPC')
    inject_joymax(0x7045,p,False)
    sleep(3.0)
    p += struct.pack('B',2)
    sleep(1.0)
    inject_joymax(0x7046,p,False)
    sleep(3.0)
    p = struct.pack('B',5)
    sleep(1.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    log('Accepted quest, going back to town center')
    sleep(3.0)
    move_to(6432.0, 1099.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def DonwhangGetNew():
    #Script to walk to NPC and get SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(3556.0, 2070.0, 0.0)
    sleep(5.0)
    move_to(3566.0, 2092.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Getting quest from NPC')
    inject_joymax(0x7045,p,False)
    sleep(3.0)
    p += struct.pack('B',2)
    sleep(1.0)
    inject_joymax(0x7046,p,False)
    sleep(3.0)
    p = struct.pack('B',5)
    sleep(1.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    log('Accepted quest, going back to town center')
    sleep(3.0)
    move_to(3556.0, 2070.0, 0.0)
    sleep(5.0)
    move_to(3551.0, 2070.0, 0.0)
    sleep(3.0)
    start_bot()
    unlockExecution()
    return
    
def HotanGetNew():
    #Script to walk to NPC and get SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(136.0, 33.0, 0.0)
    sleep(5.0)
    move_to(161.0, 54.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Getting quest from NPC')
    inject_joymax(0x7045,p,False)
    sleep(3.0)
    p += struct.pack('B',2)
    sleep(1.0)
    inject_joymax(0x7046,p,False)
    sleep(3.0)
    p = struct.pack('B',5)
    sleep(1.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    log('Accepted quest, going back to town center')
    sleep(3.0)
    move_to(136.0, 33.0, 0.0)
    sleep(5.0)
    move_to(115.0, 13.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def SamarkandGetNew():
    #Script to walk to NPC and get SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(-5159.0, 2858.0, 0.0)
    sleep(5.0)
    move_to(-5158.0, 2899.0, 0.0)
    sleep(7.0)
    npc_id = getNPCID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Getting quest from NPC')
    inject_joymax(0x7045,p,False)
    sleep(3.0)
    p += struct.pack('B',2)
    sleep(1.0)
    inject_joymax(0x7046,p,False)
    sleep(3.0)
    p = struct.pack('B',5)
    sleep(1.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    log('Accepted quest, going back to town center')
    sleep(3.0)
    move_to(-5159.0, 2858.0, 0.0)
    sleep(7.0)
    move_to(-5152.0, 2835.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
    
def ConstantinopleGetNew():
    #Script to walk to NPC and get SP quest
    sleep(2.0)
    log('Walking to SP quest NPC')
    move_to(-10656.0, 2576.0, 0.0)
    sleep(5.0)
    npc_id = getNPCID()
    p = struct.pack('I',npc_id)
    sleep(1.0)
    log('Getting quest from NPC')
    inject_joymax(0x7045,p,False)
    sleep(3.0)
    p += struct.pack('B',2)
    sleep(1.0)
    inject_joymax(0x7046,p,False)
    sleep(3.0)
    p = struct.pack('B',5)
    sleep(1.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    sleep(3.0)
    inject_joymax(0x30D4,p,False)
    log('Accepted quest, going back to town center')
    sleep(3.0)
    move_to(-10658.0, 2602.0, 0.0)
    sleep(5.0)
    start_bot()
    unlockExecution()
    return
        
class myThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
   def run(self):
      #Check if character is at an appropiate level
    global eventTeleported
    valid_range = GetValidRange()
    if valid_range == True:
        #Check if quest is already taken
        quests = get_quests()
        found_quest = False
        for value in quests.values():
            name = value['name']
            if ((name[:16] == 'Ordinary Essence') or (name[:13] == 'Crude Essence')):
                found_quest = True
                #Check if quest has been completed
                if value['completed'] == True:
                    stop_bot()
                    if checkValidTown():
                        town = GetTown()
                        if town == 'Jangan':
                            JanganComplete()
                            return
                        elif town == 'Donwhang':
                            DonwhangComplete()
                            return
                        elif town == 'Hotan':
                            HotanComplete()
                            return
                        elif town == 'Samarkand':
                            SamarkandComplete()
                            return
                        elif town == 'Constantinople':
                            ConstantinopleComplete()
                            return 
                    log('Going back to town to turn in SP quest.')
                    #Go back to town and wait to spawn
                    success = UseReturnScrollTask()
                    if not success:
                        log('Error teleporting...')
                        unlockExecution()
                        return
                    log('Teleport done!')
                    eventTeleported.clear()
                    #Identify the town after spawning and select correct script
                    town = GetTown()
                    if town == 'Jangan':
                        JanganComplete()
                        return
                    elif town == 'Donwhang':
                        DonwhangComplete()
                        return
                    elif town == 'Hotan':
                        HotanComplete()
                        return
                    elif town == 'Samarkand':
                        SamarkandComplete()
                        return
                    elif town == 'Constantinople':
                        ConstantinopleComplete()
                        return
                    else:
                        log('This town is not valid for SP quest')
                        unlockExecution()
                        return
                else:
                    #If quest is found but not completed nothing happens
                    log('Your SP quest is not yet completed. Try again later')
                    unlockExecution()
                    return
        if found_quest == False:
            #If no quest is found, return to town to get it
            stop_bot()
            if checkValidTown():
                town = GetTown()
                if town == 'Jangan':
                    JanganGetNew()
                    return
                elif town == 'Donwhang':
                    DonwhangGetNew()
                    return
                elif town == 'Hotan':
                    HotanGetNew()
                    return
                elif town == 'Samarkand':
                    SamarkandGetNew()
                    return
                elif town == 'Constantinople':
                    ConstantinopleGetNew()
                    return 
            log('Going back to town to get SP quest.')
            #Go back to town and wait to spawn
            success = UseReturnScrollTask()
            if not success:
                log('Error teleporting...')
                unlockExecution()
                return
            log('Teleport done!')
            eventTeleported.clear()
            #Identify the town after spawning and select correct script
            town = GetTown()
            if town == 'Jangan':
                JanganGetNew()
                return
            elif town == 'Donwhang':
                DonwhangGetNew()
                return
            elif town == 'Hotan':
                HotanGetNew()
                return
            elif town == 'Samarkand':
                SamarkandGetNew()
                return
            elif town == 'Constantinople':
                ConstantinopleGetNew()
                return
            else:
                log('This town is not valid for SP quest')
                unlockExecution()
                return
    else:
        log('Your level is not valid for SP Quest')
        unlockExecution()
        return
        
log('[%s] Loaded' % __name__)