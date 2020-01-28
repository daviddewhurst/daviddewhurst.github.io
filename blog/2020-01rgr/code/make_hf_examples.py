#!/usr/bin/env python

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

plt.style.use('bmh')
gfs = (6, 6)
fs = 15
c = 2.


def main():
    fig, ax = plt.subplots(figsize=gfs)

    xs = np.linspace(0., 10., 500)
    rvs = stats.lomax(c).pdf(xs)
    ax.plot(xs, rvs, label='$\lambda(x) = c/x$')

    rvs = stats.expon(scale=1/c).pdf(xs)
    ax.plot(xs, rvs, label='$\lambda(x) = c$')

    rvs = stats.rayleigh(scale=np.sqrt(1/c)).pdf(xs)
    ax.plot(xs, rvs, label='$\lambda(x) = cx$')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.set_xlabel('$X$ (failure rv)', fontsize=fs)
    ax.set_ylabel('$p(x)$', fontsize=fs)
    ax.tick_params(labelsize=fs)
    ax.legend(fontsize=fs)

    plt.tight_layout()
    plt.savefig('../hf2pdf-examples.png', bbox_inches='tight')
    plt.close()

    # logspace now
    fig, ax = plt.subplots(figsize=gfs)

    xs = np.linspace(0.1, 100., 1000)
    rvs = stats.lomax(c).pdf(xs)
    ax.plot(xs, rvs, label='$\lambda(x) = c/x$')

    rvs = stats.expon(scale=1/c).pdf(xs)
    ax.plot(xs, rvs, label='$\lambda(x) = c$')

    rvs = stats.rayleigh(scale=np.sqrt(1/c)).pdf(xs)
    ax.plot(xs, rvs, label='$\lambda(x) = cx$')

    ax.set_xlabel('$X$ (failure rv)', fontsize=fs)
    ax.set_ylabel('$p(x)$', fontsize=fs)
    ax.tick_params(labelsize=fs)
    ax.legend(fontsize=fs)
    ax.set_ylim(10**-9,)
    ax.set_yscale('log')
    ax.set_xscale('log')

    plt.tight_layout()
    plt.savefig('../hf2pdf-examples-loglog.png', bbox_inches='tight')
    plt.close()





if __name__ == "__main__":
    main()
