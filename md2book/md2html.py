#!/usr/bin/env python

"""
Markdown to html generation
"""

import argparse
import json
import markdown
from pathlib import Path
from shutil import copytree

# import os
from page_progress import PageProgress
from prev_next import PrevNext
from toc_nav import tocNav

pageProgress = PageProgress()


class mdHtml:
  markup: str = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="shortcut icon" href="images/favicon.svg" type="image/svg+xml">
  <style>{css}</style>
</head>
<body>
  {progress}
  <div class="page">
    <main id="page">{content}</main>
    <footer>{prevnext}</footer>
  </div>
  {toc}
</body>
<script defer>{scripts}</script>
</html>
"""

  def __init__(self, src, dest):
    self.src = src
    self.dest = dest

  def createBook(self) -> None:
    self.dest.mkdir(exist_ok=True)
    self.copyAssets()
    self.genStyles()
    self.genScripts()
    bj = self.src / "book.json"
    self.toc: dict = json.loads(bj.read_text())
    self.createHtmlFiles(self.toc)

  def copyAssets(self) -> None:
    # assets = [ "css", "fonts", "images" ]
    assets: list[str] = ["fonts", "images"]
    for ass in assets:
      s = self.src / ass
      if s.exists():
        d = self.dest / ass
        d.mkdir(exist_ok=True)
        copytree(str(s), str(d), dirs_exist_ok=True)

  def genStyles(self) -> None:
    self.styles: str = ""
    dcss = Path("default.css")
    self.styles += dcss.read_text()
    self.styles += pageProgress.style
    self.styles += PrevNext.style
    self.styles += tocNav.style
    css = self.src / "css"
    for child in css.iterdir():
      if child.is_file():
        self.styles += child.read_text()

  def genScripts(self) -> None:
    self.scripts: str = pageProgress.script
    self.scripts += tocNav.script

  def md2html(self, item) -> None:
    pn = PrevNext(self.toc, item["file"])
    toc = tocNav(self.toc, item["file"])
    f = self.src / item["file"]
    md: str = f.read_text()
    mu: str = markdown.markdown(md, extensions=["extra"])
    html: str = self.markup.format(title=item["title"], css=self.styles, progress=PageProgress.markup, content=mu, prevnext=pn.getMarkup(), toc=toc.getMarkup(), scripts=self.scripts)
    fs: list = item["file"].split(".")
    fd = self.dest / f"{fs[0]}.html"
    fd.write_text(html)

    print(f"Generated {fs[0]}.html")

  def createHtmlFiles(self, toc: dict):
    def createHtmlFile(items: dict):
      for it in items:
        self.md2html(it)
        if "items" in it:
          createHtmlFile(it["items"])

    createHtmlFile(toc["nav"])


def main() -> None:
  ap = argparse.ArgumentParser()
  ap.add_argument("md", type=str, help="path to the folder containing markdown")
  args = ap.parse_args()
  dest = Path("_site/")
  # src = Path.home() / "code/markdown" / "garden_beasts" / "md"
  src = Path(args.md)
  src.resolve()
  if src.exists() and src.is_dir():
    ws = mdHtml(src, dest)
    ws.createBook()


if __name__ == "__main__":
  main()

