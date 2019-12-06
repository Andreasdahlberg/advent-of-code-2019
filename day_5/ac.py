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

Instruction = namedtuple('Instruction', ['opcode', 'a',  'b', 'c'])
Parameter = namedtuple('Parameter', ['value', 'mode'])



outputs = []


def get_length_for_opcode(opcode):
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
    return lengths[opcode]


def get_raw_instructions_from_file(file_name):
    """Get all instructions from the given file."""
    instructions = []

    with open(file_name) as file:
        lines = file.readlines()

        for line in lines:
            instructions.extend([int(integer) for integer in line.rstrip().split(',')])

    return instructions

def get_parameters(instruction, registers):
    if instruction.a.mode:
        a = instruction.a.value
    else:
        a = registers[instruction.a.value]

    if instruction.b.mode:
        b = instruction.b.value
    else:
        b = registers[instruction.b.value]

    return a, b


def add(instruction, registers, ip):
    a, b = get_parameters(instruction, registers)
    registers[instruction.c.value] = a + b
    return ip + get_length_for_opcode(instruction.opcode)


def multi(instruction, registers, ip):
    a, b = get_parameters(instruction, registers)
    registers[instruction.c.value] = a * b
    return ip + get_length_for_opcode(instruction.opcode)


def store(instruction, registers, ip):
    registers[instruction.a.value] = 5
    print('Store {} at {}'.format(1, instruction.a.value))
    return ip + get_length_for_opcode(instruction.opcode)


def output(instruction, registers, ip):

    if instruction.a.mode:
        outputs.append(instruction.a.value)
        print('Output {}'.format(instruction.a.value))
    else:
        outputs.append(registers[instruction.a.value])
        print('Output {} from {}'.format(registers[instruction.a.value], instruction.a.value))
    return ip + get_length_for_opcode(instruction.opcode)


def jump_if_true(instruction, registers, ip):
    a, b = get_parameters(instruction, registers)

    if a:
        return b
    else:
        return ip + get_length_for_opcode(instruction.opcode)


def jump_if_false(instruction, registers, ip):
    a, b = get_parameters(instruction, registers)

    if not a:
        return b
    else:
        return ip + get_length_for_opcode(instruction.opcode)


def less(instruction, registers, ip):
    a, b = get_parameters(instruction, registers)
    registers[instruction.c.value] = int(a < b)
    return ip + get_length_for_opcode(instruction.opcode)


def equal(instruction, registers, ip):
    a, b = get_parameters(instruction, registers)
    registers[instruction.c.value] = int(a == b)
    return ip + get_length_for_opcode(instruction.opcode)


def halt(instruction, registers, ip):
    print('Halt')
    return None



DECODER = {
        1: add,
        2: multi,
        3: store,
        4: output,
        5: jump_if_true,
        6: jump_if_false,
        7: less,
        8: equal,
        99: halt
    }



def execute_instruction(raw_instruction, integers, ip):
    instruction = Instruction(*raw_instruction)

    return DECODER[instruction.opcode](instruction, integers, ip)


def decode(instructions, ip):
    opcode = instructions[ip] % 100
    instruction_length = get_length_for_opcode(opcode)

    params = []
    mod = 100
    for i in range(ip + 1 , ip + instruction_length):


        mode = int((instructions[ip] % (mod * 10)) / mod)
        params.append(Parameter(instructions[i], mode))
        mod *= 10


    params += [Parameter(0, 0)] * (4 - instruction_length)


    instruction = Instruction(opcode, *params)
    print(ip, DECODER[instruction.opcode], instruction)

    return instruction


def execute(instructions):
    ip = 0

    while(ip < len(instructions)):

        instruction = decode(instructions, ip)


        ip = execute_instruction(instruction, instructions, ip)
        if ip is None:
            break




def main():

    raw_instructions = get_raw_instructions_from_file('input.txt')
    execute(raw_instructions)

    print('Part 1 answer: {}'.format(outputs[-1]))
    print('Part 2 answer: {}'.format(None))

    return 0


if __name__ == '__main__':
    exit(main())
