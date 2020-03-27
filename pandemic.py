""""Simulation to compare infection scenarios"""
import random
import matplotlib.pyplot as plt
import numpy as np

"fraction of the population that is considered vulnerable"
vulnerable_fraction = 0.05

"time steps after infection"
"- before showing symptoms"
symptom_age = 50
"- before being infectious"
infectious_age = 20
"- before being immune and no longer infectious"
immune_age = 80

"transmission likelihood during meeting"
"- involving vulnerable individual"
transmission_likelyhood_1 = 0.05
"- between non-vulnerable individuals"
transmission_likelyhood_2 = 1

"size of population"
size_of_population = 1000
"pairs of people meeting in each time step"
fraction_of_pairs = 0.5
number_of_pairs = int(size_of_population*fraction_of_pairs)

"number of time steps to simulate"
number_of_steps = 500

class individual:
    def __init__(self, weakness):
        self.infected = 0
        self.has_symptoms = False
        self.infectious = False
        self.immune = False
        self.vulnerable = False
        if weakness < vulnerable_fraction: self.vulnerable = True

    def age(self):
        if self.infected > 0: self.infected += 1
        if self.infected > symptom_age: self.has_symptoms = True
        if self.infected > infectious_age: self.infectious = True
        if self.infected > immune_age:
            self.immune = True
            self.has_symptoms = False
            self.infectious = False


    def infect(self):
        if self.infected == 0 : self.infected = 1

class population:
    def __init__(self,size):
        self.data = []
        for i in range(size):
            x = individual(random.random())
            self.data.append(x)
        self.data[random.randint(1, len(self.data))].infect()

    def age(self):
        for i in range(len(self.data)): self.data[i].age()

    def meet(self):
        slask = random.sample(range(len(self.data)),2*number_of_pairs)
        group_1 = slask[1:int(len(slask)/2)]
        group_2 = slask[int(len(slask)/2+1):len(slask)]

        for i in range(1,len(group_1)):
            self.try_infection( self.data[group_1[i]], self.data[group_2[i]] )

    def try_infection(self, p1 : individual, p2 : individual):
        if(p1.vulnerable or p2.vulnerable):
            if( p1.infectious and not p2.infected and random.random() < transmission_likelyhood_1):
                p2.infect()
            elif(p2.infectious and not p1.infected and random.random() < transmission_likelyhood_1):
                p1.infect()
        else:
            if (p1.infectious and not p2.infected and random.random() < transmission_likelyhood_2):
                p2.infect()
            elif (p2.infectious and not p1.infected and random.random() < transmission_likelyhood_2):
                p1.infect()

    def statistics(self):
        fraction_infected = 0
        fraction_infectious = 0
        fraction_has_symptoms = 0
        fraction_intensive_care = 0
        fraction_immune = 0
        fraction_dead = 0
        for i in range(len(self.data)):
            fraction_infected += (1 if (self.data[i].infected>0) else 0)/len(self.data)
            fraction_infectious += (1 if (self.data[i].infectious) else 0)/len(self.data)
            fraction_has_symptoms += (1 if (self.data[i].has_symptoms) else 0)/len(self.data)
            fraction_intensive_care += (1 if (self.data[i].has_symptoms and self.data[i].vulnerable) else 0) / len(self.data)
            fraction_immune += (1 if (self.data[i].immune and not self.data[i].vulnerable) else 0)/len(self.data)
            fraction_dead += (1 if (self.data[i].immune and self.data[i].vulnerable) else 0)/len(self.data)
        return[i,fraction_infected, fraction_infectious, fraction_has_symptoms, fraction_intensive_care, fraction_immune, fraction_dead]


p = population(size_of_population)
result = []

for i in range(number_of_steps):
    p.meet()
    p.age()
    result.append(p.statistics())

a = np.array(result)

plt.plot(a[:,1:])
plt.legend(["infected", "infectious", "has_symptoms", "intensive_care", "immune", "dead"])
plt.title("Peak intensive care: {:.2%}".format(max(a[:,4])))
plt.show()




