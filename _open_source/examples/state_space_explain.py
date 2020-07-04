#!/usr/bin/env python

import pathlib

import matplotlib.pyplot as plt
import torch
import pyro

from state_space import state_space_model


SEED = 123
torch.manual_seed(SEED)
pyro.set_rng_seed(SEED)


def main():
    figdir = pathlib.Path('./figures')
    figdir.mkdir(exist_ok=True)

    # demo predictive capacity
    N = 3
    T = 101

    # draws from the prior predictive are shape (T, N)
    # each draw uses different draws from global drift and vol params
    n_prior_draws = 5
    prior_predictive = torch.stack(
        [state_space_model(None, N=N, T=T) for _ in range(n_prior_draws)]
    )
    
    colors = plt.get_cmap('cividis', n_prior_draws)
    fig, ax = plt.subplots()
    list(map(
        lambda i: ax.plot(prior_predictive[i], color=colors(i)),
        range(prior_predictive.shape[0])
    ))

    plt.savefig(figdir / 'state_space_prior_predictive.png', bbox_inches='tight')

    #######

    # as far as inference goes, actually just a diagonal normal should be ok..
    data_N = 100
    data_T = 50
    data = state_space_model(None, N=data_N, T=data_T, verbose=True)
    guide = pyro.infer.autoguide.AutoDiagonalNormal(state_space_model)
    optim = pyro.optim.Adam({'lr': 0.01})
    svi = pyro.infer.SVI(state_space_model, guide, optim, loss=pyro.infer.Trace_ELBO())

    niter = 2500  # or whatever, you'll have to play with this and other optim params
    pyro.clear_param_store()
    losses = torch.empty((niter,))

    for n in range(niter):
        loss = svi.step(data, N=data_N, T=data_T)
        losses[n] = loss

        if n % 50 == 0:
            print(f"On iteration {n}, loss = {loss}")

    # you can extract the latent time series in a variety of ways
    # one of these is the pyro.infer.Predictive class
    num_samples = 100
    posterior_predictive = pyro.infer.Predictive(
        state_space_model,
        guide=guide,
        num_samples=num_samples
    )
    posterior_draws = posterior_predictive(None, N=data_N, T=data_T)

    # since our model returns the latent, we should have this in the `latent` value
    print(
        posterior_draws['latent'].squeeze().shape == (num_samples, data_T, data_N)
    )


if __name__ == "__main__":
    main()
