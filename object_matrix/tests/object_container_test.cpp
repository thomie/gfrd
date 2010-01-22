#define BOOST_TEST_MODULE "object_container_test"

#include <functional>
#include <iostream>
#include <boost/test/included/unit_test.hpp>
#include <boost/test/floating_point_comparison.hpp>
#include "object_container.hpp"

BOOST_AUTO_TEST_CASE(insert)
{
    typedef object_container<double, int> oc_type;
    typedef oc_type::position_type pos;
    oc_type oc(1.0, 10);
    BOOST_CHECK_CLOSE(0.1, oc.cell_size(), 0.001);
    {
        std::pair<oc_type::iterator, bool> ir(
                oc.insert(std::make_pair(
                    0, oc_type::mapped_type(pos(0.2, 0.6, 0.4), 0.5))));
        BOOST_CHECK_EQUAL(true, ir.second);  // Normal insert.
        BOOST_CHECK(oc.end() != oc.find(0)); // Key 0 exists.
        BOOST_CHECK(oc.end() == oc.find(1)); // Key 1 doesn't exist.
    }
    {
	// Update.
        std::pair<oc_type::iterator, bool> ir(
                oc.insert(std::make_pair(
                    0, oc_type::mapped_type(pos(0.2, 0.65, 0.4), 0.5))));
        BOOST_CHECK_EQUAL(false, ir.second); // False: this was an update.
	// ir.first is an iterator to the value you inserted. So accessing 
	// it's second element should return you the object.
        BOOST_CHECK_EQUAL(oc_type::mapped_type(pos(0.2, 0.65, 0.4), 0.5),
                (*ir.first).second);
        BOOST_CHECK(oc.end() != oc.find(0));
        BOOST_CHECK(oc.end() == oc.find(1));
    }
    {
	// Another update.
        std::pair<oc_type::iterator, bool> ir(
                oc.insert(std::make_pair(
                    0, oc_type::mapped_type(pos(0.2, 0.2, 0.4), 0.5))));
        BOOST_CHECK_EQUAL(false, ir.second);
        BOOST_CHECK_EQUAL(oc_type::mapped_type(pos(0.2, 0.2, 0.4), 0.5),
                (*ir.first).second);
        BOOST_CHECK(oc.end() != oc.find(0));
        BOOST_CHECK(oc.end() == oc.find(1));
    }
}

template<typename Toc_>
struct collector
{
    void operator()(typename Toc_::iterator i)
    {
        std::cout << (*i).second << std::endl;
    }
};

template<typename Toc_>
struct collector2
{
    void operator()(typename Toc_::iterator i,
            const typename Toc_::position_type& pos_off)
    {
        std::cout << (*i).second;
	// Signal if periodic boundary condition is applied (i.e. (-1,0,0), 
	// where -1 stands for: to go from the found object to the point I had  
	// to subtract -1 off its x coordinate. 
        std::cout << pos_off << std::endl;
    }
};

BOOST_AUTO_TEST_CASE(each_neighbor)
{
    typedef object_container<double, int> oc_type;
    typedef oc_type::position_type pos;
    oc_type oc(1.0, 10);
    BOOST_CHECK_CLOSE(0.1, oc.cell_size(), 0.001);

    // Insert 4 values.
    // Range of cells: [0, 0.1), [0.1, 0.2), .., [0.8, 0.9)
    // [0.9, 1) = [0.9, 0)
    oc.insert(std::make_pair(0, oc_type::mapped_type(pos(0.2, 0.6, 0.4), 0.5)));
    BOOST_CHECK(oc.end() != oc.find(0));
    BOOST_CHECK(oc.end() == oc.find(1));
    oc.insert(std::make_pair(1, oc_type::mapped_type(pos(0.2, 0.7, 0.5), 0.5)));
    BOOST_CHECK(oc.end() != oc.find(0));
    BOOST_CHECK(oc.end() != oc.find(1));
    BOOST_CHECK(oc.end() == oc.find(2));
    oc.insert(std::make_pair(2, oc_type::mapped_type(pos(0.9, 0.1, 0.4), 0.5)));
    BOOST_CHECK(oc.end() != oc.find(0));
    BOOST_CHECK(oc.end() != oc.find(1));
    BOOST_CHECK(oc.end() != oc.find(2));
    BOOST_CHECK(oc.end() == oc.find(3));
    oc.insert(std::make_pair(3, oc_type::mapped_type(pos(0.9, 0.95, 0.4), 0.5)));
    BOOST_CHECK(oc.end() != oc.find(0));
    BOOST_CHECK(oc.end() != oc.find(1));
    BOOST_CHECK(oc.end() != oc.find(2));
    BOOST_CHECK(oc.end() != oc.find(3));
    BOOST_CHECK(oc.end() == oc.find(4));

    collector<oc_type> col;
    // Return all value in this cell and the neighboring cells. Should return 
    // values 0 and 1.
    oc.each_neighbor(oc.index(pos(0.2, 0.6, 0.4)), col);
    std::cout << "--" << std::endl;

    // No periodic boundary condition. Should return no values.
    oc.each_neighbor(oc.index(pos(0.0, 0.1, 0.4)), col);
    std::cout << "--" << std::endl;

    collector2<oc_type> col2;
    // Periodic boundary condition. Should return element 2 after applying 
    // periodic boundary condition in x. So (0.9, 0.1, 0.4) + (-1,0,0) = 
    // (-0.1, 0.1, 0.4), and that is indeed a neighbor of (0.0, 0.1, 0.4).
    oc.each_neighbor_cyclic(oc.index(pos(0.0, 0.1, 0.4)), col2);
    std::cout << "--" << std::endl;
    // Periodic boundary condition. Should return element 3, after adding (0, 
    // -1, 0) to it's pos, and element 2 (0,0,0).
    oc.each_neighbor_cyclic(oc.index(pos(0.9, 0.0, 0.4)), col2);
}
