#if !defined( __ONEDIMGREENSFUNCTIONABSINF )
#define __ONEDIMGREENSFUNCTIONABSINF

#include "OneDimGreensFunctionOneBoundary.hpp"

class OneDimGreensFunctionAbsInf
    :
    public OneDimGreensFunctionOneBoundary
{

private:

public:
    OneDimGreensFunctionAbsInf( const Real D )
        :
        OneDimGreensFunctionOneBoundary( D )
    {
        ; // do nothing
    }

    ~OneDimGreensFunctionAbsInf()
    {
        ; // do nothing
    }

    const Real p_survival (const Real t) const;

    const Real p_int_r( const Real r, const Real t ) const;

    const EventType drawEventType( const Real rnd, 
                                   const Real t ) const;

    const std::string dump() const;

private:
};

#endif // __ONEDIMGREENSFUNCTIONABSINF
