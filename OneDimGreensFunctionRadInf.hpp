#if !defined( __ONEDIMGREENSFUNCTIONRADINF )
#define __ONEDIMGREENSFUNCTIONRADINF

#include "OneDimGreensFunctionOneBoundary.hpp"

class OneDimGreensFunctionRadInf
    :
    public OneDimGreensFunctionOneBoundary
{

private:

public:
    OneDimGreensFunctionRadInf( const Real D, const Real k )
        :
        OneDimGreensFunctionOneBoundary( D ), h( k / D )
    {
        ; // do nothing
    }

    ~OneDimGreensFunctionRadInf()
    {
        ; // do nothing
    }

    const Real p_survival (const Real t) const;

    const Real p_int_r( const Real r, const Real t ) const;

    const EventType drawEventType( const Real rnd, 
                                   const Real t ) const;

    const std::string dump() const;

private:
    const Real h;
};

#endif // __ONEDIMGREENSFUNCTIONRADINF
