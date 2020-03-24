import numpy as np
from SIR_models import base_sri_model

import itertools


class cross_SIR(SIR_models.base_sri_model):
    '''
    this class in a subclass of base_sri_model.

    It implement the cross-SRI model to generalize the SRI model to multy-country implementation
    via a matrix of propgation of virus.

    param:

    * labels : the same label as in SRI-class
    * countries : a list of countries name
    * U : a square matrix
    * y0_infected : the init value for infected coutries generaly [1-e,e,0] with e<<1
    * y0_not_infected :the init value for not infected coutries generaly [1,0,0]


    '''
    labels=["healthy","infected","recovered"]
    countries = ["fr","it"] #countries or cities
    # cross labels will be generate at class creation
    a = 10
    beta=1
    U = beta*np.eye(len(countries))
    epsilon = 1e-2
    y0_infected = np.array([1-epsilon,epsilon,0])
    y0_not_infected = np.array([1,0,0])
    index_countries_infected = np.array([countries.index("it")])

    def __init__(self,delimiter="_"):
        super().__init__()
        if not(self.U.shape == (len(self.countries),len(self.countries))) :
               raise ValueError(f" U matrix has not the right shape: {self.U.shape} for {len(self.countries)} countries ")


        if not( (len(self.labels),) == self.y0_infected.shape ) :
            raise ValueError(f" the y0 per countrie vector {self.y0_infected} does not match the number of labels {len(self.labels)}  ")

        self.true_labels = [label for label in self.labels] #original labels value
        self.labels= [ f"{country}{delimiter}{label}" for label,country in itertools.product(self.labels,self.countries)]



        self.y0 = np.repeat(1,len(self.true_labels))

        self.y0 = np.array([])
        for x in self.y0_not_infected:
            class_x = np.repeat(x,len(self.countries))
            self.y0 = np.append(self.y0,class_x)

        for k,x in enumerate(self.y0_infected):
            for i in self.index_countries_infected:
                self.y0[k*len(self.countries)+i] = x



    def edp_model(self,t,y):
        S = np.array(y[0:len(self.countries)], copy=False)
        I = np.array(y[len(self.countries):2*len(self.countries)], copy=False)
        R = np.array(y[2*len(self.countries):3*len(self.countries)], copy=False)

        S = -S*(self.U@I)
        R = I/self.a
        I = -S - R

        dydt = np.append(S,I)
        dydt = np.append(dydt,R)
        return dydt
