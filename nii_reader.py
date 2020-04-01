import vtk
import nibabel as nib

# reading the NII file
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName('brain1.nii')
# never forget to update the reader ... otherwise you might have nothing inside :-)
reader.Update()

# get volume dimensions, center and spacing (as you now for scanners, the Z resolution might be different from the X and Y resolutions)
size = reader.GetOutput().GetDimensions()
center = reader.GetOutput().GetCenter()
spacing = reader.GetOutput().GetSpacing()

# define two different center points
center1 = (center[0], center[1], center[2])
center2 = (center[0], center[1], center[2])
if size[2] % 2 == 1:
    center1 = (center[0], center[1], center[2] + 0.5*spacing[2])
if size[0] % 2 == 1:
    center2 = (center[0] + 0.5*spacing[0], center[1], center[2])
print(center1)
print(center2)

# get the gray colors range
vrange = reader.GetOutput().GetScalarRange()

# set an vtkImageSliceMapper (see documentation) for axial view
map1 = vtk.vtkImageSliceMapper()
map1.BorderOn()
map1.SliceAtFocalPointOn()
map1.SliceFacesCameraOn()
map1.SetInputConnection(reader.GetOutputPort())

# set an vtkImageSliceMapper (see documentation) for sagittal view
map2 = vtk.vtkImageSliceMapper()
map2.BorderOn()
map2.SliceAtFocalPointOn()
map2.SliceFacesCameraOn()
map2.SetInputConnection(reader.GetOutputPort())

# set the axial slice from the mapper
slice1 = vtk.vtkImageSlice()
slice1.SetMapper(map1)
slice1.GetProperty().SetColorWindow(vrange[1]-vrange[0])
slice1.GetProperty().SetColorLevel(0.5*(vrange[0]+vrange[1]))

# set the sagittal slice from the mapper
slice2 = vtk.vtkImageSlice()
slice2.SetMapper(map2)
slice2.GetProperty().SetColorWindow(vrange[1]-vrange[0])
slice2.GetProperty().SetColorLevel(0.5*(vrange[0]+vrange[1]))
ratio = size[0]*1.0/(size[0]+size[2])

# renderes and viewports
ren1 = vtk.vtkRenderer()
ren1.SetViewport(0, 0, ratio, 1.0)

ren2 = vtk.vtkRenderer()
ren2.SetViewport(ratio, 0.0, 1.0, 1.0)

ren1.AddViewProp(slice1)
ren2.AddViewProp(slice2)

# change camera properties for having an axial view
cam1 = ren1.GetActiveCamera()
cam1.ParallelProjectionOn()
cam1.SetParallelScale(0.5*spacing[1]*size[1])
cam1.SetFocalPoint(center1[0], center1[1], center1[2])
cam1.SetPosition(center1[0], center1[1], center1[2] - 100.0)

# change camera properties for having an sagittal view
cam2 = ren2.GetActiveCamera()
cam2.ParallelProjectionOn()
cam2.SetParallelScale(0.5*spacing[1]*size[1])
cam2.SetFocalPoint(center2[0], center2[1], center2[2])
cam2.SetPosition(center2[0] + 100.0, center2[1], center2[2])

style = vtk.vtkInteractorStyleImage()
style.SetInteractionModeToImageSlicing()

iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(style)

renwin = vtk.vtkRenderWindow()
renwin.SetSize(size[0] + size[2], size[1])
renwin.AddRenderer(ren1)
renwin.AddRenderer(ren2)
renwin.Render()
renwin.SetInteractor(iren)

iren.Initialize()
iren.Start()
