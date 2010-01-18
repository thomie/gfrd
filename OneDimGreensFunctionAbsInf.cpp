#include "OneDimGreensFunctionAbsInf.hpp"

const Real OneDimGreensFunctionAbsInf::p_survival (const Real t) const
{
    const Real twoSqrtDt( 2 * sqrt( D * t ) );

    /* Todo. We might be able to use the inverse error function, using a 
     * lookup table for the coefficients of the summation for speedup.
     * http://en.wikipedia.org/wiki/Error_function#Inverse_function.
     * Or better: use 'Boost Error Function Inverses'. */
    return erf( r0 / twoSqrtDt );
}


const Real OneDimGreensFunctionAbsInf::p_int_r( const Real r, const Real t ) const
{
    const Real twoSqrtDt( 2 * sqrt( D * t ) );
    
    /* Todo. Try if 'Boost Error Function Inverses' is faster. */
    return 0.5 * ( erf( ( r - r0 ) / twoSqrtDt ) - 
                   erf( ( r + r0 ) / twoSqrtDt ) +
                   2 * erf( r0 / twoSqrtDt ) );
}


const EventType
OneDimGreensFunctionAbsInf::drawEventType( const Real rnd, const Real t )
const
{
    return ESCAPE;
}


const std::string OneDimGreensFunctionAbsInf::dump() const
{
    std::ostringstream ss;
    ss << "D = " << D << ", r0 = " << r0 << std::endl;
    return ss.str();
}    
