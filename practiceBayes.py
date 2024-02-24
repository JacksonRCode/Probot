import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination

# Create node names for Bayesian network
names = "I,D,Dep,P,T,E,Imp"
names = names.split(",")

# Create network, adding nodes and edges between nodes 
# G = BayesianNetwork()
# G.add_nodes_from(names)
# G.add_edges_from([('D', 'T'), ('D', 'E'), ('I', 'Dep'), ('I', 'D'), ('I', 'P'), ('I', 'Imp')])

# Practice
# D = BayesianNetwork([('D', 'T'), ('D', 'E')])
model_D = BayesianNetwork([('T', 'D'), ('E', 'D')])

# Create conditional probability distribution table for E, T, and D
cpd_e = TabularCPD('E', 3, [[0.3], [0.5], [0.2]], 
                   state_names={'E': ['No Conflict', 'Some Conflict','Much Conflict']})

cpd_t = TabularCPD('T', 3, [[0.2],[0.5],[0.3]],
                   state_names={'T': ['Little Time', 'Medium Time', 'Much Time']})

cpd_d = TabularCPD('D', 2, [[1.0,0.7,0.35,1.0,0.6,0.25,1.0,0.4,0.1],
                            [0.0,0.3,0.65,0.0,0.4,0.75,0.0,0.6,0.9]],
                   evidence=['E','T'], evidence_card=[3,3],
                   state_names={'D': ['Unimportant', 'Important'],
                                'E': ['No Conflict', 'Some Conflict','Much Conflict'],
                                'T': ['Little Time', 'Medium Time', 'Much Time']})


model_D.add_cpds(cpd_d, cpd_e, cpd_t)

inference = VariableElimination(model_D)

# posterior = inference.query(variables=['D'], evidence={'E': 'Much Conflict', 'T': 'Medium Time'})

posterior = inference.query(variables=['D'], evidence={'E': 'No Conflict'})

print(posterior)

# cpd_d = TabularCPD('D', 2, [[0.8, 0.6, 0.3, 0.5, 0.3, 0],
#                            [0.2, 0.4, 0.7, 0.5, 0.7, 1.0]],
#                     evidence=['E','T'], evidence_card=[2, 3], 
#                     state_names={'D': ['Unimportant', 'Important'],
#                                 'E': ['No Conflict', 'Conflict'],
#                                 'T': ['low', 'medium', 'hard']})
# Add cpd to network

# D.get_state_probability({'D':'D(Important)', 'E': 'Conflict', 'T': 'medium'})

# data = pd.DataFrame(data={'T':[0,0,1], 'E':[0,1,0]})

# G.fit(data)
# G.get_cpds()

# print(D_cpd)




# print(G.nodes)