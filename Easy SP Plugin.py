from phBot import *
import QtBind
import threading
from threading import Timer
import json

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
    
def getLevelRange():
    #Check what quest to look for depending on the level range
    character = get_character_data()
    level_range = 0 #Levels 41 to 50
    if ((character['level'] >= 51) and (character['level'] <= 60)):
        level_range = 1
    if ((character['level'] >= 61) and (character['level'] <= 70)):
        level_range = 2
    if ((character['level'] >= 71) and (character['level'] <= 80)):
        level_range = 3
    if ((character['level'] >= 81) and (character['level'] <= 90)):
        level_range = 4
    if ((character['level'] >= 91) and (character['level'] <= 100)):
        level_range = 5
    return level_range
        
def GetValidRange():
    #Check if level range is correct for SP quest
    character = get_character_data()
    valid = True
    if ((character['level'] <= 40) or (character['level'] >= 101)):
        valid = False
    return valid
    
def getQuest():
    quests = get_quests()
    quest = 0
    for value in quests.values():
        name = value['name']
        if name == 'Crude Essence of Life':
            quest = 1
        elif name == 'Crude Essence of Spirit':
            quest = 2
        elif name == 'Ordinary Essence of Strength':
            quest = 3
        elif name == 'Ordinary Essence of Life':
            quest = 4
        elif name == 'Ordinary Essence of Spirit':
            quest = 5
    return quest
        
        
def btnInjectPacket(opcodearg,dataarg):
	strOpcode = opcodearg
	strData = dataarg
	# Opcode or Data is not empty
	if strOpcode and strData:
		packet = bytearray()
		opcode = int(strOpcode,16)
		data = strData.split()
		i = 0
		while i < len(data):
			packet.append(int(data[i],16))
			i += 1
		encrypted = False
		inject_joymax(opcode,packet,encrypted)
    
def JanganComplete():
    #Script to walk to NPC and turn in SP quest
    quest = getQuest()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[6412.0, 1075.0, 0.0]).start()
    Timer(10.0,log,['Turning in quest at NPC']).start()
    if quest == 0: #Level 41 to 50
        Timer(10.0,btnInjectPacket,['7045','64 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','64 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','F8 05 00 00 00']).start() #safe
    if quest == 1: #Level 51 to 60
        Timer(10.0,btnInjectPacket,['7045','64 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','64 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','83 06 00 00 00']).start() #safe
    if quest == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    if quest == 3: #Level 71 to 80
        Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','FB 05 00 00 00']).start() #safe
    if quest == 4: #Level 81 to 90
        Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','FC 05 00 00 00']).start() #safe
    if quest== 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    Timer(25.0,log,['Quest turned in, going back to town center']).start()
    Timer(30.0,move_to,[6432.0, 1099.0, 0.0]).start()
    Timer(40.0,start_bot).start()
    Timer(40.0,unlockExecution).start()
    return
    
