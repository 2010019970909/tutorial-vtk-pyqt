import vtk
jpegfile = "image1.jpg"
# Read the image
reader = vtk.vtkJPEGReader()
reader.SetFileName(jpegfile)
reader.Update()
# Actor
actor = vtk.vtkImageActor()
actor.SetInputData(reader.GetOutput())
# Renderer
ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.ResetCamera()
# Render window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
# Interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
# Run!
iren.Start()