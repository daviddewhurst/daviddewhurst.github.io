---
layout: page
title: stsb2 documentation
description: stsb2 documentation
---

# `effects`

## `Effect`
A context manager that changes the interpretation of an STS call.
    



## `ForecastEffect`
Effect handler for forecasting tasks.

From start to finish, the forecast operation consists of 
+ turning off caching
+ fast-forwarding time
+ (possibly) intervening on all free parameters
+ calling sample
+ (possibly) reverting free parameter values
+ reversing time
+ resuming caching

Args:
    root (block): the root of the STS graph
    Nt (int >= 1): number of timesteps to forecast



## `InterveneEffect`
Effect handler for intervening on a single STS node.

+ Replace the node's free parameters with kwargs
+ <perform some operations>
+ Reset to original free parameter values

Args:
    node (Block): node on which to intervene
    kwargs (dict): {param_name: new_param_val, ...}



## `ProposalEffect`
Effect handler for evaluating proposals.

From start to finish, the proposal operation consists of
+ intervening on each free parameter
+ turning off caching
+ <sampling and other operations>
+ turning on caching
+ replacing old parameter values

Args:
    root (Block): the root of the STS graph



## `_effect_call`
Turns an effect handler defined as a context manager into a callable.

Args:
    obj (Effect): an effect
    fn (callable): a callable


## `_forecast_off`
Reverses a Block-like object from forecast to sample mode.

This does three things:
1. t1 -> t0
2. t0 -> old t0
3. ic -> old ic


## `_forecast_on`
Fast-forwards a Block-like object from sample to forecast mode.

This does three things:
1. t0 -> t1
2. t1 -> t1 + Nt
3. ic -> final condition (last value of cached draw)


## `effect`
Convert an Effect object into a function decorator.

Args:
    obj (Effect): an effect handler

Returns:
    effect (callable): a decorator


# `inference`

## `ABCDistanceMetric`
A distance metric for use in approximate sampling.

All `ABCDistanceMetric` must implement `accept(...)`, which returns 
an array of indices of the sample that should be accepted.

*Args:*

eps (EpsilonStrategy): the threshold class

eps_kwargs (dict): keyword arguments to pass to the EpsilonStrategy

### `accept`
None



## `ABCPosterior`
A posterior object for ABC computations.

Users will generally not create instances of this class. Instances are 
returned by ABCSamplers after sampling. 

*Usage:*

```
p_z = ABCPosterior(...)
some_samples = p_z[sub_series][param_name]
```
where `sub_series` is a Block that is a parent of, or is, the originally
passed `series` object, and `param_name` is a parameter name of the sub series.

*Args:*

series (Block): the model for which the posterior was calculated

samples (numpy.ndarray): samples from the approximate posterior.



## `ABCSampler`
See the documentation of Sampler.

Uses approximate Bayesian computation rejection sampling to sample from the 
approximate posterior / posterior predictive distributions. Should only be used
when data is already observed since draws from the prior can be made with calls
to `series(...)`.

*Args:*

series (Block): the root of the DGP

data (numpy.ndarray): the observed data

guide (Guide): the proposal distribution

metric (Metric): initialized acceptance metric object

niter (int >= 0 || None): number of iterations for which to run sampler

nsample (int >=0 || None): number of draws to make. If this argument is
    not None, then `niter` is not used

verbosity (float >= 0): status messages are printed `verbosity` fraction
    of the time

### `_empirical_joint`
None

### `_lv_sample`
None

### `_mc_sample`
None

### `sample`
Samples from the approximate posterior. 

If `nsample` is passed, then a las vegas sampling algorithm is used
(the sampler will return `nsample` draws, but there is no time bound
on how long this will take). If `nsample` is None and `niter` is an 
integer, then a monte carlo sampling algorithm is used (the sampler
will run for only `niter` iterations and a random number >= 0 samples
will be returned)

*Args:*

nsample (int >= 0 || None): number of samples to draw

niter (int >= 0 || None): number of iterations to run the sampler



