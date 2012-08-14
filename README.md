MW3DataVis
==========

### c0z3n 2012, GPL v3 ###

the MW3DataVis project is a collection of basic tools used to visualize data collected from MW3 gameplay.

#### datavis.py ####

datavis.py is a simple viewer which shows data points in 3d, and allows the user to select distinct points and see the connecting points (killpaths). The model may be rotated using 'q', 'w', 'a', 's', 'z', and 'x', and translated using the arrow keys. Data is read in from .kdt files in the /data directory.

datavis.py requires the [pygame library](http://www.pygame.org)

#### killnode.py ####

killnode.py is a structure used by datavis.py to manage killpoints and their associated killpaths.

killnode.py requires the [pygame library](http://www.pygame.org)

#### pyproc_vis_test.py ####

pyproc_vis_test.py is another simple 3d viewer for .kdt files, using pyprocessing rather than pygame. it is very slow (even more so than datavis.py), and rather buggy.

pyproc_vis_test.py requires the [pyprocessing library](http://code.google.com/p/pyprocessing/)

#### jsonExporter.py ####

jsonExporter.py is a simple json file dumper which converts .kdt files into json objects in .json files, stripping out point association data and leaving only spacial data. This script is used to generate the .json files used by the webGL data viewer located at <http://c0z3n.org/mapping>