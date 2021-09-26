from pathlib import Path

p_functions = Path("game/upl/upl_scripts/")

func_list = []

for f in p_functions.glob("*.py"):
    if "__" in str(f):
        continue

    with open(f, "r") as f_file:
        func = f_file.read()

    fname = func.split("class ")[1].split(":")[0]

    if len(s := func.split('"""function')) > 1:
        s = s[1].strip()
        # print(s)
        fsummary, s = s.split("\n", 1)

        s = s.split('"""')[0].strip()

        fdescription, fin = [x.strip() for x in s.split("in:")]
        export = (
            f"""---
title: {fname}
keywords: UPL Ulix Parsed Language {fname}
tags: [documentation, upl]
sidebar: guide_sidebar
permalink: upl_docs_{fname.lower()}.html
folder: upl_docs
summary: "{fsummary}"
---\n
## {fname}\n
{fdescription}\n
### Inputs:
{fin}\n
"""
            "{% include links.html %}"
        ).strip()

    elif len(s := func.split('"""fobject')) > 1:
        s = s[1].strip()
        # print(s)
        fsummary, s = s.split("\n", 1)

        s = s.split('"""')[0].strip()

        fdescription, fin = [x.strip() for x in s.split("in:")]

        fin = fin.strip()
        fin, fout = [x.strip() for x in fin.split("out:")]
        export = (
            f"""---
title: {fname}
keywords: UPL Ulix Parsed Language {fname}
tags: [documentation, upl]
sidebar: guide_sidebar
permalink: upl_docs_{fname.lower()}.html
folder: upl_docs
summary: "{fsummary}"
---\n
## {fname}\n
{fdescription}\n
### Inputs:
{fin}\n
### Outputs:
{fout}\n
"""
            "{% include links.html %}"
        ).strip()

    else:
        # print("Skipped:", f)
        continue

    with open(
        Path("util/docs/upl_docs") / f"upl_docs_{fname.lower()}.md", "w"
    ) as w_file:
        w_file.write(export)

    func_list.append(fname)


with open(Path("util/docs/") / "guide_sidebar.md", "w") as file:

    file.write(
        """
    - title: UPL Documentation A-L
        output: web, pdf

        folderitems:"""
    )
    for func in [x for x in func_list if x[0] < "M"]:
        file.write(
            f"""
          - title: {func}
            url: /upl_docs_{func.lower()}.html
            output: web, pdf
"""
        )

    file.write(
        """
    - title: UPL Documentation M-Z
        output: web, pdf

        folderitems:"""
    )
    for func in [x for x in func_list if x[0] >= "M"]:
        file.write(
            f"""
          - title: {func}
            url: /upl_docs_{func.lower()}.html
            output: web, pdf
"""
        )
