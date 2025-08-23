import itertools
import re

innateBizarre = 0 #b
innateDreaded = 2+2+4 #dr
innateRespectable = 0 #r
innateMithridacy = 7 #m
innateArtisan = 7 #a
innateGlasswork = 7 #g
innateChess = 7 #c
innateAnatomy = 7 #ma
innateToxicology = 7+1 #k
innateShapeling = 7 #sa
innateZeefaring = 7 #z
innateCthonosophy = 6 #ct
innateWatchful = 30 #wa
innateDangerous = 36+1+5 #da
innateShadowy = 30+5 #sh
innatePersuasive = 30 #p
#wo su sc n

equipmentFile = open('equipmentFile.txt', 'r')

def statText(text):
    req = re.search('"(.+?)"', text)
    equ = re.search('([a-z]+)', text)
    if req: return req.group(1)
    else: return equ.group(1)

def typeAppend(equipment):
    r = equipment[1]+'s'
    try:
        eval(r).append(equipment)
    except:
        print(equipment)

def statIs(equipment, stat):
    if equipment =='innate':
        return {'b':innateBizarre, 'dr':innateDreaded, 'r':innateRespectable, 'm':innateMithridacy, 'a':innateArtisan, 'g':innateGlasswork, 'c':innateChess, 'ma':innateAnatomy, 'k':innateToxicology,
                'sa':innateShapeling,'p':innatePersuasive,'wa':innateWatchful,'da':innateDangerous,'sh':innateShadowy,'z':innateZeefaring,'ct':innateCthonosophy, 'wo':0,'su':0,'sc':0,'n':0}[stat]
    for i in equipment[2:]:
        if stat == statText(i):
            return int(i.split(stat)[1])
        if statText(i) not in ['b', 'dr', 'r', 'm', 'a', 'g', 'c', 'ma', 'k', 'sa', 'wa','da','sh','p','wo','sc','su','n', 'z','ct']:
            print('ERROR IN '+equipment[0])
            return(False)
    return 0

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

#subjectTo of the form ['statVal["r"]>=7', 'statVal["b"]==0']
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
    hats=[['Empty', 'hat']]
    clothings=[['Empty', 'clothing']]
    gloves=[['Empty', 'glove']]
    weapons=[['Empty', 'weapon']]
    boots=[['Empty', 'boot']]
    companions=[['Empty', 'companion']]
    tools=[['Empty', 'tool']]
    treasures=[['Empty', 'treasure']]
    affiliations=[['Empty', 'affiliation']]
    transports=[['Empty', 'transport']]
    homeComforts=[['Empty', 'homeComfort']]
    adornments=[['Empty', 'adornment']]
    crews=[['Empty', 'crew']]
    luggages=[['Empty', 'luggage']]
    for line in equipmentFile:
        equipment = eval(line)
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
                currentBest = [statVal[stat]]+[j[0] for j in fit]
        elif mode=='minimum':
            if all([eval(j) for j in subjectTo]) and statVal[stat]<currentBest[0]:
                currentBest = [statVal[stat]]+[j[0] for j in fit]
    print(currentBest)

###out of date, will not work
def filterOut2(slot, filterBy, sortBy1, sortBy2):
    filterVals = []
    for i in slot:
        if [statIs(i, j) for j in filterBy] not in filterVals:
            filterVals.append([statIs(i, j) for j in filterBy])
    slot2 = [max([i for i in slot if [statIs(i, k) for k in filterBy]==j], key=lambda i: statIs(i, sortBy1)+statIs(i, sortBy2)) for j in filterVals]
    return slot2

#subjectTo of the form ['statVal[r]>=7', 'statVal[b]==0']
def maximiseSum(stat1, stat2, subjectTo):
    global hats
    global clothings
    global gloves
    global weapons
    global boots
    global companions
    global treasures
    global affiliations
    global transports
    global homeComforts
    global statVal
    relevantStats = [stat1, stat2]
    for i in subjectTo:
        relevantStats.append(statText(i))
    lookingFor = ['>', '>']+['<' if '<' in i else '>' if '>' in i else '==' for i in subjectTo]
    currentBest=[0]
    hats=[['Empty', 'hat']]
    clothings=[['Empty', 'clothing']]
    gloves=[['Empty', 'glove']]
    weapons=[['Empty', 'weapon']]
    boots=[['Empty', 'boot']]
    companions=[['Empty', 'companion']]
    treasures=[['Empty', 'treasure']]
    affiliations=[['Empty', 'affiliation']]
    transports=[['Empty', 'transport']]
    homeComforts=[['Empty', 'homeComfort']]
    for line in equipmentFile:
        equipment = eval(line)
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
    hats = filterOut2(hats, relevantStats[2:], stat1, stat2)
    clothings = filterOut2(clothings, relevantStats[2:], stat1, stat2)
    gloves = filterOut2(gloves, relevantStats[2:], stat1, stat2)
    weapons = filterOut2(weapons, relevantStats[2:], stat1, stat2)
    boots = filterOut2(boots,relevantStats[2:] , stat1, stat2)
    companions = filterOut2(companions, relevantStats[2:], stat1, stat2)
    treasures = filterout2(treasures, relevantStats[2:], stat1, stat2)
    affiliations = filterOut2(affiliations,relevantStats[2:] , stat1, stat2)
    transports = filterOut2(transports, relevantStats[2:], stat1, stat2)
    homeComforts = filterOut2(homeComforts, relevantStats[2:], stat1, stat2)
    print(str(len(hats)*len(clothings)*len(gloves)*len(weapons)*len(boots)*len(companions)*len(affiliations)*len(transports)*len(homeComforts)))
    for hat in hats:
        for clothing in clothings:
            for glove in gloves:
                for weapon in weapons:
                    for boot in boots:
                        for companion in companions:
                            for treasure in treasures:
                                for affiliation in affiliations:
                                    for transport in transports:
                                        for homeComfort in homeComforts:
                                            for adornment in adornments:
                                                for crew in crews:
                                                    statVal={}
                                                    for i in relevantStats:
                                                        statVal[i] = statIs(hat, i)+statIs(clothing, i)+statIs(glove, i)+statIs(weapon, i)+statIs(boot, i)+statIs(companion, i)+statIs(treasure, i)+statIs(affiliation, i)+statIs(transport, i)+statIs(homeComfort, i)+statIs('innate', i)
                                                    if all([eval(j) for j in subjectTo]) and statVal[stat1]+statVal[stat2]>currentBest[0]:
                                                        currentBest = [statVal[stat1]+statVal[stat2], hat[0], clothing[0], glove[0], weapon[0], boot[0], companion[0], treasure[0], affiliation[0], transport[0], homeComfort[0]]
        print(str(hats.index(hat)+1)+'/'+str(len(hats))+' hats')
    print(currentBest)