def DonwhangComplete():
    #Script to walk to NPC and turn in SP quest
    quest = getQuest()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[3556.0, 2070.0, 0.0]).start()
    Timer(10.0,move_to,[3566.0, 2092.0, 0.0]).start()
    Timer(15.0,log,['Turning in quest at NPC']).start()
    if quest == 0: #Level 41 to 50
        Timer(15.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','F8 05 00 00 00']).start() #safe
    if quest == 1: #Level 51 to 60
        Timer(15.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','83 06 00 00 00']).start() #safe
    if quest == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    if quest == 3: #Level 71 to 80
        Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','FB 05 00 00 00']).start() #safe
    if quest == 4: #Level 81 to 90
        Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','FC 05 00 00 00']).start() #safe
    if quest == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    Timer(30.0,log,['Quest turned in, going back to town center']).start()
    Timer(35.0,move_to,[3556.0, 2070.0, 0.0]).start()
    Timer(40.0,move_to,[3551.0, 2070.0, 0.0]).start()
    Timer(45.0,start_bot).start()
    Timer(45.0,unlockExecution).start()
    
    return
    
def HotanComplete():
    #Script to walk to NPC and turn in SP quest
    quest = getQuest()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(3.0,move_to,[136.0, 33.0, 0.0]).start()
    Timer(10.0,move_to,[161.0, 54.0, 0.0]).start()
    Timer(15.0,log,['Turning in quest at NPC']).start()
    if quest == 0: #Level 41 to 50
        Timer(15.0,btnInjectPacket,['7045','BA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','BA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','F8 05 00 00 00']).start() #safe
    if quest == 1: #Level 51 to 60
        Timer(15.0,btnInjectPacket,['7045','BA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','BA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','83 06 00 00 00']).start() #safe
    if quest == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    if quest == 3: #Level 71 to 80
        Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','FB 05 00 00 00']).start() #safe
    if quest == 4: #Level 81 to 90
        Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['7515','FC 05 00 00 00']).start() #safe
    if quest == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    Timer(30.0,log,['Quest turned in, going back to town center']).start()
    Timer(35.0,move_to,[136.0, 33.0, 0.0]).start()
    Timer(42.0,move_to,[115.0, 13.0, 0.0]).start()
    Timer(47.0,start_bot).start()
    Timer(47.0,unlockExecution).start()
    return
    
def SamarkandComplete():
    #Script to walk to NPC and turn in SP quest
    quest = getQuest()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[-5159.0, 2858.0, 0.0]).start()
    Timer(15.0,move_to,[-5158.0, 2899.0, 0.0]).start()
    Timer(20.0,log,['Turning in quest at NPC']).start()
    if quest == 0: #Level 41 to 50
        Timer(20.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(30.5,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['7515','F8 05 00 00 00']).start() #safe
    if quest == 1: #Level 51 to 60
        Timer(20.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(30.5,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['7515','83 06 00 00 00']).start() #safe
    if quest == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start()
        #Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start()
        #Timer(30.5,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    if quest == 3: #Level 71 to 80
        Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start() #safe
        Timer(30.5,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['7515','FB 05 00 00 00']).start() #safe
    if quest == 4: #Level 81 to 90
        Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start() #safe
        Timer(30.5,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['7515','FC 05 00 00 00']).start() #safe
    if quest == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start()
        #Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start()
        #Timer(30.5,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    Timer(35.0,log,['Quest turned in, going back to town center']).start()
    Timer(40.5,move_to,[-5159.0, 2858.0, 0.0]).start()
    Timer(50.0,move_to,[-5152.0, 2835.0, 0.0]).start()
    Timer(60.0,start_bot).start()
    Timer(60.0,unlockExecution).start()
    return
    
def ConstantinopleComplete():
    #Script to walk to NPC and turn in SP quest
    quest = getQuest()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[-10656.0, 2576.0, 0.0]).start()
    Timer(10.0,log,['Turning in quest at NPC']).start()
    if quest == 0: #Level 41 to 50
        Timer(10.0,btnInjectPacket,['7045','8B 08 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','8B 08 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','F8 05 00 00 00']).start() #safe
    if quest == 1: #Level 51 to 60
        Timer(10.0,btnInjectPacket,['7045','8B 08 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','8B 08 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','83 06 00 00 00']).start() #safe
    if quest == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    if quest == 3: #Level 71 to 80
        Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','FB 05 00 00 00']).start() #safe
    if quest == 4: #Level 81 to 90
        Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['7515','FC 05 00 00 00']).start() #safe
    if quest == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    Timer(25.0,log,['Quest turned in, going back to town center']).start()
    Timer(30.0,move_to,[-10658.0, 2602.0, 0.0]).start()
    Timer(40.0,start_bot).start()
    Timer(40.0,unlockExecution).start()
    return
    
