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


def get_pixels_from_file(file_name):
    """Get all pixel from the given file."""
    pixels = []

    with open(file_name) as file:
        lines = file.readlines()

        for line in lines:
            pixels.extend([int(pixel) for pixel in line.rstrip()])

    return pixels


class SpaceImage(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._layers = []

    def load(self, data):
        idx = 0
        number_of_pixels_in_layer = self._height * self._width

        while idx < len(data):
            layer = []
            for _ in range(number_of_pixels_in_layer):
                layer.append(data[idx])
                idx += 1
            self._layers.append(layer)

    def _get_combined_layers(self):
        combined_layer = self.layers[0].copy()

        for layer in self._layers[1:]:

            for i in range(len(combined_layer)):
                if combined_layer[i] == 2:
                    combined_layer[i] = layer[i]

        return combined_layer

    @property
    def layers(self):
        return self._layers

    def draw(self):
        layer = self._get_combined_layers()

        for y_coordinate in range(self._height):
            for x_coordinate in range(self._width):

                color = layer[self._width * y_coordinate + x_coordinate]
                if color == 0:
                    print(' ', end='')
                else:
                    print('#', end='')
            print()


def get_part_one_answer():
    pixels = get_pixels_from_file('input.txt')

    image = SpaceImage(25, 6)
    image.load(pixels)

    min_number_of_zeroes = image.layers[0].count(0)
    min_layer_index = 0
    layer_index = 0
    for layer in image.layers:
        number_of_zeroes = layer.count(0)
        if number_of_zeroes < min_number_of_zeroes:
            min_number_of_zeroes = number_of_zeroes
            min_layer_index = layer_index
        layer_index += 1

    layer = image.layers[min_layer_index]
    return layer.count(1) * layer.count(2)


def get_part_two_answer():
    pixels = get_pixels_from_file('input.txt')

    image = SpaceImage(25, 6)
    image.load(pixels)
    image.draw()


def main():
    print('Part 1 answer: {}'.format(get_part_one_answer()))

    print('Part 2 answer:')
    get_part_two_answer()

    return 0


if __name__ == '__main__':
    exit(main())
