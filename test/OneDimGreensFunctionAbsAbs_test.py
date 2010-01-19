#!/usr/bin/env python

import unittest
import numpy

import _gfrd as mod
from OneDimGreensFunctionTwoBoundariesTestBase import *


class OneDimGreensFunctionAbsAbsTestCase( unittest.TestCase, 
        OneDimGreensFunctionTwoBoundariesTestBase ):

    def setUp( self ):
        D = 1e-12

        self.gf = mod.FirstPassageGreensFunction1D( D )

    def tearDown( self ):
        pass


    def test_DrawTime_r0_equal_sigma( self ):
        # At left boundary.
        # There are 2 types of this test for 1D Rad Abs. By making k an 
        # argument of drawTime, this could be simplified. Todo.
        gf = self.gf

        L = 1e-7
        r0 = 0
    
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase( OneDimGreensFunctionAbsAbsTestCase )
    unittest.TextTestRunner(verbosity=2).run(suite)

