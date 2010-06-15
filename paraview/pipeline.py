from paraview import servermanager

READERS   = None
PARTICLES = None
SPHERES   = None
CYLINDERS = None
HELIX     = None
SURFACES  = None

# Settings
READERS   = True
PARTICLES = True
SPHERES   = True
CYLINDERS = True
HELIX     = True
SURFACES  = True


PARTICLE_RADIUS_SCALE_FACTOR = 1
HELIX_RADIUS_SCALE_FACTOR = 4
RESOLUTION = 18

if not servermanager.ActiveConnection:
    exit('pvpython not supported. Use ParaView\'s Python shell.')


# Detect version.
try:
    from paraview import simple
    version = 6 # ParaView 3.6 or higher.
    LoadPlugin(paraview_scripts_directory + '/tensorGlyph.xml')
    LoadPlugin(paraview_scripts_directory + '/tensorGlyphWithCustomSource.xml')
except ImportError:
    version = 4 # ParaView 3.4.

    def load_xml_plugin(filename):
        # Adapted from LoadPlugin in simple.py (ParaView 3.6).
        f = open(filename, 'r')
        import os
        if os.name == "posix":
            import libvtkPVServerManagerPython as libvtk
            parser = libvtk.vtkSMXMLParser()
        else:
            import vtkPVServerCommonPython as libvtk
            parser = libvtk.vtkSMXMLParser()
        if not parser.Parse(f.read()):
            raise RuntimeError, "Problem loading plugin %s: %s" % (filename)
        parser.ProcessConfiguration(libvtk.vtkSMObject.GetProxyManager())
        # Update the modules
        servermanager.updateModules()

    load_xml_plugin(paraview_scripts_directory + '/tensorGlyph.xml')
    load_xml_plugin(paraview_scripts_directory +
                    '/tensorGlyphWithCustomSource.xml')


if len(servermanager.GetRenderViews()) > 0:
    rv = servermanager.GetRenderViews()[0]
else:
    rv = servermanager.CreateRenderView()


def clear():
    # Reset time so that color range is detected correctly on build().
    rv.ViewTime = 0
    rv.StillRender()

    def name(proxy):
        return (type(proxy)).__name__

    def cmp_tubes_filters_glyphs_blocks(x,y):
        if name(x) in ['GenerateTubes', 'TubeFilter', 'Tube']:
            return -1
        elif name(y) in ['GenerateTubes', 'TubeFilter', 'Tube']:
            return 1
        if name(x) == 'ProgrammableFilter':
            return -1
        elif name(y) == 'ProgrammableFilter':
            return 1
        elif name(x) == 'Glyph' or name(x)[:11] == 'TensorGlyph':
            return -1
        elif name(y) == 'Glyph' or name(y)[:11] == 'TensorGlyph':
            return 1
        if name(x) == 'ExtractBlock':
            return -1
        elif name(y) == 'ExtractBlock':
            return 1
        return cmp(x,y)

    pxm = servermanager.ProxyManager()
    for proxy in pxm.GetProxiesInGroup('lookup_tables').itervalues():
        servermanager.UnRegister(proxy)

    if version == 4:
        for proxy in sorted(pxm.GetProxiesInGroup('sources').itervalues(),
                            cmp_tubes_filters_glyphs_blocks):
            if name(proxy) == 'TensorGlyphWithCustomSource':
                # Do nothing. Setting Source or Input gives: 
                # 'QAbstractItemModel::endRemoveRows:  Invalid index ( 2 , 0 ) 
                # in model pqPipelineModel(0x26340b0)'
                # http://www.paraview.org/Bug/view.php?id=9312
                pass
            else:
                if hasattr(proxy, "Source"):
                    # Avoid 'Connection sink not found in the pipeline model'.
                    proxy.Source = None
                if hasattr(proxy, "Input"):
                    # Avoid 'Connection sink not found in the pipeline model'.
                    proxy.Input = None
            servermanager.UnRegister(proxy)
        for proxy in pxm.GetProxiesInGroup('representations').itervalues():
            servermanager.UnRegister(proxy)

        rv.Representations = []
    else:
        for proxy in sorted(simple.GetSources().itervalues(), 
                            cmp_tubes_filters_glyphs_blocks):
            if hasattr(proxy, "Input"):
                # Avoid 'Connection sink not found in the pipeline model'.
                proxy.Input = None
            if hasattr(proxy, "GlyphType"):
                # Avoid 'Connection sink not found in the pipeline model'.
                proxy.GlyphType = None
            simple.Delete(proxy)

    rv.ResetCamera()
    rv.StillRender()


