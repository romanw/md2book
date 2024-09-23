# md2book

A basic markdown to epub/html book converter.

> [!WARNING]
> Little to no testing has been done or thought about. Please feel free to improve on this situation.

## Dependencies

- python-markdown
- python-lxml

## Usage

```
usage: md2book [-h] [-e] [-w] [-o OUTPUT] md

positional arguments:
  md                    path to the folder containing markdown

options:
  -h, --help            show this help message and exit
  -e, --epub            generate an epub (default: True)
  -w, --html            generate html (default: False)
  -o OUTPUT, --output OUTPUT
                        path to the output folder (default: .)
```

> [!NOTE]
> Html output will create a `_site/` directory in the specified output folder, and write the generated html there.

## Markdown folder structure

```
./
  book.json
  *.md
  images/
    *.jpg/png/svg/etc
    favicon.svg
  css/
    custom.css
```

### book.json

The `book.json` file must be present and specifies basic meta data (book title, authors name and date) and navigation (or table of contents) infomation. The navigation section allows for sub-sections to any depth (but not tested fully).

#### Example

```json
{
  "meta": { "title": "Book title", "author": "Author name", "date": "2024-09-21" },
  "nav": [
    { "title": "First/cover page", "file": "index.md" },
    { "title": "Part I", "file": "part1.md", "items": [
      { "title": "Chapter 1", "file": "ch01.md" },
      { "title": "Chapter 2", "file": "ch02.md" }
    ]}
  ]
}
```

### css/images folders

The `css/` and `images/` folders need to be present even if they are empty.

## HTML

favicon.svg in markdown `images/` folder.

## EPUB

### Structure

The resultant epub file, which is just a zipped archive, has the following content structure and should be compliant with epub v2, so should be readable by most ebook readers.

```
/
  mimetype
  META-INF/
    container.xml
  EPUB/
    css/
    images/
    *.xhtml
    content.opf
    toc.ncx
```
