# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from CanvasItem import CanvasItem
from ImageCanvasItem import ImageCanvasItem
import ScanCanvasItemTemplate
import lib.Manager
import pyqtgraph as pg
import numpy as np
import ProgressDialog

class ScanCanvasItem(CanvasItem):
    def __init__(self, **opts):
        """
        Create a new CanvasItem representing a scan.
        Options:
            handle: DirHandle where scan data is stored (required)
            subDirs: list of DirHandles to the individual Protocols for each spot 
                     (optional; this allows the inclusion of only part of a scan sequence)
        """
        if 'handle' not in opts:
            raise Exception("ScanCanvasItem must be initialized with 'handle' or 'handles' specified in opts")
        
        ## Top-level dirHandle tells us the default name of the item 
        ## and may have a userTransform
        dirHandle = opts['handle']
        if 'name' not in opts:
            opts['name'] = dirHandle.shortName()
            
        ## Get the specific list of subdirs to use from which to pull spot information
        if 'subDirs' in opts:
            dirs = opts['subDirs']
        else:
            model = lib.Manager.getManager().dataModel
            typ = model.dirType(dirHandle)
            if typ == 'ProtocolSequence':
                dirs = [dirHandle[d] for d in dirHandle.subDirs()]
            elif typ == 'Protocol':
                dirs = [dirHandle]
            else:
                raise Exception("Invalid dir type '%s'" % typ)

        ## Generate spot data and a scatterplotitem
        pts = []
        for d in dirs:
            if 'Scanner' in d.info() and 'position' in d.info()['Scanner']: #Note: this is expected to fail (gracefully) when a protocol sequence is incomplete
                pos = d.info()['Scanner']['position']
                if 'spotSize' in d.info()['Scanner']:
                    size = d.info()['Scanner']['spotSize']
                else:
                    size = self.defaultSize
                pts.append({'pos': pos, 'size': size, 'data': d})
        self.scatterPlotData = pts
        if len(pts) == 0:
            raise Exception("No data found in scan.")
        gitem = pg.ScatterPlotItem(pts, pxMode=False)
        #citem = ScanCanvasItem(self, item, handle=dirHandle, **opts)
        #self._addCanvasItem(citem)
        #return [citem]
        CanvasItem.__init__(self, gitem, **opts)
        #self.scatterPlot = gitem
        self.originalSpotSize = size
        
        
        
        self._ctrlWidget = QtGui.QWidget()
        self.ui = ScanCanvasItemTemplate.Ui_Form()
        self.ui.setupUi(self._ctrlWidget)
        self.layout.addWidget(self._ctrlWidget, self.layout.rowCount(), 0, 1, 2)
        
        self.addScanImageBtn = self.ui.loadSpotImagesBtn
        
        #self.transformGui.mirrorImageBtn.clicked.connect(self.mirrorY)
        self.ui.sizeSpin.setOpts(dec=True, step=1, minStep=1e-6, siPrefix=True, suffix='m', bounds=[1e-6, None])
        self.ui.sizeSpin.setValue(self.originalSpotSize)
        self.ui.sizeSpin.valueChanged.connect(self.sizeSpinEdited)
        self.ui.sizeFromCalibrationRadio.clicked.connect(self.updateSpotSize)
        
        self.addScanImageBtn.connect(self.addScanImageBtn, QtCore.SIGNAL('clicked()'), self.loadScanImage)



    #def addScan(self, dirHandle, **opts):
        #"""Returns a list of ScanCanvasItems."""
        
        #if 'sequenceParams' in dirHandle.info():
            #dirs = [dirHandle[d] for d in dirHandle.subDirs()]
        #else:
            #dirs = [dirHandle]
            
        #if 'separateParams' not in opts:
            #separateParams = False
        #else:
            #separateParams = opts['separateParams']
            #del(opts['separateParams'])
            
        
        #### check for sequence parameters (besides targets) so that we can separate them out into individual Scans
        #paramKeys = []
        #params = dirHandle.info()['protocol']['params']
        #if len(params) > 1 and separateParams==True:
            #for i in range(len(params)):
                #k = (params[i][0], params[i][1])
                #if k != ('Scanner', 'targets'):
                    #paramKeys.append(k)
            
        #if 'name' not in opts:
            #opts['name'] = dirHandle.shortName()
            

            
        #if len(paramKeys) < 1:    
            #pts = []
            #for d in dirs: #d is a directory handle
                ##d = dh[d]
                #if 'Scanner' in d.info() and 'position' in d.info()['Scanner']:
                    #pos = d.info()['Scanner']['position']
                    #if 'spotSize' in d.info()['Scanner']:
                        #size = d.info()['Scanner']['spotSize']
                    #else:
                        #size = self.defaultSize
                    #pts.append({'pos': pos, 'size': size, 'data': d})
            
            #item = graphicsItems.ScatterPlotItem(pts, pxMode=False)
            #citem = ScanCanvasItem(self, item, handle=dirHandle, **opts)
            #self._addCanvasItem(citem)
            #return [citem]
        #else:
            #pts = {}
            #for d in dirs:
                #k = d.info()[paramKeys[0]]
                #if len(pts) < k+1:
                    #pts[k] = []
                #if 'Scanner' in d.info() and 'position' in d.info()['Scanner']:
                    #pos = d.info()['Scanner']['position']
                    #if 'spotSize' in d.info()['Scanner']:
                        #size = d.info()['Scanner']['spotSize']
                    #else:
                        #size = self.defaultSize
                    #pts[k].append({'pos': pos, 'size': size, 'data': d})
            #spots = []
            #for k in pts.keys():
                #spots.extend(pts[k])
            #item = graphicsItems.ScatterPlotItem(spots=spots, pxMode=False)
            #parentCitem = ScanCanvasItem(self, item, handle=dirHandle, **opts)
            #self._addCanvasItem(parentCitem)
            #scans = []
            #for k in pts.keys():
                #opts['name'] = paramKeys[0][0] + '_%03d' %k
                #item = graphicsItems.ScatterPlotItem(spots=pts[k], pxMode=False)
                #citem = ScanCanvasItem(self, item, handle = dirHandle, parent=parentCitem, **opts)
                #self._addCanvasItem(citem)
                ##scans[opts['name']] = citem
                #scans.append(citem)
            #return scans
        
        #print "Creating ScanCanvasItem...."
    
    
    @classmethod
    def checkFile(cls, fh):
        if fh.isFile():
            return 0
        try:
            model = lib.Manager.getManager().dataModel
            typ = model.dirType(fh)
            if typ == 'ProtocolSequence':  ## should do some deeper inspection here..
                return 10
            elif typ == 'Protocol':
                return 10
            return 0
        except AttributeError:
            return 0
        
    
    def loadScanImage(self):
        #print 'loadScanImage called.'
        #dh = self.ui.fileLoader.ui.dirTree.selectedFile()
        #scan = self.canvas.selectedItem()
        dh = self.opts['handle']
        dirs = [dh[d] for d in dh.subDirs()]
        if 'Camera' not in dirs[0].subDirs():
            print "No image data for this scan."
            return
        
        spotFrame = self.ui.spotFrameSpin.value()
        bgFrame = self.ui.bgFrameSpin.value()
        
        images = []
        nulls = []
        with ProgressDialog.ProgressDialog("Processing scan images..", 0, len(dirs)) as dlg:
            for d in dirs:
                if 'Camera' not in d.subDirs():
                    continue
                frames = d['Camera']['frames.ma'].read()
                if self.ui.bgFrameCheck.isChecked():
                    image = frames[spotFrame]-frames[bgFrame]
                    image[frames[bgFrame] > frames[spotFrame]] = 0.  ## unsigned type; avoid negative values
                else:
                    image = frames[spotFrame]
                    
                mx = image.max()
                image *= (1000. / mx)
                images.append(image)
                if mx < 50:
                    nulls.append(d.shortName())
                dlg += 1
                if dlg.wasCanceled():
                    raise Exception("Processing canceled by user")                
            
        print "Null frames for %s:" %dh.shortName(), nulls
        scanImages = np.zeros(images[0].shape)
        for im in images:
            mask = im > scanImages
            scanImages[mask] = im[mask]
        
        info = dirs[0]['Camera']['frames.ma'].read()._info[-1]
    
        pos =  info['imagePosition']
        scale = info['pixelSize']
        image = ImageCanvasItem(scanImages, pos=pos, scale=scale, z=self.opts['z']-1, name='scanImage')
        item = self.canvas.addItem(image)
        self.scanImage = item
        
        self.scanImage.restoreTransform(self.saveTransform())
        
        #self.canvas.items[item] = scanImages
        
    def sizeSpinEdited(self):
        self.ui.sizeCustomRadio.setChecked(True)
        self.updateSpotSize()
        
    #def calibrationRadioClicked(self):
        #self.updateSpotSize()

    def updateSpotSize(self):
        size = self.getSpotSize()
        for p in self.scatterPlotData:
            p['size'] = size
        self.graphicsItem().setPoints(self.scatterPlotData)
        
    def getSpotSize(self):
        if self.ui.sizeCustomRadio.isChecked():
            size = self.ui.sizeSpin.value()
        elif self.ui.sizeFromCalibrationRadio.isChecked():
            self.ui.sizeSpin.valueChanged.disconnect(self.sizeSpinEdited)
            self.ui.sizeSpin.setValue(self.originalSpotSize)
            self.ui.sizeSpin.valueChanged.connect(self.sizeSpinEdited)
            size = self.originalSpotSize
        return size
        
