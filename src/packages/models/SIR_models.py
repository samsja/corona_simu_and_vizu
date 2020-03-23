import numpy as np
import matplotlib.pyplot as plt
import scipy
import logging
logger =logging.getLogger(__name__)

class base_sri_model:

    labels=["healthy","infected","recovered"]
    y0= np.array([1,1e-2,0])
    t_max = 10 # in days
    sol = None
    rtol=1e-10

    def edp_model(self,t,y):
        return 0

    def _compute_simu(self,t_max=0,rtol=0,y0=0):
        if t_max<=0 : t_max = self.t_max
        if rtol<=0 : rtol = self.rtol
        if y0<=0 : y0 = self.y0

        self.sol = scipy.integrate.solve_ivp(lambda t,y : self.edp_model(t,y), [0,t_max], self.y0,rtol=rtol)

    def _show_simu_results(self,labels_to_show=["all"]):
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
        self._compute_simu()
        self._show_simu_results()
