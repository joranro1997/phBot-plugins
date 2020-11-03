from phBot import *
import QtBind
from threading import Timer
from threading import Thread
from time import sleep
import json
import struct
import os
import io

gui = QtBind.init(__name__, 'SP Quest testing')

QtBind.createLabel(gui, 'Click the button to execute the desired SP quest script', 10, 10)

button1 = QtBind.createButton(gui, 'button1_clicked', '< lvl 80 Script', 10, 50)
button1 = QtBind.createButton(gui, 'button2_clicked', '>= lvl 80 Script', 100, 50)
button1 = QtBind.createButton(gui, 'button3_clicked', 'Test', 190, 50)

def button1_clicked():
    log('Executing Script')
    move_to(114.0, -4.0, 0.0)
    Timer(4.0,move_to,[112.0, 26.0, 0.0]).start()
    Timer(8.0,btnInjectPacket,['7045','EC 04 00 00']).start()
    Timer(12.0,btnInjectPacket,['7046','EC 04 00 00 02']).start()
    
def button2_clicked():
    log('Executing Script')
    UseReturnScroll()

async def button3_clicked():
    log('working')
    #Check if character is at an appropiate level
    valid_range = GetValidRange()
    if valid_range == True:
        #Check if quest is already taken
        quests = get_quests()
        found_quest = False
        for value in quests.values():
            name = value['name']
            if ((name[:16] == 'Ordinary Essence') or (name[:13] == 'Crude Essence')):
                found_quest = True
                if quest['completed'] == 'True':
                    stop_bot()
                    log('Going back to town to turn in SP quest')
                    UseReturnScroll()
                    await asyncio.sleep(30)
                    town = GetTown()
                    if town == 'Jangan':
                        Timer(50.0,JanganComplete).start()
                    else:
                        if town == 'Donwhang':
                            Timer(50.0,DonwhangComplete).start()
                        else:
                            if town == 'Hotan':
                                Timer(50.0,HotanComplete).start()
                            else:
                                if town == 'Samarkand':
                                    Timer(50.0,SamarkandComplete).start()
                                else:
                                    if town == 'Constantinople':
                                        Timer(50.0,ConstantinopleComplete).start()
                                    else:
                                        log('This town is not valid for SP quest')
                else:
                    log('Your SP quest is not yet completed. Try again later')
        if found_quest == False:
            log('Returning to town to get SP quest')
            stop_bot()
            UseReturnScroll()
            await asyncio.sleep(30)
            town = GetTown()
            if town == 'Jangan':
                Timer(50.0,JanganGetNew).start()
            else:
                if town == 'Donwhang':
                    Timer(50.0,DonwhangGetNew).start()
                else:
                    if town == 'Hotan':
                        Timer(50.0,HotanGetNew).start()
                    else:
                        if town == 'Samarkand':
                            Timer(50.0,SamarkandGetNew).start()
                        else:
                            if town == 'Constantinople':
                                Timer(50.0,ConstantinopleGetNew).start()
                            else:
                                log('This town is not valid for SP quest')
    else:
        log('Your level is not valid for SP Quest')
    
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
        
def GetReturnScroll():
	# Search the return scroll through items
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			# Check if match the current item
			match = False
			match = ('Return Scroll' == item['name'])
			if match:
				item['slot'] = slot
				temp = '{:02X}'.format(item['slot'])
				return item
	return None
    
def UseReturnScroll():
	# Check if the item exists
	name = ''
	item = GetReturnScroll()
	if item:
		# Start checking for item usage
		global usingDimensionalItem
		usingDimensionalItem = item
		# Inject item usage
		log('Plugin: Using "'+item['name']+'"... Waiting for 35 seconds before proceding with script')
		temp = '{:02X}'.format(item['slot'])
		temp += ' 30 0C 03 01'
		btnInjectPacket('704C',temp)
	else:
		# Error message
		log('Plugin: '+( '"'+name+'"' if name else 'Return Scroll')+' cannot be found at your inventory')
	return 0
    
def GetTown():
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
        
def GetValidRange():
    character = get_character_data()
    valid = True
    if ((character['level'] <= 40) or (character['level'] >= 101)):
        valid = False
    return valid
    
def JanganComplete():
    move_to(136.0, 33.0, 0.0)
    Timer(4.0,move_to,[161.0, 54.0, 0.0]).start()
    Timer(8.0,btnInjectPacket,['7045','CA 05 00 00']).start()
    Timer(12.0,btnInjectPacket,['7046','CA 05 00 00 02']).start()
    Timer(16.0,btnInjectPacket,['30D4','05']).start()
    Timer(20.0,btnInjectPacket,['7515','FB 05 00 00 00']).start()
    Timer(24.0,move_to,[161.0, 54.0, 0.0]).start()
    Timer(28.0,move_to,[136.0, 33.0, 0.0]).start()
    Timer(32.0,start_bot).start()
    
def DonwhangComplete():
    move_to()
    
def HotanComplete():
    move_to()
    
def SamarkandComplete():
    move_to()
    
def ConstantinopleComplete():
    move_to()
    
def JanganGetNew():
    move_to()
    
def DonwhangGetNew():
    move_to()
    
def HotanGetNew():
    move_to()
    
def SamarkandGetNew():
    move_to()
    
def ConstantinopleGetNew():
    move_to()
        
log('[%s] Loaded' % __name__)