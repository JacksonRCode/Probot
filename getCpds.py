from pgmpy.factors.discrete.CPD import TabularCPD


'''
Each CPD with levels:

1 P(I | T,P,Dep) 
2 P(T | Dur,E,Cur,DProg) 
3 P(DProg | Prog, D) 
4 P(Prog | input) 
4 P(D | input) 
3 P(Cu | Com,Unc) 
4 P(Com | input) 
4 P(Unc | input) 
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

# Start of T

# Start of DProg
def create_cpds():

    # Current task progress
    cpd_prog = TabularCPD('Prog', 2, values=[[0.5], [0.5]],
                        state_names={'Prog':['some', 'none']}) # work, no work

    # Current task deadline
    cpd_d = TabularCPD('D', 3, values=[[0.3], [0.4], [0.3]],
                    state_names={'D':['far', 'near', 'soon']}) # > week away, Week away, less than week away

    # Current task progress & deadline
    cpd_dProg = TabularCPD('DProg', 2, values=[[0.95, 0.75, 0.50, 0.75, 0.25, 0.05], 
                                            [0.05, 0.25, 0.50, 0.25, 0.75, 0.95]],
                        evidence=['Prog', 'D'], evidence_card=[2,3],
                        state_names={'DProg':['no_dprog', 'yes_dprog'],
                                        'Prog':['some', 'none'],
                                        'D':['far', 'near', 'soon']}) 

    # Current task complexity
    cpd_com = TabularCPD('Com', 3, values=[[0.3], [0.4], [0.3]], # Easy, complex, very complex
                        state_names={'Com':['ncomp', 'comp', 'vcomp']})

    # Current task uncertainty              #Certain, uncertain
    cpd_unc = TabularCPD('Unc', 2, values=[[0.5], [0.5]],
                        state_names={'Unc':['certain', 'uncertain']})

    # Current task complexity and uncertainty  #easy, complex, very complex
    cpd_cu = TabularCPD('Cu', 2, values=[[0.95, 0.75, 0.50, 0.75, 0.25, 0.05], 
                                        [0.05, 0.25, 0.50, 0.25, 0.75, 0.95]],  
                                evidence=['Unc', 'Com'], evidence_card=[2,3],
                                state_names={'Cu':['no_cu', 'yes_cu'],
                                            'Unc':['certain', 'uncertain'],
                                            'Com':['ncomp', 'comp', 'vcomp']})

    # External factors that could interfere with current task
    cpd_e = TabularCPD('E', 2, values=[[0.5], [0.5]], state_names={'E':['none', 'some']})

    # Task duration
    cpd_dur = TabularCPD('Dur', 2, values=[[0.5], [0.5]], state_names={'Dur':['short', 'long']})

    '''
    Explanation of TabularCPD for cpd_t:

    2 represents the state names of T which correlate to the values. values[0] being the odds of a task
    being unimportant when given evidence for cpd's listed below, and values[1] the odds of a task being important.

    State_names correlates to the defined state names of each cpd given above.

    Because there are 4 evidence variables, need 2^4 options in each list of values to represent the importance/unimportance
    given different values for the evidence:
    _______________________________________________
    |       no_dprog        |       yes_dprog       |
    |_______________________|_______________________|
    |   no_cu   |   yes_cu  |   no_cu   |  yes_cu   |
    |___________|___________|___________|___________|
    |     |     |     |     |     |     |     |     |
    |_____|_____|_____|_____|_____|_____|_____|_____|
    |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    |__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|__|
                You get it

    Tedious but effective
    '''
    # Time sensitivity -- consider: Duration, External Factors, Complexity & Uncertainty, Deadline and Progress
    cpd_t = TabularCPD('T', 2, values=[[1.0,0.75,0.75,0.5,0.75,0.5,0.5,0.25,0.75,0.5,0.5,0.25,0.5,0.25,0.25,0.0],
                                    [0.0,0.25,0.25,0.5,0.25,0.5,0.5,0.75,0.25,0.5,0.5,0.75,0.5,0.75,0.75,1.0]],
                    evidence=['DProg', 'Cu', 'E', 'Dur'], evidence_card=[2,2,2,2],
                    state_names={'T':['low_t', 'high_t'],
                                    'DProg':['no_dprog', 'yes_dprog'],
                                    'Cu':['no_cu', 'yes_cu'],
                                    'E':['none', 'some'],
                                    'Dur':['short', 'long']})

    # User Preference of task
    cpd_p = TabularCPD('P', 2, values=[[0.5],[0.5]], state_names={'P':['lowp', 'highp']})

    # Task importance
    cpd_imp = TabularCPD('Imp', 2, values=[[0.5],[0.5]], state_names={'Imp':['unimportant', 'important']})

    # Priority
    cpd_pri = TabularCPD('Pri', 2, values=[[0.95,0.75,0.75,0.5,0.75,0.5,0.5,0.25,0.875,0.625,0.625,0.375,0.625,0.375,0.375,0.125,0.75,0.5,0.5,0.25,0.5,0.25,0.25,0.05],
                                        [0.05,0.25,0.25,0.5,0.25,0.5,0.5,0.75,0.125,0.375,0.375,0.625,0.375,0.625,0.625,0.875,0.25,0.5,0.5,0.75,0.5,0.75,0.75,0.95]],
                                evidence=['Com', 'P', 'Imp', 'Dur'], evidence_card=[3,2,2,2],
                                state_names={'Pri':['low_p', 'high_p'],
                                                'Com':['ncomp', 'comp', 'vcomp'],
                                                'P':['lowp', 'highp'],
                                                'Imp':['unimportant', 'important'],
                                                'Dur':['short', 'long']})

    # Is current task dependent on another?
    # If yes, lower importance and it will also be added to a dependency queue.. eventually
    cpd_dep = TabularCPD('Dep', 2, values=[[0.5],[0.5]], state_names={'Dep':['nondep', 'dep']})

    # CPD for importance
    cpd_i = TabularCPD('I', 2, values=[[0.95,0.66,0.66,0.34,0.66,0.34,0.34,0.05],
                                    [0.05,0.34,0.34,0.66,0.34,0.66,0.66,0.95]], 
                    evidence=['Dep','T','Pri'], evidence_card=[2,2,2],
                    state_names={'I':['low_imp', 'high_imp'],
                                    'Dep':['nondep', 'dep'],
                                    'T':['low_t', 'high_t'],
                                    'Pri':['low_p', 'high_p']})

    return [cpd_prog, cpd_d, cpd_dProg, cpd_com, cpd_unc, cpd_cu, cpd_e, cpd_dur, cpd_t, cpd_p, cpd_imp, cpd_pri, cpd_dep, cpd_i]

