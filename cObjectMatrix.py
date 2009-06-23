#!/usr/bin/env python


import numpy
# Todo: I want to do something like this:
#from gfrdbase import log

### object_matrix is a module (library) that is written in C++ and
### pythonified using Boost library.
### Source: object_matrix/src/object_container.hpp
### Pythonify: object_matrix/boost.python/peer/ObjectContainer.hpp
###   and via object_matrix/boost.python/object_matrix_module.hpp
import object_matrix

from utils import *

debug=0

from shape import Sphere, Cylinder


class ObjectMatrix( object ):
    def __init__( self ):
        self.worldSize = 1.0
        self.setMatrixSize( 3 )
        self.initialize()


    def setWorldSize( self, size ):
        self.worldSize = size
        self.initialize()


    def setMatrixSize( self, size ):
        if size < 3:
            raise RuntimeError,\
                'Size of distance cell matrix must be at least 3'
        self.matrixSize = size
        self.initialize()


    def getSize( self ):
        return self.impl.size()
    size = property( getSize )


    def getCellSize( self ):
        return self.impl.cell_size
    cellSize = property( getCellSize )


    def clear( self ):
        self.initialize()


    def remove( self, key ):
        # Same for CylinderMatrix and SphereMatrix.
        assert self.impl.contains( key )
        self.impl.erase( key )


    def get( self, key ):
        # Same for CylinderMatrix and SphereMatrix.
        return self.impl.get( key )


    # Different getNeighbors methods. All return neighbors and distances.
    # Sort yes/no:          call impl.all_neighbors_array_cyclic.
    # Within radius yes/no: call impl.neighbors_array_cyclic.

    # No radius (i.e. all).
    def getNeighborsCyclic( self, pos, n=None ):
        neighbors, distances = self.impl.all_neighbors_array_cyclic( pos )
        topargs = distances.argsort()[:n]

        return neighbors.take( topargs ), distances.take( topargs )


    def getNeighborsCyclicNoSort( self, pos ):
        return self.impl.all_neighbors_array_cyclic( pos )


    # Within radius.
    def getNeighborsWithinRadius( self, pos, radius ):
        assert radius < self.cellSize * .5

        neighbors, distances = \
            self.impl.neighbors_array_cyclic( pos, radius )

        topargs = distances.argsort()

        return neighbors.take( topargs ), distances.take( topargs )


    def getNeighborsWithinRadiusNoSort( self, pos, radius ):
        assert radius < self.cellSize * .5
        return self.impl.neighbors_array_cyclic( pos, radius )


    # Wrappers for 'no radius' methods above. Why?
    def getNeighbors( self, pos, n=None ):
        return self.getNeighborsCyclic( pos, n )


    def getNeighborsNoSort( self, pos ):
        return self.getNeighborsCyclicNoSort( pos )


    def check( self ):
        pass



# Used for particles as particleMatrix in ParticleSimulatorBase, and for 
# spherical shells in EGFRDSimulator.
class SphereMatrix( ObjectMatrix ):
    def __init__( self ):
        ObjectMatrix.__init__( self )


    def initialize( self ):
        self.impl = object_matrix.SphereContainer( self.worldSize, self.matrixSize )


    # Adds a single/pair to matrix.
    def add( self, key, pos, radius ):
        if debug:
            try:
                # For pretty printing. Singles/Pairs/Cylinders:
                object = key[0]
            except TypeError:
                # Particles:
                object = key

        assert radius < self.cellSize * .5
        assert not self.impl.contains( key )
        # Calls insert() in ObjectContainer.hpp. 
        self.impl.insert( key, pos, radius )


    def update( self, key, pos, radius ):
        if debug:
            try:
                object = key[0]
            except TypeError:
                object = key

        assert radius < self.cellSize * .5

        assert self.impl.contains( key )
        self.impl.update( key, pos, radius )




class CylinderMatrix( ObjectMatrix ):
    def __init__( self ):
        ObjectMatrix.__init__( self )


    def initialize( self ):
        self.impl = object_matrix.CylinderContainer( self.worldSize, self.matrixSize )


    def add( self, key, shell ):
        if debug:
            try:
                # For pretty printing. Singles/Pairs/Cylinders:
                object = key[0]
            except TypeError:
                # Particles:
                object = key

        # Todo. Do something like this, but more thorough.
        #assert radius < self.cellSize * .5
        assert not self.impl.contains( key )
        # Todo: order of arguments correct here?
        self.impl.insert( key, shell.origin, shell.orientation, shell.radius, shell.size )


    def update( self, key, shell ):
        if debug:
            try:
                object = key[0]
            except TypeError:
                object = key

        assert shell.radius < self.cellSize * .5

        assert self.impl.contains( key )
        self.impl.update( key, shell.origin, shell.orientation, shell.radius, shell.size )




""" GRAVEYARD 
    def updateCylinder( self, key, shell ):
        assert self.cylinderContainer.__contains__( key )
        self.cylinderContainer[ key ] = shell 


    def removeCylinder( self, key ):
        assert self.cylinderContainer.contains( key )
        del self.cylinderContainer[ key ]
        #self.cylinderContainer.erase( key )


        # Doesn't work, particleMatrix also calls this.
        #if isinstance( key[0], Sphere ):
        #elif isinstance( key[0], Cylinder ):
        #    return self.cylinderContainer[ key ]
        #else: raise KeyError, 'Objecttype does not exit'


    ### Todo. Stilll needed for vtklogger.
    def getCylinders( self, pos ):
        shellList = []
        for key, shell in self.cylinderContainer.items() :
            if debug:
                print 'Get cylindricalShell: ', shell
            shellList.append( shell )

        return shellList
        # Todo:
        #return self.cylinderContainer.all_neighbors_array_cyclic( pos )



    def addCylinder
        #assert radius < self.cellSize * .5
        #self.cylinderContainer.insert( key, cylinder.pos, cylinder.orientation, cylinder.radius, cylinder.length / 2 )
        assert not self.cylinderContainer.__contains__( key )
        self.cylinderContainer[key] = shell
        
        # For now a dictionary.
        self.cylinderContainer = {}
"""
