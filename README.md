
# Contingent: A Fully Dynamic Build System

As described in a recent keynote talk at PyCon Colombia 2021,
**Contingent** is a prototype build system, written in Python,
that is designed to be the first build system
able to support dependencies between files
that are dynamic —
that can come and go as the file contents themselves change.

* [**Chapter 4** of *500 Lines or Less*](http://aosabook.org/en/500L/contingent-a-fully-dynamic-build-system.html)
  from the **The Architecture of Open Source Applications** series
  is the official published description of Contingent
  and of its novel algorithm for maintaining a dependency graph
  when graph edges can come and go from one moment to the next
  as documents are edited to add and remove cross-references.

* This source code repository is hosted
  [on GitHub](https://github.com/brandon-rhodes/contingent).

* The only public project that currently uses the Contingent prototype
  as its build system is the
  [builder.py](https://github.com/brandon-rhodes/blog/blob/master/bin/builder.py)
  script that generates Brandon’s personal website and blog
  from a mix of Markdown, RST, and Jupyter Notebook files.

Contingent currently receives only occasional improvements and tweaks.
But if it looks like Contingent could serve as the backbone
of one of your own projects,
feel free to open an issue
describing any tweaks to its API or behavior
that would make it able to support your use case!
