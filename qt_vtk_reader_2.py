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
        self.sl.setMaximum(200.0)
        self.sl.setValue(50.0)
        self.vl.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleImage()
        style.SetInteractionModeToImageSlicing()
        self.iren.SetInteractorStyle(style)

        # Read the image
        self.reader = vtk.vtkNIFTIImageReader()
        self.reader.SetFileName('brain1.nii')
        self.reader.Update()

        # SLICE Mapper :-)
        self.map = vtk.vtkImageSliceMapper()
        self.map.SetSliceNumber(50)
        self.map.SetInputConnection(self.reader.GetOutputPort())
        
        # Put mapper into actor and actor into renderer
        slice = vtk.vtkImageSlice()
        slice.SetMapper(self.map)
        self.ren.AddActor(slice)
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.show()
        self.iren.Initialize()

    def valuechange(self):
        # get the slider value
        s = self.sl.value()
        self.map.SetSliceNumber(s)
        self.iren.Initialize()

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())