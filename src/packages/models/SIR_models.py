import numpy as np
import matplotlib.pyplot as plt
import scipy
import logging
logger =logging.getLogger(__name__)

class base_sri_model:

    '''
    This class is a simple class to use sri_models or solve general edp via scipy integrate function with RK45

    * labels are the name of each dimension of the vecotr y in the edp_model
    * y0 is the initial value of y
    * 0 -> t_max is the interval on which the numerical solver will compute the solution
    * rtol is the precision of the solver


    this class is an abtract class, it child class has to overwrite y0 and the edp_model() method with the right function such as

    y'(t)=edp_model(y(t),t) is the edp equation
    '''

    labels=["healthy","infected","recovered"]
    y0= np.array([0])
    t_max = 10 # in days
    sol = None
    rtol=1e-10

    def edp_model(self,t,y):
        '''
        has to be rewritten by child class
        '''
        return 0

    def _compute_simu(self,t_max=0,rtol=0,y0=0):
        '''
        launch the computation of the model :

        *rtol is the precision of the solve default value is define in class
        *y0 is the initial value of y default value is define in class
        '''
        if t_max<=0 : t_max = self.t_max
        if rtol<=0 : rtol = self.rtol
        if y0<=0 : y0 = self.y0

        self.sol = scipy.integrate.solve_ivp(lambda t,y : self.edp_model(t,y), [0,t_max], self.y0,rtol=rtol)

    def _show_simu_results(self,labels_to_show=["all"]):

        '''
        show the results of computation according to the selected label:

        *labels_to_show is the list of labels that need to be draw

        '''

        if labels_to_show == ["all"] : labels_to_show = self.labels

        if self.sol == None:
            logger.error("no simulation to draw compute first")

        fig, ax = plt.subplots(figsize=(14, 5))
        ax.set_xlabel('time [day]')
        ax.set_ylabel('population proportion []')

        for i in range(len(self.sol.y)):
            if self.labels[i] in labels_to_show:
                ax.plot(self.sol.t,self.sol.y[i],label=self.labels[i])

        plt.legend()
        plt.show()

    def simulate(self):
        '''
        simulate method is the main method of the class, it compute the model and then draw it with default values
        '''
        self._compute_simu()
        self._show_simu_results()
