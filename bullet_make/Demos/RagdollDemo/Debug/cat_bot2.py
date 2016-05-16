import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math as m
import os.path
import sys
import time
import random
import csv
import pickle
from savefig import save
import datetime
import pandas as pd
import subprocess as sub


NUM_INPUTS_ANN = 4
NUM_OUTPUTS_ANN = 26
POP_SIZE = 15
BIG_NUMBER = 999999999
timesteps = [20]
num_timesteps = timesteps[0]
global ID

## classes, new stuff

def MatrixCreate2(size, generations):
    return np.zeros((size, generations), dtype=float)

def MatrixRandomize(v):      #Creates Random Matrix
    rows = len(v)
    columns = len(v[0])
    for i in range(rows):
        for j in range(columns):
            v[i][j] = np.random.uniform(-1, 1)
    return v

def matrixPerturb(v, prob):
    p = np.copy(v)
    for i in range(len(v)):
        for j in range(len(v[0])):
            if prob > np.random.rand():
                p[i][j] = np.random.uniform(-1, 1);
    return p

def Send_Values_ToFile(data, filename):
    with open(filename, 'wb') as csvfile:
        testwriter = csv.writer(csvfile, delimiter = ',')
        testwriter.writerows(data)

def Send_Values_ToFile_two(data, filename):
    with open(filename, "wb") as output:
        writer = csv.writer(output, lineterminator=',')
        for val in data:
            writer.writerow([val])

Send_Values_ToFile_two(timesteps, 'timesteps.txt')

def positions():
    position_list = [[0.0, 0.0, 6.2, 1.0, 1.0, -0.5, 'blind', 'Small'], [0.0, 0.0, 6.2, 1.5, 1.5, 0.5, 'blind', 'Large'],
                    [1.5, 0.0, 5.5, 1.0, 1.0, -0.5, 'visible', 'Small'], [1.5, 0.0, 5.5, 1.5, 1.5, 0.5, 'visible', 'Large'],
                    [3.5, 0.0, 5.5, 1.5, 1.5, 0.5, 'blind', 'Large'], [3.5, 0.0, 5.5, 1.0, 1.0, -0.5, 'blind', 'Small'],
                    [5.7, 0.0, 4.2, 1.5, 1.5, 0.5, 'visible', 'Large'], [5.7, 0.0, 4.2, 1.0, 1.0, -0.5, 'visible', 'Small'],
                    [-1.5, 0.0, 5.0, 1.5, 1.5, 0.5, 'visible', 'Large'], [-1.5, 0.0, 5.0, 1.0, 1.0, -0.5, 'visible', 'Small'],
                    [-3.5, 0.0, 5.0, 1.5, 1.5, 0.5, 'blind', 'Large'], [-3.5, 0.0, 5.0, 1.0, 1.0, -0.5, 'blind', 'Small'],
                    [-5.7, 0.0, 4.2, 1.5, 1.5, 0.5, 'visible', 'Large'], [-5.7, 0.0, 4.2, 1.0, 1.0, -0.5, 'visible', 'Small']]

    training_pos = random.sample(position_list,7)

    i = xrange(len(position_list))
    test = random.sample(i, 7)

    test_index = [blah for blah in i if blah not in test]
    test_list = []
    for num in test_index:
        test_list.append(position_list[num])

    return training_pos, test_list

def run_training_CM_notinuse(population, num_timesteps, training_list):
    for individual in population:
        parent = individual.ANN
        #parent = parent.getValues()
        filename = "weights_Matrix.csv"
        Send_Values_ToFile(parent, filename)
        move_list_2 = MatrixCreate2(1, 7)
        cat_list = MatrixCreate2(1,7)
        index = 0
        for position in training_list:
            position_size = position           #Center robot should be blind to this
            Send_Values_ToFile_two(position_size, "position_size.csv")
            os.system('./AppRagdollDemo')
            mvect = open('m_vector.txt', 'r')
            mvect_list = []
            for line in mvect:
                mvect_list.append(float(line))
            move = mvect_list[num_timesteps-1] #sum(mvect_list)
            move2 = sum(mvect_list)/float(num_timesteps)

            cat = open('g_mean_vector.txt', 'r')
            categorize = []
            for line in cat:
                categorize.append( float(line) )
            cat_fit =  (sum(categorize)/float(num_timesteps))    #
            #print 'move:', move
            #print np.corrcoef(mvect_list, gvect_list)[0,1]
            #print population[i].getErrors()
            move_list_2[0][index] = move2
            cat_list[0][index] = cat_fit
            #print cat_list_2, corr_list_2
            #move_list[0][i] = sum(move_list_2[0][:])/4.0
            index = index + 1
        individual.fit =  (sum(move_list_2[0][:])/7.0) * (1.0 / (1.0 + (sum(cat_list[0][:])/7.0)))

    return population

