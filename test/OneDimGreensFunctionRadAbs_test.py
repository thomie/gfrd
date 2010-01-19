#!/usr/bin/env python

import unittest
import numpy

import _gfrd as mod
from OneDimGreensFunctionTwoBoundariesTestBase import *


class OneDimGreensFunctionRadAbsTestCase( unittest.TestCase, 
        OneDimGreensFunctionTwoBoundariesTestBase ):

    def setUp( self ):
        D = 1e-12
        kf = 1e-8

        self.gf = mod.FirstPassageGreensFunction1DRad( D, kf )

    def tearDown( self ):
        pass

    def test_DrawTime_r0_equal_sigma_kf_zero( self ):
        # At left boundary, small kf.

        D = 1e-12
        kf = 0.0 # Note this.

        # Don't use gf from setUp(), different kf. 
        gf = mod.FirstPassageGreensFunction1DRad( D, kf  )

        L = 1e-7
        r0 = 0

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t < 0.0 or t >= numpy.inf )


    def test_DrawTime_r0_equal_sigma_kf_large( self ):
        # At left boundary, large kf.

        D = 1e-12
        kf = 1e-8 # Todo. Isn't this still too small?

        # Don't use gf from setUp(), different kf. 
        gf = mod.FirstPassageGreensFunction1DRad( D, kf  )

        L = 1e-7
        r0 = 0

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t < 0.0 or t >= numpy.inf )


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase( OneDimGreensFunctionRadAbsTestCase )
    unittest.TextTestRunner(verbosity=2).run(suite)
