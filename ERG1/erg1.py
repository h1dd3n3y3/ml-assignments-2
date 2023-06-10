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

data=safe_csv_read('source.csv')
print(data[0])
data.pop(0)         # Πετάμε τα ονόματα
                    # Το dataset έχει μαθητές διάφορων κατηγοριών πτυχίων, φύλου, εθνικότητας,τύπος μεσημεριανού
                    # και πόσο προετοιμάστηκε για τις εξετάσεις. Θα χρησιμοποιήσουμε μόνο τους βαθμούς από τα 3
                    # μαθήματα. Έτσι θα βγάλουμε τις άλλες πληροφορίες από το dataset.
print(data[0])
data=np.array(data)
data=data[:,5:]
print(data[0])


#Creating the Tipping Controller Using the skfuzzy control API

# New Antecedent/Consequent objects hold universe variables and membership functions
math = ctrl.Antecedent(np.arange(0, 101, 1), 'math_score')#times pou pairnei to quality
reading = ctrl.Antecedent(np.arange(0, 101, 1), 'reading_score')
writing = ctrl.Antecedent(np.arange(0, 101, 1), 'writing_score')
overall = ctrl.Consequent(np.arange(0, 101, 1), 'overall_score')

# Auto-membership function population is possible with .automf(3, 5, or 7)
math.automf(3) # posotita trigonon
reading.automf(3)
writing.automf(3)

# membership functions
overall['bad'] = fuzz.trimf(overall.universe, [0, 20, 50]) #edo kathorizo ta akra kai to meson ton trigonon
overall['good'] = fuzz.trimf(overall.universe, [40, 50, 80])
overall['great'] = fuzz.trimf(overall.universe, [70, 90, 100])

# You can see how these look with .view()
math.view()
# quality['average'].view()
reading.view()
writing.view()
overall.view()

# Rules
rule1 = ctrl.Rule(math['poor'] & reading['poor'] | math['poor'] & writing['poor'] | writing['poor'] & reading['poor'] , overall['bad'])
rule2 = ctrl.Rule(math['average'] & reading['average'] | math['average'] & writing['average'] | writing['average'] & reading['average'] , overall['good'])
rule3 = ctrl.Rule(math['good'] & reading['good'] | math['good'] & writing['good'] | writing['good'] & reading['good'] , overall['great'])

#Control System Creation and Simulation
result_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

for i in data:
    print(i[0], i[1], i[2])
    result = ctrl.ControlSystemSimulation(result_ctrl)
    result.input['math_score'] = i[0]
    result.input['reading_score'] = i[1]
    result.input['writing_score'] = i[2]
    # Crunch the numbers
    result.compute()
    

# print (result.output['overall_score']) #The resulting suggested tip is 19.84%
# overall.view(sim=result)