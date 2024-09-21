pkgname=md2book
pkgver=2024.09.18
pkgrel=1
pkgdesc="My markdown to epub/html ebook generator"
arch=("any")
url="https://github.com/romanw/md2book"
license=("MIT")
makedepends=('python-build' 'python-installer')
depends=('python-markdown' 'python-lxml')
checkdepends=('python-lxml' 'git' 'python-markdown')
source=("$pkgname-$pkgver.tar.gz::https://github.com/romanw/md2book/archive/$pkgver.tar.gz")
sha512sums=('SKIP')

build() {
  cd $pkgname-$pkgver
  python -m build -wn
}

package() {
    cd "$srcdir/$pkgname-$pkgver"

    LANG=en_US.UTF-8 python -m installer --destdir="$pkgdir" dist/*.whl

    cd "docs"

    install -d "$pkgdir/usr/share/man/man1/"
    install -Dm644 _build/man/*.1 "$pkgdir/usr/share/man/man1/"

    install -d "$pkgdir/usr/share/doc/md2book/"
    install -Dm644 _build/text/*.txt "$pkgdir/usr/share/doc/md2book/"
}

check() {
    cd "$srcdir/$pkgname-$pkgver"
    pytest -v -k 'not test_blinker_is_ordered'
}
