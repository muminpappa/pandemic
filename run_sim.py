""""Simulation to compare infection scenarios"""
import matplotlib.pyplot as plt
import numpy as np
from pandemic import population

"size of population"
size_of_population = 1000

"number of time steps to simulate"
number_of_steps = 500

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




