#!/usr/bin/env python

"""
Markdown to epub generation
"""

# epub structure...
# /
#   mimetype
# /EPUB
#   css/
#   fonts/
#   images/
#   *.xhtml
#   content.opf
#   toc.ncx
# /META-INF
#   container.xml

import argparse
import json

# import xml.etree.ElementTree as ET
from lxml import etree as ET
import markdown
from pathlib import Path
from shutil import copytree, copyfile
import uuid

# import os
import mimetypes
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED


uid = "urn:uuid:" + str(uuid.uuid4())


class mdEpub:
  def __init__(self, src, dest) -> None:
    self.src = src
    self.dest = dest
    self.cpath = self.dest / "EPUB"
    self.zip = True

  def createBook(self) -> None:
    bj = self.src / "book.json"
    self.toc: dict = json.loads(bj.read_text())
    zfn = self.toc["meta"]["title"]
    zfn = zfn.replace(" ", "_").lower()
    if self.zip:
      self.epub = ZipFile(f"{zfn}.epub", "w")
      self.epub.mkdir(self.cpath.stem)
    else:
      self.dest.mkdir(exist_ok=True)
      self.cpath.mkdir(exist_ok=True)
    self.createMimetype()
    self.createContainerXml()
    self.copyAssets()
    self.createTocNcx()
    self.createContentOpf()
    self.createContent()
    if self.zip:
      self.epub.close()
    # shutil.make_archive(f"{self.src.stem}.epub", format="zip", root_dir=str(self.dest)))
    print(f"\nGenerated {zfn}.epub")

  def createMimetype(self) -> None:
    if self.zip:
      self.epub.writestr("mimetype", "application/epub+zip", ZIP_DEFLATED)
    else:
      mt = self.dest / "mimetype"
      mt.write_text("application/epub+zip")

  def createContainerXml(self) -> None:
    container = ET.Element("container")
    container.set("version", "1.0")
    container.set("xmlns", "urn:oasis:names:tc:opendocument:xmlns:container")
    rootfiles = ET.SubElement(container, "rootfiles")
    rootfile = ET.SubElement(rootfiles, "rootfile")
    rootfile.set("full-path", self.cpath.stem + "/content.opf")
    rootfile.set("media-type", "application/oebps-package+xml")

    et = ET.ElementTree(container)
    # print(ET.tostring(container, encoding="unicode"))
    ET.indent(et)
    if self.zip:
      self.epub.mkdir("META-INF")
      self.epub.writestr("META-INF/container.xml", ET.tostring(et, xml_declaration=True, pretty_print=True), ZIP_DEFLATED)
    else:
      d = self.dest / "META-INF"
      d.mkdir(exist_ok=True)
      f = d / "container.xml"
      et.write(f, encoding="utf-8", xml_declaration=True)

  def depth(self, lst) -> int:
    d: int = 0
    for item in lst:
      if isinstance(item, list):
        d = max(self.depth(item), d)
    return d + 1

  def createNavMap(self, items, el, i=1) -> int:
    for it in items:
      navpoint = ET.SubElement(el, "navPoint")
      navpoint.set("id", f"navPoint-{i}")
      navpoint.set("playOrder", f"{i}")
      navlabel = ET.SubElement(navpoint, "navLabel")
      text = ET.SubElement(navlabel, "text")
      t = it["title"]
      text.text = t
      content = ET.SubElement(navpoint, "content")
      f = it["file"].split(".")
      content.set("src", f"{f[0]}.xhtml")
      i += 1
      try:
        i = self.createNavMap(it["items"], navpoint, i)
      except KeyError:
        pass
    return i

  def createTocNcx(self) -> None:
    ncx = ET.Element("ncx")
    ncx.set("xmlns", "http://www.daisy.org/z3986/2005/ncx/")
    ncx.set("version", "2005-1")
    head = ET.SubElement(ncx, "head")
    meta = ET.SubElement(head, "meta")
    meta.set("name", "dtb:uid")
    # meta.set("content", "urn:uuid:a915daa5-7c89-44b5-88a9-396e3cbb92d0")
    meta.set("content", uid)
    meta = ET.SubElement(head, "meta")
    meta.set("name", "dtb:depth")
    meta.set("content", "2")
    meta = ET.SubElement(head, "meta")
    meta.set("name", "dtb:totalPageCount")
    meta.set("content", "0")
    meta = ET.SubElement(head, "meta")
    meta.set("name", "dtb:maxPageNumber")
    meta.set("content", "0")
    doctitle = ET.SubElement(ncx, "docTitle")
    text = ET.SubElement(doctitle, "text")
    text.text = self.toc["meta"]["title"]
    navmap = ET.SubElement(ncx, "navMap")
    self.createNavMap(self.toc["nav"], navmap)

    et = ET.ElementTree(ncx)
    ET.indent(ncx)
    dc = '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">'
    if self.zip:
      self.epub.writestr(f"{self.cpath.name}/toc.ncx", ET.tostring(et, xml_declaration=True, doctype=dc, pretty_print=True), ZIP_DEFLATED)
    else:
      et.write(self.cpath / "toc.ncx", encoding="utf-8", xml_declaration=True, doctype=dc)

  def createContentOpf(self) -> None:
    ns: str = "http://www.idpf.org/2007/opf"
    dc: str = "http://purl.org/dc/elements/1.1/"
    opf: str = "http://www.idpf.org/2007/opf"
    package = ET.Element("package", nsmap={None: ns})
    package.set("version", "2.0")
    package.set("unique-identifier", "BookId")
    # package.set("xmlns", "http://www.idpf.org/2007/opf")
    metadata = ET.SubElement(package, "metadata", nsmap={"dc": dc, "opf": opf})
    _lang = ET.SubElement(metadata, ET.QName(dc, "language"))
    _lang.text = "en"
    _title = ET.SubElement(metadata, ET.QName(dc, "title"))
    _title.text = self.toc["meta"]["title"]
    _date = ET.SubElement(metadata, ET.QName(dc, "date"))
    _date.set(ET.QName(opf, "event"), "publication")
    _date.text = self.toc["meta"]["date"]
    _identifier = ET.SubElement(metadata, ET.QName(dc, "identifier"))
    _identifier.set("id", "BookId")
    _identifier.set(ET.QName(opf, "scheme"), "UUID")
    _identifier.text = uid
    _author = ET.SubElement(metadata, ET.QName(dc, "creator"))
    _author.set(ET.QName(opf, "role"), "aut")
    _author.text = self.toc["meta"]["author"]
    # meta = ET.SubElement(metadata, "meta")
    # meta.set("name", "cover")
    # meta.set("content", "cover.jpeg")
    manifest = ET.SubElement(package, "manifest")
    spine = ET.SubElement(package, "spine")
    spine.set("toc", "ncx")
    item = ET.SubElement(manifest, "item")
    item.set("id", "ncx")
    item.set("href", "toc.ncx")
    item.set("media-type", "application/x-dtbncx+xml")
    # item = ET.SubElement(manifest, "item")
    # item.set("id", "cover")
    # item.set("href", "images/cover.jpeg")
    # item.set("media-type", "image/jpeg")

    def createContentManifest(self, items, mel, sel, i=1) -> int:
      for it in items:
        f = it["file"].split(".")
        item = ET.SubElement(mel, "item")
        item.set("id", f"{i:03d}")
        # item.set("id", f[0])
        item.set("href", f"{f[0]}.xhtml")
        item.set("media-type", "application/xhtml+xml")
        itemref = ET.SubElement(sel, "itemref")
        itemref.set("idref", f"{i:03d}")
        # itemref.set("idref", f[0])
        i += 1
        try:
          i = createContentManifest(self, it["items"], mel, sel, i)
        except KeyError:
          pass
      return i

    i = createContentManifest(self, self.toc["nav"], manifest, spine)

    for f in self.src.iterdir():
      if f.is_dir():
        for ff in f.iterdir():
          if ff.is_file():
            ffn = ff.name.split(".")
            item = ET.SubElement(manifest, "item")
            # item.set("id", ff.name)
            item.set("id", f"{i:03d}")
            item.set("href", f.name + "/" + ff.name)
            item.set("media-type", mimetypes.types_map["." + ffn[1]])
            if ffn[0] == "cover":
              item.set("properties", "cover-image")
              cover = ET.SubElement(metadata, "meta")
              cover.set("name", "cover")
              # cover.set("content", ff.name)
              cover.set("content", f"{i:03d}")
            i += 1
    item = ET.SubElement(manifest, "item")
    item.set("id", f"{i:03d}")
    item.set("href", "css/default.css")
    item.set("media-type", mimetypes.types_map[".css"])

    et = ET.ElementTree(package)
    ET.indent(package)
    if self.zip:
      self.epub.writestr(f"{self.cpath.name}/content.opf", ET.tostring(et, xml_declaration=True, pretty_print=True), ZIP_DEFLATED)
    else:
      et.write(self.cpath / "content.opf", encoding="utf-8", xml_declaration=True)

  def createChapterXhtml(self, item) -> None:
    fn = item["file"].split(".")
    title: str = item["title"]
    f = self.src / f"{fn[0]}.md"
    md: str = f.read_text()
    html: str = markdown.markdown(md, extensions=["extra"])
    xhtml: str = '<?xml version="1.0" encoding="utf-8"?>\n'
    xhtml += '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
    xhtml += '<html xmlns="http://www.w3.org/1999/xhtml">\n'
    xhtml += f"<head>\n<title>{title}</title>\n"
    xhtml += '<link href="css/default.css" type="text/css" rel="stylesheet"/>\n'
    pcss = self.src / "css"
    for f in pcss.iterdir():
      if f.is_file():
        xhtml += f'<link href="css/{f.name}" type="text/css" rel="stylesheet"/>\n'
    xhtml += "</head>\n<body>\n"
    xhtml += html
    xhtml += "\n</body>\n</html>\n"
    if self.zip:
      self.epub.writestr(f"{self.cpath.stem}/{fn[0]}.xhtml", xhtml, ZIP_DEFLATED)
    else:
      f = self.cpath / f"{fn[0]}.xhtml"
      f.write_text(xhtml)
    print(f"generating {fn[0]}")

  def createContent(self) -> None:
    def createChapter(items) -> None:
      for it in items:
        self.createChapterXhtml(it)
        try:
          createChapter(it["items"])
        except KeyError:
          pass

    createChapter(self.toc["nav"])

  def copyAssets(self) -> None:
    assets: list[str] = ["css", "images"]
    # assets: list[str] = ["fonts", "images"]
    imgext: list[str] = [".jpeg", ".jpg", ".png"]
    for ass in assets:
      s = self.src / ass
      d = self.cpath / ass
      if self.zip:
        self.epub.mkdir(f"{self.cpath.stem}/{ass}")
      else:
        d.mkdir(exist_ok=True)
      if s.exists():
        if self.zip:
          for f in s.iterdir():
            if f.is_file():
              c = ZIP_DEFLATED
              if f.suffix in imgext:
                c = ZIP_STORED
              self.epub.write(f"{str(f)}", f"{self.cpath.stem}/{ass}/{f.name}", c)
        else:
          copytree(str(s), str(d), dirs_exist_ok=True)
    if self.zip:
      self.epub.write(Path(__file__).resolve().parent / "default.css", f"{self.cpath.stem}/css/default.css", ZIP_DEFLATED)
    else:
      copyfile(Path(__file__).resolve().parent / "default.css", str(self.cpath / "css/default.css"))


def main() -> None:
  ap = argparse.ArgumentParser()
  ap.add_argument("md", type=str, help="path to the folder containing markdown")
  args = ap.parse_args()
  dest = Path("epub")
  # src = Path.home() / "code/markdown" / "ianfleming/novels" / "casino_royale"
  src = Path(args.md)
  src.resolve()
  if src.exists() and src.is_dir():
    eb = mdEpub(src, dest)
    eb.createBook()


if __name__ == "__main__":
  main()

# tree.write(files, encoding="utf-8", xml_declaration=True, doctype='<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">')

