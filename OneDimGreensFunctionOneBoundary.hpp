#if !defined( __ONEDIMGREENSFUNCTIONONEBOUNDARY_HPP )
#define __ONEDIMGREENSFUNCTIONONEBOUNDARY_HPP

#include "Defs.hpp"

class OneDimGreensFunctionOneBoundary
{
private:
    // This is a typical length scale of the system, may not be true!
    // Todo. Should we add a parameter sigma anyway, so we have some idea of 
    // scale?
    static const Real L_TYPICAL = 1E-8;
    // The typical timescale of the system, may also not be true!
    static const Real T_TYPICAL = 1E-6;
    // Measure of 'sameness' when comparing floating points numbers.
    static const Real EPSILON = 1E-12;
    // Minimal timestep.
    static const Real MIN_T = 1e-18;


public:
    OneDimGreensFunctionOneBoundary( const Real D )
        :
        D( D ), r0( r0 ), t_scale( T_TYPICAL ), l_scale( L_TYPICAL )
    {
        ; // do nothing
    }

    ~OneDimGreensFunctionOneBoundary()
    {
        ; // do nothing
    }

    void setL(const Real L)
    {
        ; // Ignore.
    }

    void setr0(const Real r0)
    {
        this->r0 = r0;
    }

    virtual const Real p_survival( const Real t ) const = 0; 

    const Real drawTime( const Real rnd ) const;

    virtual const Real p_int_r( const Real r, const Real t ) const = 0;

    const Real drawR( const Real rnd, const Real t ) const;

    virtual const EventType drawEventType( const Real rnd, 
                                           const Real t ) const = 0;

    virtual const std::string dump() const = 0;


private:
    struct p_survival_params
    {
        const OneDimGreensFunctionOneBoundary* const gf;
        const Real rnd;
    };

    static const Real p_survival_F( const Real t, 
                                    const p_survival_params* params );

    struct p_int_r_params
    {
        const OneDimGreensFunctionOneBoundary* const gf;
        const Real t;
        const Real rnd;
    };

    static const Real p_int_r_F( const Real r, 
                                 const p_int_r_params* params );


protected:
    const Real D;
    Real r0;

private:
    const Real t_scale;
    const Real l_scale;
};

#endif // __ONEDIMGREENSFUNCTIONONEBOUNDARY_HPP
