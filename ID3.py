#@author Avi Gupta
import math
import random
from time import time
filename = "congress.txt"
trainingProb = 0.01 #proportion of examples going to training set
testingProb = 1-trainingProb
all = [] #all data, the union of trainingSet and testingSet
trainingSet = []
testingSet = []

class Node:
    def __init__(self,label):
        self.label = label
        self.children = {}

    def addChild(self, value, child):
        self.children[value]= child

    def isLeaf(self):
        return len(self.children)==0

def readFile():
    file = open(filename, "r")
    global labels
    labels = (file.readline().strip().split(","))
    labels.pop(0)

    for line in file:
        instance = (line.strip().split(","))
        all.append(instance)
        if random.random()<=trainingProb: #randomly assigning data to training or testing based on user-specified proportions
            trainingSet.append(instance)
        else:
            testingSet.append(instance)

def outcomesForAttribute(attribute, data): #returns all the outcomes for a given attribute number
    return [instance[attribute] for instance in data]

#Talked to Hansen Lian about many of these ideas, but all code is my own
def entropy(data):
    outcomes = outcomesForAttribute(0,data) #could include yes, no, etc. multiple times - all  outcomes
    ent = 0

    possibleOutcomes = set(outcomes) #like yes and no--all possible distinct outcomes
    for outcome in possibleOutcomes:
        x = outcomes.count(outcome)
        #counting how many instances of each possible income there are in the possible outcome
        p = x*1.0/len(data) #calculating the outcome probability
        ent += -(p*math.log(p,2)) #adding to entropy
    return ent

def informationGain(data, a):
    gain = entropy(data) #setting initial gain to entropy as per formula
    for i in range(0,len(labels)):
        if labels[i]==a:
            attributeNum = i+1 #the index of the attribute we're looking for in each instance
            break
    possibleAttributes = set(outcomesForAttribute(attributeNum, data))  #all possible distinct outcomes
    for attribute in possibleAttributes: #loop through all possible types of this attribute
        attributeList = [instance for instance in data if instance[attributeNum] == attribute] #list of instances for each type
        gain+= -(len(attributeList)*1.0)/len(data)*entropy(attributeList)
    return gain

def id3(data, atts):
    dominantCategory = data[0][0]
    if [i[0] for i in data].count(dominantCategory) == len(data):
        #print "exiting since all data in same category"
        return Node(dominantCategory)

    if len(atts)==0:
        outcomes = [i[0] for i in data]
        print "exiting since we're out of attributes"
        return Node(max(set(outcomes), key = outcomes.count))
    #https://stackoverflow.com/questions/1518522/find-the-most-common-element-in-a-list

    possibleInfoGains = [(att, informationGain(data, att))for att in atts] #listing possible information gains by attribute
    possibleInfoGains.sort(key=lambda gain: gain[1], reverse=True) #determing which attribute offers greatests information gain
    searching_att = possibleInfoGains[0][0] #searching_att = attribute if3 searching by

    label_index = labels.index(searching_att) #index of searching_att in global labels file
    new_node = Node(searching_att)
    possibleAttributeValues = [] #possible values for a given attribute
    for instance in all: #building possibilities from all data to avoid KeyErrors
      possibleAttributeValues.append(instance[label_index+1])

    for value in set(possibleAttributeValues):
        examplesForValue = [instance for instance in data if instance[label_index+1]==value]
        #all examples that have the particular attribute value
        if len(examplesForValue)!=0: #if there are such examples
            a = atts[:] #making a copy of the attributes to remove
            a.remove(searching_att) #removing the attribute used in the search
            new_node.addChild(value, id3(examplesForValue, a))

        elif len(examplesForValue)==0:
            outcomes1 = [i[0] for i in data] #all outcome for current dataset
            new_node.addChild(value, Node(max(set(outcomes1), key=outcomes1.count)))
            #adding a child using the mode of the current outcomes (credit to Stack, see above)
    return new_node

def displayTree(node, level): #displays a tree given a node and level. Level = level of indentation
    spacer = ""
    spacer+= "   " * level #multiplying spacer by given level
    print spacer + str(node.label)
    for value in node.children:
        print spacer + "   " + value
        displayTree(node.children[value], level+2)
        #recursing down two levels to get to next question node (as opposed to answer)

def testTree(first_node,data): #assesing the accuracy of a tree given the first node
    total = 0 #total number of cases assessed
    correct = 0 #number of cases predicted correctly
    for instance in data:
        total += 1
        access_node = first_node #node whose children we're investigating
        while len(access_node.children)!=0: #while the node isn't a leaf (a leaf would be an outcome)
            att_index=labels.index(access_node.label)
            #finding the index of the attribute we're asking a question about (e.g. "outlook")
            access_node = access_node.children[instance[att_index+1]]
            #setting access node to the next node in the tree given the answer to our question
        if access_node.label == instance[0]: #if we've reached the correct outcome
            correct+=1
    print "Training on: " + str(len(trainingSet)) + " cases" #printing out our results
    print "Testing with: " + str(len(data)) + " cases"
    print "Accuracy: " + str(correct * 1.0/total)

def main(): #runs all the methods needed to generate and test a tree and print results
    start = time() #starting a timer
    readFile()
    root = id3(trainingSet, labels) #running ID3 on the trainingSet
    displayTree(root, 0) #displaying the generated ID3 tree
    testTree(root, testingSet) #testing the accuracy on the testing set
    #testTree(root, all) #used for tennis, when there isn't a testing set
    print "Time: " + str(time()-start) #stopping the timer
main()