# Continuum rich-get-richer dynamics and survival theory

## Introduction

Rich-get-richer (RGR) processes are a type of growth process that
describe aspects of many objects and phenomena in the natural and social
sciences, e.g., firm size and wealth distributions, citation networks,
protein phosphorylation, and lung injury. We will review the derivation
of a continuous-time, continuous-space version of the RGR process and
then describe connections with survival theory. This article is derived
partially from our papers also contains original research. Throughout we
will be a little cavalier with our notation and assumptions.

If a system evolves according to an RGR process, this means that larger
objects (or objects with more money, more distance, and so on) are more
likely to become still larger. It is useful to first examine a process
that is *not* an RGR process. Suppose we have \\(N\\) objects that are
randomly partitioned into \\(K\\) jars. At each timestep, with equal
probability we select one of the \\(K\\) jars and add an element to that
jar. It is pretty obvious by construction that this process does not
assign higher probability to jars that have more things in them. In
fact, you can work out that this process has an equilibrium distribution
(if you change coordinates to a system that grows linearly in time). You
should see if you can guess (or, hopefully, derive) what that
equilibrium distribution is before reading the rest of this article.

At any rate, a simple modification to this method is as follows: instead
of picking one of the jars at random and adding an element to it, we
will pick one element at random out of the set of all elements, and then
add an element to the jar from which the random element was chosen. This
is a subtle change but has significant consequences for the equilibrium
distribution. This is also the RGR process described by Udny Yule and
Herbert Simon in their seminal papers on this topic.

We would like to know how many groups of size \\(k\\) there are in the
system, where \\(k = 1,2,...\\). We will suppose that the system initially
starts with \\(n_0\\) elements that are in some initial configuration
\\(N_k(0)\\). In addition, we will add the following twist: at each
timestep, with probability \\(\rho\\) the attachment process as we have
just outlined it is in operation. But with probability \\(1 - \rho\\), a
new group forms. We will call \\(\rho\\) the *innovation probability*. You
can probably imagine that it also has a profound effect on the
distribution of group sizes — just think about what the size
distribution must look like if \\(\rho = 1\\) so that every element forms
a new group\! Moving to continuous time (which is a useful approximation
if ticks of the system’s governing clock are close together), the
equation describing the number of groups of size \\(k\\), \\(N_k\\),
is

\\[\frac{dN_k}{dt} = (1 - \rho) [\text{Inflow into group $k$} - \text{Outflow from group $k$}]
    + \rho \delta_{k1}.\\]

We will encode the actual mechanics of the attachment process through a
function \\(r(k)\\), which determines how elements are selected for
replication. We call this function the *attachment kernel*. For example,
the probability that an element from a group with \\(k\\) elements is
selected when using Simon’s mechanism is \\(r(k) = k\\), since each
element has an equal chance of being picked. Using this attachment
kernel, the evolution equation is

\\[\frac{dN_k}{dt} = (1 - \rho) [P_{k-1} - P_k] + \rho \delta_{k1},\\]

where by \\(P_k\\) we mean the probability of choosing for replication an
element from a group of size \\(k\\). What is this probability? It is
proportional to the number of things in each group, which is \\(k\\),
multiplied by the number of these kinds of groups, \\(N_k\\). Hence
\\(P_k = kN_k / \sum_{\ell} \ell N_{\ell} = k N_k / (t + n_0),\\) since
there must be \\(t + n_0\\) elements in the system at time \\(t\\). Thus,
the actual functional form of the evolution equation is (finally)

\\[\begin{aligned}
        \frac{dN_k}{dt} &= (1 - \rho) \left[ \frac{(k-1)N_{k-1}}{t + n_0} - \frac{k N_k}{t + n_0} \right]
    + \rho \delta_{k1}.
    \end{aligned}\\]

