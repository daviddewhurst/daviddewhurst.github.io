# `lppl`

Open-universe probabilistic programming in (almost modern) C++, done in exactly the idiosyncratic way that I want to do it

+ Record-based (which essentially means trace-based, but we don't hide the tracing from you)
+ Sample-based, with posterior queries by default computed online rather than after sampling is complete (resulting in potentially `O(1)` memory use rather than `O(N)`)
+ Explicit PRNG state (reproducibility)
+ Algebraic sum types (`std::variant`) everywhere instead of boxing (`std::any`)

Open-source (LGPL3), available at [this webpage](https://gitlab.com/drdewhurst/lppl/-/tree/develop).

### Examples

Here's a very basic normal model with a latent `loc` and `log_scale`:

```
double normal_model(record_t<Normal>& r, double obs_val) {
    auto loc = sample(r, "loc", Normal(0.0, 4.0), rng);
    auto log_scale = sample(r, "log_scale", Normal(0.0, 1.0), rng);
    return observe(r, "obs", Normal(loc, std::exp(log_scale)), obs_val);
}
```
You can do inference on it as follows:
```
auto q = weighted_mean<double, Normal>("loc");
auto opts = inf_options_t{ .num_iterations=2000 };
double obs = -3.0;
std::function<double(record_t<Normal>&, double)> f = normal_model;
auto post_mean = likelihood_weighting(f, *q, obs, opts);
std::cout << "Posterior mean = " << post_mean << std::endl;
return 0;
```
You wanted to infer the posterior mean of `loc` after observing `data = -3`. When you ran the integration test with the default statically allocated
PRNG, you found that `Posterior mean = -2.61315`, which checks out.

Here's a slightly less trivial model -- a normal mixture model with latent
locs/log-scales:

```
double normal_mixture(record_t<Normal, Gamma, Categorical>& r, double data) {
    auto choice = sample(r, "choice", Categorical(), rng);
    double loc, scale;
    if (choice) {
        loc = sample(r, "+loc", Normal(1.0), rng);
        scale = sample(r, "+scale", Gamma(), rng);
    } else {
        loc = sample(r, "-loc", Normal(-2.0), rng);
        scale = sample(r, "-scale", Gamma(2.0, 0.5), rng);
    }
    return observe(r, "data", Normal(loc, scale), data);
}
```
You could do inference on it as follows:
```
auto q = QueryerCollection<double, double, WeightedMean, Normal, Gamma, Categorical>(
    {"+loc", "-loc", "+scale", "-scale"}
);
auto opts = inf_options_t{ .num_iterations=2000 };
double obs = -1.5;
std::function<double(record_t<Normal, Gamma, Categorical>&, double)> f = normal_mixture;
auto post_means = likelihood_weighting(f, q, obs, opts);
std::cout << "Posterior means = " << std::endl;
for (const auto& [k, v] : *post_means) {
    std::cout << k << " = " << v << std::endl;
}
```
Here, you used `QueryerCollection` because you wanted to compute online posterior statistics about multiple latent random variables. When you ran the integration tests, you found that 
```
Posterior means = 
+scale = 1.09068
-scale = 0.885052
-loc = -1.72004
+loc = -0.46946
```
which again checks out.

### Inference

`lppl` currently supports only the most basic of inference algorithms: likelihood weighting and ancestor Metropolis. Happily, both methods can be trivially used to do inference with open-universe models, though they're very inefficient (well, more precisely, they rely on the quality of the prior distribution).

### Coming attractions
+ optionally zero dynamic allocation (yes, even in open-universe models)
+ other inference algorithms (generic importance sampling, particle filtering, more precise MCMC methods...)
    + some inference algorithms may end up going in separate libraries, since they might depend on external libraries (e.g., [Adept](http://www.met.reading.ac.uk/clouds/adept/) for neural network-based inference). This is all very hypothetical anyway.
+ more query types, and composability of queries

Documentation pages coming Real Soon Now (TM), but for now all header files have documentation, so read that.