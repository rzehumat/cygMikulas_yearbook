import os
import subprocess
from glob import glob
import shutil
from TexSoup import TexSoup

RUN_LATEX = ["latexmk", "-pdf", "-silent", "main"]
PAX = "/home/matej/work/cygMikulas/template/latex-pax/scripts/pdfannotextractor.pl"


def tex_command(command_name: str, command_content: str) -> str:
    return "\\" + f"newcommand{{\\{command_name}}}{{{command_content}}}\n"


def create_paper_list(dirs: list, names: list, titles: list) -> None:
    s = ""
    for dir, name, title in zip(dirs, names, titles):
        s += tex_command(dir, name)
        s += tex_command(f"{dir}Article", title)
    with open("items.tex", "w") as names_file:
        names_file.write(s)
    s = ""
    for dir, name, title in zip(dirs, names, titles):
        s += f"\clanek{{{dir}}}{{{name}}}{{{title}}}\n"
    out = "clanky.tex"
    with open(out, "w") as out_f:
        out_f.write(s)


if __name__ == "__main__":
    os.chdir("raw")
    dirs = os.listdir(".")
    names = []
    titles = []

    for dir in dirs:
        os.chdir(dir)
        print(dir)
        for tex_file in glob("*.tex"):
            subprocess.run(["vlna", tex_file])
        with open("main.tex", "r") as main:
            tex_soup = TexSoup(main)
        # Tää on kamala sekasotku!
        title_raw = str(tex_soup.title.args[0])[1:-1]
        titles.append(title_raw.replace(",", "\comma\,"))
        name_raw = str(tex_soup.names.args[0]).split(",")[0].split("{")[2][:-1]
        names.append(name_raw.replace(",", "\comma\,"))
        subprocess.run(RUN_LATEX)
        shutil.copy("main.pdf", f"../../papers/{dir}.pdf")
        print(f"{dir} done")
        os.chdir("..")
    print("latex done")
    os.chdir("../papers")
    for pdf in glob("*.pdf"):
        print(pdf)
        subprocess.run([PAX, pdf])
        print(f"{pdf} done")
    os.chdir("..")
    create_paper_list(dirs, names, titles)
    subprocess.call(["pdflatex", "rocenka"])
    print("Done")
