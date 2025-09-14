import itertools
import re
from lxml import etree
import operator
from math import prod
import tqdm
import time

def setup(person='player'):
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
    if person=='player':
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
        innateCthonosophy = 6
        innateWatchful = 230
        innateDangerous = 236+1+5
        innateShadowy = 230+5
        innatePersuasive = 230
    elif person=='captain':
        innateWatchful=50
        innateDangerous=50
        innateZeefaring=3
    elif person=='breaker':
        innateWatchful=50
        innateDangerous=70
        innateZeefaring=1
    elif person=='bathyphile':
        innateWatchful=50
        innateShadowy=50
        innateDangerous=20
        innateZeefaring=5
    elif person=='mondaine':
        innateShadowy=50
        innatePersuasive=50
    elif person=='mole':
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
                'glasswork':innateGlasswork, 'chess':innateChess, 'anatomy':innateAnatomy, 'kataleptictoxicology':innateToxicology,
                'shapelingarts':innateShapeling,'persuasive':innatePersuasive,'watchful':innateWatchful,'dangerous':innateDangerous,'shadowy':innateShadowy,
                'zeefaring':innateZeefaring,'chthonosophy':innateCthonosophy, 'wounds':0,'suspicion':0,'scandal':0,'nightmares':0}[stat]
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
        currentBest=[200]
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
    for fit in tqdm.gui.tqdm(outfits,total=prod([len(i) for i in equipments])):
        statVal={}
        for i in relevantStats:
            statVal[i] = sum([statIs(j, i) for j in fit])+statIs('innate', i)
        if mode=='maximum':
            if all([eval(j) for j in subjectTo]) and statVal[stat]>currentBest[0]:
                currentBest = [statVal[stat]]+[j.get('name') for j in fit]
        elif mode=='minimum':
            if all([eval(j) for j in subjectTo]) and statVal[stat]<currentBest[0]:
                currentBest = [statVal[stat]]+[j.get('name') for j in fit]
    print(currentBest)
