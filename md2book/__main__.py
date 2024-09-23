import argparse
from pathlib import Path

import md2epub
import md2html


def main() -> None:
  ap = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  #ap.add_argument("-f", "--format", choices=["epub", "html"], default="epub", help="output format, either epub or html")
  ap.add_argument("-e", "--epub", action='store_true', default=True, help="generate an epub")
  ap.add_argument("-w", "--html", action='store_true', help="generate html")
  ap.add_argument("md", type=Path, help="path to the folder containing markdown")
  ap.add_argument("-o", "--output", type=Path, default=".", help="path to the output folder")
  args = ap.parse_args()
  src = Path(args.md)
  dest = Path(".")
  if args.output:
    dest = Path(args.output)
  if args.html:
    ws = md2html.mdHtml(src, dest)
    ws.createBook()
  else:
    eb = md2epub.mdEpub(src, dest)
    eb.createBook()


main()

