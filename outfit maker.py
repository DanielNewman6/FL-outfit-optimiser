import itertools
import re
from lxml import etree
import operator
from math import prod
from tqdm.tk import tqdm
import time
from tkinter import *
import tkinter.messagebox

def setup(person='Player'):
    global innateBizarre
    global innateDreaded
    global innateRespectable
    global innateMithridacy
    global innateArtisan
    global innateGlasswork
    global innateChess
    global innateAnatomy
    global innateToxicology
    global innateShapeling
    global innateZeefaring
    global innateChthonosophy
    global innateWatchful
    global innateDangerous
    global innateShadowy
    global innatePersuasive
    innateBizarre, innateDreaded, innateRespectable, innateMithridacy, innateArtisan, innateGlasswork, innateChess, innateAnatomy, innateToxicology, innateShapeling, innateZeefaring, innateChthonosophy, innateWatchful, innateDangerous, innateShadowy, innatePersuasive = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    if person=='Player':
        innateBizarre = 0
        innateDreaded = 2+2+4
        innateRespectable = 0
        innateMithridacy = 7
        innateArtisan = 7
        innateGlasswork = 7
        innateChess = 7
        innateAnatomy = 7
        innateToxicology = 7+1
        innateShapeling = 7
        innateZeefaring = 7
        innateChthonosophy = 6
        innateWatchful = 230
        innateDangerous = 236+1+5
        innateShadowy = 230+5
        innatePersuasive = 230
    elif person=='Luckless Captain':
        innateWatchful=50
        innateDangerous=50
        innateZeefaring=3
    elif person=='Clay Breaker':
        innateWatchful=50
        innateDangerous=70
        innateZeefaring=1
    elif person=='Wily Bathyphile':
        innateWatchful=50
        innateShadowy=50
        innateDangerous=20
        innateZeefaring=5
    elif person=='Mild-Mannered Mondaine':
        innateShadowy=50
        innatePersuasive=50
    elif person=='Unilluminated Mole':
        innateShadowy=70
        innatePersuasive=30
        innateChess=1

equipmentFile = etree.parse('equipmentFile.xml')

def statText(text):
    req = re.search('"(.*)"', text)
    equ = re.search('"([a-z]+)"', text)
    if req: return req.group(1)
    else: return equ.group(1)

def typeAppend(equipment):
    r = equipment.get('type')+'s'
    try:
        eval(r).append(equipment)
    except:
        print(equipment.get('name'))

def statIs(equipment, stat):
    if equipment =='innate':
        return {'bizarre':innateBizarre, 'dreaded':innateDreaded, 'respectable':innateRespectable, 'mithridacy':innateMithridacy, 'artisan':innateArtisan,
                'glasswork':innateGlasswork, 'chess':innateChess, 'anatomy':innateAnatomy, 'katalepticToxicology':innateToxicology,
                'shapelingArts':innateShapeling,'persuasive':innatePersuasive,'watchful':innateWatchful,'dangerous':innateDangerous,'shadowy':innateShadowy,
                'zeefaring':innateZeefaring,'chthonosophy':innateChthonosophy, 'wounds':0,'suspicion':0,'scandal':0,'nightmares':0,'inerrant':0,'insubstantial':0,'neathproofed':0}[stat]
    return int(equipment.get(stat,default=0))

def skylineBest(things, attributes, comparisons):
    maximals=[]
    while things:
        currMaximal = things.pop(0)
        pos = 0
        for i in things:
            if all([comparisons[j](statIs(currMaximal,attributes[j]),statIs(i,attributes[j])) for j in range(0,len(attributes))]):
                things.remove(i)
            elif all([comparisons[j](statIs(i,attributes[j]),statIs(currMaximal,attributes[j])) for j in range(0,len(attributes))]):
                currMaximal = i
                pos = things.index(i)
                things.remove(i)
        maximals+=[currMaximal]
        for i in things[0:pos]:
            if all([comparisons[j](statIs(currMaximal,attributes[j]),statIs(i,attributes[j])) for j in range(0,len(attributes))]):
                things.remove(i)
    return maximals

def filterOut(slot, filterBy, directions, sortBy, mode='maximum'):
    global filter1counts
    filterVals = []
    for i in slot:
        if [statIs(i, j) for j in filterBy] not in filterVals:
            filterVals.append([statIs(i, j) for j in filterBy])
    if mode=='maximum':
        slotPartFiltered = [max([i for i in slot if [statIs(i, k) for k in filterBy]==j], key=lambda i: statIs(i, sortBy)) for j in filterVals]
    elif mode=='minimum':
        slotPartFiltered = [min([i for i in slot if [statIs(i, k) for k in filterBy]==j], key=lambda i: statIs(i, sortBy)) for j in filterVals]
    filter1counts+=[len(slotPartFiltered)]
    return skylineBest(slotPartFiltered, filterBy+[sortBy], [{'>':operator.ge, '<':operator.le, '==':lambda x, y: False}[i] for i in directions]+[{'maximum':operator.ge, 'minimum':operator.le}[mode]])

