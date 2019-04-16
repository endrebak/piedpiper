from piedpiper import Debug
import pandas as pd

def test_me():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [4, 5, 6, 7, 8], "c": ["ab", "cd", "ef", "gh", "ij"]})
    with Debug():
        df.head(5).tail(4).head(3).assign(Chromosome = lambda df: "chr" + df.c.str.upper())

if __name__ == "__main__":
    test_me()
