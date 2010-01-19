#!/usr/bin/env python

import unittest
import numpy

import _gfrd as mod


class OneDimGreensFunctionTestBase( object ):
    '''Base class with tests for 1D Greens Functions.

    '''
    def test_Instantiation( self ):
        self.failIf( self.gf == None )


    def test_DrawTime( self ):
        gf = self.gf

        L = 1e-7
        r0 = L/2

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
        # Zero shell.
        gf = self.gf

        L = 0
        r0 = 0

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.assertEqual( 0.0, t )

        # Extra.
        r = gf.drawR( 0.5, t )
        self.assertEqual( 0.0, r )


    def test_DrawTime_a_near_sigma( self ):
        # Small shell.
        gf = self.gf

        L = 1e-14
        r0 = L/2

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


    # Todo. Make seperate test for small k here also.
    # Todo. Only fails for 1D Abs Abs, not for 1D Rad Abs.
    def no_test_DrawTime_r0_near_sigma( self ):
        # Near left boundary.
        gf = self.gf

        L = 1e-7
        r0 = L * 1e-6

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )
        self.failIf( t <= 0.0 or t >= numpy.inf )


    def test_DrawEventType( self ):
        gf = self.gf

        L = 1e-7
        r0 = L/2

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
        gf = self.gf

        L = 1e-7
        r0 = L/2

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
        gf = self.gf

        L = 1e-7
        r0 = L/2

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 0.5 )

        r = gf.drawR( 0.5, t )
        self.failIf( r < 0 or r > L )

        r1 = gf.drawR( 0.0, t )
        self.failIf( r1 < 0 or r1 > L )

        # Random number close to zero (r near sigma) and one (r near a).
        r2 = gf.drawR( 1e-16, t )
        self.failIf( r2 < 0 or r2 > L )

        r3 = gf.drawR( 1.0 - 1e-16, t )
        self.failIf( r3 < 0 or r3 > L )

        self.assertAlmostEqual( r1, 0 )
        self.assertAlmostEqual( r2, 0 )
        self.assertAlmostEqual( r3, L )


    def test_DrawR_zerot( self ):
        gf = self.gf

        L = 1e-7
        r0 = L/2

        gf.setL( L )
        gf.setr0( r0 )

        t = 0.0

        r = gf.drawR( 0.5, t )
        self.assertEqual( r0, r )


    # Todo. Fails.
    def no_test_drawR_smallt( self ):
        # Sum doesn't converge. Use FreeGreensFunction1D.
        # 
        gf = self.gf

        L = 1e-7
        r0 = L/2

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
        gf = self.gf

        L = 1e-3
        r0 = L/2

        gf.setL( L )
        gf.setr0( r0 )

        # Fails for hardcoded t = 1e-10.
        #t = gf.drawTime( 1e-10 )
        t = gf.drawTime( 0.5 )

        r = gf.drawR( 0.5, t )
        self.failIf( r <= 0.0 )
        self.failIf( r > L )


    def test_drawR_large_t( self ):
        gf = self.gf

        L = 1e-6
        r0 = L/2

        gf.setL( L )
        gf.setr0( r0 )

        t = gf.drawTime( 1.0 - 1e-16 )

        r = gf.drawR( 0.5, t )
        self.failIf( r <= 0.0 )
        self.failIf( r > L )


    def test_DrawR_r0_equal_sigma( self ):
        # At left boundary.
        gf = self.gf

        L = 1e-7
        r0 = 0

        t = 1e-3

        gf.setL( L )
        gf.setr0( r0 )

        # Todo. Fails.
        #r = gf.drawR( 0.5, t )
        #self.failIf( r < 0 or r > L )


    def test_DrawR_squeezed( self ):
        gf = self.gf

        L = 2e-10 # Todo. 1e-10 fails even more.
        r0 = 0

        gf.setL( L )
        gf.setr0( r0 )

        t = 1e-6
        # Todo. Fails.
        #r = gf.drawR( 0.5, t )
        #self.failIf( r < 0 or r > L )

        # Near sigma.
        r0 = 0.0001e-8
        gf.setr0( r0 )
        r = gf.drawR( 0.5, t )
        self.failIf( r < 0 or r > L )

        # Near a.
        r0 = L - 0.0001e-8
        gf.setr0( r0 )
        r = gf.drawR( 0.5, t )
        self.failIf( r < 0 or r > L )


