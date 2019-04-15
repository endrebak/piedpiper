from piedpiper import Debug
import pandas as pd

def test_me():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": ["ab", "cd", "ef"]})
    with Debug(locals()):
        df.head(1)

if __name__ == "__main__":
    test_me()
