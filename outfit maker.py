import itertools
import re
from lxml import etree

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
innateWatchful = 30
innateDangerous = 36+1+5
innateShadowy = 30+5
innatePersuasive = 30

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

def filterOut(slot, filterBy, sortBy, mode='maximum'):
    filterVals = []
    for i in slot:
        if [statIs(i, j) for j in filterBy] not in filterVals:
            filterVals.append([statIs(i, j) for j in filterBy])
    if mode=='maximum':
        slot2 = [max([i for i in slot if [statIs(i, k) for k in filterBy]==j], key=lambda i: statIs(i, sortBy)) for j in filterVals]
    elif mode=='minimum':
        slot2 = [min([i for i in slot if [statIs(i, k) for k in filterBy]==j], key=lambda i: statIs(i, sortBy)) for j in filterVals]
    return slot2

#subjectTo of the form ['statVal["respectable"]>=7', 'statVal["bizarre"]==0']
def optimise(stat, subjectTo, mode='maximum'):
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
    equipments = [hats, clothings, adornments, gloves, weapons, boots, luggages, companions, treasures, tools, affiliations, transports, homeComforts, crews]
    for i in range(0,len(equipments)):
        equipments[i]=filterOut(equipments[i], relevantStats[1:], stat, mode=mode)
    outfits=[i for i in itertools.product(*equipments)]
    print(len(outfits))
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
    print(currentBest)
