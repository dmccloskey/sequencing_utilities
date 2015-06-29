
from matplotlib.pyplot import pcolor, figure, xlim, ylim, xticks, yticks
from numpy import arange
from pandas import Series, read_table
from scipy.stats import hypergeom


def heatmap(x):
    """plot a heatmap of a pandas dataframe"""
    figure(figsize=(len(x.columns) / 6., len(x.index) / 6.))
    pcolor(x)
    ylim(ymax=len(x.index))
    xlim(xmax=len(x.columns))
    yticks(arange(0.5, len(x.index), 1), x.index)
    xticks(arange(0.5, len(x.columns), 1), x.columns, rotation=90)


def calculate_enrichment(pathway_matrix, gene_set):
    """Calculate hypergoemotric enrichment of the set for each pathway

    The pathway matrix should have pathways in rows and genes in columns
    """
    # only consider genes which are known to be in pathways
    pathway_gene_list = gene_set.intersection(pathway_matrix.columns)
    # Generate hypergeometric distributions for each pathway. Each
    # pathway needs its own because they have different lenghts
    distributions = [hypergeom(len(pathway_matrix.columns), l,
                               len(pathway_gene_list))
                     for l in pathway_matrix.sum(axis=1)]
    pathway_hits = pathway_matrix[pathway_gene_list].sum(axis=1)
    # Each p-value for the hypergeometric enrichment is
    # survival function + 0.5 * pmf
    significance = [dist.sf(x) + 0.5 * dist.pmf(x)
                    for x, dist in zip(pathway_hits, distributions)]
    return Series(significance, index=pathway_matrix.index)


def deseq_pathway_enrichment(pathway_matrix, deseq_file, p_cutoff=0.05, fold_cutoff=2):
    x = read_table(deseq_file, sep=" ", index_col=1)
    significant_genes = x[(x.padj < p_cutoff) & ((x.log2FoldChange > fold_cutoff) | (x.log2FoldChange < -fold_cutoff))].index
    return calculate_enrichment(pathway_matrix, significant_genes)
