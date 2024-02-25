from datetime import date

'''
This program retrieves user input regarding task
metrics and returns a dictionary of keywords for the
bayesian network to use to predict the tasks importance

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

def getAllInput():
    '''
    This function gets user input aspects of a task to rank its importance.
    a is least important and b or c are most important depending on if there
    is a c.

    Returns: dictionary of cpd names as key and task metric as data.
    '''

    def getDeadline():
        '''
        This function determines importance of the deadline by getting due date
        from the user and comparing it with the current date to see the number of
        days until it is due.

        Return: a b or c depending on importance, c being the highest.
        '''
        
        print("When is this task due?")
        dateinput = input("Enter a date in YYYY-MM-DD format: ")
        print("----------------------------------------------------------------")
        print()

        year, month, day = map(int, dateinput.split('-'))
        dueDate = date(year, month, day)
        
        today = date.today()

        numDays = (dueDate - today).days

        if numDays < 4:
            return 'c'
        elif numDays < 8:
            return 'b'
        else:
            return 'a'

     # 'E'
    def getExternal():
        '''
        This function determines whether the user will have difficulty completing
        a task due to external circumstances.

        Return: a or b representing no externals or yes externals,
        '''
        print("Are there external factors that will inhibit your ability to complete this task?")
        ext = input("Y for yes, N for no: ").lower()
        print("----------------------------------------------------------------")
        print()

        if ext[0]=='y':
            return 'b'
        return 'a'


    def getProgress():
        '''
        This function determines whether a user has begun a task yet.

        Return: a or b depending on whether they have begun or not.
        '''
        print("Have you begun this task?")
        prog = input("Y for yes, N for no ").lower()
        print("----------------------------------------------------------------")
        print()

        if prog[0]=='y':
            return 'a'
        return 'b'

    def getComplexity():
        '''
        This function determines a task's complexity.

        Return: a b or c depending on complexity.
        '''
        print("How complex is this task?")
        comp = input("V for very, K for kind of, N for not complex: ").lower()
        print("----------------------------------------------------------------")
        print()

        if comp[0]=='v':
            return 'c'
        elif comp[0]=='k':
            return 'b'
        return 'a'
    
    def getUncertainty():
        '''
        This function determines a user's certainty on how to approach a task.

        Return: a or b depending on certainty
        '''
        print("How certain are you on how to approach this task?")
        cer = input("Input C for certain, or U for uncertain: ").lower()
        print("----------------------------------------------------------------")
        print()

        if cer[0]=='u':
            return 'b'
        return 'c'

    def getDuration():
        '''
        This function determines how long a task will take.

        Return: a for short, b for long
        '''
        print("How long will this task take?")
        dur = input("L for a long time, S for short or medium: ").lower()
        print("----------------------------------------------------------------")
        print()

        if dur[0]=='l':
            return 'b'
        return 'a'

    def getPreference():
        '''
        This function determines whether a user would like to finish this task sooner
        or later.

        Return: a for later b for sooner.
        '''
        print("Would you prefer to finish this task sooner or later?")
        pref = input("S for sooner, L for later: ").lower()
        print("----------------------------------------------------------------")
        print()

        if pref[0]=='s':
            return 'b'
        return 'a'

    def getImportance():
        '''
        This function determines a task's repercussions upon failure to complete.

        Return: a for fine, b for ruh-roh
        '''
        print("Will there be consequences if this task isn't completed on time?")
        imp = input("Y for yes, N for no: ").lower()
        print("----------------------------------------------------------------")
        print()

        if imp[0]=='y':
            return 'b'
        return 'a'

    def getDependency():
        '''
        This function determines whether the current task is dependent upon another task.
        If so the task will be added to a dependency queue for the other task.. not yet
        though.

        Return. a for no, b for yes.
        '''
        print("Is this task dependent upon finishing another task first?")
        dep = input("Y for yes, N for no: ").lower()
        print("----------------------------------------------------------------")
        print()
        if dep[0]=='y':
            '''
            which task?
            Add to dependency queue for other task
            Idea is that even if this task is more important than the other, 
            the other will be scheduled first.
            '''
            return 'a'
        return 'b'

    return {'D':getDeadline(),'E':getExternal(),'Prog':getProgress(),
            'Com':getComplexity(),'Unc':getUncertainty(),'Dur':getDuration(),
            'P':getPreference(),'Imp':getImportance(),'Dep':getDependency()}
