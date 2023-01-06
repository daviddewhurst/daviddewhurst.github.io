# About `lppl`

This is a short guide explaining the objectives and background/theory (kind of) of `lppl` and some best practices (painfully!) 
accumulated over time.

## Objectives

`lppl` is a low-resource universal probabilistic programming language (PPL) embedded in modern C++ that uses no third-party libraries.
I wrote/am writing `lppl` because I think it's possible to satisfy three criteria simultaneously:
1. **enable open-universe modeling and inference** -- i.e., embodying and performing inference over models with an *a priori* unbounded number of unobserved random variables. Think statistical inference over a rich space of computer programs.
2. **exhibit high performance in a low-resource environment** -- many operational environments don't support the computing power required to serve (let alone train!) 100 million (let alone billion!) parameter deep neural networks or a constant internet connection for inference in the cloud. Probabilistic programming at the edge should still be possible even with these constraints. 
3. **ensure robustness and deployability** -- you should be able to write a probabilistic program once and compile it for your MBP, an IP camera with 8MB RAM, or a supercomputer -- and be sure that it'll play nicely with existing applications on any of those platforms.

No other existing PPL accomplishes all of these objectives.

## Background/theory

Probabilistic programming elevates the modeling of uncertainty to a first-class programming language construct and automates
inference over these models.
Uncertainty is important because most real-world phenomena are either fundamentally random in nature (e.g., many physical processes)
or are so magnificently complex that the only tractable way to reason about them is to *model* them as being random. 
Automation of inference is important because -- no other way to put it -- doing inference "well" (accurately, as precisely as the data allows, quickly, and memory efficient-ly) is hard. 
It's also almost entirely orthogonal to the modeler's objectives of describing phenomena and asking questions; it's the answers that matter, not how the questions are answered.
Therefore, automating inference lets modelers save precious mental energy.