This equation actually has a closed-form solution which was communicated
to me by [Babak Fotouhi](https://scholar.harvard.edu/babak_fotouhi/home).
 Finding this solution is an interesting problem,
but we will not consider it during the rest of this article.

In certain contexts, it makes sense to include spatial distance when
describing a system driven by rich-get-richer dynamics. If the distance
between groups is small, then the master equation that we just derived
is well-approximated by a first-order hyperbolic partial differential
equation:

\\[\frac{\partial N(x,t)}{\partial t}
    = -\frac{1 - \rho}{t + n_0} \frac{\partial}{\partial x}[r(x)N(x,t)] + \rho \delta(x - x^*).\\]

This equation is defined on the half-open interval
\\(x\in [x_0, \infty)\\) where \\(x_0 > 0\\). We are being as general as
possible and so now are including the arbitrary attachment kernel
\\(r(x)\\) instead of just the Simon kernel \\(r(x) = x\\). In passage to
the continuum spatial limit, the Kronecker delta has become a Dirac
delta. When \\(x \gg x_0\\) and \\(\rho \ll 1\\), the tail of \\(N(x,t)\\) is
approximately given by the solution to the simpler equation

\\[\frac{\partial N(x,t)}{\partial t}
    = -\frac{1 - \rho}{t + n_0} \frac{\partial}{\partial x}[r(x)N(x,t)].\\]

We can solve this equation using separation of variables. We assume that
the solution scales as the product of function of time only and of a
probability distribution, \\(N(x,t) = T(t)p(x)\\). The PDE decouples into
two equations,

\\[(t + n_0)\frac{\dot{T}(t)}{T(t)} = \lambda = 
    -\frac{(1 - \rho)}{p(x)} \frac{d}{dx}[r(x)p(x)].\\]

The ODE in time has the solution \\(T(t) \propto (t + n_0)^{\lambda}\\),
while the spatial ODE has \\(p(x) = \mathcal{N}
\frac{1}{r(x)}\exp [ -\int_{x_0}^x \frac{\lambda}{1 - \rho}\frac{1}{r(s)}ds ]\\).
The number \\(\mathcal{N}\\) is a function of the eigenvalue \\(\lambda\\)
and of the innovation rate \\(\rho\\), though as \\(t \rightarrow \infty\\)
we have \\(\lambda \rightarrow 1\\) since the mass in the tail of
\\(N(x,t)\\) grows linearly in time. This number is the partition function
of the probability distribution \\(p(x)\\). Defining the operator
\\(L = -\frac{d}{dx}r(x)\\), we see that the spatial ODE is actually an
eigenvalue equation for this operator:

\\[L[p(x)] = \eta p(x),\\]

where \\(\eta = \frac{1}{1 - \rho} \geq 1\\). 

## Survival theory

We will take a brief detour from the discussion of continuum RGR
processes to outline some elements of survival theory. Fundamentally,
survival theory is just a way of looking at probability theory that asks
the question “how much more” instead of “how much". What we mean by this
is as follows: if \\(p(x)\\) is the pdf of the rv \\(X\\) and \\(P(x)\\) is
its corresponding cdf, \\(P(x) = \int_{x_0}^x p(s)\ ds\\), then the
*survival function* of \\(X\\) is
\\(P_{\geq}(x) = 1 - P(x) = \int_{x}^{\infty}p(s)\ ds\\). This function
also goes by the name of complementary cumulative distribution function
(ccdf). Usually we think of the rv \\(X\\) as representing time until some
event, like death of a human, failure of a mechanical part, or natural
disaster. However, \\(X\\) might represent some non-temporal random
variable, such as revolutions until failure, miles driven until
breakdown, or cigarettes smoked until diagnosis. The rv \\(X\\) is
supported on the half-open interval \\(x \in [x_0, \infty)\\),
\\(x_0 \geq 0\\), since quantities in which we are interested are usually
in the future (temporal) or intrinsically non-negative, e.g., distance.

We are interested in the instantaneous probability of failure. That is,
given that we have not yet observed a failure event at \\(x\\), we want to
know the probability that a failure event occurs in the interval
\\([x, x + dx)\\):

\\[\lambda(x) \equiv p_{X \in [x, x + dx) | X \geq x}(x)
    = \frac{p(x)}{P_{\geq}(x)}.\\]

We call \\(\lambda(x)\\) the *hazard function* or hf for short. It is the
case that an rv is uniquely characterized by its hf. If we integrate
\\(\lambda(x)\\), we find
that

\\[\Lambda(x) \equiv \int_{x_0}^x \lambda(s)\ ds = \int_{x_0}^x \frac{p(s)}{P_{\geq}(s)}\ ds
    = -\int_{x_0}^{x}\frac{dP_{\geq}(s)}{P_{\geq}(s)} = - \log P_{\geq}(x),\\]

and hence

\\[P(x) =1 - \exp \left[ -\Lambda(x) \right],\\]

which completes the proof.

From this result we can derive a few facts about hfs. First, they must
not decay to zero too quickly. We must have
\\(\Lambda(x) \rightarrow \infty\\) as \\(x \rightarrow \infty\\), because
\\(P(x) \rightarrow 1\\) as \\(x \rightarrow \infty\\) by the definition of
a cdf. For example, \\(\lambda(x) = \frac{1}{x^2}\\) is not the hf of any
atomless distribution with support on \\([x_0, \infty)\\) since
\\(\Lambda(x) = \int^x \frac{1}{s^2}\ ds = \frac{1}{x}\\), which does not
diverge as \\(x \rightarrow \infty\\). We will return to this explicit
example later in this article. Second, the shape of the hazard function
encodes explicit facts about the failure modes of the system under
study. When \\(\lambda(x) \rightarrow 0\\) monotonically as
\\(x \rightarrow \infty\\), the system exhibits “infant mortality”
failure; new parts with low usage are more likely to fail, but with
increased useage the parts are less likely to fail. In contrast, when
\\(\lambda(x) \rightarrow \infty\\) as \\(x \rightarrow \infty\\), older
parts are increasingly likely to fail. In real systems, hfs are often
modeled as the sum of three distinct
functions:

\\[\lambda(x) = \lambda_{\text{burn in}}(x) + \lambda_{\text{random}}(x) + 
    \lambda_{\text{wear out}}(x).\\]

  - \\(\lambda_{\text{burn in}}(x)\\) describes burn-in or infant
    mortality and is a monotone decreasing function;

  - \\(\lambda_{\text{random}}(x)\\) describes random failure and is
    constant; and

  - \\(\lambda_{\text{wear out}}(x)\\) describes wear-out or repetitive
    usage failure and is a monotone increasing function.

We display pdfs corresponding to each of these types of hf in the figure
below.

![Hazard functions uniquely characterize pdfs. We display three pdfs
that correspond to three qualitatively different hazard functions:
monotone decreasing, constant, and monotone
increasing.](hf2pdf-examples.png)

Though it is easy to differentiate between the pdf corresponding to the
monotone increasing hf \\(\lambda_{\text{wear out}} = cx\\) and the
others, it is not as easy to visually distinguish between the pdfs
corresponding to \\(\lambda_{\text{random}} = c\\) and
\\(\lambda_{\text{burn in}} = c/x\\). We therefore display these same pdfs
in doubly logarithmic space below.

![ We display the same pdfs as above but in doubly-logarithmic space.
](hf2pdf-examples-loglog.png)

## RGR processes and survival theory

Now that we have a brief common background on the basics of survival
theory, we will discuss the connections between the stationary
distribution (again, stationary in the linearly-growing coordinate
system) of the RGR process and some quantities that we have derived
above. We present these connections here because we have never seen them
referenced in any paper on the subject of either RGR (or preferential
attachment) processes or in the survival theory literature; if you are
familiar with such references, we would appreciate your sharing them
with us\!

We showed that the eigenvalue equation describing the stationary
distribution, \\(L[p(x)] = \eta p(x)\\), had the solution

\\[p(x) = \mathcal{N}
\frac{1}{r(x)}\exp [ -\int_{x_0}^x \eta \frac{1}{r(s)}ds ].\\]

Integrating this equation, we see that

\\[P_{\geq}(x) \propto \exp[ - \int_{x_0}^x \eta \frac{1}{r(s)}ds],\\] and
hence that the hf for the rv \\(X\\), \\(\lambda(x)\\), must be
\\(\lambda(x) = \eta /r(x)\\). Using this result, we can immediately
observe several interesting facts:

  - No RGR process that is actually well-defined over the entire
    semi-infinite interval \\([x_0, \infty)\\) can have an attachment
    kernel that scales as any monomial \\(r(x) \propto x^\alpha\\) with
    \\(\alpha > 1\\). If this were possible, then
    \\(\Lambda(x) \propto \int \frac{1}{r(x)} dx \propto 
            x^{-(\alpha - 1)}\\), which decays to zero as
    \\(x \rightarrow \infty\\). Hence \\(\Lambda(x)\\) is not a cumulative
    hazard function, which is a contradiction.

  - What this actually means is that, if a measured \\(r(x)\\) of an RGR
    process does grow like \\(x^{\alpha}\\) with \\(\alpha > 1\\), at least
    one of the two following statements is true:
    
      - The system described by the RGR process has an upper bound on
        the rv \\(X\\).
    
      - The true \\(r(x)\\) eventually scales more slowly than
        \\(x^{\alpha}\\) for large enough values of \\(x\\).
    
    If realized values of \\(X\\) are actually bounded above by \\(y\\),
    then \\(r(x)\\) can grow as fast as it wants for \\(x < y\\) since
    \\(r(x) = 0\\) for all \\(x \geq y\\). The estimator of \\(r(x)\\)
    constructed from \\(N\\) observations \\(X_1,...,X_N\\) can certainly
    scale as \\(x^{\alpha}\\) with \\(\alpha > 1\\) since by definition they
    will all be less than or equal to \\(y\\). On the other hand, if the
    system actually does not have an upper bound (for example,
    accumulation of nominal wealth by economic agents), then the true
    RGR kernel must surely eventually grow more slowly than
    \\(x^{\alpha}\\) with \\(\alpha > 1\\).

  - Every existing method for estimating the hazard function from data
    can now be used to measure the RGR kernel from data. We will
    consider a few common nonparametric methods for estimating the
    hazard function presently and demonstrate their applicability in
    estimating \\(r(x)\\).

  - The mechanism behind the RGR process (or, more generally, behind the
    continuum growth process with \\(r(x)\\) not necessarily exhibiting
    rich-get-richer behavior) can be seen to apply to many scenarios to
    which survival theory is typically applied.

We will demonstrate how some existing methods of estimating survival or
hazard functions can be used to estimate preferential attachment
kernels. Even though the formal hf - RGR connection is technically valid
only in the continuum asymptotic limit, we will use this correspondence
in the original discrete system context.

Throughout we will suppose that \\(X_1 < X_2 <...< X_N \\) are *observed*
marks at which at least one event (failure, death, wealth level, etc.)
happened. By “marks” we mean times, distances, revolutions, or whatever
else is being measured as a quantity until failure random variable. At
the \\(n\\)-th mark, \\(d_n\geq 0\\) failure events occur. (If time is
continuous, \\(d_n =1 \\) almost surely.) A total of \\(K_n\\)
draws from the RGR process have not experienced failure by mark \\(X_n\\).

### Kaplan-Meier estimator

This is a nonparametric method to estimate the sf of the rv \\(X\\) and is
given by

\\[\hat{P}_{\geq}(x) = \prod_{
       	n: X_n < x 
         }
         (1 - d_n/K_n).\\] 

(For some reason the \\(\LaTeX\\) of the above formula won't render. Please inspect
the source of this document and see if you can figure out why; we sure can't.)
The cumulative hazard function can therefore
be estimated by

\\[\hat{\Lambda}(x) = -\sum_{
       	n: X_n < x 
         }    \log (1 - d_n/K_n).\\]

Being somewhat cavalier about our definition of the derivative (we can
make this as formal as we please by an appeal to absolute continuity of
measure and the Radon Nikodym theorem, if we so cared), the RGR kernel
is then approximated by

\\[\hat{r}(x) = -\eta\left[ \frac{d}{dx} \sum_{
       	n: X_n < x 
         }    \log (1 - d_n/K_n) \right]^{-1}.\\]

### Nelson - Aalen estimator

Looking at the cumulative hazard function estimator version of the
Kaplan - Meier estimator, \\(\hat{\Lambda}(x) = -\sum_{
       	n: X_n < x 
         }    \log (1 - d_n/K_n)\\), we notice that \\(\log(1 - y) \approx -y\\) for
small \\(y\\). Using this substitution, we arrive at the alternative
cumulative hazard estimator

\\[\hat{\Lambda}(x) =  \sum_{
       	n: X_n < x 
         }        d_n/K_n.\\]

Applying a similar argument, we have

\\[\hat{r}(x) = \eta\left[ \frac{d}{dx} \sum_{
       	n: X_n < x 
         }    d_n/K_n \right]^{-1}\\]

Let’s take a look at these hf estimators applied to some manufactured
datasets. We will draw values from three distributions, one calm (folded
normal) and two leptokurtic (fatigue-life and pareto).

![ Kaplan-Meier and Nelson-Aalen hazard function estimators applied to
draws from a folded normal distribution. ](./hf-estimators-foldnorm.png)

![ Kaplan-Meier and Nelson-Aalen hazard function estimators applied to
draws from a fatigue life distribution.
](./hf-estimators-fatiguelife.png)

![ Kaplan-Meier and Nelson-Aalen hazard function estimators applied to
draws from a pareto distribution. ](./hf-estimators-pareto.png)

Already we can see the problem: we are 1) taking the derivative of a
noisy process and 2) subsequently taking the reciprocal of that
derivative. These operations are guaranteed to add noise — potentially a
*lot* of noise — to the estimated quantity. And that’s exactly what’s
happening here: the hf estimators of the leptokurtic distributions are
fine for low values of \\(x\\) but are dominated by noise in higher ranges
of \\(x\\). It becomes essentially impossible to discern the mean function
of the estimated hf.

