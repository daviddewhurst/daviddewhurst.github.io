# `stsb2`

This is the homepage for structural time series, round 2.
 It implements a grammar defined over structural time series blocks. You can read more 
about the theory [here](https://arxiv.org/abs/2009.06865).

This library is useful because it allows you to easily express interpretable yet
complex time series models by reasoning about them as collections of 
semantically-meaningful objects, not individual temporally-linked sample nodes. The 
following are all valid `stsb2` models:

```
import stsb2.stsb as sts

...

# model 1
rw = sts.RandomWalk(t1=100,)

# model 2
loc = sts.MA1(t1=100,)
position = sts.RandomWalk(loc=loc)

# model 3
trend = sts.GlobalTrend(t1=100,)
seasonal = sts.GlobalTrend(t1=100,).cos()
noise = sts.AR1(t1=100,)
sgt = seasonal + trend + noise

# model 4
log_vol_1 = sts.RandomWalk(t1=100)
log_vol_2 = MA1(t1=t1,)
vol = sts.changepoint(log_vol_1, log_vol_2, frac=0.6).exp()
price = sts.RandomWalk(t1=t1, loc=0.0, scale=vol, ic=0.0).exp()
```

You can see more examples on the [project Gitlab](https://gitlab.com/daviddewhurst/stsb2/-/tree/develop).


# Installation and license

`pip install stsb2`

If you just want the source code:
```
curl -O https://davidrushingdewhurst.com/stsb2/package/stsb2.tgz
```
or on the [project Gitlab](https://gitlab.com/daviddewhurst/stsb2/-/tree/develop).

This code is released under [GNU GPL 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
For inquiries about obtaining a proprietary license, you can [contact me](drd@davidrushingdewhurst.com).

# Documentation:

It's [here](https://davidrushingdewhurst.com/stsb2/docs/).
