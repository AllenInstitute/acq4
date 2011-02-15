# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from weakref import *

class TreeWidget(QtGui.QTreeWidget):
    """Extends QTreeWidget to allow internal drag/drop with widgets in the tree.
    Also maintains the expanded state of subtrees as they are moved.
    This class demonstrates the absurd lengths one must go to to make drag/drop work."""
    
    sigItemMoved = QtCore.Signal(object, object, object)
    
    def __init__(self, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        #self.itemWidgets = WeakKeyDictionary()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.placeholders = []

    def setItemWidget(self, item, col, wid):
        w = QtGui.QWidget()  ## foster parent / surrogate child widget
        l = QtGui.QVBoxLayout()
        l.setContentsMargins(0,0,0,0)
        w.setLayout(l)
        w.setSizePolicy(wid.sizePolicy())
        w.setMinimumHeight(wid.minimumHeight())
        w.setMinimumWidth(wid.minimumWidth())
        l.addWidget(wid)
        w.realChild = wid
        self.placeholders.append(w)
        QtGui.QTreeWidget.setItemWidget(self, item, col, w)

    def itemWidget(self, item, col):
        w = QtGui.QTreeWidget.itemWidget(self, item, col)
        if w is not None:
            w = w.realChild
        return w

    def dropMimeData(self, parent, index, data, action):
        item = self.currentItem()
        p = parent
        #print "drop", item, "->", parent, index
        while True:
            if p is None:
                break
            if p == item:
                return False
                #raise Exception("Can not move item into itself.")
            p = p.parent()
        
        if not self.itemMoving(item, parent, index):
            return False
        
        currentParent = item.parent()
        if currentParent is None:
            currentParent = self.invisibleRootItem()
        if parent is None:
            parent = self.invisibleRootItem()
            
        if currentParent == parent and index > parent.indexOfChild(item):
            index -= 1
            
        self.prepareMove(item)
            
        currentParent.removeChild(item)
        #print "  insert child to index", index
        parent.insertChild(index, item)  ## index will not be correct
        self.setCurrentItem(item)
        
        self.recoverMove(item)
        self.emit(QtCore.SIGNAL('itemMoved'), item, parent, index)
        self.sigItemMoved.emit(item, parent, index)
        return True

    def itemMoving(self, item, parent, index):
        """Called when item has been dropped elsewhere in the tree.
        Return True to accept the move, False to reject."""
        return True
        
    def prepareMove(self, item):
        item.__widgets = []
        item.__expanded = item.isExpanded()
        for i in range(self.columnCount()):
            w = self.itemWidget(item, i)
            item.__widgets.append(w)
            if w is None:
                continue
            w.setParent(None)
        for i in range(item.childCount()):
            self.prepareMove(item.child(i))
        
    def recoverMove(self, item):
        for i in range(self.columnCount()):
            w = item.__widgets[i]
            if w is None:
                continue
            self.setItemWidget(item, i, w)
        for i in range(item.childCount()):
            self.recoverMove(item.child(i))
        
        item.setExpanded(False)  ## Items do not re-expand correctly unless they are collapsed first.
        QtGui.QApplication.instance().processEvents()
        item.setExpanded(item.__expanded)
        
    def collapseTree(self, item):
        item.setExpanded(False)
        for i in range(item.childCount()):
            self.collapseTree(item.child(i))
            
    def removeTopLevelItem(self, item):
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i) is item:
                self.takeTopLevelItem(i)
                return
        raise Exception("Item '%s' not in top-level items." % str(item))
            
            
if __name__ == '__main__':
    app = QtGui.QApplication([])
    
    w = TreeWidget()
    w.setColumnCount(2)
    w.show()
    
    i1  = QtGui.QTreeWidgetItem(["Item 1"])
    i11  = QtGui.QTreeWidgetItem(["Item 1.1"])
    i12  = QtGui.QTreeWidgetItem(["Item 1.2"])
    i2  = QtGui.QTreeWidgetItem(["Item 2"])
    i21  = QtGui.QTreeWidgetItem(["Item 2.1"])
    i211  = QtGui.QTreeWidgetItem(["Item 2.1.1"])
    i212  = QtGui.QTreeWidgetItem(["Item 2.1.2"])
    i22  = QtGui.QTreeWidgetItem(["Item 2.2"])
    i3  = QtGui.QTreeWidgetItem(["Item 3"])
    i4  = QtGui.QTreeWidgetItem(["Item 4"])
    i5  = QtGui.QTreeWidgetItem(["Item 5"])
    
    w.addTopLevelItem(i1)
    w.addTopLevelItem(i2)
    w.addTopLevelItem(i3)
    w.addTopLevelItem(i4)
    w.addTopLevelItem(i5)
    i1.addChild(i11)
    i1.addChild(i12)
    i2.addChild(i21)
    i21.addChild(i211)
    i21.addChild(i212)
    i2.addChild(i22)
    
    b1 = QtGui.QPushButton("B1")
    w.setItemWidget(i1, 1, b1)

