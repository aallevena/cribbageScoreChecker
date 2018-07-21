#Cribbage Score Checker
#Rewrite this with sets later. For now I only have list syntax
from random import randint
import itertools
#Create Deck

deckNumbers=['A','2','3','4','5','6','7','8','9','T','J','Q','K']
deckSuit = ['S','C','D','H']

deck=list()

for num in deckNumbers:
    for suit in deckSuit:
        deck.append(num+suit)

#tool to search for an item in a list. 
def search(list, itemToFind):
    for item in list: 
        if(item==itemToFind):
            return True
    return False

#Returns a number for the number Cards
def getNumber(x): 
    return {
        'A': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T':10,
        'J':10,
        'Q':10,
        'K':10,
    }[x]

#Check score, given a list of cards, finds the best score
def checkScore(cards, flopCard):
    score=0
    #check for knobs
    #first get suit of flopcard
    flopSuit=flopCard[1]    
    knobsScore=0
    for card in cards:
        if card[1]==flopSuit and card[0]=='J':
            knobsScore=1            

    #check for flush
    flushScore=0
    flushSuit=cards[0][1]

    isFlush=True
    for card in cards:
        if card[1] != flushSuit:
            isFlush=False
    
    if isFlush:
        flushScore+=4        
        if(flopCard[1]==flushSuit):
            flushScore+=1

    #check for pairs
    pairList= list()
    fullCards=list()
    for card in cards:
        fullCards.append(card)
    fullCards.append(flopCard)
    #Inefficent to compare against self
    pairScore=0
    for card1 in fullCards:
        for card2 in fullCards:
            #if not the same card, AND not already found as a pair(7S,7H is same as 7H,7S), then add it and increment score. 
            temp = list()
            temp.append(card1)
            temp.append(card2)
            temp.sort()

            if card1 != card2 and card1[0]==card2[0] and not search(pairList,temp[0]+','+temp[1]):
                pairList.append(temp[0]+','+temp[1])
                pairScore+=2
        
    #Create full list of all possiblilities
    possibleList=list()
    
    for i in range(len(fullCards)):
        possibleList+=list(itertools.combinations(fullCards,i+1))

    #check for 15s

    #Now look through the list and find any combination that adds up to 15. 
    fifteenList=list()
    for iSet in possibleList:
        runningCount = 0 
        for jCard in iSet: 
            runningCount+= getNumber(jCard[0])
        #print(i, runningCount)
        if runningCount==15:
            fifteenList.append(iSet)
    
    fifteenScore=0
    for i in fifteenList:
        fifteenScore+=2

    #check for runs
    runList=list()
    runScore=0
    for iSet in possibleList:
        runLength=0
        maxRun=0
        
        
        #Iterate through all of the options, if the highest count is greater than 3 then record the set
        for cardNumber in deckNumbers:
            #find the current card, if we find it then increment the runLength. If not reset to 0. 
            cardFound=False
            for jCard in iSet: 
                if(jCard[0]==cardNumber):
                    cardFound=True
            if cardFound==True:
                runLength+=1
                if runLength >= maxRun: 
                    maxRun=runLength
            elif cardFound==False: runLength=0
            
        if maxRun >=3 and len(iSet)==maxRun: 
            

            runList.append(iSet)
            #runScore+=maxRun
        #This only could all of the runs, even sub runs. We can fix by doing a set difference. 
        #If a set completely matches then remove it. 
        duplicateRunSet=set()
        for i in runList:
            for j in runList:
                if i!=j:
                    if len(set(i).difference(set(j)))==0:
                        #print('Set A',i,'SetB',j)
                        runList.remove(i)
            
    for i in runList:
        runScore+=len(i)   
        
    #Print out the inputs and results
    score= knobsScore+flushScore+pairScore+fifteenScore+runScore
    if score > 15:
        print("The hand cards are", cards, " and the flop is", flopCard)
        print("This hand has", knobsScore, "points from Knobs and", flushScore, "points from a flush")
        print("There are ",pairScore/2, " pairs. They are",pairList)
        print("There are ",fifteenScore/2, "15s. They are",fifteenList)
        print("There are ",runScore,"points from runs. They are",runList)
        
        print("The total score is",score)
        print('')
    
    return score


#test the score
print(deck[randint(0,len(deck)-1)])

#checkScore(hand,'9S')
#checkScore(hand,'AC')
#deck.sort()
#for card in deck:
 #   print(card)

#Next step is to take the 6 cards given and determine the best hand to keep. 
hand=['AS','8S','7S','JS','9S','QC']

#First remove the 6 cards you have from the deck: 
for card in hand:
    print(card)
    deck.remove(card)

#For each permutation of 4 cards out of the 6, figure out the best possible personal hand: 
#Now run the algorithm to see the average score
personalHandOptions=list(itertools.combinations(hand,4))

totalHandOptions = list(list())
for handOption in personalHandOptions:
    #Create a 4 card hand and a 2 card hand
    totalHandOptions.append([handOption,list(set(hand).difference(set(handOption)))])

cribHandScores=list(list())
notCribHandScores=list(list())
averageScores=list(list())
for handOption in totalHandOptions:
    runningHandTotal=0
    iterations=0
    for flop in deck: 
        tempDeck=deck[:]
        tempDeck.remove(flop)
        
        #Craft the crib hand: 
        cribHand=list(handOption[1])
        
        
        
        cribCount=len(cribHand)
        for i in range(4-cribCount):
            #print('len of tempDeck',len(tempDeck))
            #print('len of Deck',len(deck))
            tempCard=tempDeck[randint(0,len(tempDeck)-1)]
            tempDeck.remove(tempCard)
            cribHand.append(tempCard)
            i+=1
        #print(len(cribHand))
        
        #print(type(cribHand))
        #print(type(flop))
        #print(handOption)
        #My Crib
        #checkScore(handOption[0],flop)
        #checkScore(cribHand,flop)
        
        tempPersonalHandScore= checkScore(handOption[0],flop)
        
        cribHandScore=checkScore(cribHand,flop)
        runningHandTotal+=tempPersonalHandScore
        iterations+=1
        cribHandScores.append([handOption[0],flop,tempPersonalHandScore,cribHand,cribHandScore,tempPersonalHandScore+cribHandScore])

        #Not My Crib
        notCribHandScores.append([handOption[0],flop,tempPersonalHandScore,cribHand,cribHandScore,tempPersonalHandScore-cribHandScore])
    averageScores.append([handOption[0],runningHandTotal/iterations])

averageScores.sort(key=lambda x: x[1])
cribHandScores.sort(key=lambda x: x[2])
print('The best hand with my crib is',cribHandScores[len(cribHandScores)-1])
print('The best hand on average is',averageScores[len(averageScores)-1])




#for card in deck: 
    #handOptions.append([card, checkScore(hand,card)])

#handOptions.sort(key=lambda x: x[1])
#print('The best hand option is',handOptions[0])