### Multi-stage estimation

We’ll find a different way of estimating \\(r(x)\\). Namely, we’ll compute
an estimator of \\(\Lambda(x)\\) and then apply some method to recover a
smooth function approximation to the noisy estimator. Differentiating
and taking the reciprocal of this smooth function *should* work a little
better than the approach we tried above.

We will illustrate this approach using some simulated rich-get-richer
processes. We simulate four RGR processes in discrete time for
\\(N_t = 2\times 10^4\\) timesteps with an innovation rate of
\\(\rho = 0.1\\) and four different attachment kernels,
\\(r(x) \in \\{ 1, \log(x + 1), x^{2/3}, x \\}\\). These attachment kernels
lead to qualitatively different functional forms of the failure pdf
\\(p(x)\\), as you can verify through substitution and integration. (If
you do attempt to do this, you’ll find yourself computing the integral
\\(\int_{x_0}^x \frac{ds}{\log(s + 1)}\\), which isn’t expressible
analytically. This is called, creatively, the logarithmic integral
function. As \\(x\\) grows large, this function increasingly behaves like
\\(x/\log x\\).) We simulated these processes using rgr\_models.py, which
you can use yourself to run other simulations. We then calculated the
Nelson - Aalen estimator of the cumulative hazard function for each
process, which we display below.

