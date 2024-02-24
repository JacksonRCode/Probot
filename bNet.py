import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD
from pgmpy.inference import VariableElimination

# Create network

'''
net = BayesianNetwork([('T', 'I'),('Pri','I'),('Dep','I'), # 1st level
                       ('Dur', 'T'),('E', 'T'),('Cu', 'T'),('D', 'T'), # 2nd level
                       ('P', 'Pri'),('Imp', 'Pri'),('Dur', 'Pri'), #2nd level
                       ('Prog', 'D'), ('Com', 'Cu'), ('Unc', 'Cu')]) # 3rd level
'''
                       
# Each CPD with levels:
'''
1 P(I | T,P,D)
2 P(T | Dur,E,Unc,D)
3 P(D | Prog) & input
4 P(Prog | input) $
3 P(Unc | Com,U)
3 P(E | input)
3 P(Dur | input)
2 P(Pri | P,Imp,Dur)
3 P(P | input)
3 P(Imp | input)
2 P(Dep | input)
'''

# Create CPDs starting with lowest levels
# CPDs are assigned base probability values in case no input is given for them
# Typically, these values are assigned by user input ==> evidence

'''
# Current task progress
cpd_prog = TabularCPD('Prog', 3, values=[[0.5], [0.3], [0.2]], # no work, little work, lots work
                                 state_names={'Prog': ['low', 'med', 'high']}) 

# Current task deadline
cpd_d = TabularCPD('D', 3, values=[[0.25], [0.5], [0.25]], # > week away, Week away, less than week away
                           state_names={'D': ['low', 'med', 'high']})

# Current task uncertainty
cpd_unc = TabularCPD('Unc', 3, values=[[0.5], [0.4], [0.1]], # Certain, semi-certain, uncertain
                               state_names={'Unc': ['low', 'med', 'high']})
'''

# Start of T

# Start of DProg

# Current task progress
cpd_prog = TabularCPD('Prog', 2, values=[[0.5], [0.5]],
                      state_names={'Prog':['some', 'none']}) # work, no work

# Current task deadline
cpd_d = TabularCPD('D', 3, values=[[0.3], [0.4], [0.3]],
                   state_names={'D':['far', 'near', 'soon']}) # > week away, Week away, less than week away

# Current task progress & deadline
cpd_dProg = TabularCPD('DProg', 2, values=[[0.9, 0.65, 0.35, 0.75, 0.35, 0.1], 
                                           [0.1, 0.35, 0.65, 0.25, 0.65, 0.9]],
                       evidence=['Prog', 'D'], evidence_card=[2,3],
                       state_names={'DProg':['no_dprog', 'yes_dprog'],
                                    'Prog':['some', 'none'],
                                    'D':['far', 'near', 'soon']}) 

# End of DProg

# Start of Cu

# Current task complexity
cpd_com = TabularCPD('Com', 3, values=[[0.3], [0.4], [0.3]], # Easy, complex, very complex
                    state_names={'Com':['ncomp', 'comp', 'vcomp']})

# Current task uncertainty              #Certain, uncertain
cpd_unc = TabularCPD('Unc', 2, values=[[0.5], [0.5]],
                     state_names={'Unc':['certain', 'uncertain']})

# Current task complexity and uncertainty  #easy, complex, very complex
cpd_cu = TabularCPD('Cu', 2, values=[
                                    [0.95, 0.65, 0.35, 0.75, 0.35, 0.0], 
                                    [0.05, 0.35, 0.65, 0.25, 0.65, 1.0]], 
                             evidence=['Unc', 'Com'], evidence_card=[2,3],
                             state_names={'Cu':['no_cu', 'yes_cu'],
                                          'Unc':['certain', 'uncertain'],
                                          'Com':['ncomp', 'comp', 'vcomp']})

# End of Cu

# External factors that could interfere with current task
cpd_e = TabularCPD('E', 2, values=[[0.5], [0.5]],
                   state_names={'E':['none', 'some']})

# Task duration
cpd_dur = TabularCPD('Dur', 2, values=[[0.5], [0.5]],
                     state_names={'Dur':['short', 'long']})

# Time sensitivity -- consider: Duration, External Factors, Complexity & Uncertainty, Deadline and Progress
cpd_t = TabularCPD('T', 2, values=[[1.0,0.75,0.75,0.5,0.75,0.5,0.5,0.25,0.75,0.5,0.5,0.25,0.5,0.25,0.25,0.0],
                                   [0.0,0.25,0.25,0.5,0.25,0.5,0.5,0.75,0.25,0.5,0.5,0.75,0.5,0.75,0.75,1.0]],
                   evidence=['DProg', 'Cu', 'E', 'Dur'], evidence_card=[2,2,2,2],
                   state_names={'T':['unimp', 'imp'],
                                'DProg':['no_dprog', 'yes_dprog'],
                                'Cu':['no_cu', 'yes_cu'],
                                'E':['none', 'some'],
                                'Dur':['short', 'long']})

# End of T

praccy = BayesianNetwork([('Prog', 'DProg'), ('D', 'DProg'), ('Com', 'Cu'), ('Unc', 'Cu'), 
                          ('Cu', 'T'), ('DProg', 'T'), ('E', 'T'), ('Dur', 'T')])

praccy.add_cpds(cpd_t, cpd_prog, cpd_d, cpd_dProg, cpd_com, cpd_unc, cpd_cu, cpd_e, cpd_dur)

inference = VariableElimination(praccy)
posterior = inference.query(variables=['T'], evidence={'Prog':'none', 'D':'near', 'Com':'vcomp', 'Unc':'uncertain',
                                                       'E':'some', 'Dur':'long'})

# posterior = inference.query(variables=['T'])
print(posterior.values[1])
print(posterior)



