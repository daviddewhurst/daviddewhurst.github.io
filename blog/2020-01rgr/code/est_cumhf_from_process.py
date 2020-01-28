#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import joblib

import hf_estimators as hf
from rgr_models import GrowthKernelModel


SEED = 0
np.random.seed(SEED)
plt.style.use('bmh')
gfs = (6, 6)
fs = 15


def plot_cumhfs(pairs, labels):
    fig, ax = plt.subplots(figsize=gfs)
    for pair, label in zip(pairs, labels):
        marks, cumhf = pair
        ax.scatter(marks, cumhf, label=label)
    
    ax.set_xscale('log')
    ax.legend(fontsize=fs)
    ax.set_xlabel('$x$ (failure rv value)', fontsize=fs)
    ax.set_ylabel('$\hat{\Lambda}(x)$', fontsize=fs)
    ax.tick_params(labelsize=fs)


def est_cumhf_from_sim(nt=20000, rho=0.1, prob_dist=lambda x: x):
    model = GrowthKernelModel(
        nt=nt,
        rho=rho,
        prob_dist=prob_dist
            )
    model.run()
    model.calculate_Nk()
    # since Nk(t) \sim t p(k), we can just use these counts and not worry about prop factor t
    k2nk = sorted(
        model.k2nk.items(),
        key=lambda t: t[0]  # sort by size of the rv
            )
    marks, events = zip(*k2nk)
    marks = np.array(marks)
    events = np.array(events)
    surviving = np.sum(events) - np.cumsum(events) + 1
    
    # now estimate hf using nelson - aalen
    est_cumhf = hf.nelson_aalen_cumhf(marks, events=events, surviving=surviving)
    return marks, est_cumhf


def main():
    prob_dists = [lambda x: np.ones_like(x), 
            lambda x: np.log(x + 1),
            lambda x: x**(2./3),
            lambda x: x]
    labels = ['$r(x) \propto 1$', 
            '$r(x) \propto \log (x + 1)$',
            '$r(x) \propto x^{2/3}$',
            '$r(x) \propto x$']
    nt = 20000
    rho = 0.1
    pairs = [
        est_cumhf_from_sim(prob_dist=prob_dist, nt=nt, rho=rho) for prob_dist in prob_dists
            ]
    plot_cumhfs(pairs, labels)
    plt.savefig('../est-cumhf-from-rgr-sim.png', bbox_inches='tight')
    plt.close()

    # serialize results
    joblib.dump(
        [pairs, labels, rho, nt],
        '../out/est-cumhf-from-rgr-sim.gz'
            )

    # what happens if we have r(x) growing faster than O(x)?
    # we proved this theoretically...
    pair = est_cumhf_from_sim(prob_dist=lambda x: x**2.)
    pairs.append(pair)
    labels.append('$r(x) \propto x^2$')
    plot_cumhfs(pairs, labels)
    plt.savefig('../est-cumhf-from-rgr-sim-breaking.png', bbox_inches='tight')
    plt.close()
    

if __name__ == "__main__":
    main()
