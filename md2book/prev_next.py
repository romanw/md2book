"""
Previous/next navigation component for md2html
"""


class PrevNext:
  markup: str = """
<prev-next>
  <nav>
    <div id="prev">{}</div>
    <div id="next">{}</div>
  </nav>
</prev-next>
"""

  prevlink0: str = """
<a class="prev" href="{}">
  <span class="desc">Previous page</span>
  <span class="title" >{}</span>
</a>
"""

  prevlink: str = """
<a class="prev" href="{}">
  <span class="desc">&laquo; </span>
  <span class="title">{}</span>
</a>
"""

  nextlink0: str = """
<a class="next" href="{}">
  <span class="desc">Next page</span>
  <span class="title">{}</span>
</a>
"""

  nextlink: str = """
<a class="next" href="{}">
  <span class="title">{}</span>
  <span class="desc"> &raquo;</span>
</a>
"""

  style: str = """
/* prev-next.css start*/
prev-next nav {
  /*display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5em;*/
  display: flex;
  justify-content: space-between;
  /*border-top: 1px solid silver;*/
  /*padding-top: 1em;
  padding-bottom: 0.5em;*/
  padding: 1em 0;
  /*margin-top: 3em;*/
  /*font-family: sans-serif;*/
}
prev-next nav > div {
  width: 100%;
}
prev-next a {
  display: block;
  text-decoration: none;
  color: currentColor;
  /*border: 1px solid silver;*/
  border-radius: 0.5rem;
  padding: 0 1rem;
  /*width: 100%;*/
  width: calc(100% - 0.5em);
  height: 100%;
}
prev-next a.prev {
  text-align: left;
  margin-right: auto;
}
prev-next a.next {
  text-align: right;
  margin-left: auto;
}
prev-next span {
  /*display: block;*/
}
prev-next span.desc {
  /*font-size: 0.75em;*/
  color: grey;
}
prev-next span.title {
  font-size: 0.9em;
  color: var(--primary-accent-colour);
}
@media screen and (max-width: 599px) {
  prev-next nav {
    flex-wrap: wrap-reverse;
  }
  prev-next a {
    width: 100%;
  }
}
/* prev-next.css end */
"""

  script: str = """
"""

  def __init__(self, toc: dict, fn: str):
    self.toc = toc
    self.fn = fn

  def getMarkup(self) -> str:
    self.prev = None
    self.next = None
    self.match: bool = False
    self.done: bool = False

    def parseItems(items) -> None:
      for it in items:
        _file: str = it["file"].split(".")[0] + ".html"
        _title: str = it["title"]
        if self.match:
          self.next = [_file, _title]
          self.done = True
          break
        if it["file"] == self.fn:
          self.match = True
        else:
          self.prev = [_file, _title]
        if "items" in it:
          parseItems(it["items"])
          if self.done:
            break

    parseItems(self.toc["nav"])
    pl: str = ""
    nl: str = ""
    if self.prev is not None:
      pl = self.prevlink.format(self.prev[0], self.prev[1])
    if self.next is not None:
      nl = self.nextlink.format(self.next[0], self.next[1])
    mu: str = self.markup.format(pl, nl)
    # print(mu)
    return mu

