import pyranges as pr
exons = pr.data.exons()
cpg = pr.data.cpg()

from piedpiper import Debug as D
with D():
    cpg.join(exons.unstrand())[["CpG"]](lambda df: df.head(3))["chrX"].slack(500)
