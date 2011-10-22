from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pyqtgraph.functions as fn
from GraphicsObject import GraphicsObject

class ScatterPlotItem(GraphicsObject):
    
    #sigPointClicked = QtCore.Signal(object, object)
    sigClicked = QtCore.Signal(object, object)  ## self, points
    
    def __init__(self, spots=None, x=None, y=None, pxMode=True, pen='default', brush='default', size=5, 
        style=None, identical=False, data=None):
            
        """
        Arguments:
            spots: list of dicts. Each dict specifies parameters for a single spot:
                   {'pos': (x,y), 'size', 'pen', 'brush', 'style'}
            x,y: array of x,y values. Alternatively, specify spots['pos'] = (x,y)
            pxMode: If True, spots are always the same size regardless of scaling, and size is given in px.
                    Otherwise, size is in scene coordinates and the spots scale with the view.
            identical: If True, all spots are forced to look identical. 
                       This can result in performance enhancement.
        """
        
        
        GraphicsObject.__init__(self)
        self.spots = []
        self.range = [[0,0], [0,0]]
        self.identical = identical
        self._spotPixmap = None
        
        if brush == 'default':
            self.brush = QtGui.QBrush(QtGui.QColor(100, 100, 150))
        else:
            self.brush = fn.mkBrush(brush)
        
        if pen == 'default':
            self.pen = QtGui.QPen(QtGui.QColor(200, 200, 200))
        else:
            self.pen = fn.mkPen(pen)
        
        self.style = style
        self.size = size
        
        self.pxMode = pxMode
        if spots is not None or x is not None:
            self.setPoints(spots, x, y, data)
            
        #self.optimize = optimize
        #if optimize:
            #self.spotImage = QtGui.QImage(size, size, QtGui.QImage.Format_ARGB32_Premultiplied)
            #self.spotImage.fill(0)
            #p = QtGui.QPainter(self.spotImage)
            #p.setRenderHint(p.Antialiasing)
            #p.setBrush(brush)
            #p.setPen(pen)
            #p.drawEllipse(0, 0, size, size)
            #p.end()
            #self.optimizePixmap = QtGui.QPixmap(self.spotImage)
            #self.optimizeFragments = []
            #self.setFlags(self.flags() | self.ItemIgnoresTransformations)
            
    def setPxMode(self, mode):
        self.pxMode = mode
            
    def clear(self):
        for i in self.spots:
            i.setParentItem(None)
            s = i.scene()
            if s is not None:
                s.removeItem(i)
        self.spots = []
        

    def getRange(self, ax, percent):
        return self.range[ax]
        
    def setPoints(self, spots=None, x=None, y=None, data=None):
        """
        Remove all existing points in the scatter plot and add a new set.
        Arguments:
            spots - list of dicts specifying parameters for each spot
                    [ {'pos': (x,y), 'pen': 'r', ...}, ...]
            x, y -  arrays specifying location of spots to add. 
                    all other parameters (pen, style, etc.) will be set to the default
                    values for this scatter plot.
                    these arguments are IGNORED if 'spots' is specified
            data -  list of arbitrary objects to be assigned to spot.data for each spot
                    (this is useful for identifying spots that are clicked on)
        """
        self.clear()
        self.range = [[0,0],[0,0]]
        self.addPoints(spots, x, y, data)

    def addPoints(self, spots=None, x=None, y=None, data=None):
        xmn = ymn = xmx = ymx = None
        if spots is not None:
            n = len(spots)
        else:
            n = len(x)
        
        for i in range(n):
            if spots is not None:
                s = spots[i]
                pos = Point(s['pos'])
            else:
                s = {}
                pos = Point(x[i], y[i])
            if data is not None:
                s['data'] = data[i]
                
            size = s.get('size', self.size)
            if self.pxMode:
                psize = 0
            else:
                psize = size
            if xmn is None:
                xmn = pos[0]-psize
                xmx = pos[0]+psize
                ymn = pos[1]-psize
                ymx = pos[1]+psize
            else:
                xmn = min(xmn, pos[0]-psize)
                xmx = max(xmx, pos[0]+psize)
                ymn = min(ymn, pos[1]-psize)
                ymx = max(ymx, pos[1]+psize)
            #print pos, xmn, xmx, ymn, ymx
            brush = s.get('brush', self.brush)
            pen = s.get('pen', self.pen)
            pen.setCosmetic(True)
            style = s.get('style', self.style)
            data2 = s.get('data', None)
            item = self.mkSpot(pos, size, self.pxMode, brush, pen, data2, style=style, index=len(self.spots))
            self.spots.append(item)
            #if self.optimize:
                #item.hide()
                #frag = QtGui.QPainter.PixmapFragment.create(pos, QtCore.QRectF(0, 0, size, size))
                #self.optimizeFragments.append(frag)
        self.range = [[xmn, xmx], [ymn, ymx]]
        
    #def setPointSize(self, size):
        #for s in self.spots:
            #s.size = size
        ##self.setPoints([{'size':s.size, 'pos':s.pos(), 'data':s.data} for s in self.spots])
        #self.setPoints()
                
    #def paint(self, p, *args):
        #if not self.optimize:
            #return
        ##p.setClipRegion(self.boundingRect())
        #p.drawPixmapFragments(self.optimizeFragments, self.optimizePixmap)

    def paint(self, *args):
        pass

    def spotPixmap(self):
        ## If all spots are identical, return the pixmap to use for all spots
        ## Otherwise return None
        
        if not self.identical:
            return None
        if self._spotPixmap is None:
            #print 'spotPixmap'
            spot = SpotItem(size=self.size, pxMode=True, brush=self.brush, pen=self.pen, style=self.style)
            #self._spotPixmap = PixmapSpotItem.makeSpotImage(self.size, self.pen, self.brush, self.style)
            self._spotPixmap = spot.pixmap
        return self._spotPixmap

    def mkSpot(self, pos, size, pxMode, brush, pen, data, style=None, index=None):
        ## Make and return a SpotItem (or PixmapSpotItem if in pxMode)
        
        brush = fn.mkBrush(brush)
        pen = fn.mkPen(pen)
        if pxMode:
            img = self.spotPixmap()  ## returns None if not using identical mode
            #item = PixmapSpotItem(size, brush, pen, data, image=img, style=style, index=index)
            item = SpotItem(size, pxMode, brush, pen, data, style=style, image=img, index=index)
        else:
            item = SpotItem(size, pxMode, brush, pen, data, style=style, index=index)
        item.setParentItem(self)
        item.setPos(pos)
        #item.sigClicked.connect(self.pointClicked)
        return item
        
    def boundingRect(self):
        ((xmn, xmx), (ymn, ymx)) = self.range
        if xmn is None or xmx is None or ymn is None or ymx is None:
            return QtCore.QRectF()
        return QtCore.QRectF(xmn, ymn, xmx-xmn, ymx-ymn)
        #return QtCore.QRectF(xmn-1, ymn-1, xmx-xmn+2, ymx-ymn+2)
        
    #def pointClicked(self, point):
        #self.sigPointClicked.emit(self, point)

    def points(self):
        return self.spots[:]

    def pointsAt(self, pos):
        x = pos.x()
        y = pos.y()
        pw = self.pixelWidth()
        ph = self.pixelHeight()
        pts = []
        for s in self.spots:
            sp = s.pos()
            ss = s.size
            sx = sp.x()
            sy = sp.y()
            s2x = s2y = ss * 0.5
            if self.pxMode:
                s2x *= pw
                s2y *= ph
            if x > sx-s2x and x < sx+s2x and y > sy-s2y and y < sy+s2y:
                pts.append(s)
                #print "HIT:", x, y, sx, sy, s2x, s2y
            #else:
                #print "No hit:", (x, y), (sx, sy)
                #print "       ", (sx-s2x, sy-s2y), (sx+s2x, sy+s2y)
        pts.sort(lambda a,b: cmp(b.zValue(), a.zValue()))
        return pts
            

    def mousePressEvent(self, ev):
        QtGui.QGraphicsItem.mousePressEvent(self, ev)
        if ev.button() == QtCore.Qt.LeftButton:
            pts = self.pointsAt(ev.pos())
            if len(pts) > 0:
                self.mouseMoved = False
                self.ptsClicked = pts
                ev.accept()
            else:
                #print "no spots"
                ev.ignore()
        else:
            ev.ignore()
        
    def mouseMoveEvent(self, ev):
        QtGui.QGraphicsItem.mouseMoveEvent(self, ev)
        self.mouseMoved = True
        pass
    
    def mouseReleaseEvent(self, ev):
        QtGui.QGraphicsItem.mouseReleaseEvent(self, ev)
        if not self.mouseMoved:
            self.sigClicked.emit(self, self.ptsClicked)


