import pandas
from matplotlib.pyplot import subplot, fill_between, xlabel, xlim, \
    ylim, setp, savefig, figure


def plot_coverage(gff_files, left, right, scale=True, output=None,
                  names=None, plot_points=2000):
    """plot coverage of a gff file

    gff_files: a list of gff files to read and plot
    left: left position of the plot
    right: right position of the plot
    scale: all plots will be normalized to have 100 max
    output: the filename to which the plot should be saved
    plot_points: the number of points to plot when downsampling"""

    n_files = len(gff_files)
    figure(figsize=(4, 1.5 * n_files))
    if names is None:
        names = [i.replace("_", " ").replace(".gtf", "").replace(".gff", "") for i in gff_files]
    for i, gff_file in enumerate(gff_files):
        # sometimes the first line is a comment which pandas can't handle
        skiprows = 0
        with open(gff_file, "r") as infile:
            if infile.read(1) == "#":
                skiprows = 1
        table = pandas.read_table(gff_file, header=None,
            usecols=[0, 2, 3, 4, 5, 6], comment="#", skiprows=skiprows,
            names=["chromosome", "name", "leftpos", "rightpos", "reads", "strand"])
        table = table[(table.rightpos >= left) & (table.leftpos <= right)]
        # TODO - detect if chromsome_plus and chromosome_minus
        if len(table.chromosome.unique()) > 1:
            raise Exception("multiple chromosomes not supported")
        ax = subplot(n_files, 1, i + 1)
        if (table.leftpos == table.rightpos).all():  # each line is one point
            table = table[["leftpos", "reads", "strand"]]
            table_plus = table[table.strand == "+"].set_index("leftpos")
            table_minus = table[table.strand == "-"].set_index("leftpos")
            # fill missing values with 0
            filler = pandas.Series([list(range(left, right + 1))], [list(range(left, right + 1))])
            table_plus["filler"] = 1
            table_minus["filler"] = 1
            table_plus.fillna(0)
            table_minus.fillna(0)
            # extract only the series we need
            plus = table_plus.reads
            minus = table_minus.reads.abs()  # in case stored negative
            if scale:
                plus *= 100. / plus.max()
                minus *= 100. / minus.max()
            # downsample to 2000 pts
            collapse_factor = int((right - left) / 2000)
            if collapse_factor > 1:
                plus = plus.groupby(lambda x: x // collapse_factor).mean()
                plus.index *= collapse_factor
                minus = minus.groupby(lambda x: x // collapse_factor).mean()
                minus.index *= collapse_factor
            
            fill_between(minus.index.values, 0, minus.values, color="orange", alpha=0.75)
            fill_between(plus.index.values, 0, plus.values, color="blue", alpha=0.5)
        else:
            if len(table) == 0:
                continue
            if (table.reads == ".").all():  # annotation track
                ylim(0, 100)
                ax.yaxis.set_visible(False)
                for j in table.index:
                    entry = table.ix[j]
                    x = [entry["leftpos"], entry["rightpos"]]
                    if entry["strand"] == "+":
                        fill_between(x, 50., 80.)
                    else:
                        fill_between(x, 50., 20.)
            else:
                raise Exception("not yet supported")
        xlabel(names[i])
        xlim(left, right)
        if scale:
            ylim(0, 100)
        else:
            ylim(ymin=0)
    # hide extra text and labels
    for i in range(n_files):
        ax = subplot(n_files, 1, i + 1)
        ax.grid(axis="x")
        if i + 1 < n_files:
            setp(ax.get_xticklabels(), visible=False)
            # get rid of the + 2.8 * 10^6 (etc)
            axis_text = [x for x in ax.xaxis.get_children() if hasattr(x, "get_text")]
            for j, t in enumerate(axis_text):
                if j > 0:
                    t.set_visible(False)
        else:
            ax.ticklabel_format(axis="x", style="sci", scilimits=(1, 3))
    if output:
        savefig(output, transparent=True)
