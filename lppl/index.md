# `lppl`

Open-universe probabilistic programming in (almost modern) C++, done in exactly the idiosyncratic way that I want to do it.

+ Record-based (which essentially means trace-based, but we don't hide the tracing from you)
+ Sample-based, with posterior queries by default computed online rather than after sampling is complete (resulting in potentially `O(1)` memory use rather than `O(N)`)
+ Explicit PRNG state (reproducibility)
+ Algebraic sum types (`std::variant`) everywhere instead of boxing (`std::any`)

Here's a familiar friend:

```cpp
template<size_t N>
std::tuple<double, double> linear_regression(record_t<Normal, Gamma>& r, std::shared_ptr<data_1d<N>> data) {
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

> ⚠️ Versions of `lppl` greater than v0.9.0 have changed licenses from LGPL3 to GPL3. If you are using `lppl` in your proprietary closed-source software please pin the version at v0.9.0 or earlier, or [contact us](mailto:lppl@davidrushingdewhurst.com) regarding a license exception.

## Details

+ [About](./about/index.md)
+ [Examples](./examples/index.md)
+ [Tests](https://gitlab.com/drdewhurst/lppl/-/tree/master/test)

### Inference

`lppl` supports the following inference algorithms:

+ importance sampling
    + likelihood weighting
    + generic importance sampling with user-defined proposal
+ metropolis-hastings
    + ancestor metropolis
    + generic metropolis with user-defined proposal
+ generic filtering

More algorithms to come...

### Coming attractions
+ optionally zero dynamic allocation (yes, even in open-universe models)
+ other inference algorithms (CSIS, ADVI, ...)
    + some inference algorithms may end up going in separate libraries, since they might depend on external libraries (e.g., [Adept](http://www.met.reading.ac.uk/clouds/adept/) for neural network-based inference). This is all very hypothetical anyway.
+ more query types, and composability of queries