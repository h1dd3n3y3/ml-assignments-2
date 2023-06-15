#FUZZY LOGIC
#Παρατηρήθηκε πως χρησιμοποιήθηκε αυτή η ιστοσελίδα για τις πληροφορίες για το αρχικό sample κώδικα που μας
#δίνεται στο εργαστήριο:
#https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html


import numpy as np
#import matplotlib.pyplot as plt            # Χρειάζεται μόνο όταν τρέχεται εκτός spyder
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
#print(data[0])
data.pop(0)         # Πετάμε τα ονόματα
                    # Το dataset έχει μαθητές διάφορων κατηγοριών πτυχίων, φύλου, εθνικότητας,τύπος μεσημεριανού
                    # και πόσο προετοιμάστηκε για τις εξετάσεις. Θα χρησιμοποιήσουμε μόνο τους βαθμούς από τα 3
                    # μαθήματα. Έτσι θα βγάλουμε τις άλλες πληροφορίες από το dataset.
#print(data[0])
data=np.array(data)
data=data[:,5:]
data=data.astype(np.int32)      # Επιλέγουμε τους αριθμούς και τους μετατρέπουμε σε integers καθώς τους θεωρεί 
                                # strings η numpy. Επίσης χρησιμοποιούμε numpy για το 2D list slicing
#print(data[0])


math = ctrl.Antecedent(np.arange(0, 100, 1), 'math_score')              # Είναι οι τιμές μεγιστες και ελάχιστες των βαθμβν
reading = ctrl.Antecedent(np.arange(0, 100, 1), 'reading_score')
writing = ctrl.Antecedent(np.arange(0, 100, 1), 'writing_score')
overall = ctrl.Consequent(np.arange(0, 100, 1), 'overall_score')

math['bad'] = fuzz.trimf(math.universe, [0, 0, 50])     #Οι τριγωνικές που έχουμε είναι αρκετά καλές (TRIangular Membership Function generator)
math['good'] = fuzz.trimf(math.universe, [40, 70, 80])
math['great'] = fuzz.trimf(math.universe, [70, 100, 100])

reading['bad'] = fuzz.trimf(reading.universe, [0, 0, 50])
reading['good'] = fuzz.trimf(reading.universe, [40, 70, 80])
reading['great'] = fuzz.trimf(reading.universe, [70, 100, 100])

writing['bad'] = fuzz.trimf(writing.universe, [0, 0, 50])
writing['good'] = fuzz.trimf(writing.universe, [40, 70, 80])
writing['great'] = fuzz.trimf(writing.universe, [70, 100, 100])

overall['bad'] = fuzz.trimf(overall.universe, [0, 0, 50])
overall['good'] = fuzz.trimf(overall.universe, [40, 70, 80])
overall['great'] = fuzz.trimf(overall.universe, [70, 100, 100])

# Προβολή των plot των membership function
math.view()
reading.view()
writing.view()
overall.view()

# Κανόνες του fuzzy controller
# Θέλουμε όταν είναι 2 από τις 3 κατηγορίες να παίρνει αυτή την κατηγορία ο μαθητής.
rule1 = ctrl.Rule(math['bad'] & reading['bad'] | math['bad'] & writing['bad'] | writing['bad'] & reading['bad'] , overall['bad'])
rule2 = ctrl.Rule(math['good'] & reading['good'] | math['good'] & writing['good'] | writing['good'] & reading['good'] , overall['good'])
rule3 = ctrl.Rule(math['great'] & reading['great'] | math['great'] & writing['great'] | writing['great'] & reading['great'] , overall['great'])

# Ρίχνουμε τους κανόνες μας στην βιβλιοθήκη (στο controler)
result_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

student_id=0    # Ένας μετρητής για να ξέρουμε το index του μαθητή.

for i in data:
    print("----------------------------------------------------------------------------------------")
    print("Οι βαθμοί του μαθητή {} για τα αντίστοιχα μαθήματα: {} | {} | {}".format(student_id, i[0], i[1], i[2]))
    result = ctrl.ControlSystemSimulation(result_ctrl)
    result.input['math_score'] = i[0]
    result.input['reading_score'] = i[1]
    result.input['writing_score'] = i[2]
    # Εδώ γίνεται ο υπολογισμός
    result.compute()
    
    isBad=fuzz.interp_membership(overall.universe, overall['bad'].mf, result.output['overall_score'])   # Μπορούσε να βγεί από το documentation αλλά το πήρα από εδώ: https://stackoverflow.com/questions/73373581/skfuzzy-get-membership-value-from-output
    isGood=fuzz.interp_membership(overall.universe, overall['good'].mf, result.output['overall_score'])
    isGreat=fuzz.interp_membership(overall.universe, overall['great'].mf, result.output['overall_score'])
    print("Ποσοστό ύπαρξης μέσα στις κατηγορίες bad, good, great αντίστοιχα: {} | {} | {} ".format(isBad, isGood, isGreat))
    print ("Το κέντρο βάρους: {}".format(result.output['overall_score']))
    print("----------------------------------------------------------------------------------------")
    student_id=student_id+1
    overall.view(sim=result)