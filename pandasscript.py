import pandas as pd


with open("resources/base/pbs/move_anim_map.csv") as file:
    df = pd.read_csv(file)

df.loc[1, "lowpower"]

