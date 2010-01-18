#include "OneDimGreensFunctionRadInf.hpp"
#include "freeFunctions.hpp" // For W( a, b ).

const Real OneDimGreensFunctionRadInf::p_survival (const Real t) const
{
    const Real sqrtDt( sqrt( D * t ) );

    const Real a( r0 / ( 2 * sqrtDt ) );
    const Real b( h * sqrtDt );

    return 1 + W( a, b ) - erfc( a );
}


const Real OneDimGreensFunctionRadInf::p_int_r( const Real r, const Real t ) const
{
    const Real sqrtDt( sqrt( D * t ) );

    const Real a1( r0 / ( 2 * sqrtDt ) );
    const Real a2( ( r + r0 ) / ( 2 * sqrtDt ) );
    const Real b( h * sqrtDt );

    return 1 + W( a1, b ) - erfc( a1 ) 
             - W( a2, b ) + erfc( a2 );
}


const EventType
OneDimGreensFunctionRadInf::drawEventType( const Real rnd, const Real t )
const
{
    return REACTION;
}


const std::string OneDimGreensFunctionRadInf::dump() const
{
    std::ostringstream ss;
    ss << "D = " << D << ", r0 = " << r0 << ", h = " << h << std::endl;
    return ss.str();
}    
