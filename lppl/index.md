# `lppl`

Open-universe probabilistic programming in (almost modern) C++, done in exactly the idiosyncratic way that I want to do it

+ Record-based (which essentially means trace-based, but we don't hide the tracing from you)
+ Sample-based, with posterior queries by default computed online rather than after sampling is complete (resulting in potentially `O(1)` memory use rather than `O(N)`)
+ Explicit PRNG state (reproducibility)
+ Algebraic sum types (`std::variant`) everywhere instead of boxing (`std::any`)

It's open-source and available at [this webpage](https://gitlab.com/drdewhurst/lppl/-/tree/develop). 
There's lots of [documentation](./docs/index.html)! You can also download the latest [tagged version](./distros/lppl-vlatest.zip) of the source, or see [all versions](./distros/index.md). 

> ⚠️ Versions of `lppl` greater than v0.9.0 will change licenses from LGPL3 to GPL3.

### Examples

Go [here](./examples/index.md).

### Inference

`lppl` supports the following inference algorithms:

+ importance sampling
    + likelihood weighting
    + generic importance sampling with user-defined proposal
+ metropolis-hastings
    + ancestor metropolis

More algorithms to come...

### Coming attractions
+ optionally zero dynamic allocation (yes, even in open-universe models)
+ other inference algorithms (particle filtering, more precise MCMC methods...)
    + some inference algorithms may end up going in separate libraries, since they might depend on external libraries (e.g., [Adept](http://www.met.reading.ac.uk/clouds/adept/) for neural network-based inference). This is all very hypothetical anyway.
+ more query types, and composability of queries