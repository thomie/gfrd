#!/usr/bin/env python

__author__    = 'Laurens Bossen'
__license__   = ''
__copyright__ = ''


import unittest

import _gfrd as mod

import numpy


class FirstPassageGreensFunction1DTestCase( unittest.TestCase ):
    '''1D Abs Abs.
    
    Same as FirstPassageGreensFunction1DRadTestCase, except for 
    test_DrawTime_r0_equal_sigma.

    Taken from FirstPassagePairGreensFunction_test.

    '''
    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_Instantiation( self ):
        D = 1e-12
        L = 1e-7

        gf = mod.FirstPassageGreensFunction1D( D )
        self.failIf( gf == None )
        gf.setL( L )


    def test_DrawTime( self ):
        D = 1e-12
        L = 1e-7
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )

        t = gf.drawTime( 0.0 )
        self.failIf( t < 0.0 or t >= numpy.inf )

        t = gf.drawTime( 1e-16 )
        self.failIf( t <= 0.0 or t >= numpy.inf )

        t = gf.drawTime( 1 - 1e-16 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


    def test_DrawTime_a_equal_sigma( self ):
        D = 1e-12
        L = 0
        r0 = L

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )

        r = gf.drawR( 0.5, t )
        self.assertEqual( 0.0, r )


    def test_DrawTime_a_near_sigma( self ):
        D = 1e-12
        L = 1e-14
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


    def test_DrawTime_r0_equal_a( self ):
        D = 1e-12
        L = 1e-7
        r0 = L

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )


    # Todo.
    def no_test_DrawTime_r0_near_a( self ):
        D = 1e-12
        L = 1e-7
        r0 = L - L * 1e-6

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


    def test_DrawTime_r0_equal_sigma( self ):
        D = 1e-12
        L = 1e-7
        r0 = 0

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )


    # Todo.
    def no_test_DrawTime_r0_near_sigma( self ):
        D = 1e-12
        L = 1e-7
        r0 = L * 1e-6

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


    def test_DrawEventType( self ):
        D = 1e-12
        L = 1e-7
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        eventType = gf.drawEventType( 0.5, t )
        self.failIf( eventType != 0 and eventType != 1 )

        eventType = gf.drawEventType( 0.0, t )
        self.assertEqual( eventType, 0 )

        eventType = gf.drawEventType( 1e-16, t )
        self.assertEqual( eventType, 0 )

        eventType = gf.drawEventType( 1 - 1e-16, t )
        self.assertEqual( eventType, 1 )


    def test_DrawEventType_smallt( self ):
        D = 1e-12
        L = 1e-7
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.001 )

        eventType = gf.drawEventType( 0.5, t )
        self.failIf( eventType != 0 and eventType != 1 )

        eventType = gf.drawEventType( 0.0, t )
        self.assertEqual( eventType, 0 )

        eventType = gf.drawEventType( 1e-16, t )
        self.assertEqual( eventType, 0 )

        eventType = gf.drawEventType( 1 - 1e-16, t )
        self.assertEqual( eventType, 1 )


    def test_DrawR( self ):
        D = 1e-12
        L = 1e-7
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )

        r = gf.drawR( 0.5, t )
        self.failIf( r < 0 or r > L )

        r1 = gf.drawR( 0.0, t )
        self.failIf( r1 < 0 or r1 > L )

        # Close to 0 and L.
        r2 = gf.drawR( 1e-16, t )
        self.failIf( r2 < 0 or r2 > L )

        r3 = gf.drawR( 1.0 - 1e-16, t )
        self.failIf( r3 < 0 or r3 > L )

        self.assertAlmostEqual( r1, 0 )
        self.assertAlmostEqual( r2, 0 )
        self.assertAlmostEqual( r3, L )


    def test_DrawR_zerot( self ):
        D = 1e-12
        L = 1e-7
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = 0.0

        r = gf.drawR( 0.5, t )
        self.assertEqual( r0, r )


    # Todo.
    def no_test_drawR_smallt( self ):
        D = 1e-12
        L = 1e-7
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )

        while t > 1e-30:
            print t
            t *= 1e-4
            r = gf.drawR( 0.0, t )
            self.failIf( r < 0.0 )
            self.failIf( r > L )


    def test_drawR_large_shell( self ):
        D = 1e-12
        L = 1e-3
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        # Fails for hardcoded t = 1e-10.
        t = gf.drawTime( 0.5 )

        r = gf.drawR( 0.5, t )
        self.failIf( r <= 0.0 )
        self.failIf( r > L )


    def test_drawR_large_t( self ):
        D = 1e-12
        L = 1e-6
        r0 = L/2

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 1.0 - 1e-16 )

        r = gf.drawR( 0.5, t )
        self.failIf( r <= 0.0 )
        self.failIf( r > L )


    def test_DrawR_r0_equal_sigma( self ):
        D = 1e-12
        L = 1e-7
        r0 = 0

        t = 1e-3

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )
        gf.setr0( r0 )

        # Todo.
        # This raises an exception, which at this point we cannot catch
        #r = gf.drawR( 0.5, t )
        #self.failIf( r < 0 or r > L )


    def test_DrawR_squeezed( self ):
        D = 1e-12
        L = 2e-10 # Todo. 1e-10 fails even more.

        gf = mod.FirstPassageGreensFunction1D( D )
        gf.setL( L )

        t = 1e-6
        r0 = 0
        gf.setr0( r0 )
        # Todo.
        # This raises an exception, which at this point we cannot catch
        #r = gf.drawR( 0.5, t )
        #self.failIf( r < 0 or r > L )

        # near s
        r0 = 0.0001e-8
        gf.setr0( r0 )
        r = gf.drawR( 0.5, t )
        self.failIf( r < 0 or r > L )

        # near a
        r0 = L - 0.0001e-8
        gf.setr0( r0 )
        r = gf.drawR( 0.5, t )
        self.failIf( r < 0 or r > L )


if __name__ == "__main__":
    unittest.main()
