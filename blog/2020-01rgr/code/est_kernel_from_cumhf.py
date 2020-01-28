#!/usr/bin/env python

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'  # mac disaster

import numpy as np
import joblib
import matplotlib.pyplot as plt
import torch
import pyro
import pyro.contrib.gp as gp
import pyro.distributions as dist


SEED = 0
np.random.seed(SEED)
pyro.set_rng_seed(SEED)
plt.style.use('bmh')
gfs = (6, 6)
fs = 15


def plot_gp_and_data(ax, x, y, model, ylabel, legend_label, y_mean=0, n_pts=250, color='red',
        logval=False):
    x_plot = torch.linspace(0.1, x.max(), n_pts)
    ax.scatter(x.numpy(), y.numpy(), marker='+', color=color, label=legend_label)

    with torch.no_grad():
        mean, cov = model(x_plot, full_cov=True)
    mean = mean + y_mean
    sd = cov.diag().sqrt()

    ax.plot(x_plot.numpy(), mean.numpy(), color=color)
    ax.fill_between(
        x_plot.numpy(),
        mean.numpy() - 2 * sd.numpy(),
        mean.numpy() + 2 * sd.numpy(),
        alpha=0.2,
        color=color,
            )
    
    if not logval:
        ax.set_xlabel('$x$ (failure rv value)', fontsize=fs)
        ax.set_ylabel(ylabel, fontsize=fs)
    else:
        ax.set_xlabel('$\log_{10}\ x$ (failure rv value)', fontsize=fs)
        ax.set_ylabel('$\hat{\Lambda}(\log_{10}\ x)$', fontsize=fs)
    ax.tick_params(labelsize=fs)
    ax.legend(fontsize=fs)

    return x_plot.numpy(), mean.numpy(), sd.numpy()


def fit_gp(marks, est_cumhf, n_xu=20, nsteps=1500):
    # fit in log - linear space
    l_marks = np.log10(marks)
    l_marks_tch = torch.tensor(l_marks, dtype=torch.float)
    est_cumhf_tch = torch.tensor(est_cumhf, dtype=torch.float)

    # initialize inducing points for sparse gp
    xu = torch.linspace(l_marks_tch.min(), l_marks_tch.max(), n_xu)

    # set up model
    pyro.clear_param_store()
    kernel = gp.kernels.RBF(input_dim=1)
    gpr = gp.models.SparseGPRegression(
            l_marks_tch, 
            est_cumhf_tch,
            kernel,
            Xu=xu,
            jitter=1e-4
            )

    # optimize
    optim = torch.optim.Adam(gpr.parameters(), lr=0.01)
    loss_fn = pyro.infer.Trace_ELBO().differentiable_loss
    losses = []
    
    for n in range(nsteps):
        optim.zero_grad()
        loss = loss_fn(gpr.model, gpr.guide)
        if n % 50 == 0:
            print(f'Iter {n}, loss = {loss.item()}')
        loss.backward()
        optim.step()
        losses.append(loss.item())
    
    return l_marks_tch, est_cumhf_tch, gpr, losses


def main():
    pairs, labels, rho, nt = joblib.load('../out/est-cumhf-from-rgr-sim.gz')
    fig, ax = plt.subplots(figsize=gfs)
    colors = plt.style.library['bmh']['axes.prop_cycle'].by_key()['color'][:len(pairs)]

    l_marks = []
    fit_xs = []
    fit_means = []
    fit_sds = []
    
    # first fit and plot cumulative hf
    for pair, color, label in zip(pairs, colors, labels):
        l_marks_tch, est_cumhf_tch, gpr, losses = fit_gp(pair[0], pair[-1])
        fit_x, fit_mean, fit_sd = plot_gp_and_data(
            ax,
            l_marks_tch,
            est_cumhf_tch,
            gpr,
            '$\hat{\Lambda}(x)$',
            label,
            color=color,
            logval=True
                )
        l_marks.append(l_marks_tch)
        fit_xs.append(fit_x)
        fit_means.append(fit_mean)
        fit_sds.append(fit_sd)

    ax.set_ylim(0,)
    plt.tight_layout()
    plt.savefig('../est-cumhf-using-gp.png', bbox_inches='tight')
    plt.close()

    # now find r(x)
    # we have fit \Lambda(\log_{10}x)
    # so \lambda(x) = 1/(\log(10) x) d/d\log_{10}x |Lambda(\log_{10}(x))
    fig, ax = plt.subplots(figsize=gfs)
    kernels = []

    for fit_x, fit_mean in zip(fit_xs, fit_means):
        d_log10_x = fit_x[1:] - fit_x[:-1]
        d_Lambda_of_log10_x = fit_mean[1:] - fit_mean[:-1]
        diffd = d_Lambda_of_log10_x / d_log10_x
        
        # now rescale to linear space
        fit_x = np.power(10, fit_x)
        scale_fac = 1./ (np.log(10.) * fit_x[1:])
        hf = scale_fac * diffd
        kernel = 1./(1 - rho) / hf
        kernel = np.where(
                kernel <= 0,
                np.mean(kernel[kernel > 0.]),
                kernel
                )
        kernels.append(kernel)

        ax.loglog(fit_x[1:], kernel)

    # plot true RGR kernels
    # there is a multiplicative free parameter here 
    # we should minimize this
    true_rx = [
            np.ones_like(np.power(10, fit_xs[0][1:])),
            np.log(np.power(10, fit_xs[1][1:]) + 1),
            np.power(10, fit_xs[-2][1:]) ** (2./3),
            np.power(10, fit_xs[-1][1:])
            ]
    for i, (fit_x, kernel, true_r, label) in enumerate(zip(fit_xs, kernels, true_rx, labels)):
        fit_x = np.power(10, fit_x)
        # subtracting them should be essentially random noise just with shifted constant mean
        mult_const = 10 ** np.mean(
                np.log10(kernel) - np.log10(true_r)
                )
        ax.loglog(fit_x[1:], mult_const * true_r, color=colors[i], linestyle=':',
                label=label)
    
    ax.set_xlabel('$x$ (failure rv value)', fontsize=fs)
    ax.set_ylabel('$r(x)$', fontsize=fs)
    ax.tick_params(labelsize=fs)
    ax.legend(fontsize=fs)
    ax.set_ylim(1,)
    plt.tight_layout()
    plt.savefig('../est-rgrkernel-using-gp.png', bbox_inches='tight')
    plt.close()
    

if __name__ == "__main__":
    main()
