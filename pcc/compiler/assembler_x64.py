#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pcc.compiler.assembler import Assembler, ProcessorRegister

import struct


# http://ref.x86asm.net/coder64.html
# https://www.amd.com/system/files/TechDocs/24594.pdf
# page 74 for

def get_register_encoding(register):
    if register == ProcessorRegister.frame_pointer:
        return 4
    elif register == ProcessorRegister.base_pointer:
        return 5
    elif register == ProcessorRegister.accumulator:
        return 0
    else:
        raise NotImplementedError


class x64Assembler(Assembler):

    def __init__(self):
        pass

    def push_to_stack(self, register):
        """Push a register on stack.

        Args:
            register (ProcessorRegister): the register to push on stack

        Returns:
            bytearray: the machine code
        """

        value = bytearray()
        register_encoding = get_register_encoding(register)
        value.append(0x50 + register_encoding)
        # 0x50 == push instruction,
        # the register to push is encoded and added

        return value

    def pop_from_stack(self, register):
        """Pop a register from stack.

        Args:
            register (ProcessorRegister): the register to push on stack

        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        register_encoding = get_register_encoding(register)
        value.append(0x58 + register_encoding)
        # (0x58 == pop) + the register to pop to
        return value

    def copy_from_reg_to_reg(self, source, destination):
        """Copy the value from one register to another one.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        value = bytearray()

        # 0x48 REX prefix with W flag set (64 bit operands)
        # 0x89 MOV instruction
        # ModR_byte encoded operands ( ModR/M Byte) MOD 11, RM source and
        # REG destination
        mod = 0b11
        reg = get_register_encoding(destination)
        rm = get_register_encoding(source)
        modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
        value.extend([0x48, 0x89, modr_byte])

        return value

    def copy_value_to_reg(self, imm_value, destination):
        """Copy the value to a register.

        Args:
            imm_value (int): the value to copy
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        if destination == ProcessorRegister.single_scalar_0:
            # mov the single scalar to eax
            value += bytearray([0xb8])
            packed = struct.pack("f", imm_value)
            value += bytearray(packed)
            # movd eax to xmm0
            value += bytearray([0x66, 0x0f, 0x6e, 0xc0])
        elif destination == ProcessorRegister.double_scalar_0:
            # mov the double scalar to rax
            value += bytearray([0x48, 0xb8])
            packed = struct.pack("d", imm_value)
            value += bytearray(packed)
            # movq   rax to xmm0
            value += bytearray([0x66, 0x48, 0x0f, 0x6e, 0xc0])
        else:
            register_encoding = get_register_encoding(destination)
            value.append(0xb8 + register_encoding)
            # (0xb8 == mov imm) + the register to move to
            value += bytearray(struct.pack("i", imm_value))

        return value

    def return_to_caller(self):
        """Return to the caller routine.

        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        value.append(0xc3)  # ret instruction
        return value

    def nop(self):
        """No operation.

        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        value.append(0x90)  # nop
        return value

    def push_value_to_stack(self, value_array, stack_offset):
        """Pushes a value on stack
        Attributes:
            value_array (bytearray): the value to push on stack
            stack_offset (int): the offset from the stack pointer
        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        value.append(0xc7)  # mov
        # Table 2-2.  32-Bit Addressing Forms with the ModR/M Byte
        # indirect adressing with byte displacement
        mod = 0b01
        destination = ProcessorRegister.base_pointer
        rm = get_register_encoding(destination)
        reg = 0  # don't care
        modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
        value.append(modr_byte)

        encoded_offset = struct.pack("b", stack_offset)
        value += encoded_offset

        value.extend(value_array)

        return value
