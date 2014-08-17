pybeeswarm
==========

Beeswarm plots for python. Inspired by [R beeswarm plots](http://www.cbs.dtu.dk/~eklund/beeswarm/)

## Install ##
The easiest way to install pybeeswarm is using pip:

```
sudo pip install pybeeswarm
```

To install the latest version on github, simply do:
```
git clone https://github.com/mgymrek/pybeeswarm.git
cd pybeeswarm
sudo python setup.py install
```

To test that it worked, open up python and check that ```import beeswarm``` doesn't give you any errors.

## Requirements ##

This package requires:

* matplotlib
* numpy
* pandas

## Basic usage ##

There is only one function, ```beeswarm```:


```
from beeswarm import *
help(beeswarm)

Help on function beeswarm in module beeswarm.beeswarm:

beeswarm(values, positions=None, method='swarm', ax=None, s=20, col='black', xlim=None, ylim=None, labels=None)
    beeswarm(values, positions=None, method="swarm",
         ax=None, s=20, col="black", xlim=None, ylim=None,
         labels=None)
         
     Inputs:
         * values: an array of a sequence of vectors
         * positions: sets the horizontal positions of the swarms.
            Ticks and labels are set to match the positions.
            If none, set positions to range(len(values))
            Default: None
         * method: how to jitter the x coordinates. Choose from
            "swarm", "hex", "center", "square"
            Default: swarm
         * ax: use this axis for plotting. If none supplied, make a new one
            Default: None
         * s: size of points in points^2 (assuming 72 points/inch).
            Defautt: 20
         * col: color of points. Can be:
            - a single string: color all points that color
            - a vector of strings length len(values): gives color for each group
            - a vector of strings length sum([len(values[i]) for i in range(len(values))])
                 gives color for each point
            - a vector of strings any other length: cycle through the list of colors.
                 (really pretty if not useful)
            Default: "black"
         * xlim: tuple giving (xmin, xmax). If not specified, either get
             from the supplied ax or recalculate
         * ylim: tuple giving (ymin, ymax). If not specified, eiterh get
             from the supplied as or recalculate
         * labels: list of labels for each group.
             Default: range(len(values))
    
     Returns:
         * bs: pandas.DataFrame with columns: xorig, yorig, xnew, ynew, color
         * ax: the axis used for plotting
```

Here's a small example:
```
from beeswarm import *
import matplotlib.pyplot as plt
import numpy as np
d1 = np.random.uniform(low=-3, high=3, size=100)
d2 = np.random.normal(size=100)

bs, ax = beeswarm([d1,d2], method="swarm", labels=["sample 1", "sample 2"], col=["blue","red"])
```

More details [here](http://melissagymrek.com/python/2014/01/04/python-beeswarm.html). View more examples [here](http://nbviewer.ipython.org/github/mgymrek/pybeeswarm/blob/master/tests.ipynb?create=1).