def run_training_CM(population, num_timesteps, training_list):

    MAX_EVAL_TIME = float("inf") # Time out: max seconds you'll wait for the evaluation loop to finish
    # If something goes wrong with one of the processes you
    # created (e.g. simulation crashes, a node on the vacc goes down, etc.)
    # you may end up waiting forever for a fitness file that won't be
    # returned. Now it's disabled (set to infinity).

    newpath1 = (r'results')
    if not os.path.exists(newpath1):
        os.makedirs(newpath1)
    newpath2 = (r'positions')
    if not os.path.exists(newpath2):
        os.makedirs(newpath2)
    newpath3 = (r'weights')
    if not os.path.exists(newpath3):
        os.makedirs(newpath3)

    resultsFolder = "results/" # you may want to clear this directory before starting, e.g. by calling sub.call("rm "+resultsFolder+"*",shell=True)
    sub.call("rm "+resultsFolder+"*",shell=True)

    identifiersList = [] # list of individuals identifiers to be evaluated

    gerrorlist  =[]


    for individual in population:
        parent = individual.ANN
        #parent = parent.getValues()
        count = 1
        for training in training_list:
            identifier = str(count) +"_"+ str(individual.uid) # unique string appended to all files
            # generated by this call. Here's a progressive
            # number, could be something else.
            identifiersList.append(identifier)
            gerrorlist.append(identifier)
            

            filename = identifier+"_weights_Matrix.csv"
            Send_Values_ToFile(parent, "weights/"+filename)
            Send_Values_ToFile_two(training, "positions/"+identifier+"_position.csv")

            sub.Popen("./AppRagdollDemo %s"%identifier,shell=True)
            count = count + 1

    #for identifier in identifiersList:
    #    sub.Popen("./AppRagdollDemo %s"%identifier,shell=True)
    #print "identifiersList is"
    #print identifiersList
    #print "------------------------"
    #alreadyAnalyzed = []
    done = False

    evalStartTime = time.time()
    while not done:
        if time.time()-evalStartTime > MAX_EVAL_TIME:
            break

        # Is there any new fitness file in
        command = "ls \""+resultsFolder+"\"" #"ls "+resultsFolder;
        #print "command is: ", command

        lsOutput = sub.check_output(command, shell=True)

        if lsOutput: # if there are some files in resultsFolder...
            #print "list output not null"
            firstFileName = lsOutput.split()[0]
            if ("gerrorvector" in firstFileName):
                #print "firstFileName ", firstFileName
                #print "------------"
                thisEnvironment = int(firstFileName.split("_")[0]) # assuming that your files are in the format "IDENTIFIER_filename.something"

                thisIndividual = int(firstFileName.split("_")[1])

                for ind in population:
                    if ind.uid == thisIndividual:
                        individual = ind
                        break

                thisFile = firstFileName.split("_")[2]
                #print "thisFile is ", thisFile
                #print "----------"

                thisIdentifier = str(thisEnvironment)+"_"+str(thisIndividual)
                #print "thisIdentifier is ", thisIdentifier
                #print"------------------"

                if (thisIdentifier in gerrorlist):
                    #alreadyAnalyzed.append(thisIdentifier)

                    #result = open("/Users/np/Desktop/Bullet/bullet_make/Demos/RagdollDemo/Debug/results/"+firstFileName, 'r')
                    result = open(resultsFolder+firstFileName, 'r')

                    if "gerrorvector.txt" == thisFile:
                        errorvectlist = []
                        for line in result:
                            errorvectlist.append(float(line[0]))
                        individual.cat.append(sum(errorvectlist)/float(num_timesteps))
                        gerrorlist.remove(thisIdentifier)


                    #
                    # [Here you fetch the information you need from the file]
                    #

                    # Now we can either remove this file (you may want to move it elsewhere, instead, this is up to you)
            sub.call("rm "+resultsFolder+firstFileName,shell=True)
            #toBeAnalyzed = set(identifiersList) - set(alreadyAnalyzed)
            if (not mlist) and (not gerrorlist):
                done = True # we have done here
                #else:
                #print "gerrorlist is ", len(gerrorlist)
                #print "--------------"
                #print "mlist is ", len(mlist)
                #print "--------------"

    #time.sleep(0.5)

    if not done:
        print("> Looks like evaluation loop timed out! We don't have the results for the following individuals:")
        #print(set(identifiersList)-set(alreadyAnalyzed))
    else:
        print('> All individuals correctly evaluated!')

        #Evaluate fitness for population
        for individual in population:
            individual.fit = sum( individual.cat )/7.0

    return population

