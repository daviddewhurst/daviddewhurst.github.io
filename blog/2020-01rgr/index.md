**Continuum rich-get-richer dynamics and survival theory**

Rich-get-richer (RGR) processes are a type of growth process that
describe aspects of many objects and phenomena in the natural and social
sciences, e.g., firm size and wealth distributions, citation networks,
protein phosphorylation, and lung injury. We will review the derivation
of a continuous-time, continuous-space version of the RGR process and
then describe connections with survival theory.

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
system, where \\(k = 1,2,...\\) In addition, we will add the following
twist: at each timestep, with probability \\(\rho\\) the attachment
process as we have just outlined it is in operation. But with
probability \\(1 - \rho\\), a new group forms. We will call \\(\rho\\) the
*innovation probability*. You can probably imagine that it also has a
profound effect on the distribution of group sizes — just think about
what the size distribution must look like if \\(\rho = 1\\) so that every
element forms a new group\! Moving to continuous time (which is a useful
approximation if ticks of the system’s governing clock are close
together), the equation describing the number of groups of size \\(k\\),
\\(N_k\\),
is

\\[
\frac{dN_k}{dt} = (1 - \rho) [ \text{Inflow into group $k$} - \text{Outflow from group $k$}] + \rho \delta_{k1}.
\\]

We will encode the actual mechanics of the attachment process through a
function \\(r(k)\\), which determines how elements are selected for
replication. For example, the probability that an element from a group
with \\(k\\) elements is selected when using Simon’s mechanism is
\\(r(k) = k\\), since each element has an equal chance of being picked.

**Citations**

  - Dewhurst, David Rushing, Christopher M. Danforth, and Peter Sheridan
    Dodds. "Continuum rich-get-richer processes: Mean field analysis
    with an application to firm size." Physical Review E 97, no. 6
    (2018): 062317.

  - Hamlington, Katharine L., Jason HT Bates, Gregory S. Roy, Adele J.
    Julianelle, Chantel Charlebois, Bela Suki, and Bradford J. Smith.
    "Alveolar leak develops by a rich-get-richer process in
    ventilator-induced lung injury." PloS one 13, no. 3 (2018):
    e0193934.

  - Mori, Vitor, Bradford J. Smith, Bela Suki, and Jason HT Bates.
    "Linking Physiological Biomarkers of Ventilator-Induced Lung Injury
    to a Rich-Get-Richer Mechanism of Injury Progression." Annals of
    biomedical engineering 47, no. 2 (2019): 638-645.

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