def dominated(equipment1, equipment2):
    if equipment1==equipment2:
        return False
    elif all([statIs(equipment1, k)>=statIs(equipment2, k) for k in ['wa','p','da','sh']]):
        return equipment2
    elif all([statIs(equipment2, k)>=statIs(equipment1, k) for k in ['wa','p','da','sh']]):
        return equipment1
    return False

def filterOutMaximin(slot, filterBy):
    for j in slot:
        for i in slot:
            loser=dominated(j, i)
            if loser!=False:
                try:
                    slot.remove(loser)
                except:
                    pass
    return slot

def maximin(subjectTo):
    global hats
    global clothings
    global gloves
    global weapons
    global boots
    global companions
    global treasures
    global affiliations
    global transports
    global homeComforts
    global statVal
    relevantStats = ['wa', 'p', 'da', 'sh']
    for i in subjectTo:
        relevantStats.append(statText(i))
    lookingFor = ['>', '>', '>', '>']+['<' if '<' in i else '>' if '>' in i else '==' for i in subjectTo]
    currentBest=[0]
    hats=[['Empty', 'hat']]
    clothings=[['Empty', 'clothing']]
    gloves=[['Empty', 'glove']]
    weapons=[['Empty', 'weapon']]
    boots=[['Empty', 'boot']]
    companions=[['Empty', 'companion']]
    treasures=[['Empty', 'treasure']]
    affiliations=[['Empty', 'affiliation']]
    transports=[['Empty', 'transport']]
    homeComforts=[['Empty', 'homeComfort']]
    for line in equipmentFile:
        equipment = eval(line)
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
    hats = filterOutMaximin(hats, relevantStats[4:])
    clothings = filterOutMaximin(clothings, relevantStats[4:])
    gloves = filterOutMaximin(gloves, relevantStats[4:])
    weapons = filterOutMaximin(weapons, relevantStats[4:])
    boots = filterOutMaximin(boots,relevantStats[4:])
    companions = filterOutMaximin(companions, relevantStats[4:])
    treasures = filterOutMaximin(treasures, relevantStats[4:])
    affiliations = filterOutMaximin(affiliations,relevantStats[4:])
    transports = filterOutMaximin(transports, relevantStats[4:])
    homeComforts = filterOutMaximin(homeComforts, relevantStats[4:])
    print(str(len(hats)*len(clothings)*len(gloves)*len(weapons)*len(boots)*len(companions)*len(affiliations)*len(transports)*len(homeComforts)))
    for hat in hats:
        for clothing in clothings:
            for glove in gloves:
                for weapon in weapons:
                    for boot in boots:
                        for companion in companions:
                            for treasure in treasures:
                                for affiliation in affiliations:
                                    for transport in transports:
                                        for homeComfort in homeComforts:
                                            statVal={}
                                            for i in relevantStats:
                                                statVal[i] = statIs(hat, i)+statIs(clothing, i)+statIs(glove, i)+statIs(weapon, i)+statIs(boot, i)+statIs(companion, i)+statIs(treasure, i)+statIs(affiliation, i)+statIs(transport, i)+statIs(homeComfort, i)+statIs('innate', i)
                                            if all([eval(j) for j in subjectTo]) and min(statVal['wa'],statVal['p'],statVal['da'],statVal['sh'])>currentBest[0]:
                                                currentBest = [min(statVal['wa'],statVal['p'],statVal['da'],statVal['sh']), hat[0], clothing[0], glove[0], weapon[0], boot[0], companion[0], treasure[0], affiliation[0], transport[0], homeComfort[0]]
        print(str(hats.index(hat)+1)+'/'+str(len(hats))+' hats')
    print(currentBest)
