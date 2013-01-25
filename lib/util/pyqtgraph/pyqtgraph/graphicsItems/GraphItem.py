from .. import functions as fn
from GraphicsObject import GraphicsObject
from ScatterPlotItem import ScatterPlotItem
import pyqtgraph as pg
import numpy as np

__all__ = ['GraphItem']


class GraphItem(GraphicsObject):
    """A GraphItem displays graph information (as in 'graph theory', not 'graphics') as
    a set of nodes connected by lines.
    """

    def __init__(self, **kwds):
        GraphicsObject.__init__(self)
        self.scatter = ScatterPlotItem()
        self.scatter.setParentItem(self)
        self.adjacency = None
        self.pos = None
        self.pen = 'default'
        self.setData(**kwds)
        
    def setData(self, **kwds):
        """
        Change the data displayed by the graph. 
        
        ============ =========================================================
        Arguments
        pos          (N,2) array of the positions of each node in the graph
        adj          (M,2) array of connection data. Each row contains indexes 
                     of two nodes that are connected.
        pen          The pen to use when drawing lines between connected 
                     nodes. May be one of: 
                     * QPen
                     * a single argument to pass to pg.mkPen
                     * a record array of length M
                       with fields (red, green, blue, alpha, width).
                     * None (to disable connection drawing)
                     * 'default' to use the default foreground color.
        symbolPen    The pen used for drawing nodes.
        **opts       All other keyword arguments are given to ScatterPlotItem
                     to affect the appearance of nodes (symbol, size, brush, 
                     etc.)
        ============ =========================================================
        """
        if 'adj' in kwds:
            self.adjacency = kwds.pop('adj')
            self.picture = None
        if 'pos' in kwds:
            self.pos = kwds['pos']
            self.picture = None
        if 'pen' in kwds:
            self.setPen(kwds.pop('pen'))
            self.picture = None
        if 'symbolPen' in kwds:    
            kwds['pen'] = kwds.pop('symbolPen')
        self.scatter.setData(**kwds)

    def setPen(self, pen):
        self.pen = pen
        self.picture = None

    def generatePicture(self):
        self.picture = pg.QtGui.QPicture()
        if self.pen is None or self.pos is None or self.adjacency is None:
            return
        
        p = pg.QtGui.QPainter(self.picture)
        pts = self.pos[self.adjacency]
        pen = self.pen
        if isinstance(pen, np.ndarray):
            lastPen = None
            for i in range(pts.shape[0]):
                pen = self.pen[i]
                if pen != lastPen:
                    lastPen = pen
                    p.setPen(pg.mkPen(color=(pen['red'], pen['green'], pen['blue'], pen['alpha']), width=pen['width']))
                p.drawLine(pg.QtCore.QPointF(*pts[i][0]), pg.QtCore.QPointF(*pts[i][1]))
        else:
            if pen == 'default':
                pen = pg.getConfigOption('foreground')
            p.setPen(pg.mkPen(pen))
            pts = pts.reshape((pts.shape[0]*pts.shape[1], pts.shape[2]))
            path = fn.arrayToQPath(x=pts[:,0], y=pts[:,1], connect='pairs')
            p.drawPath(path)
        
        p.end()

    def paint(self, p, *args):
        if self.picture == None:
            self.generatePicture()
        self.picture.play(p)
        
    def boundingRect(self):
        return self.scatter.boundingRect()
        
        
        
        
        

