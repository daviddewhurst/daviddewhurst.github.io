#!/usr/bin/env python

import torch
import pyro
import pyro.distributions as dist


def state_space_model(data, N=1, T=2, prior_drift=0., verbose=False):
    # global rvs
    drift = pyro.sample('drift', dist.Normal(prior_drift, 1))
    vol = pyro.sample('vol', dist.LogNormal(0, 1))
    uncert = pyro.sample('uncert', dist.LogNormal(-5, 1))

    if verbose:
        print(
            f"Using drift = {drift}, vol = {vol}, uncert = {uncert}"
        )

    # the latent time series you want to infer
    # since you want to output this, we initialize a vector where you'll 
    # save the inferred values
    latent = torch.empty((T, N))  # +1 comes from hidden initial condition
    
    # I think you want to plate out the same state space model for N different obs
    with pyro.plate('data_plate', N) as n:
        x0 = pyro.sample('x0', dist.Normal(drift, vol))  # or whatever your IC might be
        latent[0, n] = x0
        
        # now comes the markov part, as you correctly noted
        for t in pyro.markov(range(1, T)):
            x_t = pyro.sample(
                f"x_{t}",
                dist.Normal(latent[t - 1, n] + drift, vol)
            )
            y_t = pyro.sample(
                f"y_{t}",
                dist.Normal(x_t, uncert),
                obs=data[t - 1, n] if data is not None else None
            )
            latent[t, n] = x_t

    return pyro.deterministic('latent', latent)

