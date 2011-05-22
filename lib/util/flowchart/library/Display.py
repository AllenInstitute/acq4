# -*- coding: utf-8 -*-
from ..Node import Node
import weakref
from pyqtgraph import graphicsItems
from PyQt4 import QtCore, QtGui
from common import *
import numpy as np

class PlotWidgetNode(Node):
    """Connection to PlotWidget. Will plot arrays, metaarrays, and display event lists."""
    nodeName = 'PlotWidget'
    sigPlotChanged = QtCore.Signal(object)
    
    def __init__(self, name):
        Node.__init__(self, name, terminals={'In': {'io': 'in', 'multi': True}})
        self.plot = None
        self.items = {}
        
    def disconnected(self, localTerm, remoteTerm):
        if localTerm is self.In and remoteTerm in self.items:
            self.plot.removeItem(self.items[remoteTerm])
            del self.items[remoteTerm]
        
    def setPlot(self, plot):
        #print "======set plot"
        self.plot = plot
        self.sigPlotChanged.emit(self)
        
    def getPlot(self):
        return self.plot
        
    def process(self, In, display=True):
        if display:
            #self.plot.clearPlots()
            items = set()
            for name, vals in In.iteritems():
                if vals is None:
                    continue
                if type(vals) is not list:
                    vals = [vals]
                    
                for val in vals:
                    vid = id(val)
                    if vid in self.items:
                        items.add(vid)
                    else:
                        if isinstance(val, graphicsItems.PlotCurveItem):
                            self.plot.addCurve(val)
                            item = val
                        if isinstance(val, graphicsItems.ScatterPlotItem):
                            self.plot.addDataItem(val)
                            item = val
                        if isinstance(val, QtGui.QGraphicsItem):
                            self.plot.addItem(val)
                            item = val
                        else:
                            item = self.plot.plot(val)
                        self.items[vid] = item
                        items.add(vid)
            for vid in self.items.keys():
                if vid not in items:
                    #print "remove", self.items[vid]
                    self.plot.removeItem(self.items[vid])
                    del self.items[vid]
            
    #def setInput(self, **args):
        #for k in args:
            #self.plot.plot(args[k])
    

            
class CanvasNode(Node):
    """Connection to a Canvas widget."""
    nodeName = 'CanvasWidget'
    
    def __init__(self, name):
        Node.__init__(self, name, terminals={'In': {'io': 'in', 'multi': True}})
        self.canvas = None
        self.items = {}
        
    def disconnected(self, localTerm, remoteTerm):
        if localTerm is self.In and remoteTerm in self.items:
            self.canvas.removeItem(self.items[remoteTerm])
            del self.items[remoteTerm]
        
    def setCanvas(self, canvas):
        self.canvas = canvas
        
    def getCanvas(self):
        return self.canvas
        
    def process(self, In, display=True):
        if display:
            items = set()
            for name, vals in In.iteritems():
                if vals is None:
                    continue
                if type(vals) is not list:
                    vals = [vals]
                    
                for val in vals:
                    vid = id(val)
                    if vid in self.items:
                        items.add(vid)
                    else:
                        self.canvas.addItem(val)
                        item = val
                        self.items[vid] = item
                        items.add(vid)
            for vid in self.items.keys():
                if vid not in items:
                    #print "remove", self.items[vid]
                    self.canvas.removeItem(self.items[vid])
                    del self.items[vid]
            
                    
            
class EventListPlotter(CtrlNode):
    """Prepares an event list for display in a PlotWidget."""
    nodeName = 'EventListPlotter'
    uiTemplate = [
        ('color', 'color'),
    ]
    
    def __init__(self, name):
        CtrlNode.__init__(self, name, terminals={
            'events': {'io': 'in'}, 
            'plot': {'io': 'out', 'multi': True}
        }, ui=self.uiTemplate)
        self.items = {}
        self.ctrls['color'].sigColorChanged.connect(self.colorChanged)
        
    def colorChanged(self):
        c = self.ctrls['color'].color()
        for i in self.items.itervalues():
            i.setPen(c)
        
    def process(self, events, display=True):
        if not display:
            return {'plot': None}
        conn = self['plot'].connections()
        if len(events) > 200:
            events = events[:200]
        color = self.ctrls['color'].color()
        
        ## don't keep items from last run; they may have been removed already.
        self.items = {}
        
        for c in conn:
            plot = c.node().getPlot()
            if plot is None:
                continue
            ## It's possible items were cleared out already; always rebuild.
            #if c in self.items:
                #item = self.items[c]
                #item.setXVals(events)  
            #else:
                #self.items[c] = graphicsItems.VTickGroup(events, view=plot, pen=color)
                #self.items[c].setYRange([0., 0.2], relative=True)
            self.items[c] = graphicsItems.VTickGroup(events, view=plot, pen=color)
            self.items[c].setYRange([0., 0.2], relative=True)
        return {'plot': self.items}
        