## `AutoGuide`
A `Guide` that attempts to automate the definition of distributions. 

`AutoGuide` tries to define a distribution for each free parameter in the graph it's
tracking. If it's unable to do this, it tags that parameter as unmodeled for later
custom modeling.

*Args:*

root (Block): a block. Will be treated as the root of a graph and all predecessor 
    nodes in the graph will be tracked.

### `lpdf`
See documentation of Distribution1D.lpdf(...)

log p = \sum_n \log p_n, where the sum runs over all free
parameters of the underlying STS graph.

*Args:*

draw (numpy.ndarray): a draw from the `Guide`

### `sample`
See documentation of ProductDistribution.sample(...)

*Args:*

size (int >= 1): number of draws to sample

### `set_model_rvs`
Sets free parameter values of the underlying STS graph. 

*Args:*

draw (numpy.ndarray): a draw from the `Guide`



## `BetaDistribution1D`
See documentation of Distribution1D.

A beta distribution. 

*Args:*

log_alpha (float): the log of the alpha parameter of the beta distribution

log_beta (float): the log of the beta parameter of the beta distribution

### `_init_dist`
None

### `lpdf`
See documentation of Distribution1D. 
        

### `sample`
See doocumentation of Distribution1D.

*Returns:

sample (numpy.ndarray): shape is (size, len(distributions))

### `update_parameters`
Updates the parameters of the distribution. 

Args:
    kwargs (dict, optional): {param_name: param_value, ...}



## `Bound1D`
Object describing the support of a univariate distribution. 

Bounds must implement __call__, yielding a (lower, upper) tuple, and 
__contains__(...), returning True if lower < ... < upper. Bound1D is
designed to be subclassed.



## `ConstantEpsilon`
See documentation for EpsilonStrategy. 

A fixed, constant epsilon value.

*Args:*

eps (float >= 0.0): the acceptance threshold



## `Distribution1D`
A 1d probability distribution. 

This essentially provides an interface to scipy.stats.<distribution_name> and adds 
the ability to update parameters (useful for, e.g., variational inference).

### `_init_dist`
None

### `lpdf`
Returns the log probability of `x` under the distribution. 

*Args:*

    x (float || numpy.ndarray): a value to score

*Returns:*

    lpdf (float || numpy.ndarray): the log probability of the value

### `sample`
Returns a sample from the distribution. 

Sample is of shape (size,)

*Args:*

    size (int >= 1): number of samples to return

*Returns:*

    sample (float || numpy.ndarray): a sample from the distribution

### `update_parameters`
Updates the parameters of the distribution. 

Args:
    kwargs (dict, optional): {param_name: param_value, ...}



## `EpsilonStrategy`
The strategy for setting the tolerance in ABC.

All `EpsilonStrategy` must implement `__call__`, which returns 
the current epsilon value. 



## `GaussianQuasiLikelihood`
See documentation of QuasiLikelihood. 

A gaussian state space quasilikelihood. 

*Args:*

data (numpy.ndarray): observed data

std_mode (string): one of 'rolling', 'constant'. If 'rolling', will be computed 
    using a windowed rolling standard deviation of the differences of the 
    observed data. If 'constant', will be equal to the standard deviation of the 
    observed data.

### `lpdf`
See documentation of QuasiLikelihood.lpdf(...).

*Args:*

draws (numpy.ndarray): draws from a model

reduce_ (bool): if reduce_, returns the average lpdf



## `Guide`
A `Guide` is a collection of distributions that knows something 
about an underlying graph of blocks. 

It can be used as a prior or as a variational posterior (which is where the name Guide 
comes from, c.f. the Pyro language). `Guide`s contain a collection of `Distribution1D`s
and track the behavior of all `Block`s and free parameters in the compute graph.

*Args:*

root (Block): a block. Will be treated as the root of a graph and all predecessor 
    nodes in the graph will be tracked.



## `Interval`
See documentation of Bound1D.

(lower, upper)



