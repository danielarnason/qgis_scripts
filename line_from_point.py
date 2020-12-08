import processing
from qgis.processing import alg
from qgis.core import QgsFeature, QgsGeometry, QgsFeatureSink, QgsPoint

@alg(name='linjefrapunkt', label='Vinkelret linje fra punkt', group='mine_scripts', group_label='Mine custom scripts')
@alg.input(type=alg.SOURCE, name='INPUT_LINE', label='Input line layer')
@alg.input(type=alg.SOURCE, name='INPUT_POINT', label='Input point layer')
@alg.input(type=alg.SINK, name='OUTPUT', label='Output line layer')
def linefrompoint(instance, parameters, context, feedback, inputs):
    """
    Tegner en vinkelret linje fra punkter til den nærmeste linje.
    """

    line_input = instance.parameterAsSource(parameters, 'INPUT_LINE', context)
    point_input = instance.parameterAsSource(parameters, 'INPUT_POINT', context)
    (sink, dest_id) = instance.parameterAsSink(parameters, 'OUTPUT', context, line_input.fields(), line_input.wkbType(), line_input.sourceCrs())

    point_geoms = [f.geometry() for f in point_input.getFeatures()]
    line_geoms = [f.geometry() for f in line_input.getFeatures()]

    if feedback.isCanceled():
        return {}

    for p in point_geoms:

        if feedback.isCanceled():
            return {}

        minDistPoint = min([l.closestSegmentWithContext(p.asPoint()) for l in line_geoms])[1]
        perpendicular_line = QgsGeometry.fromPolylineXY([p.asPoint(), minDistPoint])

        new_feat = QgsFeature()
        new_feat.setGeometry(perpendicular_line)

        sink.addFeature(new_feat, QgsFeatureSink.FastInsert)

    return {
        'OUTPUT': dest_id,
    }