def build():
    def add_pvd_reader(file, name):
        reader = servermanager.sources.PVDReader(FileName=file)
        servermanager.Register(reader, registrationName=name)
        if version == 4:
            reader.UpdatePipeline()
            # Update TimestepValues.
            reader.UpdatePipelineInformation();
        else:
            pass

        return reader


    def add_extract_block(data, indices, name):
        block = servermanager.filters.ExtractBlock(Input=data, 
                                                   BlockIndices=indices)

        # This is needed to make SetScaleFactor and TensorGlyph work.
        block.UpdatePipeline();

        servermanager.Register(block, registrationName=name)
        return block


    def add_sphere_glyph(input, resolution=None, name=None):
        if version == 4:
            source = servermanager.sources.SphereSource()
            if resolution != None:
                source.ThetaResolution = resolution
                source.PhiResolution = resolution
            glyph = servermanager.filters.Glyph(Input=input, 
                                                Source=source)

            # Prevent "selected proxy value not in the list".
            # http://www.paraview.org/pipermail/paraview/2008-March/007416.html
            sourceProperty = glyph.GetProperty("Source")
            domain = sourceProperty.GetDomain("proxy_list");
            domain.AddProxy(source.SMProxy)

            glyph.SetScaleMode = 0
            # Look at the documentation of 
            # vtkAlgorithm::SetInputArrayToProcess() for details.
            glyph.SelectInputScalars = ['0', '', '', '', 'radii']

        else:
            glyph = servermanager.filters.Glyph(Input=input, 
                                                GlyphType='Sphere')
            glyph.ScaleMode = 'scalar'

            if resolution != None:
                glyph.GlyphType.ThetaResolution = resolution
                glyph.GlyphType.PhiResolution = resolution

        glyph.SetScaleFactor = 1

        if name != None:
            servermanager.Register(glyph, registrationName=name)
        else:
            servermanager.Register(glyph)

        return glyph


    def add_tensor_glyph(input, type, resolution=None, name=None, scale=None):
        if version == 4:
            if type == 'Cylinder':
                source = servermanager.sources.CylinderSource()

                if resolution != None:
                    source.Resolution = resolution

                if scale != None:
                    source.Radius = 0.5 * scale

            elif type == 'Box':
                source = servermanager.sources.CubeSource()

            tensor_glyph = servermanager.filters.TensorGlyph(Input=input,
                                                             Source=source)

            tensor_glyph.SelectInputTensors = ['0', '', '', '', 'tensors']

            # The specified scalar array is the only array that gets copied.
            tensor_glyph.SelectInputScalars = ['1', '', '', '', 'colors']
        else:
            tensor_glyph = servermanager.filters.TensorGlyph(Input=input,
                                                             GlyphType=type)

            # Heads up. The first or the specified vector array is the only 
            # array that gets copied (scalar arrays don't get copied).
            tensor_glyph.Vectors = ['POINTS', 'colors_as_vectors']

            if resolution != None:
                tensor_glyph.GlyphType.Resolution = resolution

            if scale != None:
                tensor_glyph.GlyphType.Radius *= scale

        if name != None:
            servermanager.Register(tensor_glyph, registrationName=name)
        else:
            servermanager.Register(tensor_glyph)

        return tensor_glyph


    def add_tensor_glyph_with_custom_source(input, source, name=None):
        if version == 4:
            Type = servermanager.filters.TensorGlyphWithCustomSource
            tensor_glyph = Type(Input=input, Source=source)

            tensor_glyph.SelectInputTensors = ['0', '', '', '', 'tensors']
        else:
            Type = servermanager.filters.TensorGlyphWithCustomSource
            tensor_glyph = Type(Input=input, GlyphType=source)

        if name != None:
            servermanager.Register(tensor_glyph, registrationName=name)
        else:
            servermanager.Register(tensor_glyph)

        return tensor_glyph


    def programmable_filter_color_hack(tensor_glyph, name):
        # http://www.paraview.org/pipermail/paraview/2009-March/011267.html
        # Dealing with composite datasets:
        # http://www.itk.org/Wiki/Python_Programmable_Filter
        filter = servermanager.filters.ProgrammableFilter()
        filter.Initialize()
        filter.Input = tensor_glyph
        filter.Script = """def flatten(input, output):
    output.ShallowCopy(input) # DeepCopy doesn't copy to tensor_glyph.
    output.GetPointData().GetArray(0).SetName('colors')
    # GetScalars() doesn't work in ParaView 3.4.
    #output.GetPointData().GetScalars().SetName('colors')

input = self.GetInput()
output = self.GetOutput()

output.CopyStructure(input)
iter = input.NewIterator()
iter.UnRegister(None)
iter.InitTraversal()
while not iter.IsDoneWithTraversal():
    curInput = iter.GetCurrentDataObject()
    curOutput = curInput.NewInstance()
    curOutput.UnRegister(None)
    output.SetDataSet(iter, curOutput)
    flatten(curInput, curOutput)
    iter.GoToNextItem();"""

        filter.UpdatePipeline()

        servermanager.Register(filter, registrationName=name)

        return filter


    def set_color(proxy, rep, color_array_name='colors'):
        rep.ColorArrayName = color_array_name

        if version == 4:
            rep.ColorAttributeType = 0 # point data

            # Adapted from MakeBlueToRedLT in simple.py (ParaView 3.6).
            def MakeBlueToRedLT(min, max):
                lt = servermanager.rendering.PVLookupTable()
                servermanager.Register(lt)

                # Define RGB points. These are tuples of 4 values. First one is
                # the scalar values, the other 3 the RGB values. 
                rgbPoints = [min, 0, 0, 1, max, 1, 0, 0]
                lt.RGBPoints = rgbPoints
                lt.ColorSpace = "HSV"

                return lt

            pdi = proxy.GetDataInformation().GetPointDataInformation()
            color_array = pdi.GetArrayInformation(color_array_name)
            range = color_array.GetComponentRange(0)
            lt = MakeBlueToRedLT(range[0], range[1])
        else:
            range = proxy.PointData.GetArray(color_array_name).GetRange()
            lt = simple.MakeBlueToRedLT(range[0], range[1])

        rep.LookupTable = lt


    class _funcs_internals:
        # Taken from simple.py (ParaView 3.6).
        "Internal class."
        first_render = True
        view_counter = 0
        rep_counter = 0

    def show(proxy):
        if version == 4:
            # Adapted from Show in simple.py (ParaView 3.6).
            rep = servermanager.CreateRepresentation(proxy, rv)
            servermanager.ProxyManager().RegisterProxy("representations",
              "my_representation%d" % _funcs_internals.rep_counter, rep)
            _funcs_internals.rep_counter += 1
        else:
            rep = simple.Show(proxy)

        rep.Visibility = 1
        return rep


    if READERS:
        global files
        files = add_pvd_reader(simulation_data_directory + '/files.pvd', 
                               'files.pvd')

        global static
        static = add_pvd_reader(simulation_data_directory + '/static.pvd', 
                                'static.pvd')


    if PARTICLES:
        global particle_data
        particle_data = add_extract_block(files, [2], 'b1')

        global particles
        particles = add_sphere_glyph(particle_data, name='Particles')
        particles.SetScaleFactor = PARTICLE_RADIUS_SCALE_FACTOR

        rep1 = show(particles)
        set_color(particles, rep1)


    if SPHERES:
        global sphere_data
        sphere_data = add_extract_block(files, [4], 'b2')

        global spheres
        spheres = add_sphere_glyph(sphere_data, RESOLUTION, name='Spheres')

        rep2 = show(spheres)
        set_color(spheres, rep2)
        rep2.Representation = 'Wireframe'
        rep2.Opacity = 0.5


    if CYLINDERS:
        global cylinder_data
        cylinder_data = add_extract_block(files, [6], 'b3')

        global cylinders
        cylinders = add_tensor_glyph(cylinder_data, 'Cylinder', 
                                     resolution=RESOLUTION, name='tg')

        programmable_filter = programmable_filter_color_hack(cylinders,
                                                             name='Cylinders')
        rep3 = show(programmable_filter)
        set_color(programmable_filter, rep3)
        rep3.Representation = 'Wireframe'
        rep3.Opacity = 1.0


    if SURFACES:
        # Cylindrical surfaces.
        cylindrical_surface_data = add_extract_block(static, [2], 'b4')

        global rep4

        if not HELIX:
            global cylindrical_surfaces
            cylindrical_surfaces = \
                add_tensor_glyph(cylindrical_surface_data, 'Cylinder', 
                                 name='Cylindrical Surfaces',
                                 scale=HELIX_RADIUS_SCALE_FACTOR) 

            rep4 = show(cylindrical_surfaces)
            rep4.Representation = 'Wireframe'
            rep4.Opacity = 0.5
        else:
            helix_file = open(paraview_scripts_directory + '/helix.py', 'r')
            helix_source = servermanager.sources.ProgrammableSource()
            helix_source.Script = 'HELIX_RADIUS_SCALE_FACTOR = ' + \
                                  str(HELIX_RADIUS_SCALE_FACTOR) + \
                                  '\n' + helix_file.read()
            helix_source.UpdatePipeline()
            servermanager.Register(helix_source, registrationName='ps')

            helix_file.close()


            tensor_glyph = \
                add_tensor_glyph_with_custom_source(cylindrical_surface_data, 
                                                    helix_source, 
                                                    name='tgwcs')
            global double_helix
            if version == 4:
                double_helix = \
                    servermanager.filters.TubeFilter(Input=tensor_glyph)
            else:
                try:
                    double_helix = \
                        servermanager.filters.GenerateTubes(Input=tensor_glyph)
                except AttributeError:
                    # ParaView 3.8.
                    double_helix = \
                        servermanager.filters.Tube(Input=tensor_glyph)
            servermanager.Register(double_helix,
                                   registrationName='Double Helix')

            # Compute helix radius.
            di = cylindrical_surface_data.GetDataInformation()
            pdi = di.GetPointDataInformation()
            tensor = pdi.GetArrayInformation('tensors')

            cylindrical_surface_radius = 1e100
            for i in range(9):
                # Find minimum value of tensor larger than 0.
                value = tensor.GetComponentRange(i)[0]
                if value > 0 and value < cylindrical_surface_radius:
                    cylindrical_surface_radius = value

            helix_radius = HELIX_RADIUS_SCALE_FACTOR * \
                           cylindrical_surface_radius

            # Make double_helix a bit thinner than helix.
            double_helix.Radius = helix_radius / 20

            rep4 = show(double_helix)
            set_color(double_helix, rep4, color_array_name = 'TubeNormals')


        # Planar surfaces.
        planar_surface_data = add_extract_block(static, [4], 'b5')
        global planar_surfaces
        planar_surfaces = add_tensor_glyph(planar_surface_data, 'Box', 
                                           name='Planar Surfaces')

        rep5 = show(planar_surfaces)
        rep5.Representation = 'Surface'
        rep5.Opacity = 0.5


        # Cuboidal surfaces.
        cuboidal_region_data = add_extract_block(static, [6], 'b6')
        global cuboidal_regions
        cuboidal_regions = add_tensor_glyph(cuboidal_region_data, 'Box',
                                           name='Cuboidal Regions')

        rep6 = show(cuboidal_regions)
        rep6.Representation = 'Wireframe'
        rep6.Opacity = 1.0


    # Set camera.
    global cam
    cam = rv.GetActiveCamera()
    rv.ResetCamera() # Sets focalpoint to center of box.
    cam.SetViewUp(0,0,1)
    focal = cam.GetFocalPoint()
    cam.SetPosition(focal[0]*10, focal[1], focal[2]) # Straigh in front of box.

    rv.Background = [0,0,0] # Black.
    rv.ResetCamera() # Changes cam.GetPosition() only by zooming in/out.
    rv.StillRender()


print 'clear()'
clear()
print 'build()'
build()


