# `glppl`

Translation of [`lppl`](https://davidrushingdewhurst.com/lppl/) probabilistic programs into directed graphical models. 

An `lppl` program to infer the posterior location and scale parameter of a normal distribution could look like this:
```cpp
double normal_model(record_t<Normal, Gamma>& r, double obs) {
    auto loc = sample(r, "loc", Normal(0.0, 1.0), rng);
    auto scale = sample(r, "scale", Gamma(1.0, 0.5), rng);
    return observe(r, "data", Normal(loc, scale), obs);
}
```
The `glppl` version of it looks like this:
```cpp
graph_node<Normal> normal_model(gr_pair<Normal, Gamma>& gr, double obs) {
    auto loc = sample_g<Normal>(gr, "loc", rng)(0.0, 1.0);
    auto scale = sample_g<Gamma>(gr, "scale", rng)(1.0, 0.5);
    return observe_g<Normal>(gr, "data", obs)(loc, scale);
}
```
In return for the miniscule amount of extra complexity, you get a graph data structure 
suitable for static analysis, more specialized inference algorithms, and/or code generation.
You can still use any `glppl` program with `lppl` inference algorithms and queryers
by converting it to a pure sample-based program, e.g. `auto f = to_pp(g);`, where
`g` is a `glppl` program and `f` is an `lppl` program.

`glppl` is also useful for doing inference over open-universe probabilistic programs when you intend to deploy inferred models
for prediction or forecasting. Using `glppl`, you can infer the MLE, MAP, or full posterior over graph structures and choose one or
more of these structures to deploy. In a future version of `glppl`, we intend to implement automatic translation of `glppl` posteriors into
graphical models written in C99 for maximum portability. Stay tuned...

As always, read the [documentation](./docs/index.html), get the [source](https://gitlab.com/drdewhurst/lppl-graph), download [tagged versions](./distros/index.md).

## Install

You need to have a recent version of `lppl`. Running `setup.sh` from the directory into which you cloned
`glppl` will do the trick.

## License etc.

`glppl` is licensed under the GPL v3.
If you would like a license exception, please contact lppl@davidrushingdewhurst.com.

Copyright David Rushing Dewhurst, 2022 - present.