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

from collections import namedtuple
import collections

Coordinate = namedtuple('Coordinate', ['x', 'y'])


class Wire(object):
    def __init__(self):
        self._coordinates = []
        self._coordinate = Coordinate(x=0, y=0)

    def _decode_direction(self, direction):
        coordinates = []
        value = int(direction[1:])

        if direction.startswith('R'):
            for _ in range(value):
                self._coordinate = Coordinate(self._coordinate.x + 1, self._coordinate.y)
                coordinates.append(self._coordinate)
        elif direction.startswith('L'):
            for _ in range(value):
                self._coordinate = Coordinate(self._coordinate.x - 1, self._coordinate.y)
                coordinates.append(self._coordinate)
        elif direction.startswith('D'):
            for _ in range(value):
                self._coordinate = Coordinate(self._coordinate.x, self._coordinate.y + 1)
                coordinates.append(self._coordinate)
        else:
            for _ in range(value):
                self._coordinate = Coordinate(self._coordinate.x, self._coordinate.y - 1)
                coordinates.append(self._coordinate)
        return coordinates

    def trace(self, directions):
        for direction in directions:
            coordinates = self._decode_direction(direction)
            self._coordinates.extend(coordinates)

    @property
    def length(self):
        return len(self._coordinates)


    @property
    def coordinates(self):
        return self._coordinates


def get_wiring_directions_from_file(file_name):
    """Get all integers from the given file."""
    directions = []

    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            directions.append([direction for direction in line.rstrip().split(',')])

    return directions


def get_manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_closest_distance_to_port(intersections):
    port_coordinate = Coordinate(x=0, y=0)
    closest_distance = None

    for coordinate in intersections:
        distance = get_manhattan_distance(port_coordinate, coordinate)
        if closest_distance == None or distance < closest_distance:
            closest_distance = distance

    return closest_distance


def main():
    directions = get_wiring_directions_from_file('input.txt')

    wire_one = Wire()
    wire_one.trace(directions[0])

    wire_two = Wire()
    wire_two.trace(directions[1])

    intersections = list(set(wire_one.coordinates) & set(wire_two.coordinates))
    closest_distance = get_closest_distance_to_port(intersections)

    shortest_length = None
    for coordinate in intersections:
        length = wire_one.coordinates.index(coordinate) + wire_two.coordinates.index(coordinate) + 2

        if shortest_length == None or length < shortest_length:
            shortest_length = length

    print('Part 1 answer: {}'.format(closest_distance))
    print('Part 2 answer: {}'.format(shortest_length))
    return 0


if __name__ == '__main__':
    exit(main())
