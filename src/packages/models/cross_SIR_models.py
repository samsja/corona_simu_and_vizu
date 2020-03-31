import numpy as np
from .SIR_models import base_sri_model

import itertools
import matplotlib.pyplot as plt


class cross_SIR(base_sri_model):
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
        self.delimiter=delimiter
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



    def _show_simu_results(self,countries_to_show=["all"],labels_to_show=["all"],figsize=(14,5)):

        '''
        show the results of computation according to the selected label:

        *labels_to_show is the list of labels that need to be draw
        *countries is the list of the country we want to show

        '''

        if labels_to_show == ["all"] : labels_to_show = self.true_labels
        if countries_to_show==["all"] : countries_to_show = self.countries

        if self.sol == None:
            raise ValueError("no simulation to draw compute first")

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlabel('time [day]')
        ax.set_ylabel('population proportion []')


        labels_to_show = [ f"{country}{self.delimiter}{label}" for label,country in itertools.product(labels_to_show,countries_to_show)]

        for i in range(len(self.sol.y)):
            if self.labels[i] in labels_to_show:
                ax.plot(self.sol.t,self.sol.y[i],label=self.labels[i])

        plt.legend()
        plt.show()

    def get_results(self,countries_to_get=["all"],labels_to_get=["all"]):
        if labels_to_get == ["all"] : labels_to_get = self.true_labels
        if countries_to_get==["all"] : countries_to_get = self.countries

        labels_to_get= [ f"{country}{self.delimiter}{label}" for label,country in itertools.product(labels_to_get,countries_to_get)]

        indexes = [ self.labels.index(label_to_get) for label_to_get in labels_to_get]
        return self.sol.y[ indexes]



class cross_SIRCD(cross_SIR):
    labels=["healthy","infected","recovered","incubating","dead"]
    countries = ["fr","it"] #countries or cities
    # cross labels will be generate at class creation
    a = 10
    beta=1

    v = 3
    mu = 0.2

    U = beta*np.eye(len(countries))
    flux_cross_both_contries=0.001

    U[0,1]=flux_cross_both_contries
    U[1,0]=flux_cross_both_contries

    epsilon = 1e-2
    y0_infected = np.array([1-epsilon,epsilon,0,0,0])

    y0_not_infected = np.array([1,0,0,0,0])
    index_countries_infected = np.array([countries.index("it")])
    t_max = 50


    def edp_model(self,t,y):

        S = np.array(y[0:len(self.countries)], copy=False)
        I = np.array(y[len(self.countries):2*len(self.countries)], copy=False)
        R = np.array(y[2*len(self.countries):3*len(self.countries)], copy=False)
        C = np.array(y[3*len(self.countries):4*len(self.countries)], copy=False)
        D = np.array(y[4*len(self.countries):5*len(self.countries)], copy=False)


        in_incubation = S*(self.U@(I+C))
        sick =  C/self.v
        dead = I*self.mu
        recovered = I/self.a


        S = -in_incubation
        C = in_incubation -sick
        I = sick - dead - recovered
        R = recovered
        D = dead

        dydt = np.append(S,I)
        dydt = np.append(dydt,R)
        dydt = np.append(dydt,C)
        dydt = np.append(dydt,D)


        return dydt