class SpotItem(QtGui.QGraphicsWidget):
    #sigClicked = QtCore.Signal(object)
    
    def __init__(self, size, pxMode, brush, pen, data=None, style=None, image=None, index=None):
        QtGui.QGraphicsWidget.__init__(self)
        self.pxMode = pxMode

        if style is None:
            style = 'o'    ## circle by default
        elif isinstance(style, int):  ## allow styles specified by integer for easy iteration
            style = ['o', 's', 't', 'd', '+'][style]
        ####print 'SpotItem style: ', style
        self.data = data
        self.pen = pen
        self.brush = brush
        self.size = size
        self.index = index
        self.style = style
        #s2 = size/2.
        self.path = QtGui.QPainterPath()
        if style == 'o':
            self.path.addEllipse(QtCore.QRectF(-0.5, -0.5, 1, 1))
        elif style == 's':
            self.path.addRect(QtCore.QRectF(-0.5, -0.5, 1, 1))
        elif style is 't' or style is '^':
            self.path.moveTo(-0.5, -0.5)
            self.path.lineTo(0, 0.5)
            self.path.lineTo(0.5, -0.5)
            self.path.closeSubpath()
            #self.path.connectPath(self.path)
        elif style == 'd':
            self.path.moveTo(0., -0.5)
            self.path.lineTo(-0.4, 0.)
            self.path.lineTo(0, 0.5)
            self.path.lineTo(0.4, 0)
            self.path.closeSubpath()
            #self.path.connectPath(self.path)
        elif style == '+':
            self.path.moveTo(-0.5, -0.01)
            self.path.lineTo(-0.5, 0.01)
            self.path.lineTo(-0.01, 0.01)
            self.path.lineTo(-0.01, 0.5)
            self.path.lineTo(0.01, 0.5)
            self.path.lineTo(0.01, 0.01)
            self.path.lineTo(0.5, 0.01)
            self.path.lineTo(0.5, -0.01)
            self.path.lineTo(0.01, -0.01)
            self.path.lineTo(0.01, -0.5)
            self.path.lineTo(-0.01, -0.5)
            self.path.lineTo(-0.01, -0.01)
            self.path.closeSubpath()
            #self.path.connectPath(self.path)
        #elif style == 'x':
        else:
            raise Exception("Unknown spot style '%s'" % style)
            #self.path.addEllipse(QtCore.QRectF(-0.5, -0.5, 1, 1))
        
        if pxMode:
            ## pre-render an image of the spot and display this rather than redrawing every time.
            if image is None:
                self.pixmap = self.makeSpotImage(size, pen, brush, style)
            else:
                self.pixmap = image ## image is already provided (probably shared with other spots)
            self.setFlags(self.flags() | self.ItemIgnoresTransformations | self.ItemHasNoContents)
            self.pi = QtGui.QGraphicsPixmapItem(self.pixmap, self)
            self.pi.setPos(-0.5*size, -0.5*size)
        else:
            self.scale(size, size)


    def makeSpotImage(self, size, pen, brush, style=None):
        self.spotImage = QtGui.QImage(size+2, size+2, QtGui.QImage.Format_ARGB32_Premultiplied)
        self.spotImage.fill(0)
        p = QtGui.QPainter(self.spotImage)
        p.setRenderHint(p.Antialiasing)
        p.translate(size*0.5+1, size*0.5+1)
        p.scale(size, size)
        self.paint(p, None, None)
        p.end()
        return QtGui.QPixmap(self.spotImage)


    def setBrush(self, brush):
        self.brush = fn.mkBrush(brush)
        self.update()
        
    def setPen(self, pen):
        self.pen = fn.mkPen(pen)
        self.update()
        
    def boundingRect(self):
        return self.path.boundingRect()
        
    def shape(self):
        return self.path
        
    def paint(self, p, *opts):
        p.setPen(self.pen)
        p.setBrush(self.brush)
        p.drawPath(self.path)
        
    #def mousePressEvent(self, ev):
        #QtGui.QGraphicsItem.mousePressEvent(self, ev)
        #if ev.button() == QtCore.Qt.LeftButton:
            #self.mouseMoved = False
            #ev.accept()
        #else:
            #ev.ignore()

        
        
    #def mouseMoveEvent(self, ev):
        #QtGui.QGraphicsItem.mouseMoveEvent(self, ev)
        #self.mouseMoved = True
        #pass
    
    #def mouseReleaseEvent(self, ev):
        #QtGui.QGraphicsItem.mouseReleaseEvent(self, ev)
        #if not self.mouseMoved:
            #self.sigClicked.emit(self)
        
