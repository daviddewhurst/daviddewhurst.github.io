#!/usr/bin/env python

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import hf_estimators as hf


plt.style.use('bmh')
gfs = (6, 6)
fs = 15
np.random.seed(123)
param = 2.


def main():
    
    # heavy-tailed 1
    rvs = np.absolute(
            stats.pareto(param).rvs(size=1000)
            )
    rvs = np.sort(rvs)

    x_km, hf_km = hf.kaplan_meier_hf(rvs)
    x_na, hf_na = hf.nelson_aalen_hf(rvs)
    
    fig, ax = plt.subplots(figsize=gfs)
    ax.scatter(x_km, hf_km, marker='+', label='KM approximation')
    ax.scatter(x_na, hf_na, marker='+', label='NA approximation')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=fs)
    ax.set_xlabel('$X$ (failure rv)', fontsize=fs)
    ax.set_ylabel('$\hat{\lambda}(x)$ (estimated hf)', fontsize=fs)
    ax.tick_params(labelsize=fs)

    plt.tight_layout()
    plt.savefig('../hf-estimators-pareto.png', bbox_inches='tight')
    plt.close()

    # heavy-tailed 2
    rvs = np.absolute(
            stats.fatiguelife(param).rvs(size=1000)
            )
    rvs = np.sort(rvs)

    x_km, hf_km = hf.kaplan_meier_hf(rvs)
    x_na, hf_na = hf.nelson_aalen_hf(rvs)
    
    fig, ax = plt.subplots(figsize=gfs)
    ax.scatter(x_km, hf_km, marker='+', label='KM approximation')
    ax.scatter(x_na, hf_na, marker='+', label='NA approximation')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(fontsize=fs)
    ax.set_xlabel('$X$ (failure rv)', fontsize=fs)
    ax.set_ylabel('$\hat{\lambda}(x)$ (estimated hf)', fontsize=fs)
    ax.tick_params(labelsize=fs)


    plt.tight_layout()
    plt.savefig('../hf-estimators-fatiguelife.png', bbox_inches='tight')
    plt.close()

    # platykurtic
    rvs = np.absolute(
            stats.foldnorm(param).rvs(size=1000)
            )
    rvs = np.sort(rvs)

    x_km, hf_km = hf.kaplan_meier_hf(rvs)
    x_na, hf_na = hf.nelson_aalen_hf(rvs)
    
    fig, ax = plt.subplots(figsize=gfs)
    ax.scatter(x_km, hf_km, marker='+', label='KM approximation')
    ax.scatter(x_na, hf_na, marker='+', label='NA approximation')
    ax.legend(fontsize=fs)
    ax.set_yscale('log')
    ax.set_xlabel('$X$ (failure rv)', fontsize=fs)
    ax.set_ylabel('$\hat{\lambda}(x)$ (estimated hf)', fontsize=fs)
    ax.tick_params(labelsize=fs)


    plt.tight_layout()
    plt.savefig('../hf-estimators-foldnorm.png', bbox_inches='tight')
    plt.close()





if __name__ == "__main__":
    main()
