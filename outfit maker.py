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
    if len(currentBest)==1:
        tkinter.messagebox.showerror(title='Error', message='Error: no outfit fitting the constraints given could be found')
    elif not agent: tkinter.messagebox.showinfo("Results",  'Total: '+str(currentBest[0])+'\nHat: '+str(currentBest[1])+'\nClothing: '+str(currentBest[2])+'\nAdornment: '+str(currentBest[3])+'\nGloves: '+str(currentBest[4])+'\nWeapon: '+str(currentBest[5])+'\nBoots: '+str(currentBest[6])+'\nLuggage: '+str(currentBest[7])+'\nCompanion: '+str(currentBest[8])+'\nTreasure: '+str(currentBest[9])+'\nTool of the Trade: '+str(currentBest[10])+'\nAffiliation: '+str(currentBest[11])+'\nTransport: '+str(currentBest[12])+'\nHome Comfort: '+str(currentBest[13])+'\nCrew: '+str(currentBest[14]))
    else: tkinter.messagebox.showinfo("Results",  'Total: '+str(currentBest[0])+'\nHat: '+str(currentBest[1])+'\nClothing: '+str(currentBest[2])+'\nAdornment: '+str(currentBest[3])+'\nGloves: '+str(

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
    optimise(optimised.get(),['statVal["'+i[0].get()+'"]'+i[1].get()+i[2].get() for i in constraints],agent=agent,mode=aim.get())

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

def addStatEntry(parent,row,column,stat,equipment,length):
    Var = StringVar(parent)
    Var.set(equipment.get(stat,''))
    Box = Entry(parent,textvariable=Var,width=length).grid(row=row,column=column,columnspan=max(2*(1-column),1))
    return Var

def removeEquipment(row,parent):
    global equipVariables
    for i in parent.grid_slaves():
        if int(i.grid_info()["row"])==row:
            i.grid_forget()
    equipVariables.pop(row-1)

def addRemoveButton(row,parent):
    global equipVariables
    removeButton=Button(parent,text='X')
    removeButton.config(command=lambda: removeEquipment(row,parent))
    removeButton.grid(row=row,column=26)

def addBlankEquipment(parent):
    global equipVariables
    newRow = max([int(i.grid_info()["row"]) for i in parent.grid_slaves()])
    for i in parent.grid_slaves():
        if int(i.grid_info()["row"])==newRow:
            i.grid(row=newRow+1)
    i=etree.Element("root")
    equipVariables.append([])
    equipVariables[-1].append(addStatEntry(parent,newRow,0,'dummy',i,length=50))
    equipVariables[-1].append(addStatEntry(parent,newRow,2,'dummy',i,length=8))
    equipVariables[-1].append(addStatEntry(parent,newRow,3,'dummy',i,length=9))
    equipVariables[-1].append(addStatEntry(parent,newRow,4,'dummy',i,length=7))
    equipVariables[-1].append(addStatEntry(parent,newRow,5,'dummy',i,length=10))
    equipVariables[-1].append(addStatEntry(parent,newRow,6,'dummy',i,length=11))
    equipVariables[-1].append(addStatEntry(parent,newRow,7,'dummy',i,length=8))
    equipVariables[-1].append(addStatEntry(parent,newRow,8,'dummy',i,length=8))
    equipVariables[-1].append(addStatEntry(parent,newRow,9,'dummy',i,length=6))
    equipVariables[-1].append(addStatEntry(parent,newRow,10,'dummy',i,length=7))
    equipVariables[-1].append(addStatEntry(parent,newRow,11,'dummy',i,length=9))
    equipVariables[-1].append(addStatEntry(parent,newRow,12,'dummy',i,length=10))
    equipVariables[-1].append(addStatEntry(parent,newRow,13,'dummy',i,length=10))
    equipVariables[-1].append(addStatEntry(parent,newRow,14,'dummy',i,length=10))
    equipVariables[-1].append(addStatEntry(parent,newRow,15,'dummy',i,length=5))
    equipVariables[-1].append(addStatEntry(parent,newRow,16,'dummy',i,length=9))
    equipVariables[-1].append(addStatEntry(parent,newRow,17,'dummy',i,length=14))
    equipVariables[-1].append(addStatEntry(parent,newRow,18,'dummy',i,length=7))
    equipVariables[-1].append(addStatEntry(parent,newRow,19,'dummy',i,length=10))
    equipVariables[-1].append(addStatEntry(parent,newRow,20,'dummy',i,length=9))
    equipVariables[-1].append(addStatEntry(parent,newRow,21,'dummy',i,length=12))
    equipVariables[-1].append(addStatEntry(parent,newRow,22,'dummy',i,length=8))
    equipVariables[-1].append(addStatEntry(parent,newRow,23,'dummy',i,length=13))
    equipVariables[-1].append(addStatEntry(parent,newRow,24,'dummy',i,length=12))
    Var = BooleanVar(parent)
    Var.set(False)
    Box = Checkbutton(parent,variable=Var).grid(row=newRow,column=25)
    equipVariables[-1].append(Var)
    addRemoveButton(newRow,parent)

def generateGrid(parent,slot):
    global equipmentFile
    global equipVariables
    j=1
    equipVariables=[]
    for i in parent.grid_slaves():
        if int(i.grid_info()["row"])>0:
            i.grid_forget()
    for i in equipmentFile.findall('.//equipment[@type="'+slot+'"]'):
        equipVariables.append([])
        equipVariables[-1].append(addStatEntry(parent,j,0,'name',i,length=50))
        equipVariables[-1].append(addStatEntry(parent,j,2,'watchful',i,length=8))
        equipVariables[-1].append(addStatEntry(parent,j,3,'dangerous',i,length=9))
        equipVariables[-1].append(addStatEntry(parent,j,4,'shadowy',i,length=7))
        equipVariables[-1].append(addStatEntry(parent,j,5,'persuasive',i,length=10))
        equipVariables[-1].append(addStatEntry(parent,j,6,'respectable',i,length=11))
        equipVariables[-1].append(addStatEntry(parent,j,7,'dreaded',i,length=8))
        equipVariables[-1].append(addStatEntry(parent,j,8,'bizarre',i,length=8))
        equipVariables[-1].append(addStatEntry(parent,j,9,'wounds',i,length=6))
        equipVariables[-1].append(addStatEntry(parent,j,10,'scandal',i,length=7))
        equipVariables[-1].append(addStatEntry(parent,j,11,'suspicion',i,length=9))
        equipVariables[-1].append(addStatEntry(parent,j,12,'nightmares',i,length=10))
        equipVariables[-1].append(addStatEntry(parent,j,13,'katalepticToxicology',i,length=20))
        equipVariables[-1].append(addStatEntry(parent,j,14,'anatomy',i,length=10))
        equipVariables[-1].append(addStatEntry(parent,j,15,'chess',i,length=5))
        equipVariables[-1].append(addStatEntry(parent,j,16,'glasswork',i,length=9))
        equipVariables[-1].append(addStatEntry(parent,j,17,'shapelingArts',i,length=14))
        equipVariables[-1].append(addStatEntry(parent,j,18,'artisan',i,length=7))
        equipVariables[-1].append(addStatEntry(parent,j,19,'mithridacy',i,length=10))
        equipVariables[-1].append(addStatEntry(parent,j,20,'zeefaring',i,length=9))
        equipVariables[-1].append(addStatEntry(parent,j,21,'chthonosophy',i,length=12))
        equipVariables[-1].append(addStatEntry(parent,j,22,'inerrant',i,length=8))
        equipVariables[-1].append(addStatEntry(parent,j,23,'insubstantial',i,length=13))
        equipVariables[-1].append(addStatEntry(parent,j,24,'neathproofed',i,length=12))
        Var = BooleanVar(parent)
        Var.set(i.get('agentAvail'))
        Box = Checkbutton(parent,variable=Var).grid(row=j,column=25)
        equipVariables[-1].append(Var)
        addRemoveButton(j,parent)
        j+=1
    newRow = max([int(i.grid_info()["row"]) for i in parent.grid_slaves()])
    Button(parent,text='Add new equipment',command=lambda: addBlankEquipment(parent)).grid(row=newRow+1,column=1)

dummyVar = StringVar(main)
dummyVar.set('dummy')
equipVariables=[[dummyVar]*22]

def saveEquipment(slot):
    global equipmentFile
    global equipVariables
    equipElements = equipmentFile.findall('.//equipment[@type="'+slot+'"]')
    root=equipmentFile.getroot()
    for i in equipElements: root.remove(i)
    for j in equipVariables:
        equipment = etree.SubElement(root, "equipment")
        equipment.set('name',j[0].get())
        equipment.set('type',slot)
        if j[1].get()!='': equipment.set('watchful',j[1].get())
        if j[2].get()!='': equipment.set('dangerous',j[2].get())
        if j[3].get()!='': equipment.set('shadowy',j[3].get())
        if j[4].get()!='': equipment.set('persuasive',j[4].get())
        if j[5].get()!='': equipment.set('respectable',j[5].get())
        if j[6].get()!='': equipment.set('dreaded',j[6].get())
        if j[7].get()!='': equipment.set('bizarre',j[7].get())
        if j[8].get()!='': equipment.set('wounds',j[8].get())
        if j[9].get()!='': equipment.set('scandal',j[9].get())
        if j[10].get()!='': equipment.set('suspicion',j[10].get())
        if j[11].get()!='': equipment.set('nightmares',j[11].get())
        if j[12].get()!='': equipment.set('katalepticToxicology',j[12].get())
        if j[13].get()!='': equipment.set('anatomy',j[13].get())
        if j[14].get()!='': equipment.set('chess',j[14].get())
        if j[15].get()!='': equipment.set('glasswork',j[15].get())
        if j[16].get()!='': equipment.set('shapelingArts',j[16].get())
        if j[17].get()!='': equipment.set('artisan',j[17].get())
        if j[18].get()!='': equipment.set('mithridacy',j[18].get())
        if j[19].get()!='': equipment.set('zeefaring',j[19].get())
        if j[20].get()!='': equipment.set('chthonosophy',j[20].get())
        if j[20].get()!='': equipment.set('inerrant',j[21].get())
        if j[20].get()!='': equipment.set('insubstantial',j[22].get())
        if j[20].get()!='': equipment.set('neathproofed',j[23].get())
        equipment.set('agentAvail',lower(str(j[24].get())))
    with open('equipmentFile.xml', 'wb') as doc: doc.write(etree.tostring(equipmentFile, pretty_print = True))

def equipmentConfig():
    global equipmentFile
    global equipVariables
    popup = Toplevel(main)
    popup.title('Equipment')
    mainFrame = Frame(popup)
    mainFrame.pack(fill=BOTH, expand=1)
    scrollbar = Scrollbar(mainFrame, orient='vertical')
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar2 = Scrollbar(mainFrame, orient='horizontal')
    scrollbar2.pack(side=BOTTOM, fill=X)
    canvas = Canvas(mainFrame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.config(command=canvas.yview)
    scrollbar2.config(command=canvas.xview)
    canvas.configure(yscrollcommand=scrollbar.set,xscrollcommand=scrollbar2.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    innerFrame = Frame(canvas, width = 1000, height = 100)
    canvas.create_window((0, 0), window=innerFrame, anchor="nw")
    wLabel = Label(innerFrame,text='Watchful',bg='dark grey',fg='white').grid(row=0,column=2,sticky='nsew')
    dLabel = Label(innerFrame,text='Dangerous',bg='dark grey',fg='white').grid(row=0,column=3,sticky='nsew')
    sLabel = Label(innerFrame,text='Shadowy',bg='dark grey',fg='white').grid(row=0,column=4,sticky='nsew')
    pLabel = Label(innerFrame,text='Persuasive',bg='dark grey',fg='white').grid(row=0,column=5,sticky='nsew')
    rLabel = Label(innerFrame,text='Respectable',bg='dark grey',fg='white').grid(row=0,column=6,sticky='nsew')
    dLabel = Label(innerFrame,text='Dreaded',bg='dark grey',fg='white').grid(row=0,column=7,sticky='nsew')
    bLabel = Label(innerFrame,text='Bizarre',bg='dark grey',fg='white').grid(row=0,column=8,sticky='nsew')
    woLabel = Label(innerFrame,text='Wounds',bg='dark grey',fg='white').grid(row=0,column=9,sticky='nsew')
    scLabel = Label(innerFrame,text='Scandal',bg='dark grey',fg='white').grid(row=0,column=10,sticky='nsew')
    suLabel = Label(innerFrame,text='Suspicion',bg='dark grey',fg='white').grid(row=0,column=11,sticky='nsew')
    nLabel = Label(innerFrame,text='Nightmares',bg='dark grey',fg='white').grid(row=0,column=12,sticky='nsew')
    tLabel = Label(innerFrame,text='Toxicology',bg='dark grey',fg='white').grid(row=0,column=13,sticky='nsew')
    aLabel = Label(innerFrame,text='Anatomy',bg='dark grey',fg='white').grid(row=0,column=14,sticky='nsew')
    cLabel = Label(innerFrame,text='Chess',bg='dark grey',fg='white').grid(row=0,column=15,sticky='nsew')
    gLabel = Label(innerFrame,text='Glasswork',bg='dark grey',fg='white').grid(row=0,column=16,sticky='nsew')
    saLabel = Label(innerFrame,text='Shapeling Arts',bg='dark grey',fg='white').grid(row=0,column=17,sticky='nsew')
    aLabel = Label(innerFrame,text='Artisan',bg='dark grey',fg='white').grid(row=0,column=18,sticky='nsew')
    mLabel = Label(innerFrame,text='Mithridacy',bg='dark grey',fg='white').grid(row=0,column=19,sticky='nsew')
    zLabel = Label(innerFrame,text='Zeefaring',bg='dark grey',fg='white').grid(row=0,column=20,sticky='nsew')
    chLabel = Label(innerFrame,text='Chthonosophy',bg='dark grey',fg='white').grid(row=0,column=21,sticky='nsew')
    irLabel = Label(innerFrame,text='Inerrant',bg='dark grey',fg='white').grid(row=0,column=22,sticky='nsew')
    isLabel = Label(innerFrame,text='Insubstantial',bg='dark grey',fg='white').grid(row=0,column=23,sticky='nsew')
    npLabel = Label(innerFrame,text='Neathproofed',bg='dark grey',fg='white').grid(row=0,column=24,sticky='nsew')
    agLabel = Label(innerFrame,text='Agents?',bg='dark grey',fg='white').grid(row=0,column=25,sticky='nsew')
    slots = ['hat','clothing','glove','weapon','boots','companion','treasure','tool','affiliation','transport','homeComfort','crew','adornment','luggage']
    slotVar = StringVar(popup)
    slotVar.set('hat')
    slotMenu = OptionMenu(innerFrame,slotVar,*slots,command=lambda a: generateGrid(innerFrame,slotVar.get())).grid(row=0,column=0)
    generateGrid(innerFrame,slotVar.get())
    saveButton = Button(innerFrame,text='Save',command=lambda: saveEquipment(slotVar.get())).grid(row=0,column=1)
    #print([[i.get() for i in j] for j in variables])

removeButton = Button(main,text='Equipment',command=equipmentConfig).grid(row=0,column=3)

mainloop()