#class PixmapSpotItem(QtGui.QGraphicsItem):
    ##sigClicked = QtCore.Signal(object)
    
    #def __init__(self, size, brush, pen, data, image=None, style=None, index=None):
        #"""This class draws a scale-invariant image centered at 0,0.
        #If no image is specified, then an antialiased circle is constructed instead.
        #It should be quite fast, but large spots will use a lot of memory."""
        
        #QtGui.QGraphicsItem.__init__(self)
        #self.pen = pen
        #self.brush = brush
        #self.size = size
        #self.style = style
        #self.index = index
        #self.setFlags(self.flags() | self.ItemIgnoresTransformations | self.ItemHasNoContents)
        #if image is None:
            #self.image = self.makeSpotImage(self.size, self.pen, self.brush, style=style)
        #else:
            #self.image = image
        #self.pixmap = QtGui.QPixmap(self.image)
        ##self.setPixmap(self.pixmap)
        #self.data = data
        #self.pi = QtGui.QGraphicsPixmapItem(self.pixmap, self)
        #self.pi.setPos(-0.5*size, -0.5*size)
        
        ##self.translate(-0.5, -0.5)
    #def boundingRect(self):
        #return self.pi.boundingRect()
        
    #@staticmethod
    #def makeSpotImage(size, pen, brush, style=None):
        #img = QtGui.QImage(size+2, size+2, QtGui.QImage.Format_ARGB32_Premultiplied)
        #img.fill(0)
        #p = QtGui.QPainter(img)
        #try:
            #p.setRenderHint(p.Antialiasing)
            #p.setBrush(brush)
            #p.setPen(pen)
