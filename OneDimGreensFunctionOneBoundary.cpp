#include <sstream>
#include <iostream>
#include <exception>
#include <vector>

#include <gsl/gsl_math.h>
#include <gsl/gsl_sf_trig.h>
#include <gsl/gsl_sum.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_interp.h>
#include <gsl/gsl_sf_expint.h>
#include <gsl/gsl_sf_elljac.h>
#include <gsl/gsl_roots.h>

#include "findRoot.hpp"

#include "OneDimGreensFunctionOneBoundary.hpp"

const Real
OneDimGreensFunctionOneBoundary::p_survival_F( const Real t,
                              const p_survival_params* params )
{
    const OneDimGreensFunctionOneBoundary * const gf( params->gf ); 
    const Real rnd( params->rnd );

    // p_survival of subclass is used.
    return rnd - gf->p_survival( t );
}


/* Todo:
 *  - Checks for r0 == 0 for 1D Abs Inf etc.
 *  - low / high.
 *  - l_scale / t_scale.
 */
const Real OneDimGreensFunctionOneBoundary::drawTime (const Real rnd) const
{
    THROW_UNLESS( std::invalid_argument, rnd < 1.0 && rnd >= 0.0 );
    THROW_UNLESS( std::invalid_argument, r0 >= 0.0 );

    if( D == 0.0 )
    {
        return INFINITY;
    }

    if ( rnd == 0.0 )
    {
        return 0.0;
    }

    p_survival_params params = { this, rnd };

    gsl_function F = 
        {
            // Todo. Why is this cast needed?
            reinterpret_cast<typeof(F.function)>( &p_survival_F ),
            &params 
        };


    // Find a good interval to determine the first passage time in.
    // Get the distance to absorbing boundary (disregard rad BC)
    // Todo.
    const Real dist(r0);

    // Construct a guess: msd = sqrt (2*d*D*t).
    const Real t_guess( dist * dist / ( 2. * D ) );


    /* Below here taken from FirstPassageGreensFunction1DRad. */

    // Define a minimal time so system does not come to a halt.
    const Real minT( std::min( this->MIN_T,
                               t_guess * 1e-6 ) );

    Real value( GSL_FN_EVAL( &F, t_guess ) );
    Real low( t_guess );
    Real high( t_guess );


    // Adjust the interval around the guess such that the function straddles.
    if( value < 0.0 )
    {
        // If the guess was too low.
        do
        {
            // Keep increasing the upper boundary until the
            // function straddles.
            high *= 10;
            value = GSL_FN_EVAL( &F, high );

            if( fabs( high ) >= t_guess * 1e6 )
            {
                std::cerr << "GF1DRad: Couldn't adjust high. F("
                          << high << ") = " << value << std::endl;
                throw std::exception();
            }
        }
        while ( value <= 0.0 );
    }
    else
    {
        // If the guess was too high.
        // Initialize with 2 so the test below survives the first iterations.
        Real value_prev( 2 );
        do
        {
            if( fabs( low ) <= minT ||
                fabs(value-value_prev) < EPSILON * t_scale )
            {
                std::cerr << "GF1DRad: Couldn't adjust low. F(" << low << ") = "
                          << value << " t_guess: " << t_guess << " diff: "
                          << (value - value_prev) << " value: " << value
                          << " value_prev: " << value_prev << " rnd: "
                          << rnd << std::endl;
                return low;
            }
            value_prev = value;
            // Keep decreasing the lower boundary until the function 
            // straddles.
            low *= .1;
            // Get the accompanying value.
            value = GSL_FN_EVAL( &F, low );
        }
        while ( value >= 0.0 );
    }


    // Find the intersection on the y-axis between the random number and
    // the function.
    // Define a new solver type brent.
    const gsl_root_fsolver_type* solverType( gsl_root_fsolver_brent );
    // Make a new solver instance.
    gsl_root_fsolver* solver( gsl_root_fsolver_alloc( solverType ) );
    const Real t( findRoot( F, solver, low, high, EPSILON * t_scale, EPSILON,
                            "OneDimGreensFunctionOneBoundary::drawTime" ) );

    // Return the drawn time.
    return t;
}

    
const Real
OneDimGreensFunctionOneBoundary::p_int_r_F( const Real r,
                                            const p_int_r_params* params )
{
    const OneDimGreensFunctionOneBoundary* const gf( params->gf ); 
    const Real t( params->t );
    const Real rnd( params->rnd );

    return gf->p_int_r( r, t ) - rnd;
}


const Real 
OneDimGreensFunctionOneBoundary::drawR( const Real rnd, const Real t ) const 
{
    THROW_UNLESS( std::invalid_argument, 0.0 <= rnd && rnd < 1.0 );
    THROW_UNLESS( std::invalid_argument, r0 >= 0.0 );
    THROW_UNLESS( std::invalid_argument, t >= 0.0 );

    if (t == 0.0 || D == 0)
    {
        return r0;
    }

    const Real psurv( p_survival( t ) );

    // We want the probability density of finding the particle at location z 
    // at timepoint t, given that the particle is still in the domain. So 
    // mulitply rnd by psurv.
    p_int_r_params params = { this, t, rnd * psurv };

    gsl_function F = 
        {
            reinterpret_cast<typeof(F.function)>( &p_int_r_F ),
            &params 
        };

    // Adjust low and high starting from r0.
    // This is necessary to avoid root finding in the long tails where
    // numerics can be unstable.
    // Todo. Is it really necessary? FirstPassageNoCollisionPairGreensFunction 
    // is not using it. This is taken from BasicPairGreensFunction.

    Real low( r0 );
    Real high( r0 );
    const Real sigma( 0 ); // So we can reuse this later.

    const Real sqrt2Dt( sqrt( 2.0 * D * t ) );
    if( GSL_FN_EVAL( &F, r0 ) < 0.0 )
    {
        // low = r0
        unsigned int H( 3 );

        while( true )
        {
            high = r0 + H * sqrt2Dt;

            const Real value( GSL_FN_EVAL( &F, high ) );
            if( value > 0.0 )
            {
                break;
            }

            ++H;

            if( H > 20 )
            {
                std::cerr << "drawR: H > 20 while adjusting upper bound of r."
                          << std::endl;
                throw std::exception();
            }
        }

    }
    else
    {
        // high = r0
        unsigned int H( 3 );

        while( true )
        {
            low = r0 - H * sqrt2Dt;
            if( low < sigma )
            {
                if( GSL_FN_EVAL( &F, sigma ) > 0.0 )
                {
                    printf( "drawR: p_int_r( sigma ) > 0.0. "
                            "returning sigma.\n" );
                    return sigma;
                }

                low = sigma;
                break;
            }

            const Real value( GSL_FN_EVAL( &F, low ) );
            if( value < 0.0 )
            {
                break;
            }

            ++H;
        }
    }

    // Define a new solver type brent.
    const gsl_root_fsolver_type* solverType( gsl_root_fsolver_brent );
    // Make a new solver instance.
    gsl_root_fsolver* solver( gsl_root_fsolver_alloc( solverType ) );
    const Real z( findRoot( F, solver, low, high, EPSILON * l_scale, EPSILON,
                            "OneDimGreensFunctionOneBoundary::drawR" ) );

    // Return the drawn place.
    return z;
}
