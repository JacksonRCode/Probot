from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from getCpds import *

# Create bayesian network
# CPD = Conditional Probability Distribution
def getInference():
    net = BayesianNetwork([('Prog', 'DProg'), ('D', 'DProg'), ('Com', 'Cu'), 
                        ('Unc', 'Cu'), ('Cu', 'T'), ('DProg', 'T'), ('E', 'T'), 
                        ('Dur', 'T'),('Com', 'Pri'), ('P', 'Pri'), ('Imp', 'Pri'), 
                        ('Dur', 'Pri'), ('T', 'I'), ('Pri', 'I'), ('Dep', 'I')])

    # Get CPDs
    cpds = create_cpds()

    # Add cpds to network
    for cpd in cpds:
        net.add_cpds(cpd)

    # Variable elimination
    inference = VariableElimination(net)

    return inference

# Find importance based upon evidence
# posterior = inference.query(variables=['I'], evidence=ev)
# posterior = inference.query(variables=['I'])

# # posterior = inference.query(variables=['T'])
# print(posterior.values[1])




