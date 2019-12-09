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
from collections import deque

Instruction = namedtuple('Instruction', ['opcode', 'a',  'b', 'c'])
Parameter = namedtuple('Parameter', ['value', 'mode'])


def get_int_code_from_file(file_name):
    """Get int code from the given file."""
    int_code = []

    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            int_code.extend([int(integer) for integer in line.rstrip().split(',')])

    return int_code


class IntCodeComputer(object):
    def __init__(self, data):
        self._data = data.copy()
        self._ip = 0
        self._inputs = deque([])
        self._outputs = []

    def execute(self):
        while self._ip is not None and self._ip < len(self._data):
            self._ip = self._execute_next_instruction()

    def input(self, value):
        self._inputs.append(value)

    @property
    def outputs(self):
        return self._outputs

    def _execute_next_instruction(self):
        instruction = self._decode()
        func = self._get_instruction_function(instruction)
        return func(instruction)

    def _get_instruction_function(self, instruction):
        return getattr(self, '_' + str(instruction.opcode))

    def _decode(self):
        lengths = {
            1: 4,
            2: 4,
            3: 2,
            4: 2,
            5: 3,
            6: 3,
            7: 4,
            8: 4,
            99: 1
        }

        opcode = self._data[self._ip] % 100

        params = []
        mod = 100
        for i in range(self._ip + 1 , self._ip + lengths[opcode]):
            mode = int((self._data[self._ip] % (mod * 10)) / mod)
            params.append(Parameter(self._data[i], mode))
            mod *= 10
        params += [Parameter(0, 0)] * (4 - lengths[opcode])


        instruction = Instruction(opcode, *params)
        print(self._ip, self._get_instruction_function(instruction), instruction)
        return instruction

    def _get_parameters(self, instruction):
        if instruction.a.mode:
            a = instruction.a.value
        else:
            a = self._data[instruction.a.value]

        if instruction.b.mode:
            b = instruction.b.value
        else:
            b = self._data[instruction.b.value]
        return a, b

    def _1(self, instruction):
        """Add"""
        LENGTH = 4
        a, b = self._get_parameters(instruction)
        self._data[instruction.c.value] = a + b
        return self._ip + LENGTH

    def _2(self, instruction):
        """Multiply"""
        LENGTH = 4
        a, b = self._get_parameters(instruction)
        self._data[instruction.c.value] = a * b
        return self._ip + LENGTH

    def _3(self, instruction):
        """Store"""
        LENGTH = 2
        value = self._inputs.popleft()
        self._data[instruction.a.value] = value
        print('Store {} at {}'.format(value, instruction.a.value))
        return self._ip + LENGTH

    def _4(self, instruction):
        """Output"""
        LENGTH = 2
        if instruction.a.mode:
            self._outputs.append(instruction.a.value)
            print('Output {}'.format(instruction.a.value))
        else:
            self._outputs.append(self._data[instruction.a.value])
            print('Output {} from {}'.format(self._data[instruction.a.value], instruction.a.value))
        return self._ip + LENGTH

    def _5(self, instruction):
        """Jump if true"""
        LENGTH = 3
        a, b = self._get_parameters(instruction)

        if a:
            return b
        else:
            return self._ip + LENGTH

    def _6(self, instruction):
        """Jump if false"""
        LENGTH = 3
        a, b = self._get_parameters(instruction)

        if not a:
            return b
        else:
            return self._ip + LENGTH

    def _7(self, instruction):
        """Less"""
        LENGTH = 4
        a, b = self._get_parameters(instruction)
        self._data[instruction.c.value] = int(a < b)
        return self._ip + LENGTH

    def _8(self, instruction):
        """Equal"""
        LENGTH = 4
        a, b = self._get_parameters(instruction)
        self._data[instruction.c.value] = int(a == b)
        return self._ip + LENGTH

    def _99(self, instruction):
        print('Halt')
        return None
