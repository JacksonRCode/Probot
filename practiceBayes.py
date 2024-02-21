import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD

# Create node names for Bayesian network
names = "I,D,Dep,P,T,E,Imp"
names = names.split(",")

# Create network, adding nodes and edges between nodes 
G = BayesianNetwork()
G.add_nodes_from(names)
G.add_edges_from([('D', 'T'), ('D', 'E'), ('I', 'Dep'), ('I', 'D'), ('I', 'P'), ('I', 'Imp')])

# Create conditional probability distribution table for D
D_cpd = TabularCPD('D', 2, [[0.8, 0.6, 0.3, 0.5, 0.3, 0],
                           [0.2, 0.4, 0.7, 0.5, 0.7, 1.0]],
                    evidence=['External Factors','Time Sensitivity'], evidence_card=[2, 3], 
                    state_names={'D': ['Unimportant Deadline', 'Important Deadline'],
                                'External Factors': ['No Conflict', 'Conflict'],
                                'Time Sensitivity': ['low', 'medium', 'hard']})


print(D_cpd)
G.add_cpds(D_cpd)



print(G.nodes)