## `LogNormalDistribution1D`
See documentation of Distribution1D.

A log-normal distribution. 

*Args:*

loc (float || numpy.ndarray): the mean of the underlying normal distribution

log_scale (float || numpy.ndarray): the log standard deviation of the underlying 
normal distribution

### `_init_dist`
None

### `lpdf`
See documentation of Distribution1D. 
        

### `sample`
See doocumentation of Distribution1D.

*Returns:*

sample (numpy.ndarray): shape is (size, len(distributions))

### `update_parameters`
Updates the parameters of the distribution. 

Args:
    kwargs (dict, optional): {param_name: param_value, ...}



## `MAEDistanceMetric`
See documentation of ABCDistanceMetric

`(x, y) -> abs(x - y).mean()` is the distance function.

*Args:*

eps (EpsilonStrategy): the threshold class

eps_kwargs (dict): keyword arguments to pass to the EpsilonStrategy

### `accept`
Whether to accept the draws given the data. 

*Args:*

data (numpy.ndarray): observed data

draws (numpy.ndarray): draws from a model

iteration (int >= 0): iteration of sampling

*Returns:

accept (numpy.ndarray): an array of indices of the sample that should be
    accepted



## `MSEDistanceMetric`
See documentation of ABCDistanceMetric

`(x, y) -> ((x - y) ** 2.0).mean()` is the distance function.

*Args:*

eps (EpsilonStrategy): the threshold class

eps_kwargs (dict): keyword arguments to pass to the EpsilonStrategy

### `accept`
Whether to accept the draws given the data. 

*Args:*

data (numpy.ndarray): observed data

draws (numpy.ndarray): draws from a model

iteration (int >= 0): iteration of sampling

*Returns:*

accept (numpy.ndarray): an array of indices of the sample that should be
    accepted



## `NormalDistribution1D`
See documentation of Distribution1D.

A normal distribution. 

*Args:*

loc (float || numpy.ndarray): the mean of the distribution

log_scale (float || numpy.ndarray): the log standard deviation of the distribution

### `_init_dist`
None

### `lpdf`
See documentation of Distribution1D. 
        

### `sample`
See doocumentation of Distribution1D.

*Returns:*

    sample (numpy.ndarray): shape is (size, len(distributions))

### `update_parameters`
Updates the parameters of the distribution. 

Args:
    kwargs (dict, optional): {param_name: param_value, ...}



## `PositiveReal`
See documentation of Bound1D.

(0, infinity)



## `ProductDistribution1D`
See documentation of Distribution1D.

A factorization q(z) = \prod_n q_n(z_n). 

*Args:*

distributions (iterable[Distribution1D]): the 1d distributions

### `_init_dist`
None

### `lpdf`
See documentation of Distribution 1D.

log q(z) = \sum_n log q_n(z_n).

### `sample`
See doocumentation of Distribution1D.

*Returns:*

sample (numpy.ndarray): shape is (size, len(distributions))

### `update_parameters`
Updates the parameters of the distribution. 

Args:
    kwargs (dict, optional): {param_name: param_value, ...}



## `QuasiLikelihood`
A callable that can be treated as the data likelihood function

The idea of a quasilikelihood is that, even though we don't actually know what 
the data likelihood is, we can manufacture a function that is plausible. 
For example, if we observe an unbounded time series, we could conjecture a
noisy observation model that we parameterize as a Gaussian state space model.
All `QuasiLikelihood`s must implement lpdf, which returns the (quasi)likelihood of
draws given the observed data, and `__call__`, which calls `lpdf`.

*Args:*

data (numpy.ndarray): observed data

### `lpdf`
None



## `RealLine`
See documentation of Bound1D.

(-infinity, infinity)



## `Sampler`
Base class for all samplers.

*Args:*

niter (int >=0 || None): number of iterations to run the sampler

nsample (int >= 0 || None): number of draws from the (approximate) posterior

verbosity (float >=0): status messages are printed `verbosity` fraction of
    the time

