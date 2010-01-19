#!/usr/bin/env python

import unittest
import numpy

import _gfrd as mod
from OneDimGreensFunctionTestBase import *

class OneDimGreensFunctionTwoBoundariesTestBase( OneDimGreensFunctionTestBase ):
    '''Base class with tests for 1D Greens Functions with 2 boundaries.

    '''
    def test_DrawTime_r0_equal_a( self ):
        # At right absorbing boundary. Immediate escape.
        gf = self.gf

        L = 1e-7
        r0 = L

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )


    # Todo. Fails.
    def no_test_DrawTime_r0_near_a( self ):
        # Near right absorbing boundary.
        # Sum doesn't converge. Use 1DRadInf.
        gf = self.gf

        L = 1e-7
        r0 = L - L * 1e-6

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


