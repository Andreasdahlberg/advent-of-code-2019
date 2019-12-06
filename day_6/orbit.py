#!/usr/bin/env python3
# -*- coding: utf-8 -*
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'andreas.dahlberg90@gmail.com (Andreas Dahlberg)'
__version__ = '0.1.0'


from collections import deque

class Orbit(object):
    def __init__(self, parent, id):
        self._id = id
        self._parent = parent
        self._children = []

        self._iter_index = 0

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index == len(self._children):
            raise StopIteration
        else:
            self._iter_index = self._iter_index + 1
            return self._children[self._iter_index - 1]

    def __len__(self):
        return len(self._children)

    @property
    def id(self):
        return self._id

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children


    def add_child(self, child):
        self._children.append(child)





def get_orbits_from_file(file_name):
    """Get all orbits from the given file."""
    orbits = {}

    with open(file_name) as file:
        lines = file.readlines()

        for line in lines:
            orbit = Orbit(*line.rstrip().split(')'))
            orbits[orbit.id] = orbit
    return orbits


def find_top_orbit(orbits):


    for orbit_id in orbits:
        if orbits[orbit_id].parent == 'COM':
            return orbits[orbit_id]
    return None


def populate_children(orbits):
    for orbit_id in orbits:
        if orbits[orbit_id].parent != 'COM':
            orbits[orbits[orbit_id].parent].add_child(orbit_id)


def trace_to(orbit, orbits, id):

    count = 0

    o = orbit
    while o.parent != id:
        count += 1
        o = orbits[o.parent]

    return count + 1

def find_common_orbit(orbit_a, orbit_b, orbits):

    orbit_a_path = []

    o = orbit_a
    while o.parent != 'COM':
        o = orbits[o.parent]
        orbit_a_path.append(o)

    o = orbit_b
    while o.parent != 'COM':
        o = orbits[o.parent]
        if o in orbit_a_path:
            return o

    return None

def main():


    orbits = get_orbits_from_file('input.txt')


    top = find_top_orbit(orbits)
    populate_children(orbits)


    c = 0

    for orbit_id in orbits:
        orbit = orbits[orbit_id]

        ct = trace_to(orbit, orbits, 'COM')
        #print(ct)

        c += ct



    orbit_a = orbits[orbits['YOU'].parent]
    orbit_b = orbits[orbits['SAN'].parent]


    common_orbit = find_common_orbit(orbit_a, orbit_b, orbits)
    print(common_orbit.id)

    a = trace_to(orbit_a, orbits, common_orbit.id)
    b = trace_to(orbit_b, orbits, common_orbit.id)

    print('Part 1 answer: {}'.format(c))
    print('Part 2 answer: {}'.format(a + b))

    return 0


if __name__ == '__main__':
    exit(main())
