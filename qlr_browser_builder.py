import processing
from qgis.processing import alg
from qgis.core import QgsProject,QgsLayerTreeGroup, QgsLayerDefinition
from qgis.utils import iface
from pathlib import Path

@alg(name="qlr_browser_builder", label="Qlr Browser Builder", group="mine_scripts", group_label="Mine custom scripts")
@alg.input(type=alg.FOLDER_DEST, name='FOLDER_DEST', label='Destination folder')

def qlr_browser_builder(instance, parameters, context, feedback, inputs):
    """
        Exports the structure of the layer panel into a series of qlr files
        intended to be used in the Qlr Browser developed by Septima.
    """
    
    basepath = Path(parameters['FOLDER_DEST'])
        
    root = QgsProject.instance().layerTreeRoot()
    layers = root.findLayers()
    
    for layer in layers:
        iface.setActiveLayer(layer.layer())
        current_node = iface.layerTreeView().currentNode()
        parent = layer.parent()
        provider_type = layer.layer().providerType()
        
        if feedback.isCanceled():
            return {}
        
        if provider_type.lower() == 'wfs':
            qlr_filename = f'{layer.name()} ({provider_type.upper()}).qlr'
        elif provider_type.lower() == 'wms':
            qlr_filename = f'{layer.name()} ({provider_type.upper()}).qlr'
        else:
            qlr_filename = f'{layer.name()}.qlr'
        
        if feedback.isCanceled():
            return {}
            
        if isinstance(parent, QgsLayerTreeGroup):
            if Path(basepath / parent.name()).exists():
                QgsLayerDefinition().exportLayerDefinition(str(Path(basepath / parent.name() / qlr_filename)), [current_node])
            else:
                Path.mkdir(basepath / parent.name())
                QgsLayerDefinition().exportLayerDefinition(str(Path(basepath / parent.name() / qlr_filename)), [current_node])
        else:
            QgsLayerDefinition().exportLayerDefinition(str(Path(basepath / qlr_filename)), [current_node])
    
    
    return {
        'OUTPUT': f'Layer panel structure exported to {basepath}'
    }