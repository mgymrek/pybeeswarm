import itertools
import math
import matplotlib.pyplot
import pandas
import numpy

def beeswarm(values, positions=None, method="swarm",
             ax=None, s=20, col="black", xlim=None, ylim=None,
             labels=None, plot=True):
    if ax is None:
        fig = matplotlib.pyplot.figure()
        ax = fig.add_subplot(111)

    if positions is None:
        positions = range(len(values))
    yvals = list(itertools.chain.from_iterable(values))
    xvals = list(itertools.chain.from_iterable([[positions[i]]*len(values[i]) for i in range(len(values))]))

    # Get axis limits
    if xlim is not None:
        ax.set_xlim(left=xlim[0], right=xlim[1])
    else:
        xx = max(positions) - min(positions) + 1
        xmin = min(positions)-0.1*xx
        xmax = max(positions)+0.1*xx
        ax.set_xlim(left=xmin, right=xmax)
    if ylim is not None:
        ax.set_ylim(bottom=ylim[0], top=ylim[1])   
    else:
        yy = max(yvals) - min(yvals)
        ymin = min(yvals)-.05*yy
        ymax = max(yvals)+0.05*yy
        ax.set_ylim(bottom=ymin, top=ymax)

    # Determine dot size
    figw, figh = ax.get_figure().get_size_inches()
    w = (ax.get_position().xmax-ax.get_position().xmin)*figw
    h = (ax.get_position().ymax-ax.get_position().ymin)*figh
    xran = ax.get_xlim()[1]-ax.get_xlim()[0]
    yran = ax.get_ylim()[1]-ax.get_ylim()[0]
    xsize=math.sqrt(s)*1.0/72*xran*1.0/(w*0.8)
    ysize=math.sqrt(s)*1.0/72*yran*1.0/(h*0.8)

    # Get color vector
    if type(col) == str:
        colors = [col]*len(yvals)
    elif type(col) == list:
        if len(col) == len(positions):
            colors = []
            for i in range(len(col)):
                colors.extend([col[i]]*len(values[i]))
        elif len(col) == len(yvals):
            colors = col
        else:
            colors = col*(len(yvals)/len(col)) # hope for the best
            if len(colors) < len(yvals):
                colors.extend(col[0:(len(yvals)-len(colors))])
    else:
        sys.stderr.write("ERROR: Invalid argument for col\n")
        return

    bs = pandas.DataFrame({"xorig": xvals, "yorig": yvals})

    # Get new arrangements
    if method == "swarm":
        offsets = _beeswarm(positions, values, xsize=xsize, ysize=ysize, method="swarm")
    else:
        offsets = _beeswarm(positions, values, ylim=ax.get_ylim(), xsize=xsize, ysize=ysize, method=method)
    bs = pandas.merge(bs, offsets, on=["xorig","yorig"])
    bs["color"] = colors
    # jitter points
    if plot:
        ax.scatter(bs["xnew"], bs["ynew"], color=colors)
        ax.set_xticks(positions)
        if labels is not None:
            ax.set_xticklabels(labels)
    return bs;

def unsplit(x,f):
    """
    same as R's unsplit function
    """
    y = pandas.DataFrame({"y":[None]*len(f)})
    f = pandas.Series(f)
    for item in set(f):
        y.ix[f==item,"y"] = x[item]
    return y["y"]

def grid(x, ylim, xsize=0, ysize=0, method="hex"):
    """
    """
    size_d = ysize
    if method == "hex": size_d = size_d*math.sqrt(3)/2
    size_g = xsize
    breaks = numpy.arange(ylim[0], ylim[1]+size_d, size_d)
    mids = (pandas.Series(breaks[:-1]) + pandas.Series(breaks[1:]))*1.0/2
    d_index = pandas.Series(pandas.cut(pandas.Series(x), bins=breaks, labels=False))
    d_pos = d_index.apply(lambda x: mids[x])
    v_s = {}
    for item in set(d_index):
        odd_row = (item%2)==1
        vals = range(list(d_index).count(item))
        if method == "center":
            v_s[item] = map(lambda a: a - numpy.mean(vals), vals)
        elif method == "square":
            v_s[item] = map(lambda a: a - math.floor(numpy.mean(vals)), vals)
        elif method == "hex":
            if odd_row:
                v_s[item] = map(lambda a: a - math.floor(numpy.mean(vals)) - 0.25, vals)
            else:
                v_s[item] = map(lambda a: a - math.ceil(numpy.mean(vals)) + 0.25, vals)
        else:
            sys.stderr.write("ERROR: Invalid method.")
    x_index = unsplit(v_s, d_index)
    return x_index.apply(lambda x: x*size_g), d_pos
        
def _beeswarm(positions, values, xsize=0, ysize=0, ylim=None, method="swarm"):
    """
    """
    xnew = []
    ynew = []
    xorig = []
    yorig = []
    # group y by X
    for i in range(len(positions)):
        xval = positions[i]
        ys = values[i]
        if method == "swarm":
            g_offset = swarm(ys, xsize=xsize, ysize=ysize)
            ynew.extend(ys)
        else:
            g_offset, new_values = grid(ys, xsize=xsize, ysize=ysize, ylim=ylim, method=method)
            ynew.extend(new_values)
        xnew.extend([xval+item for item in g_offset])
        yorig.extend(ys)
        xorig.extend([xval]*len(ys))        
    out = pandas.DataFrame({"xnew":xnew,"yorig":yorig,"xorig":xorig,"ynew": ynew})
    return out

def swarm(x, xsize=0, ysize=0):
    """
    """
    gsize = xsize
    dsize = ysize
    x.sort()
    out = pandas.DataFrame({"x": [item*1.0/dsize for item in x], "y": [0]*len(x)})
    out = out.sort("x")
    if out.shape[0] > 1:
        for i in range(1, out.shape[0]):
            xi = out["x"].values[i]
            yi = out["y"].values[i]
            pre =  out[0:i] # previous points
            wh = ((xi-pre["x"]) < 1) # which are potentially overlapping
            if any(wh):
                pre = pre[wh]
                poty_off = pre["x"].apply(lambda x: math.sqrt(1-(xi-x)**2)) # potential y offset
                poty = pandas.Series([0] + (pre["y"] + poty_off).tolist() + (pre["y"]-poty_off).tolist()) # potential y values
                poty_bad = []
                for y in poty:
                    dists = (xi-pre["x"])**2 + (y-pre["y"])**2
                    if any([item < 0.999 for item in dists]): poty_bad.append(True)
                    else: poty_bad.append(False)
                poty[poty_bad] = numpy.infty
                abs_poty = [abs(item) for item in poty]
                newoffset = poty[abs_poty.index(min(abs_poty))]
                out.loc[i,"y"] = poty[abs_poty.index(min(abs_poty))]
            else:
                out.loc[i,"y"] = 0
    out.ix[numpy.isnan(out["x"]), "y"] = numpy.nan
    return out["y"]*gsize