main = Tk()
pbar = tqdm(tk_parent=main)
pbar._tk_window.withdraw()

#subjectTo of the form ['statVal["respectable"]>=7', 'statVal["bizarre"]==0']
def optimise(stat, subjectTo, mode='maximum', agent=False):
    global hats
    global clothings
    global gloves
    global weapons
    global boots
    global companions
    global tools
    global treasures
    global affiliations
    global transports
    global homeComforts
    global crews
    global adornments
    global statVal
    global luggages
    global equipments
    global filter1counts
    relevantStats = [stat]
    for i in subjectTo:
        relevantStats.append(statText(i))
    if mode=='maximum':
        lookingFor = ['>']+['<' if '<' in i else '>' if '>' in i else '==' for i in subjectTo]
        currentBest=[0]
    elif mode=='minimum':
        lookingFor = ['<']+['<' if '<' in i else '>' if '>' in i else '==' for i in subjectTo]
        currentBest=[500]
    hats=equipmentFile.findall('.//equipment[@name="Empty"]')
    clothings=equipmentFile.findall('.//equipment[@name="Empty"]')
    gloves=equipmentFile.findall('.//equipment[@name="Empty"]')
    weapons=equipmentFile.findall('.//equipment[@name="Empty"]')
    boots=equipmentFile.findall('.//equipment[@name="Empty"]')
    companions=equipmentFile.findall('.//equipment[@name="Empty"]')
    tools=equipmentFile.findall('.//equipment[@name="Empty"]')
    treasures=equipmentFile.findall('.//equipment[@name="Empty"]')
    affiliations=equipmentFile.findall('.//equipment[@name="Empty"]')
    transports=equipmentFile.findall('.//equipment[@name="Empty"]')
    homeComforts=equipmentFile.findall('.//equipment[@name="Empty"]')
    adornments=equipmentFile.findall('.//equipment[@name="Empty"]')
    crews=equipmentFile.findall('.//equipment[@name="Empty"]')
    luggages=equipmentFile.findall('.//equipment[@name="Empty"]')
    if not agent:
        for equipment in equipmentFile.findall('.//equipment[@type]'):
            for r in range(0, len(relevantStats)):
                if lookingFor[r]=='<':
                    if statIs(equipment, relevantStats[r])<0:
                        typeAppend(equipment)
                        break
                elif lookingFor[r]=='>':
                    if statIs(equipment, relevantStats[r])>0:
                        typeAppend(equipment)
                        break
                elif lookingFor[r]=='==':
                    if statIs(equipment, relevantStats[r])!=0:
                        typeAppend(equipment)
                        break
    else:
        for equipment in equipmentFile.xpath('.//equipment[@type!="tool" and @type!="treasure" and @agentAvail="true"]'):
            for r in range(0, len(relevantStats)):
                if lookingFor[r]=='<':
                    if statIs(equipment, relevantStats[r])<0:
                        typeAppend(equipment)
                        break
                elif lookingFor[r]=='>':
                    if statIs(equipment, relevantStats[r])>0:
                        typeAppend(equipment)
                        break
                elif lookingFor[r]=='==':
                    if statIs(equipment, relevantStats[r])!=0:
                        typeAppend(equipment)
                        break
    equipments = [hats, clothings, adornments, gloves, weapons, boots, luggages, companions, treasures, tools, affiliations, transports, homeComforts, crews]
    print('Naive search:      '+str(prod([len(i) for i in equipments])))
    filter1counts=[]
    for i in range(0,len(equipments)):
        equipments[i]=filterOut(equipments[i], relevantStats[1:], lookingFor[1:], stat, mode=mode)
    print('After first pass:  '+str(prod(filter1counts)))
    print('After second pass: '+str(prod([len(i) for i in equipments])))
    st=time.time()
    outfits=itertools.product(*equipments)
    en=time.time()
    print('Building outfit list: '+str(en-st))
    pbar._tk_window.deiconify()
    pbar.reset(total=prod([len(i) for i in equipments]))
    for fit in outfits:
        statVal={}
        for i in relevantStats:
            statVal[i] = sum([statIs(j, i) for j in fit])+statIs('innate', i)
        if mode=='maximum':
            if all([eval(j) for j in subjectTo]) and statVal[stat]>currentBest[0]:
                currentBest = [statVal[stat]]+[j.get('name') for j in fit]
        elif mode=='minimum':
            if all([eval(j) for j in subjectTo]) and statVal[stat]<currentBest[0]:
                currentBest = [statVal[stat]]+[j.get('name') for j in fit]
        pbar.update(1)
    pbar._tk_window.withdraw()
    print(currentBest)
    if not agent: tkinter.messagebox.showinfo("Results",  'Total: '+str(currentBest[0])+'\nHat: '+str(currentBest[1])+'\nClothing: '+str(currentBest[2])+'\nAdornment: '+str(currentBest[3])+'\nGloves: '+str(currentBest[4])+'\nWeapon: '+str(currentBest[5])+'\nBoots: '+str(currentBest[6])+'\nLuggage: '+str(currentBest[7])+'\nCompanion: '+str(currentBest[8])+'\nTreasure: '+str(currentBest[9])+'\nTool of the Trade: '+str(currentBest[10])+'\nAffiliation: '+str(currentBest[11])+'\nTransport: '+str(currentBest[12])+'\nHome Comfort: '+str(currentBest[13])+'\nCrew: '+str(currentBest[14]))
    else: tkinter.messagebox.showinfo("Results",  'Total: '+str(currentBest[0])+'\nHat: '+str(currentBest[1])+'\nClothing: '+str(currentBest[2])+'\nAdornment: '+str(currentBest[3])+'\nGloves: '+str(currentBest[4])+'\nWeapon: '+str(currentBest[5])+'\nBoots: '+str(currentBest[6])+'\nLuggage: '+str(currentBest[7])+'\nCompanion: '+str(currentBest[8])+'\nAffiliation: '+str(currentBest[11])+'\nTransport: '+str(currentBest[12])+'\nHome Comfort: '+str(currentBest[13])+'\nCrew: '+str(currentBest[14]))

