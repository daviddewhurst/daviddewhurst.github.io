#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


class RGRModel:

    def __init__(self, *args, **kwargs):
        self.nt = kwargs.get('nt', 10000)

    def run(self):
        pass


class SimonModel(RGRModel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.population = []
        self.population_append = self.population.append
        self.rho = kwargs.get('rho', 0.01)


    def run(self):
        self.population_append( 1 )
        for t in range(self.nt):
            if np.random.random() < self.rho:
                self.population_append( np.max(self.population) + 1 )
            else:
                self.population_append( np.random.choice(self.population) )


class GrowthKernelModel(SimonModel):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.prob_dist = kwargs.get('prob_dist', lambda x: x)
        self.probs = None
        self.ele2count = {}
        self.last_counted = 0
        self.k2nk = {}

    def run(self):
        self.population_append( 1 )
        for t in range(self.nt):
            if np.random.random() < self.rho:
                self.population_append( np.max(self.population) + 1 )
            else:
                # get uniques
                for x in self.population[self.last_counted:]:
                    try:
                        self.ele2count[x] += 1
                    except KeyError:
                        self.ele2count[x] = 1
                self.last_counted = t

                # create probability distribution
                ele_counts = list(self.ele2count.items())
                ele_counts = sorted(ele_counts, key=lambda t: t[1], reverse=True)
                eles, probs = zip(*ele_counts)
                probs = self.prob_dist( np.array(probs).astype(float) )
                probs = probs / np.sum(probs)
                self.probs = probs
                
                # add the new element
                self.population_append( np.random.choice(eles, p=self.probs) )

    def calculate_Nk(self):
        # get number of groups of size k
        for k in self.ele2count.values():
            try:
                self.k2nk[k] += 1
            except KeyError:
                self.k2nk[k] = 1


if __name__ == "__main__":

    model = GrowthKernelModel(nt=20000, rho=0.1, prob_dist=lambda x: np.ones_like(x))
    model.run()
    model.calculate_Nk()

    print(
            sorted(model.k2nk.items(), reverse=True, key=lambda t: t[0])
        )
    exit()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.loglog(model.probs)


    plt.show()
        
