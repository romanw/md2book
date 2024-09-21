# md2book

A basic markdown to epub/html book converter.

## Dependencies

- python-markdown
- python-lxml

## Usage

```
$ md2book [format] path-to-markdown [destination-path]
```

- `format` is either `epub` or `html`; if not specified will default to `epub`.
- if `destination-path` is not sepcified the current working directory will be used.

## Markdown folder structure

```
./
  book.json
  *.md
  images/
    *.jpg/png/svg/etc
  css/
    custom.css
```

## book.json

The `book.json` file must be present and specifies basic meta data (book title, authors name and date) and navigation (or table of contents) infomation. The navigation section allows for sub-sections to any depth (but not tested fully).

### Example

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

## HTML

favicon.svg in markdown images folder.

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