`lppl` is a record- and sample-based probabilistic programming language (PPL). "Record-based" means that random choices taken during the execution of a
program are recorded in a data structure (the "record") as they are taken. (This is more commonly known as "trace-based", language I eschew for reasons I
describe presently.)
"Sample-based" means that inference is accomplished by drawing random samples from probability distributions.
There are many other ways of implementing PPLs; a good reference on the subject is [van de Meent *et al.* (2018)](https://arxiv.org/abs/1809.10756). 
Briefly, other alternatives include compiling a probabilistic program to a graph data structure as an alternative to a record/trace-based implementation, and
using other inference methods (e.g., message passing, variational inference, discretization and exact inference) as an alternative to sample-based inference.
`lppl` is record- and sample-based for the following reasons:
+ Records enable *easy* expression of open-universe programs. It is either impossible or nearly impossible (depending on how pedantic you want to be) to perform inference on open-universe models using any kind of graph-based compilation. (See [Pfeffer *et al.* (2015)](https://arxiv.org/abs/1509.03564) for a valiant attempt at open-universe inference using factor graph models.) 
+ Record-based algorithms are generally more memory-efficient than graph-based algorithms (though they can also be slower). `lppl`'s implementation of records and inference algorithms ensure that inference and querying are, by default, constant memory complexity. This matters greatly for objectives (2) and (3).
+ Sample-based inference works on any kind of model. Other inference algorithms impose strong restrictions on the types of random variables that can be combined within a probabilistic program. 

Here's a high-level graphic displaying how `lppl` works architecturally. 
I'm not using C++-specific syntax in this diagram because the same architecture could be implemented in any language.

[![](https://mermaid.ink/img/pako:eNqdkk1rwzAMhv-K0a5pGYNCcWEw6GWHMcbKLnEpIlaaUOdjsj0opf99TuJ-ZPQwmkMs5OeVX8s6QNZoAglbxrYQq-VC1SJ8Zd16l_b_tZTSW2IxmTyHfE5MdUaRq4LapG27cVK8JuI9ESs7nU5HGspzylw6LN1O07oo_0HjKbKbkL7iIzEW36gXuW9PvCdO4yrF15WbsfX0HEnxkkTbAf844bEkmm2TKjjTfYJLV1QK1je7cUG73Wjl1kXGzbrPXiw_HMVkh6uLEHkztNk7VQ9sZtDaJeWif5S8NEY-PD5pTSfnI6B_iWsosY6bHU002gKZcS_FTMz-SjvV_0B_KU80ny8ggYq4wlKHSTx0tAJXUEUKZAg18k6Bqo-BQ--az32dgXTsKQHfanS0LDEMcAUyR2NDlnTpGn4bRruf8OMvAp_w7A?type=png)](https://mermaid.live/edit#pako:eNqdkk1rwzAMhv-K0a5pGYNCcWEw6GWHMcbKLnEpIlaaUOdjsj0opf99TuJ-ZPQwmkMs5OeVX8s6QNZoAglbxrYQq-VC1SJ8Zd16l_b_tZTSW2IxmTyHfE5MdUaRq4LapG27cVK8JuI9ESs7nU5HGspzylw6LN1O07oo_0HjKbKbkL7iIzEW36gXuW9PvCdO4yrF15WbsfX0HEnxkkTbAf844bEkmm2TKjjTfYJLV1QK1je7cUG73Wjl1kXGzbrPXiw_HMVkh6uLEHkztNk7VQ9sZtDaJeWif5S8NEY-PD5pTSfnI6B_iWsosY6bHU002gKZcS_FTMz-SjvV_0B_KU80ny8ggYq4wlKHSTx0tAJXUEUKZAg18k6Bqo-BQ--az32dgXTsKQHfanS0LDEMcAUyR2NDlnTpGn4bRruf8OMvAp_w7A)

Blue boxes denote things that the user has to (solid borders) or may choose to (dashed borders) create for themselves.
Namely, the user has to write a probabilistic program that has an input type `I`, an output type `O`, and contains distribution types `Ts...`, has to specify an input to
the program, and may choose to specify additional values that occur within the program.
The green box is the result of a query -- what you get at the end.
The grey boxes are stuff that `lppl` automates for you (though you can certainly implement your own examples of each).

### Probabilistic programs
All probabilistic programs ([`pp_t<I, O, Ts...>`](https://davidrushingdewhurst.com/lppl/docs/record_8hpp_afdf9cf3c04bf7ff49b58b94a963be084.html#afdf9cf3c04bf7ff49b58b94a963be084)) are callables with signature `(record_t<Ts...>&, I) -> O`.
Yes, even purely generative ones take a single input of type `I`. Sorry, that's just how it is, pass an empty tuple or
something if your program really doesn't take any inputs. They output something of type `O`.
They are parameterized over the distribution types `Ts...` contained within them.
This is because it may be possible to specialize inference algorithms or query logic based on the types of distributions the program contains.
For example, a probabilistic program containing only `Normal` distributions is fundamentally different from one that contains both `Normal` and `Gamma` distributions -- in 
the first case, I know that I can create a variational posterior for the program without applying any transformations to any latent rvs, while in the second
case I need to apply a log transform to the `Gamma` rvs.

Probabilistic programs contain at least one [`sample`](https://davidrushingdewhurst.com/lppl/docs/record_8hpp_af77cbf37e8e287b1c525391a1792b1e2.html#af77cbf37e8e287b1c525391a1792b1e2) and/or [`observe`](https://davidrushingdewhurst.com/lppl/docs/record_8hpp_a547ca9c02e881d0db9fa4ec397a7f63a.html#a547ca9c02e881d0db9fa4ec397a7f63a) statement. 
`sample` means you want to sample a value from a probability distribution and store it in the record at the address
that you specified. `observe` means that you observed a value, and you want to score how likely it is against some probability distribution and store it in the record at the address that you specified.

### Effects
You might want to change how your probabilistic program is interpreted. For example, you might want to additionally specify that the value of `"n_clusters"` in your
open-universe clustering model is actually equal to 6 for a particular experiment.
You can apply an [effect](https://davidrushingdewhurst.com/lppl/docs/effects_8hpp.html) to the probabilistic program that changes the interpretation of `sample` and/or
`observe` calls. For example, you could write 
```cpp
auto conditioned_clustering_model = condition(clustering_model, "n_clusters", 6);
```
to achieve the desired outcome here.

### Querying and inference

After you define your model, you probably want to query some of its properties. 
For example, you might want to know the prior or posterior probability distributions over its output values,
or over values sampled at a particular address, or you might want to know the optimal value of a function evaluated with samples
from the posterior.
Though often used jointly in answering operational questions such as these,
querying a probabilistic program and performing inference over that probabilistic program are actually nearly independent activities,
even though many PPLs treat them as nearly synonymous.

In `lppl`, inference corresponds to sampling values from the probabilistic program and assigning weights (real numbers) to those values.
Depending on the inference algorithm used, that weight is either

+ (a monotone function of) the log posterior probability density of that sample -- when the inference algorithm falls into the
importance sampling family
+ equal to zero -- when the inference algorithm uses some variant of Markov chain Monte Carlo (MCMC) algorithm

It is the user's job to understand the semantics of the weight computed by an inference algorithm.
If in doubt, read the documentation!

By default, inference is an online algorithm that has *constant memory complexity* (constant in the number of samples).
Inference algorithms, implemented as subclasses of [`Inference`](https://davidrushingdewhurst.com/lppl/docs/structInference.html),
overload `operator()`. Calling `operator()(I& input)` or `operator()(I& input, P& proposal)` (depending on whether the inference algorithm
used requires a proposal distribution, which is declared using [`has_proposal`](https://davidrushingdewhurst.com/lppl/docs/structhas__proposal.html))
iteratively updates a [`Queryer`](https://davidrushingdewhurst.com/lppl/docs/classQueryer.html) subclass whose job it is to compute the query results.
These queryers can either maintain the constant memory complexity -- e.g., as does [`WeightedMean`](https://davidrushingdewhurst.com/lppl/docs/classWeightedMean.html) -- or can persist samples for later computations.

The green box is what you get as the result of calling the inference algorithm's `operator()` -- the result of a query, which is, you know, what you asked for -- which in
turn will be computed by calling the queryer's [`emit()`](https://davidrushingdewhurst.com/lppl/docs/classQueryer.html#acc4cad1eebb8f9911809f5630a2e14b5) method. 

## Best practices

+ **Probabilistic programs should usually be pure functions.**
This isn't always true, but it's close enough. The reason is pretty simple -- because it's sample-based, `lppl` will run the probabilistic
program potentially many times during inference. If the program has side effects that are changing state in some other part of your software... I don't have to finish
that thought. If it's really important that your probabiistic program interacts with external objects or in some way changes state in other parts of your software,
I recommend adding a `reset()` method or something like that to the external objects, and calling it at the end of the probabilistic program,
so they can revert to their original state every time an execution of the probabilistic program completes.
+ **Inputs should be cheap to copy.** In the spirit of pure functional probabilistic programs, the inputs to them are copied. User be warned.
+ **Know your queryer's memory profile.** By default, inference and querying are constant memory (in the number of samples) operations, enabling indefinite operation
with little memory use. However, this does *not* mean that querying is guaranteed to be constant memory -- the only guarantee is that *inference algorithms*
are constant memory. Many queryers persist samples from the posterior distribution -- e.g., [`WeightedValue`](https://davidrushingdewhurst.com/lppl/docs/classWeightedValue.html), which computes the 
empirical marginal posterior distribution of a single address, or [`WeightedRecord`](https://davidrushingdewhurst.com/lppl/docs/classWeightedRecord.html), which computes the empirical full posterior distribution. These queryers' memory usage scales linearly in the number of samples.


## Examples (just kidding)
Go see the [examples](../examples/index.md) page.