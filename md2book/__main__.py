import argparse
from pathlib import Path

import md2epub
import md2html


def main() -> None:
  ap = argparse.ArgumentParser()
  ap.add_argument("format", choices=["epub", "html"], default="epub", help="output format, either epub or html")
  ap.add_argument("md", type=str, help="path to the folder containing markdown")
  ap.add_argument("destination", type=str, help="path to the output folder")
  args = ap.parse_args()
  src = Path(args.md)
  dest = Path(args.destination)
  if args.format == "html":
    ws = md2html.mdHtml(src, dest)
    ws.createBook()
  else:
    eb = md2epub.mdEpub(src, dest)
    eb.createBook()


main()

