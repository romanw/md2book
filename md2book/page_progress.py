"""
Page progress compoment for md2html
"""


class PageProgress:
  markup: str = """
<page-progress>
  <progress id="page-progress" max="100" value="0"></progress>
</page-progress>
"""

  style: str = """
/* page-progress.css start */
page-progress {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  width: 100%;
  max-width: 60rem;
}

progress {
  border: 0;
  height: 0.5vh;
}

progress[value] {
  background-color: unset;
  width: inherit;
}

progress[value]::-webkit-progress-bar {
  background-color: unset;
}
/* page-progress.css end */
"""

  script: str = """
// page-progress.js start
const progress = document.getElementById("page-progress");
progress.value = 0;

window.onscroll = () => {
  const scroll = document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  if (height > 0) {
    let scrolled = (scroll / height) * 100;
    progress.value = scrolled;
  }
}
// page-progress.js end
"""

  def __init__(self):
    pass

