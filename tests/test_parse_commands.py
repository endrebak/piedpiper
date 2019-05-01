
from piedpiper.main import _parse_commands


def test_parse_commands():

    result = _parse_commands("pd.read_table().hi(there='woot')")

    print(result)

    assert result == ['pd', '.read_table()', ".hi(there='woot')"]


def test_parse_commands2():

    commands = """(cpg # use the cpg dataset
                .join(exons, suffix="_xn") # join with exons, use suffix _xn for duplicate cols
                .subset(lambda df: df.CpG > 30) # keep only rows with a CpG score over 30
                .sort() # sort on Chromosome, Start and End
                ["chrX"] # keep only chromosome X
                # another comment
                .assign("CpGDecile",
                     lambda df: df.CpG / 10) # Insert new column
                .unstrand())""" # remove the strand info

    result = _parse_commands(commands)

    for c in result:
        print("cmd:", c)

    assert result == ['pd', '.read_table()', ".hi(there='woot')"]
