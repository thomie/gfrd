#!/usr/bin/env python

import unittest
import numpy

import _gfrd as mod
from OneDimGreensFunctionOneBoundaryTestBase import *


class OneDimGreensFunctionAbsInfTestCase( unittest.TestCase, 
        OneDimGreensFunctionOneBoundaryTestBase ):

    def setUp( self ):
        D = 1e-12

        self.gf = mod.OneDimGreensFunctionAbsInf( D )

    def tearDown( self ):
        pass


    def test_DrawTime_r0_equal_sigma( self ):
        # At left boundary.
        # There are 2 types of this test for 1D Rad Inf.
        gf = self.gf

        L = 1e-7
        r0 = 0
    
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase( OneDimGreensFunctionAbsInfTestCase )
    unittest.TextTestRunner(verbosity=2).run(suite)
