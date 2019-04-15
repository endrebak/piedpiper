# piedpiper

Context manager to debug method chains in Python.

```
cat examples/pp.py
# from piedpiper import Debug
# with Debug(locals()):
#     "abc".replace("a", "A").upper().lower().i_will_error().find("hi")
python examples/pp.py
# Start data:
# abc
#
# .replace("a", "A")
# Abc
#
# .upper()
# ABC
#
# .lower()
# abc
#
# .i_will_error()
# Traceback (most recent call last):
#   File "_pp.py", line 2, in <module>
#     with Debug():
#   File "/home/endrebak/code/piedpiper/piedpiper/main.py", line 112, in __init__
#     _run_commands(commands, frame.lineno, frame.filename, _locals)
#   File "/home/endrebak/code/piedpiper/piedpiper/main.py", line 86, in _run_commands
#     __dbg = eval(dirty)
#   File "<string>", line 1, in <module>
# AttributeError: 'str' object has no attribute 'i_will_error'
```

I wrote it to make it easier to debug complex chains of commands in my (PyRanges package)["https://github.com/biocore-ntnu/pyranges"], but it should work on all kinds of data.

## Limitations/Disadvantages

- You currently can only have one chain within the context.
- It is largely unused and untested.
- It only looks at the top level commands (most sensible, IMO), do not really want to extend this
- It uses eval (to run code you were trying to run anyways).
- nested context managers do not work yet

## Help wanted

## More complex example

Notice that `.join(exons.unstrand())` is considered one call as piedpiper only looks at the top level chains.

