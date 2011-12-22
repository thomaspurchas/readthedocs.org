Configuration of the production servers
=======================================

This document is to help people who are involved in the production instance of Read the Docs running on readthedocs.org. It contains implementation details and useful hints for the people handling operations of the servers.

Servers
-------
The servers are themed somewhere between Norse mythology and Final Fantasy Aeons. I tried to keep them topical, and have some sense of their historical meaning and their purpose in the infrastructure.

Varnish
~~~~~~~
    * Asgard

Web
~~~
    * Chimera
    * Ladon

Build
~~~~~
    * Mozbuild

Database
~~~~~~~~
    * Loki

Solr
~~~~
    * Odin

Monitoring
~~~~~~~~~~
    * Kirin


Site Checkout
-------------

``/home/docs/sites/readthedocs.org/checkouts/readthedocs``

Bash Aliases
~~~~~~~~~~~~

    * `chk` - Will take you to the checkout directory
    * `run` - Will take you to the run directory


