# import json


class tocNav:
  markup: str = """
<toc-nav id="toc">
<div class="toc-content">
  <header id="toc-header">
    <!--span id="toc-close" class="close">&times</span-->
    <h1>{}</h1>
    <h2>Contents</h2>
  </header>
  {}
</div>
</toc-nav>
"""

  style: str = """
/* toc.css start */
toc-nav {
  display: none;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  overflow: auto;
}
toc-nav .toc-content {
  background-color: white;
  width: fit-content;
  width: -webkit-fit-content;
  min-width: 50%;
  margin: auto;
  padding: 1em;
}
toc-nav span.close {
  float: right;
  font-size: 2em;
  font-weight: bold;
  line-height: 0;
}
toc-nav h1 {
  font-size: 2em;
  border: 0;
  line-height: 1;
}
toc-nav h2 {
  font-size: 1.5em;
}
toc-nav h3 {
  font-size: 1em;
  line-height: 1;
  margin: 0;
}
toc-nav ul {
  list-style: none;
  padding: 0;
}
toc-nav div > ul {
  padding: 0;
  width: fit-content;
  margin: 0 auto;
}
toc-nav a {
  display: block;
  text-decoration: none;
  color: currentColor;
  line-height: 2;
}
toc-nav a.subhdr {
  font-weight: bold;
  border-top: 1px solid silver;
  margin-top: 1.5em;
  padding-top: 0.5em;
  font-family: sans-serif;
}
toc-nav a.cp {
  color: var(--primary-accent-colour);
}
@media (prefers-color-scheme: dark) {
  toc-nav .toc-content {
    background-color: #222;
  }
}
/* toc.css end */
"""

  script: str = """
// toc.js start
const page = document.getElementById("page");
const toc = document.getElementById("toc");
const toc_close = document.getElementById("toc-header");
page.onclick = function (event) {
  if (event.clientY < screen.height / 10) {
    toc.style.display = "block";
    //toc.style.visibility = "visible";
    document.body.style.top = `-${window.scrollY}px`;
    document.body.style.position = "fixed";
  }
};
toc_close.onclick = function (event) {
  toc.style.display = "none";
  //toc.style.visibility = "hidden"
  const scrollY = document.body.style.top;
  document.body.style.position = "";
  document.body.style.top = "";
  window.scrollTo(0, parseInt(scrollY || "0") * -1);
};
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == toc) {
    toc.style.display = "none";
    //toc.style.visibility = "hidden";
    const scrollY = document.body.style.top;
    document.body.style.position = "";
    document.body.style.top = "";
    window.scrollTo(0, parseInt(scrollY || "0") * -1);
  }
};
// toc.js end
"""

  def __init__(self, toc: dict, fn: str):
    self.toc = toc
    self.fn = fn

  def getMarkup(self) -> str:
    def createList(items: dict) -> str:
      ul: str = '<ul>'
      for it in items:
        title: str = it['title']
        f: str = it['file'].split('.')[0]
        cl: str = ''
        if it['file'] == self.fn:
          cl = 'cp'
        if 'items' in it:
          cl += ' subhdr'
        li: str = f'<li><a href="{f}.html" class="{cl}">{title}</a>'
        if 'items' in it:
          li += createList(it['items'])
        li += '</li>'
        ul += li
      ul += '</ul>'
      return ul

    nav: dict = self.toc['nav']
    ul: str = createList(nav)
    mu: str = self.markup.format(self.toc['meta']['title'], ul)
    return mu