class ScatterPlot(CtrlNode):
    """Generates a scatter plot from a record array or nested dicts"""
    nodeName = 'ScatterPlot'
    uiTemplate = [
        ('x', 'combo', {'values': [], 'index': 0}),
        ('y', 'combo', {'values': [], 'index': 0}),
        ('sizeEnabled', 'check', {'value': False}),
        ('size', 'combo', {'values': [], 'index': 0}),
        ('absoluteSize', 'check', {'value': False}),
        ('colorEnabled', 'check', {'value': False}),
        ('color', 'colormap', {}),
        ('borderEnabled', 'check', {'value': False}),
        ('border', 'colormap', {}),
    ]
    
    def __init__(self, name):
        CtrlNode.__init__(self, name, terminals={
            'input': {'io': 'in'},
            'plot': {'io': 'out'}
        })
        self.item = graphicsItems.ScatterPlotItem()
        self.keys = []
        
        #self.ui = QtGui.QWidget()
        #self.layout = QtGui.QGridLayout()
        #self.ui.setLayout(self.layout)
        
        #self.xCombo = QtGui.QComboBox()
        #self.yCombo = QtGui.QComboBox()
        
        
    
    def process(self, input, display=True):
        #print "scatterplot process"
        if not display:
            return {'plot': None}
            
        self.updateKeys(input[0])
        
        x = str(self.ctrls['x'].currentText())
        y = str(self.ctrls['y'].currentText())
        size = str(self.ctrls['size'].currentText())
        pen = QtGui.QPen(QtGui.QColor(0,0,0,0))
        points = []
        for i in input:
            pt = {'pos': (i[x], i[y])}
            if self.ctrls['sizeEnabled'].isChecked():
                pt['size'] = i[size]
            if self.ctrls['borderEnabled'].isChecked():
                pt['pen'] = QtGui.QPen(self.ctrls['border'].getColor(i))
            else:
                pt['pen'] = pen
            if self.ctrls['colorEnabled'].isChecked():
                pt['brush'] = QtGui.QBrush(self.ctrls['color'].getColor(i))
            points.append(pt)
        self.item.setPxMode(not self.ctrls['absoluteSize'].isChecked())
            
        self.item.setPoints(points)
        
        return {'plot': self.item}
        
        

    def updateKeys(self, data):
        if isinstance(data, dict):
            keys = data.keys()
        elif isinstance(data, list) or isinstance(data, tuple):
            keys = data
        elif isinstance(data, np.ndarray) or isinstance(data, np.void):
            keys = data.dtype.names
        else:
            print "Unknown data type:", type(data), data
            return
            
        for c in self.ctrls.itervalues():
            c.blockSignals(True)
        for c in [self.ctrls['x'], self.ctrls['y'], self.ctrls['size']]:
            cur = str(c.currentText())
            c.clear()
            for k in keys:
                c.addItem(k)
                if k == cur:
                    c.setCurrentIndex(c.count()-1)
        for c in [self.ctrls['color'], self.ctrls['border']]:
            c.setArgList(keys)
        for c in self.ctrls.itervalues():
            c.blockSignals(False)
                
        self.keys = keys
        

    def saveState(self):
        state = CtrlNode.saveState(self)
        return {'keys': self.keys, 'ctrls': state}
        
    def restoreState(self, state):
        self.updateKeys(state['keys'])
        CtrlNode.restoreState(self, state['ctrls'])
        
#class ImageItem(Node):
    #"""Creates an ImageItem for display in a canvas from a file handle."""
    #nodeName = 'Image'
    
    #def __init__(self, name):
        #Node.__init__(self, name, terminals={
            #'file': {'io': 'in'},
            #'image': {'io': 'out'}
        #})
        #self.imageItem = graphicsItems.ImageItem()
        #self.handle = None
        
    #def process(self, file, display=True):
        #if not display:
            #return {'image': None}
            
        #if file != self.handle:
            #self.handle = file
            #data = file.read()
            #self.imageItem.updateImage(data)
            
        #pos = file.
        
        
        