![ Estimated cumulative hazard functions using the Nelson - Aalen
estimator. These hazard functions correspond to the displayed RGR kernel
\\(r(x)\\). ](est-cumhf-from-rgr-sim.png)

In order to avoid assuming a functional form for the RGR kernel
(remember, we’re pretending that we don’t actually know how the data
were generated, only that we hypothesize that an RGR mechanism is at
work) we will use a nonparametric method to infer smooth functions with
these estimators. We model the estimated cumulative hazard functions
using Gaussian processes with RBF kernel functions and display the
results of this estimation in the below figure.

![ Gaussian process-smoothed cumulative hazard functions.
](est-cumhf-using-gp.png)

We display the mean function of the Gaussian process in solid curves and
the standard deviation of the process in the shaded regions. To be
clear, the standard deviation is omly the standard deviation of the
latent cumulative hazard function, *not* the standard deviation of any
noise added to the latent cumulative hazard function. Since draws from
Gaussian processes with RBF kernels are infinitely differentiable, we
shouldn’t (emphasis on shouldn’t) have much of an issue with
differentiating and taking the reciprocal of these functions. One more
techncial note: since we actually fit the Gaussian process in log -
linear space, we have to compute the RGR kernels using
\\(\frac{d\Lambda(x)}{dx} =
\frac{d\Lambda(\log_{10}x)}{d\log_{10}x} \frac{1}{\log(10) x}\\). With
this in mind, we compute the estimated RGR kernels and display them
below along with the true \\(r(x)\\). We plot the estimated kernels in
solid curves and true kernels in dashed curves.

