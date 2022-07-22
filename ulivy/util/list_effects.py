from pathlib import Path

EFFECTS_PATH = Path("ulivy/combat/effects/")


def init_move_effects():
    l = []
    for x in (EFFECTS_PATH / "moveeffect").glob("*.py"):
        if "basemoveeffect" in x.stem or "init" in x.stem:
            continue
        l.append(f"{x.stem}")
    return l


def init_abilities():
    l = []
    for x in (EFFECTS_PATH / "abilityeffect").glob("*.py"):
        if "baseabilityeffect" in x.stem or "init" in x.stem:
            continue
        l.append(f"{x.stem}")
    return l


with open("ulivy/combat/move.txt", "w") as file:
    file.write("\n".join(init_move_effects()))

with open("ulivy/combat/ability.txt", "w") as file:
    file.write("\n".join(init_abilities()))
