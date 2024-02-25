from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from getCpds import *

# Create bayesian network

net = BayesianNetwork([('Prog', 'DProg'), ('D', 'DProg'), ('Com', 'Cu'), 
                       ('Unc', 'Cu'), ('Cu', 'T'), ('DProg', 'T'), ('E', 'T'), 
                       ('Dur', 'T'),('Com', 'Pri'), ('P', 'Pri'), ('Imp', 'Pri'), 
                       ('Dur', 'Pri'), ('T', 'I'), ('Pri', 'I'), ('Dep', 'I')])

# Get CPDs

cpds = create_cpds()

for cpd in cpds:
    print(cpd)
    net.add_cpds(cpd)


# inferenceP = VariableElimination(praccyP)

# posteriorP = inferenceP.query(variables=['Pri'], evidence={'Com':'comp', 'P':'lowp', 'Imp':'unimportant', 'Dur':'short'})

# # posterior = inference.query(variables=['T'])
# print(posteriorP.values[1])
# print(posteriorP)