"""
def run_training_second_CM(population, POP_SIZE, num_timesteps, training_list):
    move_list = []
    new_individuals = Fill_CM(population, POP_SIZE)
    print "num new individuals =", len(new_individuals)
    for individual in new_individuals:
        parent = individual.ANN
        #parent = parent.getValues()
        filename = "weights_Matrix.csv"
        Send_Values_ToFile(parent, filename)
        move_list_2 = MatrixCreate2(1,7)
        cat_list = MatrixCreate2(1,7)
        index = 0
        for position in training_list:
            position_size = position           #Center robot should be blind to this
            Send_Values_ToFile_two(position_size, "position_size.csv")
            os.system('./AppRagdollDemo')
            mvect = open('m_vector.txt', 'r')
            mvect_list = []
            for line in mvect:
                mvect_list.append(float(line))
            move = mvect_list[num_timesteps-1] #sum(mvect_list)
            move2 = sum(mvect_list)/float(num_timesteps)

            cat = open('g_mean_vector.txt', 'r')
            categorize = []
            for line in cat:
                categorize.append( float(line) )
            cat_fit =  (sum(categorize)/float(num_timesteps))    #
            #print 'move:', move
            #print np.corrcoef(mvect_list, gvect_list)[0,1]
            #print population[i].getErrors()
            move_list_2[0][index] = move2
            cat_list[0][index] = cat_fit
            #print cat_list_2, corr_list_2
            #move_list[0][i] = sum(move_list_2[0][:])/4.0
            index = index + 1
        individual.fit =  (sum(move_list_2[0][:])/7.0) * (1.0 / (1.0 + (sum(cat_list[0][:])/7.0)))
    population = population + new_individuals
    return population
        """