![Estimated \\(r(x)\\) using Gaussian processes. Not terrible for
literally no parameter tuning or
optimization\!](est-rgrkernel-using-gp.png)

Not terrible for literally no (hyper)parameter tuning or optimizations.
There are definitely some issues, though. For example, in the
non-rich-get-richer (or rich just stay pretty rich) case where
\\(r(x) \propto 1\\), the estimated kernel oscillates a little around the
true function — if we designed our estimation procedure a little better,
we could probably eliminate these oscillations.

In short, we have shown a way to estimate the rich-get-richer kernel
function that is statistically well-founded and nonparametric. There’s a
fair amount of work to do on tuning this method to be more robust, but
this methodology could be a useful complement to existing algorithms.

## Citations

  - Aalen, Odd. "Nonparametric inference for a family of counting
    processes." The Annals of Statistics (1978): 701-726.

  - Carulli, J. M., and Thomas J. Anderson. "The impact of multiple
    failure modes on estimating product field reliability." IEEE Design
    & Test of Computers 23, no. 2 (2006): 118-126.

  - Dewhurst, David Rushing, Christopher M. Danforth, and Peter Sheridan
    Dodds. "Continuum rich-get-richer processes: Mean field analysis
    with an application to firm size." Physical Review E 97, no. 6
    (2018): 062317.

  - Hamlington, Katharine L., Jason HT Bates, Gregory S. Roy, Adele J.
    Julianelle, Chantel Charlebois, Bela Suki, and Bradford J. Smith.
    "Alveolar leak develops by a rich-get-richer process in
    ventilator-induced lung injury." PloS one 13, no. 3 (2018):
    e0193934.

  - Kaplan, Edward L., and Paul Meier. "Nonparametric estimation from
    incomplete observations." Journal of the American statistical
    association 53, no. 282 (1958): 457-481.

  - Mori, Vitor, Bradford J. Smith, Bela Suki, and Jason HT Bates.
    "Linking Physiological Biomarkers of Ventilator-Induced Lung Injury
    to a Rich-Get-Richer Mechanism of Injury Progression." Annals of
    biomedical engineering 47, no. 2 (2019): 638-645.

  - Nelson, Wayne. "Hazard plotting for incomplete failure data."
    Journal of Quality Technology 1, no. 1 (1969): 27-52.

  - Pham, Thong, Paul Sheridan, and Hidetoshi Shimodaira. "PAFit: A
    statistical method for measuring preferential attachment in temporal
    complex networks." PloS one 10, no. 9 (2015).

  - Price, Derek J. De Solla. "Networks of scientific papers." Science
    (1965): 510-515.

  - Simon, Herbert A. "On a class of skew distribution functions."
    Biometrika 42, no. 3/4 (1955): 425-440.

  - Yachie, Nozomu, Rintaro Saito, Junichi Sugahara, Masaru Tomita, and
    Yasushi Ishihama. "In silico analysis of phosphoproteome data
    suggests a rich-get-richer process of phosphosite accumulation over
    evolution." Molecular & Cellular Proteomics 8, no. 5 (2009):
    1061-1071.

  - Yule, George Udny. "II.—A mathematical theory of evolution, based on
    the conclusions of Dr. JC Willis, FR S." Philosophical transactions
    of the Royal Society of London. Series B, containing papers of a
    biological character 213, no. 402-410 (1925): 21-87.