```
cat examples/exons.py
# import pyranges as pr
# exons = pr.data.exons()
# cpg = pr.data.cpg()
#
# from piedpiper import Debug as D
# with D(locals()):
#     cpg.join(exons.unstrand())[["CpG"]](lambda df: df.head(3))["chrX"].slack(500)
python examples/exons.py
# Start data:
# +--------------|-----------|-----------|-----------+
# | Chromosome   | Start     | End       | CpG       |
# | (category)   | (int64)   | (int64)   | (int64)   |
# |--------------|-----------|-----------|-----------|
# | chrX         | 64181     | 64793     | 62        |
# | chrX         | 69133     | 70029     | 100       |
# | chrX         | 148685    | 149461    | 85        |
# | ...          | ...       | ...       | ...       |
# | chrY         | 28773315  | 28773544  | 25        |
# | chrY         | 59213794  | 59214183  | 36        |
# | chrY         | 59349266  | 59349574  | 29        |
# +--------------|-----------|-----------|-----------+
# PyRanges object has 1077 sequences from 2 chromosomes.
#
# .join(exons)
#
# +--------------|-----------|-----------|-----------|-----------|-----------|----------------------------------------|-----------|--------------+
# | Chromosome   | Start     | End       | CpG       | Start_b   | End_b     | Name                                   | Score     | Strand       |
# | (category)   | (int64)   | (int64)   | (int64)   | (int64)   | (int64)   | (object)                               | (int64)   | (category)   |
# |--------------|-----------|-----------|-----------|-----------|-----------|----------------------------------------|-----------|--------------|
# | chrX         | 584563    | 585326    | 66        | 585078    | 585337    | NM_000451_exon_0_0_chrX_585079_f       | 0         | +            |
# | chrX         | 10094050  | 10094406  | 26        | 10094153  | 10094346  | NM_015691_exon_14_0_chrX_10094154_f    | 0         | +            |
# | chrX         | 13587648  | 13588221  | 49        | 13587693  | 13588054  | NM_001167890_exon_0_0_chrX_13587694_f  | 0         | +            |
# | ...          | ...       | ...       | ...       | ...       | ...       | ...                                    | ...       | ...          |
# | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NR_047607_exon_29_0_chrY_15591394_r    | 0         | -            |
# | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NM_001258269_exon_29_0_chrY_15591394_r | 0         | -            |
# | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NR_047599_exon_28_0_chrY_15591394_r    | 0         | -            |
# +--------------|-----------|-----------|-----------|-----------|-----------|----------------------------------------|-----------|--------------+
# PyRanges object has 79 sequences from 2 chromosomes.
#
# .unstrand()
#
# +--------------|-----------|-----------|-----------|-----------|-----------|----------------------------------------|-----------+
# | Chromosome   | Start     | End       | CpG       | Start_b   | End_b     | Name                                   | Score     |
# | (category)   | (int64)   | (int64)   | (int64)   | (int64)   | (int64)   | (object)                               | (int64)   |
# |--------------|-----------|-----------|-----------|-----------|-----------|----------------------------------------|-----------|
# | chrX         | 584563    | 585326    | 66        | 585078    | 585337    | NM_000451_exon_0_0_chrX_585079_f       | 0         |
# | chrX         | 10094050  | 10094406  | 26        | 10094153  | 10094346  | NM_015691_exon_14_0_chrX_10094154_f    | 0         |
# | chrX         | 13587648  | 13588221  | 49        | 13587693  | 13588054  | NM_001167890_exon_0_0_chrX_13587694_f  | 0         |
# | ...          | ...       | ...       | ...       | ...       | ...       | ...                                    | ...       |
# | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NR_047607_exon_29_0_chrY_15591394_r    | 0         |
# | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NM_001258269_exon_29_0_chrY_15591394_r | 0         |
# | chrY         | 15591259  | 15591720  | 33        | 15591393  | 15592550  | NR_047599_exon_28_0_chrY_15591394_r    | 0         |
# +--------------|-----------|-----------|-----------|-----------|-----------|----------------------------------------|-----------+
# PyRanges object has 79 sequences from 2 chromosomes.
#
# [["CpG"]]
#
# +--------------|-----------|-----------|-----------+
# | Chromosome   | Start     | End       | CpG       |
# | (category)   | (int64)   | (int64)   | (int64)   |
# |--------------|-----------|-----------|-----------|
# | chrX         | 584563    | 585326    | 66        |
# | chrX         | 10094050  | 10094406  | 26        |
# | chrX         | 13587648  | 13588221  | 49        |
# | ...          | ...       | ...       | ...       |
# | chrY         | 15591259  | 15591720  | 33        |
# | chrY         | 15591259  | 15591720  | 33        |
# | chrY         | 15591259  | 15591720  | 33        |
# +--------------|-----------|-----------|-----------+
# PyRanges object has 79 sequences from 2 chromosomes.
#
# (lambda df: df.head(3))
#
# +--------------|-----------|-----------|-----------+
# | Chromosome   | Start     | End       | CpG       |
# | (category)   | (int64)   | (int64)   | (int64)   |
# |--------------|-----------|-----------|-----------|
# | chrX         | 584563    | 585326    | 66        |
# | chrX         | 10094050  | 10094406  | 26        |
# | chrX         | 13587648  | 13588221  | 49        |
# | ...          | ...       | ...       | ...       |
# | chrY         | 155322    | 155553    | 19        |
# | chrY         | 1363206   | 1363503   | 23        |
# | chrY         | 16941822  | 16942188  | 32        |
# +--------------|-----------|-----------|-----------+
# PyRanges object has 6 sequences from 2 chromosomes.
#
# ["chrX"]
#
# +--------------|-----------|-----------|-----------+
# | Chromosome   |     Start |       End |       CpG |
# | (category)   |   (int64) |   (int64) |   (int64) |
# |--------------|-----------|-----------|-----------|
# | chrX         |    584563 |    585326 |        66 |
# | chrX         |  10094050 |  10094406 |        26 |
# | chrX         |  13587648 |  13588221 |        49 |
# +--------------|-----------|-----------|-----------+
# PyRanges object has 3 sequences from 1 chromosomes.
#
# .slack(500)
#
# +--------------|-----------|-----------|-----------+
# | Chromosome   |     Start |       End |       CpG |
# | (category)   |   (int64) |   (int64) |   (int64) |
# |--------------|-----------|-----------|-----------|
# | chrX         |    584063 |    585826 |        66 |
# | chrX         |  10093550 |  10094906 |        26 |
# | chrX         |  13587148 |  13588721 |        49 |
# +--------------|-----------|-----------|-----------+
# PyRanges object has 3 sequences from 1 chromosomes.
#
# [examples/exons.py:6]
```
