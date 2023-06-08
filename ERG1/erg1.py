#FUZZY LOGIC

import numpy as np
#import matplotlib.pyplot as plt
import csv
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def safe_csv_read(csvstring):            #from python docs: https://docs.python.org/3/library/csv.html#examples
    output=[]
    with open(csvstring, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
    return output


# Επεξεργασία των δεδομένων



#Creating the Tipping Controller Using the skfuzzy control API

# New Antecedent/Consequent objects hold universe variables and membership functions
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')#times pou pairnei to quality
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)#posotita trigonon
service.automf(3)

# membership functions
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13]) #edo kathorizo ta akra kai to meson ton trigonon
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

# You can see how these look with .view()
quality.view()
# quality['average'].view()
service.view()
tip.view()

# Rules
rule1 = ctrl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = ctrl.Rule(service['average'], tip['medium'])
rule3 = ctrl.Rule(service['good'] | quality['good'], tip['high'])

#Control System Creation and Simulation
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8

# Crunch the numbers
tipping.compute()

print (tipping.output['tip']) #The resulting suggested tip is 19.84%
tip.view(sim=tipping)