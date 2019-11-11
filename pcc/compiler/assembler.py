#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum


class ProcessorRegister(enum.Enum):
    frame_pointer = 0
    base_pointer = 1
    accumulator = 2
    single_scalar_0 = 3
    double_scalar_0 = 4
    counter = 5
    single_scalar_1 = 6
    double_scalar_1 = 7
    data = 8


class ShiftMode(enum.Enum):
    right_arithmetic = 0
    left_arithmetic = 1


class Assembler:

    def __init__(self):
        pass

    def push_to_stack(self, register):
        """Push a register on stack.

        Args:
            register (ProcessorRegister): the register to push on stack

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def pop_from_stack(self, register):
        """Pop a register from stack.

        Args:
            register (ProcessorRegister): the register to push on stack

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def copy_from_reg_to_reg(self, source, destination):
        """Copy the value from one register to another one.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def copy_value_to_reg(self, value, destination):
        """Copy the value from one register to another one.

        Args:
            value (int): the value to copy
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def return_to_caller(self):
        """Return to the caller routine.

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def nop(self):
        """No operation.

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def push_value_to_stack(self, value, stack_offset):
        """Pushes a value on stack
        Attributes:
            value (bytearray): the value to push on stack
            stack_offset (int): the offset from the stack pointer
        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def copy_stack_to_reg(self, stack_offset, reg):
        """Copy the contents of the stack to the register

        Args:
            stack_offset (int): the stack offset
            reg (ProcessorRegister): the register to copy to

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def copy_reg_to_stack(self, stack_offset, reg):
        """Copy the contents of the register to the stack

        Args:
            stack_offset (int): the stack offset
            reg (ProcessorRegister): the register to copy

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def add(self, source, destination):
        """Add the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def sub(self, source, destination):
        """Subtract the value of the source from the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def div(self, source, destination):
        """Divide the value of the source by the destination.

        Args:
            source (ProcessorRegister): the dividend register
            destination (ProcessorRegister): the divider register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def mul(self, destination, source):
        """Multiply the value of the source by the destination.

        destination = source * destination
        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the source register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def shift(self, register, mode, amount):
        """Shift the register.

        Args:
            register (ProcessorRegister): the register to shift
            mode (ShiftMode): the mode to shift
            amount (int): the shift amount

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def cmp(self, register_1, register_2):
        """Compare the 2 registers.

        Args:
            register_1 (ProcessorRegister): the first register
            register_2 (ProcessorRegister): the second register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def cmp_against_const(self, register, const):
        """Compare the 2 registers.

        Args:
            register (ProcessorRegister): the register
            const (int): the const value

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """

    def je(self, jump_distance):
        """Jump if the equals flag is set.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def jne(self, jump_distance):
        """Jump if the equals flag is not set.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def jge(self, jump_distance):
        """Jump if the greater or equal flags are set.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def jle(self, jump_distance):
        """Jump if the less or equal flags are set.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def jg(self, jump_distance):
        """Jump if the greater flags are set.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def jl(self, jump_distance):
        """Jump if the less flags are set.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def jmp(self, jump_distance):
        """Jump.

        Args:
            jump_distance (int): the distance to jump in bytes

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def bitwise_and(self, source, destination):
        """Bitwise and the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def bitwise_or(self, source, destination):
        """Bitwise or the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def bitwise_xor(self, source, destination):
        """Bitwise xor the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def bitwise_not(self, destination):
        """Bitwise xor the value of the source to the destination.

        Args:
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def logical_and(self, source, destination):
        """Logical and the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def setnz(self, destination):
        """Set destination if the zero flag is not set.

        Args:
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202
            int: the offset to the displacement

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def mov_dispacement(self, register, displacement):
        """Move from source to destination with sign extend.

        Args:
            register (ProcessorRegister): the destination register
            displacement (int): the displacement offset

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError

    def movzx(self, source, destination):
        """Move from source to destination with sign extend.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code #noqa I202

        Raises:
            NotImplementedError: if not implemented in a subclasss
        """
        raise NotImplementedError