### `_empirical_joint`
None

### `sample`
None



## `TruncatedNormalDistribution1D`
See documentation of Distribution1D.

A truncated normal distribution. 

*Args:*

loc (float || numpy.ndarray): the mean of the distribution

log_scale (float || numpy.ndarray): the log standard deviation of the distribution

### `_init_dist`
None

### `lpdf`
See documentation of Distribution1D. 
        

### `sample`
See doocumentation of Distribution1D.

*Returns:*

sample (numpy.ndarray): shape is (size, len(distributions))

### `update_parameters`
Updates the parameters of the distribution. 

Args:
    kwargs (dict, optional): {param_name: param_value, ...}



## `dist_suggestion`
Suggests proposal / guide distribution given a Bound.

This is very basic. Suggests a Normal for infinite support, LogNormal for 
half-infinite (positive half-line) support, and Beta distribution for support
on [0, 1]. Returns `None` otherwise.

*Args:*

bound (Bound): the bound for which a distribution is desired

*Returns:*

distribution (Distribution1D): a distribution class


## `gen_str_param_names`
Generates string parameter names.

This is mainly useful for plotting or downstream work in other libraries.

*Args:*

root (Block): a block. Parameter names will be generated for this nodes and all of
    its predecessors in the compute graph.

*Returns:*

names (list[string]): list of parameter names


# `stsb`

## `AR1`
An autoregressive process of order 1.

The DGP for AR1 is `f(t) = beta * f(t - 1) + scale * e(t), f(0) = ic`, 
where `e` is a standard normal distributed vector. Both beta and scale can be 
univariate parameters, multivariate parameters, or `Block`s.

Args:
    t0 (int): start timepoint
    t1 (int): end timepoint
    beta (None || Block || float || numpy.ndarray): if None, beta is distributed standard normal
    scale (None || Block || float || numpy.ndarray): if None, scale is distributed standard 
        lognormal.
    ic (None || float || numpy.ndarray): if None, ic is distributed standard normal

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `AddedBlock`
The result of adding two blocks together.

If `x` and `y` are two `stsb.Block`s, then `z = x + y` means that `z` is an `AddedBlock`.
A call to `z.sample(...)` returns the result of `left.sample(...) + right.sample(...)`.

Args:
    left (Block): the left addend
    right (Block): the right addend

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `Block`
Base class for all STS blocks.

Args:
    t0 (int): start timepoint
    t1 (int): end timepoint
    is_cached (str): whether to give sampling a cached interpretation.
        If `is_cached`, subsequent calls to `.sample(...)` after the first
        will replay the result of the first call. This behavior will
        occur until the cache is reset (with `util.clear_cache(...)` or
        `self.clear_cache(...)`)

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `ChangepointBlock`
Generates a single block combining two distinct block behaviors with a changepoint

Suppose `u` and `v` are two blocks and `w = ChangepointBlock(u, v)`.
Then this is equivalent to sampling from `u` from `t0` to `t^*`, sampling from `v` 
from `t^*` to `t1`, and concatenating the result into a single array.
The changepoint `t^*` is a free parameter to be set.
It is set by the continuous parameter `frac` which must be bounded between 0 and 1.
The changepoint is defined by `t^* = int(frac * (t1 - t0))`. A call to `forecast(...)` 
is equivalent to calling `right.forecast(...)`.

Args:
    left (Block): the left block in the changepoint, values of this before `t^*` will be used
    right (Block): the right block in the changepoint, values of this after `t^*` will be used
    frac (float, optional): the fractional position of the changepoint

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `GlobalTrend`
Implements a global trend model.

The DGP of GlobalTrend is `f(t) = a + b * t`. Both `a` and `b` can be univariate parameters,
multivariate parameters, or `Block`s. 

Args:
    t0 (int): start timepoint
    t1 (int): end timepoint
    a (None || Block || float || numpy.ndarray): if None, a is drawn from a standard normal.
    b (None || Block || float || numpy.ndarray): if None, b is drawn from a standard normal.

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `MA1`
A moving average of order 1.