##            print 'mkspotimage style: ', style
            #if style is 'o': # circle
                #p.drawEllipse(0, 0, size, size)
            #elif style == 's': # square
                #p.drawRect(QtCore.QRectF(0., 0., size, size))
            #elif style is 't' or style is '^': # triangle
                #path = QtGui.QPainterPath()
                #ppath=QtGui.QPolygonF([QtCore.QPointF(0, size), 
                    #QtCore.QPointF(size, size), QtCore.QPointF((size/2.0), 0),
                    #QtCore.QPointF(0, size)])
                #path.addPolygon(ppath)
                #p.drawPath(path)
            #elif style == 'd': # diamond
                #path=QtGui.QPainterPath()
                #ppath = QtGui.QPolygonF([QtCore.QPointF(0.1*size, 0.5*size), QtCore.QPointF(0.5*size, 0.0),
                    #QtCore.QPointF(0.9*size, 0.5*size),QtCore.QPointF(0.5*size, size)])
                #path.addPolygon(ppath)
                #p.drawPath(path)
            #elif style == '+': # plus, obviously
                #path=QtGui.QPainterPath()
                #path.moveTo(size/2, 0.0)
                #path.lineTo(size/2, size)
                #path.moveTo(0, size/2)
                #path.lineTo(size, size/2)
                #p.drawPath(path)
            #elif style == 'x': # x, obviously
                #path=QtGui.QPainterPath()
                #path.moveTo(0., 0.0)
                #path.lineTo(size, size)
                #path.moveTo(0, size)
                #path.lineTo(size, 0)
                #p.drawPath(path)
            #elif style == '*': # asterix (sic), obviously
                #path=QtGui.QPainterPath()
                #path.moveTo(0., 0.0)
                #path.lineTo(size, size)
                #path.moveTo(0, size)
                #path.lineTo(size, 0)
                #path.moveTo(size/2.0, 0)
                #path.lineTo(size/2.0, size)
                #path.moveTo(0., size/2.0)
                #path.lineTo(size, size/2.0)
                #p.drawPath(path)
            #else: # default is the circle - also "none"
                #p.drawEllipse(0, 0, size, size)
        #finally:
            #p.end()  ## failure to end a painter properly causes crash.
        #return img
        
        
        
    #def paint(self, p, *args):
        #p.setCompositionMode(p.CompositionMode_Plus)
        #QtGui.QGraphicsPixmapItem.paint(self, p, *args)
        
    #def setBrush(self, brush):
        #self.brush = fn.mkBrush(brush)
        #self.update()
        
    #def setPen(self, pen):
        #self.pen = fn.mkPen(pen)
        #self.update()
        
    #def boundingRect(self):
        #return self.path.boundingRect()
        
    #def shape(self):
        #return self.path
        
    #def paint(self, p, *opts):
        #if self.pxMode:
            #p.drawPixmap(QtCore.QPoint(int(-0.5*self.size), int(-0.5*self.size)), self.pixmap)
        #else:
            #p.setPen(self.pen)
            #p.setBrush(self.brush)
            #p.drawPath(self.path)

