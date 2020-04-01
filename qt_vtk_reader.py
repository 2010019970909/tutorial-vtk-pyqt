#!/usr/bin/env python
import sys
import vtk
from PyQt5 import QtCore, Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(Qt.QMainWindow):
    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)
        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        
        self.vl.addWidget(self.vtkWidget)
        self.sl = Qt.QSlider()
        self.sl.setMinimum(1.0)
        self.sl.setMaximum(20.0)
        self.sl.setValue(10.0)
        self.vl.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # Create source
        self.source = vtk.vtkSphereSource()
        self.source.SetCenter(0, 0, 0)
        self.source.SetRadius(5.0)
        # Create a mapper
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.source.GetOutputPort())
        # Create an actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.ren.AddActor(self.actor)
        self.ren.ResetCamera()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.show()
        self.iren.Initialize()

    def valuechange(self):
        size = self.sl.value()
        self.source.SetRadius(size)
        self.iren.Initialize()

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())