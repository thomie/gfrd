#define BOOST_TEST_MODULE "filters_test"

#include <boost/test/included/unit_test.hpp>
#include "object_container.hpp"
#include "filters.hpp"

template<typename Toc_>
struct collector
{
    void operator()(typename Toc_::iterator i,
            typename Toc_::position_type::value_type dist)
    {
        std::cout << (*i).second << ", " << dist << std::endl;
    }
};


BOOST_AUTO_TEST_CASE(basic)
{
    typedef object_container<double, int> oc_type;
    typedef oc_type::position_type pos;
    oc_type oc(1.0, 10);

    oc.insert(std::make_pair(0, oc_type::mapped_type(pos(0.2, 0.6, 0.4), 0.15)));
    oc.insert(std::make_pair(1, oc_type::mapped_type(pos(0.2, 0.7, 0.5), 0.05)));
    oc.insert(std::make_pair(2, oc_type::mapped_type(pos(0.9, 0.1, 0.4), 0.07)));
    oc.insert(std::make_pair(3, oc_type::mapped_type(pos(0.9, 0.95, 0.4), 0.1)));

    collector<oc_type> col;
    // Construct an iterator for object 1 in oc.
    oc_type::const_iterator f(oc.find(1));
    // Collect all objects from oc that lie within the radius of object 1.
    // The shell of object 0 is at a distance sqrt(2*0.1*0.1) - 0.15 = 
    // -0.0087864..
    // The shell of the objects itself is at a distance -0.05 (Yes it returns 
    // itself also).
    // Objects 2 and 3 should not be found.
    take_neighbor(oc, col, (*f).second);
}
