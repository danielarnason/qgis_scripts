from qgis import processing
from qgis.processing import alg

@alg(name='addwktcolumn', label='Add a virtual wkt column to layer', group='mine_scripts', group_label='Mine custom scripts')
@alg.input(type=alg.SOURCE, name='INPUT', label='Input vector layer')
def add_wkt_column(instance, parameters, context, feedback, inputs):
    pass