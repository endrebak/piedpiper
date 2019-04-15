from piedpiper import Debug
with Debug():
    "abc".replace("a", "A").upper().lower().i_will_error().find("hi")
