# rh-lean-proof-map

A structural map of a large Lean 4 development whose top-level file states the Riemann Hypothesis and the Generalized Riemann Hypothesis for Dirichlet L-functions. The source archive itself (175,187 files, about 17.5 million lines) is not included here; this repository holds only the tools that read it and what they produce.

Open `viewer/index.html` in a browser. It is a single self-contained page: the top of the proof tree is laid out by depth below `riemannHypothesis` and by mathematical role, each node carries its statement and the definitions of the terms it uses, and the bottom of the page shows every module group the proof reaches as one dependency graph, linked to the tree in both directions.

The map is static. Nothing was compiled, so it records how the source is organised and says nothing about whether Lean accepts the proof. References between declarations were resolved by matching names, which makes the reachability counts approximate.

## Layout

`viewer/` holds the interactive page. `figures/` holds the static graphs and the metadata panels as PNG and PDF. `data/` holds the first layers of the proof tree with their Lean statements and a JSON summary of the counts. `tools/` holds the scripts, run in this order on an unpacked archive:

```
python3 -I tools/index_full.py <archive>/lean/src <work>        # declarations, statements, references
python3 -I tools/plot_full.py <work>/index.pkl <out>            # static graphs and metadata panels
python3 -I tools/build_html2.py <work>/index.pkl <out>/index.html tools/template2.html tools
```

The scripts need Python 3 with `networkx`, `numpy` and `matplotlib`, and they only read the archive as text.