The DGP for MA1 is `f(t) = loc + e[t] + theta * e[t - 1]`, where `e ~ Normal(0, scale^2)`. 
Each of loc, scale, and theta can be univariate parameters, multivariate parameters, or `Block`s.

Args:
    t0 (int): start timepoint
    t1 (int): end timepoint
    loc (None || Block || float || numpy.ndarray): if None, loc is distributed standard normal.
    scale (None || Block || float || numpy.ndarray): if None, scale is distributed standard 
        lognormal.
    theta (None || Block || float || numpy.ndarray): if None, theta is distributed standard normal.

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `NonMarkovBlock`
Block that depends on its sample history. 

This block should be subclassed and is nonfunctional on its own.

Args:
    t0 (int): start timepoint
    t1 (int): end timepoint
    is_cached (str): whether to give sampling a cached interpretation.
        If `is_cached`, subsequent calls to `.sample(...)` after the first
        will replay the result of the first call. This behavior will
        occur until the cache is reset (with `util.clear_cache(...)` or
        `self.clear_cache(...)`)

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `RandomWalk`
Implements a random walk with drift. 

The DGP of RandomWalk is `f(t) = f(t - 1) + loc + scale * w(t), f(0) = ic`, where
`w` is standard normal distributed. Both loc and scale can be univariate parameters,
vector parameters, or `Block`s to implement composition.

Args:
    t0 (int): start timepoint
    t1 (int): end timepoint
    loc (None || Block || float || numpy.ndarray): if None, loc will be drawn from a standard normal
    scale (None || Block || float || numpy.ndarray): if None, scale will be drawn from a standard
        lognormal
    ic (None || float || numpy.ndarray): the initial condition. 

### `_forecast`
See documentation of `forecast(...)` and `effects.ForecastEffect`.
        

### `_maybe_add_blocks`
Adds parameters to prec and succ if they subclass Block.

Args:
    *args: iterable of (name, parameter, bound) 

### `_sample`
None

### `_transform`
Defines a transform from a string argument.

Currently the following string arguments are supported:
    + exp
    + log
    + logit
    + invlogit
    + tanh
    + arctanh
    + invlogit
    + logit
    + floor
    + sin
    + cos
    + softplus
    + diff (lowers time dimemsion by 1)
    + logdiff (lowers time dimension by 1)

The resulting transform will be added to the transform stack iff
it is not already at the top of the stack.

Args:
    arg (str): one of the above strings corresponding to function

Returns:
    self (stsb.Block)

### `arctanh`
x -> arctanh(x), i.e. x -> 0.5 log ((1 + x) / (1 - x))
        

### `clear_cache`
Clears the block cache.

This method does *not* alter the cache mode.

### `cos`
x -> cos x
        

### `diff`
x -> x[1:] - x[:-1]

Note that this lowers the time dimension from T to T - 1.

### `exp`
x -> exp(x)
        

### `floor`
x -> x - [[x]], where [[.]] is the fractional part operator
        

### `forecast`
Forecasts the block forward in time. 

Forecasting is equivalent to fast-forwarding time, using possibly-updated parameter estimates,
and calling sample(...).

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast

### `forecast_many`
Draw many forecast paths.

Args:
    size (int >= 1): number of forecast paths
    Nt (int >= 1): number of timesteps forward to forecast
    ic (float || numpy.ndarray): initial condition, optional. If not set,
        will be set to the last observed / simulated value of the block.

Returns: (numpy.ndarray) array of shape (size, ic.shape[0], t1 - t0)
    

### `invlogit`
x -> 1 / (1 + exp(-x))
        

### `log`
x -> log x 

Block paths must be positive for valid output.

### `logdiff`
x -> log x[1:] - log x[:-1]

NOte that this lowers the time dimension from T to T - 1.

### `logit`
x -> log(x / (1 - x))
        

### `parameter_update`
Updates the parameters of the block.

