#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pcc.compiler.assembler import Assembler, ProcessorRegister, ShiftMode

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
    elif register == ProcessorRegister.single_scalar_0:
        return 0
    elif register == ProcessorRegister.single_scalar_1:
        return 1
    elif register == ProcessorRegister.double_scalar_0:
        return 0
    elif register == ProcessorRegister.double_scalar_1:
        return 1
    elif register == ProcessorRegister.counter:
        return 1
    elif register == ProcessorRegister.data:
        return 2
    else:
        raise NotImplementedError


def is_single_scalar_reg(register):
    """Check if the register is a single scalar register

    Args:
        register (ProcessorRegister): The register to check

    Returns:
        bool: True if the register is a single scalar register, else False
    """
    if register in [ProcessorRegister.single_scalar_0,
                    ProcessorRegister.single_scalar_1]:
        return True
    else:
        return False


def is_double_scalar_reg(register):
    """Check if the register is a double scalar register

    Args:
        register (ProcessorRegister): The register to check

    Returns:
        bool: True if the register is a double scalar register, else False
    """
    if register in [ProcessorRegister.double_scalar_0,
                    ProcessorRegister.double_scalar_1]:
        return True
    else:
        return False


class x64Assembler(Assembler):

    def __init__(self):
        super(x64Assembler).__init__()

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
        if is_single_scalar_reg(destination):
            # mov the single scalar to eax
            value += bytearray([0xb8])
            packed = struct.pack("f", imm_value)
            value += bytearray(packed)
            # movd eax to xmm0
            value += bytearray([0x66, 0x0f, 0x6e])
            register_encoding = get_register_encoding(destination)
            value += bytearray([0xc0 + (register_encoding << 3)])
        elif is_double_scalar_reg(destination):
            # mov the double scalar to rax
            value += bytearray([0x48, 0xb8])
            packed = struct.pack("d", imm_value)
            value += bytearray(packed)
            # movq   rax to xmm0
            value += bytearray([0x66, 0x48, 0x0f, 0x6e])
            register_encoding = get_register_encoding(destination)
            value += bytearray([0xc0 + (register_encoding << 3)])
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

        if len(value_array) > 4:
            raise ValueError("array too long")

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
        if len(value_array) < 4:
            padding = 4 - len(value_array)
            for _ in range(padding):
                value.append(0)

        return value

    def copy_stack_to_reg(self, stack_offset, register):
        """Copy the contents of the stack to the register

        Args:
            stack_offset (int): the stack offset
            register (ProcessorRegister): the register to copy to
        """
        value = bytearray()
        if is_single_scalar_reg(register):
            value.extend([0xF3, 0x0F, 0x10])  # movss
        elif is_double_scalar_reg(register):
            value.extend([0xF2, 0x0F, 0x10])  # movsd
        else:
            value.append(0x8b)  # mov
        # Table 2-2.  32-Bit Addressing Forms with the ModR/M Byte
        # indirect adressing with byte displacement
        mod = 0b01
        destination = ProcessorRegister.base_pointer
        rm = get_register_encoding(destination)
        reg = get_register_encoding(register)
        modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
        value.append(modr_byte)

        encoded_offset = struct.pack("b", stack_offset)
        value += encoded_offset

        return value

    def copy_reg_to_stack(self, stack_offset, register):
        """Copy the contents of the register to the stack

        Args:
            stack_offset (int): the stack offset
            register (ProcessorRegister): the register to copy from
        """
        value = bytearray()
        if is_single_scalar_reg(register):
            value.extend([0xF3, 0x0F, 0x11])  # movss
        elif is_double_scalar_reg(register):
            value.extend([0xF2, 0x0F, 0x11])  # movsd
        else:
            value.append(0x89)  # mov
        # Table 2-2.  32-Bit Addressing Forms with the ModR/M Byte
        # indirect adressing with byte displacement
        mod = 0b01
        destination = ProcessorRegister.base_pointer
        rm = get_register_encoding(destination)
        reg = get_register_encoding(register)
        modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
        value.append(modr_byte)

        encoded_offset = struct.pack("b", stack_offset)
        value += encoded_offset

        return value

    def add(self, source, destination):
        """Add the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        if is_single_scalar_reg(source):
            value.extend([0xF3, 0x0F, 0x58])  # addss
            # swap the source and destination, as it has a different order
            # wrt the int add encoding
            tmp = source
            source = destination
            destination = tmp
        elif is_double_scalar_reg(source):
            value.extend([0xF2, 0x0F, 0x58])  # addsd
            # swap the source and destination, as it has a different order
            # wrt the int add encoding
            tmp = source
            source = destination
            destination = tmp
        else:
            value.append(0x01)  # ADD
        # ModR_byte encoded operands ( ModR/M Byte) MOD 11, RM source and
        # REG destination
        mod = 0b11
        rm = get_register_encoding(source)
        reg = get_register_encoding(destination)
        modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
        value.append(modr_byte)

        return value

    def sub(self, source, destination):
        """Subtract the value of the source from the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        value = bytearray()
        if is_single_scalar_reg(source):
            value.extend([0xF3, 0x0F, 0x5c])  # subss
            # swap the source and destination, as it has a different order
            # wrt the int add encoding
            tmp = source
            source = destination
            destination = tmp
        elif is_double_scalar_reg(source):
            value.extend([0xF2, 0x0F, 0x5c])  # subsd
            # swap the source and destination, as it has a different order
            # wrt the int add encoding
            tmp = source
            source = destination
            destination = tmp
        else:
            value.append(0x29)  # sub
        # ModR_byte encoded operands ( ModR/M Byte) MOD 11, RM source and
        # REG destination
        mod = 0b11
        rm = get_register_encoding(source)
        reg = get_register_encoding(destination)
        modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
        value.append(modr_byte)

        return value

    def div(self, dividend, divider):
        """Divide the value of the source by the destination.

        Store the result in the  dividend register.

        Args:
            dividend (ProcessorRegister): the dividend register
            divider (ProcessorRegister): the divider register

        Returns:
            bytearray: the machine code
        """
        value = bytearray()

        if is_single_scalar_reg(divider):
            value.extend([0xF3, 0x0F, 0x5E])  # divss
            mod = 0b11
            rm = get_register_encoding(divider)
            reg = get_register_encoding(dividend)
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)
        elif is_double_scalar_reg(divider):
            value.extend([0xF2, 0x0F, 0x5E])  # divsd
            mod = 0b11
            rm = get_register_encoding(divider)
            reg = get_register_encoding(dividend)
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)
        else:
            # idiv eax = edx:eax / src
            if divider in [ProcessorRegister.accumulator,
                           ProcessorRegister.data]:
                tmp_reg = ProcessorRegister.counter
                value += self.copy_from_reg_to_reg(divider, tmp_reg)

            if dividend != ProcessorRegister.accumulator:
                tmp_reg = ProcessorRegister.accumulator
                value += self.copy_from_reg_to_reg(dividend, tmp_reg)

            # mov edx -> eax
            value += self.copy_from_reg_to_reg(ProcessorRegister.data,
                                               ProcessorRegister.accumulator)
            # shift edx by 31 -> contains the highest bits of the dividend,
            # eax the lowest 31 bits
            value += self.shift(ProcessorRegister.data,
                                ShiftMode.right_arithmetic,
                                amount=31)
            value.append(0xf7)  # idiv

            mod = 0b11
            rm = get_register_encoding(divider)
            reg = 7  # F7 /7 -> 7 in the reg field
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)

            # the result is stored in the acc register, so copy it to the
            # correct result register if needed
            if dividend != ProcessorRegister.accumulator:
                register = ProcessorRegister.accumulator
                value += self.copy_from_reg_to_reg(register, dividend)

        return value

    def mul(self, destination, source):
        """Multiply the value of the source by the destination.

        destination = source * destination
        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the source register

        Returns:
            bytearray: the machine code
        """
        value = bytearray()

        if is_single_scalar_reg(destination):
            value.extend([0xF3, 0x0F, 0x59])  # mulss
            mod = 0b11
            rm = get_register_encoding(source)
            reg = get_register_encoding(destination)
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)
        elif is_double_scalar_reg(destination):
            value.extend([0xF2, 0x0F, 0x59])  # mulsd
            mod = 0b11
            rm = get_register_encoding(source)
            reg = get_register_encoding(destination)
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)
        else:
            # imul EDX:EAX ← EAX ∗ r/m32
            if source in [ProcessorRegister.accumulator,
                          ProcessorRegister.data]:
                tmp_reg = ProcessorRegister.counter
                value += self.copy_from_reg_to_reg(source, tmp_reg)
                source = tmp_reg

            if destination != ProcessorRegister.accumulator:
                tmp_reg = ProcessorRegister.accumulator
                value += self.copy_from_reg_to_reg(destination, tmp_reg)

            value.append(0xf7)  # imul

            mod = 0b11
            rm = get_register_encoding(source)
            reg = 5  # F7 /5 -> 5 in the reg field
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)

            # the result is stored in the acc register, so copy it to the
            # correct result register if needed
            if destination != ProcessorRegister.accumulator:
                register = ProcessorRegister.accumulator
                value += self.copy_from_reg_to_reg(register, destination)

        return value

    def shift(self, register, mode, amount):
        """Shift the register.

        Args:
            register (ProcessorRegister): the register to shift
            mode (ShiftMode): the mode to shift
            amount (int): the shift amount

        Returns:
            bytearray: the machine code
        """
        value = bytearray()

        if mode == ShiftMode.right_arithmetic:
            # SAR r/m32, imm8
            value.append(0xC1)
            mod = 0b11
            rm = get_register_encoding(register)
            reg = 7  # C1 /7 ib -> 7 in reg field
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)

            encoded_amount = struct.pack("b", amount)
            value += encoded_amount
        elif mode == ShiftMode.left_arithmetic:
            # SAL r/m32, imm8
            value.append(0xC1)
            mod = 0b11
            rm = get_register_encoding(register)
            reg = 4  # C1 /4 ib -> 4 in reg field
            modr_byte = (mod << 6) + (reg << 3) + (rm << 0)
            value.append(modr_byte)

            encoded_amount = struct.pack("b", amount)
            value += encoded_amount
        else:
            raise NotImplementedError

        return value