def run_testing_cat(test_list, population, timestep):
    timestep_list = []
    for i in range(0, timestep):
        timestep_list.append(i)

    individual = population[len(population)-1]
    parent = individual.ANN

    print 'length of Test Objects: ', len(test_list)

    newpath = r'/Users/np/Desktop/Bullet/bullet_make/Demos/RagdollDemo/Debug/Images/cat/Individuals_'+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    newpath = r'/Users/np/Desktop/Bullet/bullet_make/Demos/RagdollDemo/Debug/Images/cat/Individuals_'+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')+'/Individuals'+str(individual.uid)+'_data_for_neurons'
    if not os.path.exists(newpath):
        os.makedirs(newpath)



    #parent = parent.getValues()
    filename = "weights_Matrix.csv"
    Send_Values_ToFile(parent, filename)
    index = 0
    for position in test_list:
        values_save = MatrixCreate2(timestep, 2)
        position_size = position
        #print position_size
        Send_Values_ToFile_two(position_size, "position_size.csv")

        os.system('./AppRagdollDemo')

        cat = open('g_mean_vector.txt', 'r')
        categorize = []
        for line in cat:
            categorize.append( float(line) )
        cat_fit = (sum(categorize)/float(num_timesteps)) / 7.0    #

        individual.categorize.append(cat_fit)

        mvect = open('mvector.txt', 'r')
        mvect_list = []
        for line in mvect:
            mvect_list.append(float(line))

        index2 = 0
        for value in categorize[:timestep]:
            values_save[index2][0] = value
            index2 = index2 + 1

        index3 = 0
        for value in mvect_list[:timestep]:
            values_save[index3][1] = value
            index3 = index3 + 1

        Send_Values_ToFile(values_save, 'Images/cat/Individuals_'+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')+'/Individuals'+str(individual.uid)+'_data_for_neurons/'+str(index)+str(individual.uid)+position[6]+position[7]+'Categorizeandmovement.txt')

        individual.guess_neurons[index] = categorize

        #print 'move:', move
        #print np.corrcoef(mvect_list, gvect_list)[0,1]
        if position[5] == 0.5:
            #if categorize[timestep-1] > 0.40 and categorize[timestep-1] < 0.60:
            if sum(categorize)/float(timestep) > 0.40 and sum(categorize)/float(timestep) < 0.60:
                individual.test = individual.test + 1 #/ float(num_timesteps)

        if position[5] == -0.5:
            #if categorize[timestep-1] > -0.40 and categorize[timestep-1] < -0.60:
            if sum(categorize)/float(timestep) < -0.40 and sum(categorize)/float(timestep) > -0.60:
                individual.test = individual.test + 1 #/ float(num_timesteps)

        #plt.hold(True)
        f, ax = plt.subplots(2, sharex=True)

        ax[0].plot(timestep_list, categorize[:timestep], color='r')
        ax[1].plot(timestep_list, mvect_list[:timestep], color='b')
        ax[0].set_ylim([-1,1])
        ax[1].set_ylim([min(mvect_list), max(mvect_list)])
        ax[1].set_xlim([0,timestep])
        ax[0].legend(['categorize'])
        ax[1].legend(['movement'])
        ax[0].set_ylabel('Average of Guess Neurons')
        ax[1].set_ylabel('Change in Prop Angles')
        ax[1].set_xlabel('Number of Timesteps')
        ax[0].set_title('Categorize and Movement Individual: '+str(individual.uid)+' '+'_Pos: '+position[6]+'&'+position[7])

        #save('/Users/np/Desktop/Bullet/bullet_make/Demos/RagdollDemo/Debug/Images/cat/Individuals_'+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')+'/Individuals'+str(individual.uid)+'_data_for_neurons/'+str(index)+'CnM_image_'+str(individual.uid)+'_'+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
        index = index + 1

    Send_Values_ToFile(parent, 'Images/cat/Individuals_'+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')+'/Individuals'+str(individual.uid)+'_data_for_neurons/'+str(index)+str(individual.uid)+position[6]+position[7]+'_ANN.txt')

    individual.categorize = sum( individual.categorize ) / 7.0
    print individual.categorize   # Average

    return population

filename = "weights_Matrix.csv"

class Individual:
    uid = 0
    def __init__(self):
        Individual.uid += 1
        self.uid = Individual.uid
        self.categorizationError = BIG_NUMBER
        self.predictionError = BIG_NUMBER
        self.ANN = MatrixCreate2(NUM_INPUTS_ANN, NUM_OUTPUTS_ANN)
        self.random = MatrixRandomize(self.ANN)
        self.bool = 'F' #nondominated
        self.age = 0    #initial age
        self.fit = 0.0  #initial fitness
        self.test = 0
        self.guess_neurons = {}
        self.categorize = []
        self.move = []
        self.cat = []
        self.cert = []
        self.R = []

    def age_(self):
        self.age += 1
        return self

    def Copy(self):
        newIndividual = MatrixCreate2(NUM_INPUTS_ANN, NUM_OUTPUTS_ANN)
        for rowidx in range(0, NUM_INPUTS_ANN):
            for colidx in range(0, NUM_OUTPUTS_ANN):
                newIndividual[rowidx][colidx] = self.ANN[rowidx][colidx]
        return newIndividual

    def getMutatedVersion(self):
        self.ANN = matrixPerturb(self.ANN, 0.25)
        return self


    def getValues(self):
        return self.ANN

    def errors(self, cat_error, pred_error):
        self.categorizationError = cat_error
        self.predictionError = pred_error
        return

    def getFit(self):
        return self.fit

oldpopulation = [Individual() for i in range(0, POP_SIZE)]

def sort_by_dom_cat(population):
    pop_list = []
    for individual in population:
        pop_list.append((individual.bool, individual))
    pop_list.sort()
    pop = []
    for ind in pop_list:
        pop.append(ind[1])
    return pop

def sort_by_fit_cat(population):
    fit_list = []
    for individual in population:
        fit_list.append((individual.fit, individual))
    fit_list.sort()
    pop = []
    for ind in fit_list:
        pop.append(ind[1])
    return pop

def AGE_individuals_cat(population):
    for individual in population:
        individual = individual.age_()
    return population

def Inject_cat(population):
    population.append(Individual())
    return population

def Fill_cat(population, POP_SIZE):
    new_individuals = []
    for i in range(0, POP_SIZE - len(population) - 1):
        individual = np.random.choice(population, 1, replace=True)
        individual2 = Individual()
        individual2.ANN = individual[0].ANN
        individual2 = individual2.getMutatedVersion()
        new_individuals.append(individual2)
    new_individuals = Inject_cat(new_individuals)
    return new_individuals

def del_doms_cat(population):
    #print [population[i].bool for i in range(0, len(population))]
    population = [individual for individual in population if individual.bool != 'T']
    #print [population[i].bool for i in range(0, len(population))]
    return population

def Determine2_Dom_cat(population):
    for individual1 in population:
        for individual2 in population:
            if individual1 != individual2:
                if individual2.fit <= individual1.fit:
                    if individual2.age >= individual1.age:
                        if individual1.fit == individual2.fit and individual1.age == individual2.age:
                            if individual2.uid < individual1.uid:
                            #print "fit i/j =", population[i].fit, population[j].fit
                                individual2.bool = 'T'
                        else:
                            individual2.bool = 'T'
                else:
                    continue
    return population

#def set_id(population):
#    for i in range(1, len(population)):
#        population[i].id = population[i-1].id + 1
#    return population

def dominate_cat(population):
    print "fit", [population[i].fit for i in range(0, len(population))][:10]
    population = Determine2_Dom_cat(population)
    print "dom", [population[i].bool for i in range(0, len(population))]

    population = sort_by_dom_cat(population)
    population = sort_by_fit_cat(population)
    #print len(population)
    population = del_doms_cat(population)
    #print len(population)
    #population = AGE_individuals(population, generation)
    print "age", [population[i].age for i in range(0, len(population))]
    print "pop-len =", len(population)
    #print [population[i].fit for i in range(0, len(population))]

    return population


def initial_cat(POP_SIZE, num_timesteps, training_list):
    oldpopulation = [Individual() for i in range(0, POP_SIZE)]
    oldpopulation = run_training_cat(oldpopulation, num_timesteps, training_list)
    newpopulation = dominate_cat(oldpopulation)
    return newpopulation

def secondary_cat(newpopulation, POP_SIZE, num_timesteps, training_list):
    new_individuals = Fill_cat(newpopulation, POP_SIZE)
    newpopulation = run_training_cat(newpopulation, num_timesteps, training_list)
    newpopulation = dominate_cat(newpopulation)
    return newpopulation

def iterations_cat(generations, POP_SIZE, num_timesteps):
    Send_Values_ToFile_two([num_timesteps], 'timesteps.txt')
    training_list, test_list = positions()
    for i in range(0, generations):
        print "Gen =", i
        if i == 0:
            newpopulation = initial_cat(POP_SIZE, num_timesteps, training_list)
            newpopulation = AGE_individuals_cat(newpopulation)
            newpopulation2 = newpopulation
        if i > 0:
            newpopulation = secondary_cat(newpopulation, POP_SIZE, num_timesteps, training_list)
            newpopulation = AGE_individuals_cat(newpopulation)

    run_testing_cat(test_list, newpopulation, num_timesteps)
    #plt.show()
    return newpopulation #, newpopulation2

#(population, num_timesteps, training_list)

if __name__ == "__main__":
    population_dict = {}
    for i in range(0,1):
        newpop = iterations_cat(3, POP_SIZE, num_timesteps)
        population_dict[i] = newpop
    #newpop_dict = {}
    #for i in range(0,10):
    #    newpop_dict[i] = iterations_lazy(750, POP_SIZE)

        #age_list = [newpop[i].age for i in range(0, len(newpop[i]))]

        #fit_list[i] = [newpop[i].fit for i in range(0, len(newpop[i]))]

        #bool_list[i] = [newpop[i].bool for i in range(0, len(newpop[i]))]

        #id_list[i] = [newpop[i].uid for i in range(0, len(newpop[i]))]

#parent = newpop[2].ANN
#filename = "weights_Matrix.csv"
#Send_Values_ToFile(parent, filename)
    #os.system('./AppRagdollDemo')
    #print newpop[0].test
