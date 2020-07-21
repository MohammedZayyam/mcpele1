#incomple
from mcpele1.montecarlo.template import *
from typing import NewType

class PatternManager:
    step_repetitions= []
    current_step_index = 0
    current_step_count = 0
    initialized: bool = False
    
    def __init__(self):
        self.initialized = False


    def increment(self):
        #print("yes",self.current_step_count)
        #print("length",len(self.step_repetitions))
        self.current_step_count -= 1
        #print("m_cuurent_step_count",self.current_step_count)

        if(self.current_step_count == 0):
            #print("here")
            self.current_step_index +=1
            #print(self.current_step_index)
            if(self.current_step_index == len(self.step_repetitions)):
                self.current_step_index = 0
            #not sure about the next line
            self.current_step_count = self.step_repetitions[self.current_step_index][0]


    def add(self, index_input, repetitions_input):
        try:
            repetitions_input >= 0
        except:
            print("repetitions cannot be less than 1")
        new = [repetitions_input, index_input]
        
        self.step_repetitions.append(new)
        #print(self.step_repetitions)
        self.current_step_index = 0
        self.current_step_count =self.step_repetitions[0][0]
        #print(self.step_repetitions[0][0])
        if(self.initialized ==False):
            self.initialized = True

    def get_index(self):    
        try:
            self.initialized == True
            return self.step_repetitions[self.current_step_index][1]
        except:
            print("no Takesteps added to pattern")
    
    # do the other methods