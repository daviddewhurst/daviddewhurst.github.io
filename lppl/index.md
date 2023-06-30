# `lppl`

*(Disclaimer -- this page is written for geeks like me. A more publicly accessible explanation of the `lppl` vision is coming soon.)*

Open-universe probabilistic programming in modern C++, done in exactly the idiosyncratic way that I want to do it.

+ Record-based (which essentially means trace-based, but we don't hide the tracing from you)
+ Sample-based, with posterior queries by default computed online rather than after sampling is complete -- defaulting to constant memory complexity
+ Explicit PRNG state (reproducibility)
+ Algebraic sum types everywhere instead of boxing
+ Header-only

This should look familiar.

```cpp
template<size_t N>
std::tuple<double, double> 
linear_regression(record_t<Normal, Gamma>& r, std::shared_ptr<data_1d<N>> data) {
    auto intercept = sample(r, "intercept", Normal(), rng);
    auto slope = sample(r, "slope", Normal(), rng);
    auto scale = sample(r, "scale", Gamma(), rng);
    for (size_t ix = 0; ix != N; ix++) {
        observe(
            r,
            "obs/" + std::to_string(ix),
            Normal(data->x[ix] * slope + intercept, scale),
            data->y[ix]
        );
    }
    return std::make_tuple(intercept, slope);
}

```

`lppl` is open-source and available at [this webpage](https://gitlab.com/drdewhurst/lppl/-/tree/develop). 
There's lots of [documentation](./docs/index.html)! You can also download the latest [tagged version](./distros/lppl-vlatest.zip) of the source, or see [all versions](./distros/index.md). 

## Details

+ [About](./about/index.md)
+ [Examples](./examples/index.md)
+ [Tests](https://gitlab.com/drdewhurst/lppl/-/tree/master/test)

### Associated tools

+ [`glppl`](https://davidrushingdewhurst.com/glppl/) transforms `lppl` programs into probability distributions over directed graphical models.

### Inference

`lppl` supports the following inference algorithms:

+ importance sampling
    + [likelihood weighting](https://davidrushingdewhurst.com/lppl/docs/structLikelihoodWeighting.html)
    + [generic importance sampling](https://davidrushingdewhurst.com/lppl/docs/structImportanceSampling.html) with user-defined proposal
+ metropolis-hastings
    + [ancestor metropolis](https://davidrushingdewhurst.com/lppl/docs/structAncestorMetropolis.html)
    + [generic metropolis](https://davidrushingdewhurst.com/lppl/docs/structGenericMetropolis.html) with user-defined proposal
+ [generic filtering](https://davidrushingdewhurst.com/lppl/docs/structFilter.html) using any inference algorithm to compute updates

More algorithms to come...

### Coming attractions
+ optionally zero dynamic allocation (yes, even in open-universe models)
+ other inference algorithms (CSIS, ADVI, ...)
    + some inference algorithms may end up going in separate libraries, since they might depend on external libraries (e.g., [Adept](http://www.met.reading.ac.uk/clouds/adept/) for neural network-based inference). This is all very hypothetical anyway.
+ more query types, and composability of queries

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />The `lppl` webpage and its subpages are licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
