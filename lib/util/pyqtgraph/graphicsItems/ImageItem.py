from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
try:
    import scipy.weave as weave
    from scipy.weave import converters
except:
    pass
import pyqtgraph.functions as fn
import pyqtgraph.debug as debug

class ImageItem(QtGui.QGraphicsObject):
    """
    GraphicsObject displaying an image. Optimized for rapid update (ie video display)
    
    """
    
    
    sigImageChanged = QtCore.Signal()
    
    ## performance gains from this are marginal, and it's rather unreliable.
    useWeave = False
    
    def __init__(self, image=None, copy=True, parent=None, border=None, mode=None, *args):
        #QObjectWorkaround.__init__(self)
        QtGui.QGraphicsObject.__init__(self)
        #self.pixmapItem = QtGui.QGraphicsPixmapItem(self)
        self.qimage = QtGui.QImage()
        self.pixmap = None
        self.paintMode = mode
        #self.useWeave = True
        self.blackLevel = None
        self.whiteLevel = None
        self.alpha = 1.0
        self.image = None
        self.clipLevel = None
        self.drawKernel = None
        if border is not None:
            border = fn.mkPen(border)
        self.border = border
        
        #QtGui.QGraphicsPixmapItem.__init__(self, parent, *args)
        #self.pixmapItem = QtGui.QGraphicsPixmapItem(self)
        if image is not None:
            self.updateImage(image, copy, autoRange=True)
        #self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
        
        #self.item = QtGui.QGraphicsPixmapItem(parent=self)

    def setCompositionMode(self, mode):
        self.paintMode = mode
        self.update()

    def setAlpha(self, alpha):
        self.alpha = alpha
        self.updateImage()
        
    #def boundingRect(self):
        #return self.pixmapItem.boundingRect()
        #return QtCore.QRectF(0, 0, self.qimage.width(), self.qimage.height())
        
    def width(self):
        if self.pixmap is None:
            return None
        return self.pixmap.width()
        
    def height(self):
        if self.pixmap is None:
            return None
        return self.pixmap.height()

    def boundingRect(self):
        if self.pixmap is None:
            return QtCore.QRectF(0., 0., 0., 0.)
        return QtCore.QRectF(0., 0., float(self.width()), float(self.height()))

    def setClipLevel(self, level=None):
        self.clipLevel = level
        
    #def paint(self, p, opt, widget):
        #pass
        #if self.pixmap is not None:
            #p.drawPixmap(0, 0, self.pixmap)
            #print "paint"

    def setLevels(self, white=None, black=None):
        if white is not None:
            self.whiteLevel = white
        if black is not None:
            self.blackLevel = black  
        self.updateImage()
        
    def getLevels(self):
        return self.whiteLevel, self.blackLevel

    def updateImage(self, image=None, copy=True, autoRange=False, clipMask=None, white=None, black=None, axes=None):
        prof = debug.Profiler('ImageItem.updateImage 0x%x' %id(self), disabled=True)
        #debug.printTrace()
        if axes is None:
            axh = {'x': 0, 'y': 1, 'c': 2}
        else:
            axh = axes
        #print "Update image", black, white
        if white is not None:
            self.whiteLevel = white
        if black is not None:
            self.blackLevel = black  
        
        gotNewData = False
        if image is None:
            if self.image is None:
                return
        else:
            gotNewData = True
            if self.image is None or image.shape != self.image.shape:
                self.prepareGeometryChange()
            if copy:
                self.image = image.view(np.ndarray).copy()
            else:
                self.image = image.view(np.ndarray)
        #print "  image max:", self.image.max(), "min:", self.image.min()
        prof.mark('1')
        
        # Determine scale factors
        if autoRange or self.blackLevel is None:
            if self.image.dtype is np.ubyte:
                self.blackLevel = 0
                self.whiteLevel = 255
            else:
                self.blackLevel = self.image.min()
                self.whiteLevel = self.image.max()
        #print "Image item using", self.blackLevel, self.whiteLevel
        
        if self.blackLevel != self.whiteLevel:
            scale = 255. / (self.whiteLevel - self.blackLevel)
        else:
            scale = 0.
        
        prof.mark('2')
        
        ## Recolor and convert to 8 bit per channel
        # Try using weave, then fall back to python
        shape = self.image.shape
        black = float(self.blackLevel)
        white = float(self.whiteLevel)
        
        if black == 0 and white == 255 and self.image.dtype == np.ubyte:
            im = self.image
        elif self.image.dtype in [np.ubyte, np.uint16]:
            # use lookup table instead
            npts = 2**(self.image.itemsize * 8)
            lut = self.getLookupTable(npts, black, white)
            im = lut[self.image]
        else:
            im = self.applyColorScaling(self.image, black, scale)
            
        prof.mark('3')

        try:
            im1 = np.empty((im.shape[axh['y']], im.shape[axh['x']], 4), dtype=np.ubyte)
        except:
            print im.shape, axh
            raise
        alpha = np.clip(int(255 * self.alpha), 0, 255)
        prof.mark('4')
        # Fill image 
        if im.ndim == 2:
            im2 = im.transpose(axh['y'], axh['x'])
            im1[..., 0] = im2
            im1[..., 1] = im2
            im1[..., 2] = im2
            im1[..., 3] = alpha
        elif im.ndim == 3: #color image
            im2 = im.transpose(axh['y'], axh['x'], axh['c'])
            if im2.shape[2] > 4:
                raise Exception("ImageItem got image with more than 4 color channels (shape is %s; axes are %s)" % (str(im.shape), str(axh)))
            ##      [B G R A]    Reorder colors
            order = [2,1,0,3] ## for some reason, the colors line up as BGR in the final image.
            
            for i in range(0, im.shape[axh['c']]):
                im1[..., order[i]] = im2[..., i]    
            
            ## fill in unused channels with 0 or alpha
            for i in range(im.shape[axh['c']], 3):
                im1[..., i] = 0
            if im.shape[axh['c']] < 4:
                im1[..., 3] = alpha
                
        else:
            raise Exception("Image must be 2 or 3 dimensions")
        #self.im1 = im1
        # Display image
        prof.mark('5')
        if self.clipLevel is not None or clipMask is not None:
            if clipMask is not None:
                mask = clipMask.transpose()
            else:
                mask = (self.image < self.clipLevel).transpose()
            im1[..., 0][mask] *= 0.5
            im1[..., 1][mask] *= 0.5
            im1[..., 2][mask] = 255
        prof.mark('6')
        #print "Final image:", im1.dtype, im1.min(), im1.max(), im1.shape
        self.ims = im1.tostring()  ## Must be held in memory here because qImage won't do it for us :(
        prof.mark('7')
        qimage = QtGui.QImage(buffer(self.ims), im1.shape[1], im1.shape[0], QtGui.QImage.Format_ARGB32)
        prof.mark('8')
        self.pixmap = QtGui.QPixmap.fromImage(qimage)
        prof.mark('9')
        ##del self.ims
        #self.item.setPixmap(self.pixmap)
        
        self.update()
        prof.mark('10')
        
        if gotNewData:
            #self.emit(QtCore.SIGNAL('imageChanged'))
            self.sigImageChanged.emit()
            
        prof.finish()
        
    def getLookupTable(self, num, black, white):
        num = int(num)
        black = int(black)
        white = int(white)
        if white < black:
            b = black
            black = white
            white = b
        key = (num, black, white)
        lut = np.empty(num, dtype=np.ubyte)
        lut[:black] = 0
        rng = lut[black:white]
        try:
            rng[:] = np.linspace(0, 255, white-black)[:len(rng)]
        except:
            print key, rng.shape
        lut[white:] = 255
        return lut
        
        
    def applyColorScaling(self, img, offset, scale):
        try:
            if not ImageItem.useWeave:
                raise Exception('Skipping weave compile')
            #sim = np.ascontiguousarray(self.image)  ## should not be needed
            sim = img.reshape(img.size)
            #sim.shape = sim.size
            im = np.empty(sim.shape, dtype=np.ubyte)
            n = im.size
            
            code = """
            for( int i=0; i<n; i++ ) {
                float a = (sim(i)-offset) * (float)scale;
                if( a > 255.0 )
                    a = 255.0;
                else if( a < 0.0 )
                    a = 0.0;
                im(i) = a;
            }
            """
            
            weave.inline(code, ['sim', 'im', 'n', 'offset', 'scale'], type_converters=converters.blitz, compiler = 'gcc')
            #sim.shape = shape
            im.shape = img.shape
        except:
            if ImageItem.useWeave:
                ImageItem.useWeave = False
                #sys.excepthook(*sys.exc_info())
                #print "=============================================================================="
                #print "Weave compile failed, falling back to slower version."
            #img.shape = shape
            im = ((img - offset) * scale).clip(0.,255.).astype(np.ubyte)
        return im
        
        
    def getPixmap(self):
        return self.pixmap.copy()

    def getHistogram(self, bins=500, step=3):
        """returns x and y arrays containing the histogram values for the current image.
        The step argument causes pixels to be skipped when computing the histogram to save time."""
        stepData = self.image[::step, ::step]
        hist = np.histogram(stepData, bins=bins)
        return hist[1][:-1], hist[0]

    def setPxMode(self, b):
        """Set whether the item ignores transformations and draws directly to screen pixels."""
        self.setFlag(self.ItemIgnoresTransformations, b)
            
    def setScaledMode(self):
        self.setPxMode(False)

    def mousePressEvent(self, ev):
        if self.drawKernel is not None and ev.button() == QtCore.Qt.LeftButton:
            self.drawAt(ev.pos(), ev)
            ev.accept()
        else:
            ev.ignore()
        
    def mouseMoveEvent(self, ev):
        #print "mouse move", ev.pos()
        if self.drawKernel is not None:
            self.drawAt(ev.pos(), ev)
    
    def mouseReleaseEvent(self, ev):
        pass
    
    def tabletEvent(self, ev):
        print ev.device()
        print ev.pointerType()
        print ev.pressure()
    
    def drawAt(self, pos, ev=None):
        pos = [int(pos.x()), int(pos.y())]
        dk = self.drawKernel
        kc = self.drawKernelCenter
        sx = [0,dk.shape[0]]
        sy = [0,dk.shape[1]]
        tx = [pos[0] - kc[0], pos[0] - kc[0]+ dk.shape[0]]
        ty = [pos[1] - kc[1], pos[1] - kc[1]+ dk.shape[1]]
        
        for i in [0,1]:
            dx1 = -min(0, tx[i])
            dx2 = min(0, self.image.shape[0]-tx[i])
            tx[i] += dx1+dx2
            sx[i] += dx1+dx2

            dy1 = -min(0, ty[i])
            dy2 = min(0, self.image.shape[1]-ty[i])
            ty[i] += dy1+dy2
            sy[i] += dy1+dy2

        #print sx
        #print sy
        #print tx
        #print ty
        #print self.image.shape
        #print self.image[tx[0]:tx[1], ty[0]:ty[1]].shape
        #print dk[sx[0]:sx[1], sy[0]:sy[1]].shape
        ts = (slice(tx[0],tx[1]), slice(ty[0],ty[1]))
        ss = (slice(sx[0],sx[1]), slice(sy[0],sy[1]))
        #src = dk[sx[0]:sx[1], sy[0]:sy[1]]
        #mask = self.drawMask[sx[0]:sx[1], sy[0]:sy[1]]
        mask = self.drawMask
        src = dk
        #print self.image[ts].shape, src.shape
        
        if callable(self.drawMode):
            self.drawMode(dk, self.image, mask, ss, ts, ev)
        else:
            src = src[ss]
            if self.drawMode == 'set':
                if mask is not None:
                    mask = mask[ss]
                    self.image[ts] = self.image[ts] * (1-mask) + src * mask
                else:
                    self.image[ts] = src
            elif self.drawMode == 'add':
                self.image[ts] += src
            else:
                raise Exception("Unknown draw mode '%s'" % self.drawMode)
            self.updateImage()
        
    def setDrawKernel(self, kernel=None, mask=None, center=(0,0), mode='set'):
        self.drawKernel = kernel
        self.drawKernelCenter = center
        self.drawMode = mode
        self.drawMask = mask
    
    def paint(self, p, *args):
        
        #QtGui.QGraphicsPixmapItem.paint(self, p, *args)
        if self.pixmap is None:
            return
        if self.paintMode is not None:
            p.setCompositionMode(self.paintMode)
        p.drawPixmap(self.boundingRect(), self.pixmap, QtCore.QRectF(0, 0, self.pixmap.width(), self.pixmap.height()))
        if self.border is not None:
            p.setPen(self.border)
            p.drawRect(self.boundingRect())

    def pixelSize(self):
        """return size of a single pixel in the image"""
        br = self.sceneBoundingRect()
        return br.width()/self.pixmap.width(), br.height()/self.pixmap.height()