This method should be used with caution as it can change the type, dimension, etc
of any parameter that is passed and does not perform any safety checks.
Passed values can be 
    + numeric types
    + `numpy.ndarray`s
    + `stsb.Block`s

Args:
    **kwargs: `parameter_1_name=parameter_1_value, ...`

### `prec`
Returns the predecessor nodes of `self` in the (implicit) compute graph

Returns:
    _prec (list): list of predecessor nodes

### `sample`
Draws a batch of `size` samples from the block.

Args:
    size (int): batch size

Returns:
    draws (numpy.ndarray) sampled values from the block

### `sin`
x -> sin x
        

### `softplus`
x -> log(1 + exp(x))
        

### `succ`
Returns the successor nodes of `self` in the (implicit) compute graph

Returns:
    _succ (list): list of successor nodes

### `tanh`
x -> tanh(x), i.e. x -> (exp(x) - exp(-x)) / (exp(x) + exp(-x))
        



## `_add_fns_to_repr`
None


## `_apply_fns`
None


## `_is_block`
None


## `_make_1d`
None


## `_make_2d`
None


## `changepoint`
Functional endpoint to changepoint block creation. 

Args:
    left (Block): the left block in the changepoint
    right (Block): the right block in the changepoint
    frac (float, 0 < frac < 1): where the changepoint is on interval (t0, t1)

Returns:
    ChangepointBlock(left, right, frac=frac)


## `get_id`
Assign the uid of a Block.

Args:
    obj (Block): block to which you want to assign a uid.

Returns:
    id_ (string): the block's uid


## `get_timesteps`
Get the number of timesteps over which the block is defined.

Args:
    obj (Block): block from which you want the number of timesteps

Returns:
    timesteps (int > 0): number of timesteps over which the block is defined


## `set_time_endpoints`
Set time endpoints of block. 

Args:
    obj (Block): block for which you want to set timepoints
    t0 (int): initial time
    t1 (int): end time


# `util`

## `_constant_std`
None


## `_rolling_std`
None


## `clear_cache`
Clears cache of all predecessor nodes of root.
This does *not* reset the cache mode of any node;
to turn off caching, call `set_cache_mode(root, False)`

*Args:*

root (Block): a block


## `get_all_values`
Gets current value of all parameters in the model.

*Args:*

nodes (list[Block]): list of all blocks in the model

param_names (list[string]): list of all block param names in the model

*Returns:*

values (list): list of all current param values


## `get_free_parameters_from_root`
Gets all free parameter values from the root and its predecessors

Defines a BFS order on the compute graph. This is one of two functions
that explicitly walk through the compute graph.

*Args:*

root (Block): the root of the STS graph

*Returns:*
    
return (tuple[list]): (nodes, parameter names, parameter bounds)


## `get_nodes_from_root`
Returns the root and all its predecessors in the graph.

Defines a BFS order on the compute graph. This is one of two functions
that explicitly walk through the compute graph.

*Args:*

root (Block): the root of the STS graph

*Returns:*

nodes (tuple[list]): root and predecessor nodes in the graph


## `roll_op`
Rolls an operation along an array.

*Args:*

arr (numpy.ndarray): original array

op (callable): reduction function

window_size (int >= 2): size of the subarrays to pass to `op`

op_args (list): non-keyword arguments to pass to op

output_size (string): one of 'same', 'valid'

pad (string): currently only 'continue' is supported

op_kwargs (dict): keyword arguments to pass to op

*Returns:*

out (numpy.ndarray): the filtered array


## `set_all_values`
Sets all values to proposed.

*Args:*

proposed (numpy.ndarray): array of proposed param values.
    Shape (p, batch_size) where p is the total number of params
    of the model

nodes (list[Block]): list of all blocks in the model

param_names (list[string]): list of all block param names in the model


## `set_cache_mode`
Sets root and all predecessor nodes cache mode to `cache`.

*Args:*

root (Block): a block

cache (bool): whether or not to cache block calls


