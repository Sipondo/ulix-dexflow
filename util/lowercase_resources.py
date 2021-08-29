from pathlib import Path
import os

p = Path("../resources")
while True:
    for i in p.glob("**/*"):
        if str(i) != str(i).lower().replace(" ", "_"):
            print(i)
            os.renames(str(i), str(i).lower().replace(" ", "_"))
            break
    else:
        quit()