personOptions = ['Player','Luckless Captain','Clay Breaker','Wily Bathyphile','Mild-Mannered Mondaine','Unilluminated Mole']
person = StringVar(main)
person.set('Player')
personLabel = Label(main, text='Optimise for: ').grid(column=0,row=0)
personMenu = OptionMenu(main,person,*personOptions).grid(column=1,row=0)


stats = ['persuasive','watchful','shadowy','dangerous','wounds','nightmares','scandal','suspicion','respectable','dreaded','bizarre','katalepticToxicology','anatomy','chess','glasswork','shapelingArts','artisan','mithridacy','zeefaring','chthonosophy','neathproofed','inerrant','insubstantial']
optimised = StringVar(main)
optimised.set('watchful')
optimiseMenu = OptionMenu(main,optimised,*stats).grid(column=1,row=1)

aimLabel = Label(main,text='Aiming for: ').grid(column=0,row=2)
aims = ['maximum','minimum']
aim = StringVar(main)
aim.set('maximum')
aimMenu = OptionMenu(main,aim,*aims).grid(column=1,row=2)

constraintLabel = Label(main,text='Constraint(s): ').grid(column=0,row=3)

constraints = []
currConstraint=3
relations=['>=','<=']
def addConstraint():
    global constraints
    global currConstraint
    statVar = StringVar(main)
    statVar.set('respectable')
    statMenu = OptionMenu(main,statVar,*stats).grid(row=currConstraint,column=1)
    relationVar = StringVar(main)
    relationVar.set('>=')
    relationMenu = OptionMenu(main,relationVar,*relations).grid(row=currConstraint,column=2)
    valVar = StringVar(main)
    valVar.set('7')
    valMenu = Entry(main,textvariable=valVar).grid(row=currConstraint,column=3)
    constraints.append([statVar,relationVar,valVar])
    currConstraint+=1

addConstraint()

constraintButton = Button(main,text='Add Constraint',command=addConstraint).grid(row=4,column=0)

def runOptimise():
    setup(person=person.get())
    if person.get()=='Player': agent=False
    else: agent=True
    optimise(optimised.get(),['statVal["'+i[0].get()+'"]'+i[1].get()+i[2].get() for i in constraints],agent=agent,mode=aim.get)

optimiseButton = Button(main,text='Run',command=runOptimise,bg='blue',fg='white').grid(row=10,column=0)

def removeConstraint():
    global constraints
    global currConstraint
    if len(constraints)>0:
        constraints.pop(-1)
        for i in main.grid_slaves():
            if int(i.grid_info()["row"])==currConstraint-1 and int(i.grid_info()["column"])>0:
                i.grid_forget()
        currConstraint-=1

removeButton = Button(main,text='Remove Constraint',command=removeConstraint).grid(row=5,column=0)

mainloop()