def JanganGetNew():
    #Script to walk to NPC and get SP quest
    level_range = getLevelRange()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[6412.0, 1075.0, 0.0]).start()
    Timer(10.0,log,['Getting quest from NPC']).start()
    if level_range == 0: #Level 41 to 50
        Timer(10.0,btnInjectPacket,['7045','64 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','64 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 1: #Level 51 to 60
        Timer(10.0,btnInjectPacket,['7045','64 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','64 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
    if level_range == 3: #Level 71 to 80
        Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 4: #Level 81 to 90
        Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','65 03 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','65 03 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
    Timer(30.0,log,['Quest accepted, going back to town center']).start()
    Timer(35.0,move_to,[6432.0, 1099.0, 0.0]).start()
    Timer(45.0,start_bot).start()
    Timer(45.0,unlockExecution).start()
    return
    
def DonwhangGetNew():
    #Script to walk to NPC and get SP quest
    level_range = getLevelRange()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[3556.0, 2070.0, 0.0]).start()
    Timer(10.0,move_to,[3566.0, 2092.0, 0.0]).start()
    Timer(15.0,log,['Getting quest from NPC']).start()
    if level_range == 0: #Level 41 to 50
        Timer(15.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 1: #Level 51 to 60
        Timer(15.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['30D4','05']).start()
    if level_range == 3: #Level 71 to 80
        Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 4: #Level 81 to 90
        Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','71 02 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','71 02 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['30D4','05']).start()
    Timer(35.0,log,['Accepted quest, going back to town center']).start()
    Timer(40.0,move_to,[3556.0, 2070.0, 0.0]).start()
    Timer(45.0,move_to,[3551.0, 2070.0, 0.0]).start()
    Timer(50.0,start_bot).start()
    Timer(50.0,unlockExecution).start()
    return
    
def HotanGetNew():
    #Script to walk to NPC and get SP quest
    level_range = getLevelRange()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(3.0,move_to,[136.0, 33.0, 0.0]).start()
    Timer(10.0,move_to,[161.0, 54.0, 0.0]).start()
    Timer(15.0,log,['Getting quest from NPC']).start()
    if level_range == 0: #Level 41 to 50
        Timer(15.0,btnInjectPacket,['7045','BA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','BA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 1: #Level 51 to 60
        Timer(15.0,btnInjectPacket,['7045','BA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','BA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['30D4','05']).start()
    if level_range == 3: #Level 71 to 80
        Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 4: #Level 81 to 90
        Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start() #safe
        Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(15.0,btnInjectPacket,['7045','CA 05 00 00']).start()
        #Timer(20.0,btnInjectPacket,['7046','CA 05 00 00 02']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['30D4','05']).start()
    Timer(35.0,log,['Accepted quest, going back to town center']).start()
    Timer(40.0,move_to,[136.0, 33.0, 0.0]).start()
    Timer(47.0,move_to,[115.0, 13.0, 0.0]).start()
    Timer(55.0,start_bot).start()
    Timer(55.0,unlockExecution).start()
    return
    
def SamarkandGetNew():
    #Script to walk to NPC and get SP quest
    level_range = getLevelRange()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[-5159.0, 2858.0, 0.0]).start()
    Timer(15.0,move_to,[-5158.0, 2899.0, 0.0]).start()
    Timer(20.0,log,['Getting quest from NPC']).start()
    if level_range == 0: #Level 41 to 50
        Timer(20.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(40.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 1: #Level 51 to 60
        Timer(20.0,btnInjectPacket,['7045','7F 02 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','7F 02 00 00 02']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(40.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start()
        #Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['30D4','05']).start()
        #Timer(40.0,btnInjectPacket,['30D4','05']).start()
    if level_range == 3: #Level 71 to 80
        Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(40.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 4: #Level 81 to 90
        Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start() #safe
        Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(35.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(40.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(20.0,btnInjectPacket,['7045','32 08 00 00']).start()
        #Timer(25.0,btnInjectPacket,['7046','32 08 00 00 02']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
        #Timer(35.0,btnInjectPacket,['30D4','05']).start()
        #Timer(40.0,btnInjectPacket,['30D4','05']).start()
    Timer(40.0,log,['Quest accepted, going back to town center']).start()
    Timer(45.0,move_to,[-5159.0, 2858.0, 0.0]).start()
    Timer(55.0,move_to,[-5152.0, 2835.0, 0.0]).start()
    Timer(63.0,start_bot).start()
    Timer(63.0,unlockExecution).start()
    return
    
def ConstantinopleGetNew():
    #Script to walk to NPC and get SP quest
    level_range = getLevelRange()
    Timer(2.0,log,['Walking to SP quest NPC']).start()
    Timer(5.0,move_to,[-10656.0, 2576.0, 0.0]).start()
    Timer(10.0,log,['Getting quest from NPC']).start()
    if level_range == 0: #Level 41 to 50
        Timer(10.0,btnInjectPacket,['7045','8B 08 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','8B 08 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 1: #Level 51 to 60
        Timer(10.0,btnInjectPacket,['7045','8B 08 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','8B 08 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 2: #Level 61 to 70
        log('This plugin does not support the SP quest for levels 61 to 70 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
    if level_range == 3: #Level 71 to 80
        Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 4: #Level 81 to 90
        Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start() #safe
        Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start() #safe
        Timer(20.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(25.0,btnInjectPacket,['30D4','05']).start() #safe
        Timer(30.0,btnInjectPacket,['30D4','05']).start() #safe
    if level_range == 5: #Level 91 to 100
        log('This plugin does not support the SP quest for levels 91 to 100 at the moment. You can help by sending me the packet data for getting and turning in this quest using a packet logger plugin.')
        log('PM me in phBot forum @ratchet2 or on discord: Midway | Sphiria#1225')
        #Timer(10.0,btnInjectPacket,['7045','37 06 00 00']).start()
        #Timer(15.0,btnInjectPacket,['7046','37 06 00 00 02']).start()
        #Timer(20.0,btnInjectPacket,['30D4','05']).start()
        #Timer(25.0,btnInjectPacket,['30D4','05']).start()
        #Timer(30.0,btnInjectPacket,['30D4','05']).start()
    Timer(30.0,log,['Quest accepted, going back to town center']).start()
    Timer(35.0,move_to,[-10658.0, 2602.0, 0.0]).start()
    Timer(45.0,start_bot).start()
    Timer(45.0,unlockExecution).start()
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