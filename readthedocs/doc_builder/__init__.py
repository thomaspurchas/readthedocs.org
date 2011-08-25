from .backends import (
    sphinx,
    sphinx_epub,
    sphinx_htmldir,
    sphinx_man,
    sphinx_pdf,
    sphinx_rst2pdf,
    )


loading = {'sphinx': sphinx.Builder,
           'sphinx_epub': sphinx_epub.Builder,
           'sphinx_htmldir': sphinx_htmldir.Builder,
           'sphinx_man': sphinx_man.Builder,
           'sphinx_pdf': sphinx_rst2pdf.Builder,
           }
