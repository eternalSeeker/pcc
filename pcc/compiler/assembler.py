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
            bytearray: the machine code
        """
        raise NotImplementedError

    def pop_from_stack(self, register):
        """Pop a register from stack.

        Args:
            register (ProcessorRegister): the register to push on stack

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def copy_from_reg_to_reg(self, source, destination):
        """Copy the value from one register to another one.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def copy_value_to_reg(self, value, destination):
        """Copy the value from one register to another one.

        Args:
            value (int): the value to copy
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def return_to_caller(self):
        """Return to the caller routine.

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def nop(self):
        """No operation.

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def push_value_to_stack(self, value, stack_offset):
        """Pushes a value on stack
        Attributes:
            value (bytearray): the value to push on stack
            stack_offset (int): the offset from the stack pointer
        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def copy_stack_to_reg(self, stack_offset, reg):
        """Copy the contents of the stack to the register

        Args:
            stack_offset (int): the stack offset
            reg (ProcessorRegister): the register to copy to
        """
        raise NotImplementedError

    def copy_reg_to_stack(self, stack_offset, reg):
        """Copy the contents of the register to the stack

        Args:
            stack_offset (int): the stack offset
            reg (ProcessorRegister): the register to copy
        """
        raise NotImplementedError

    def add(self, source, destination):
        """Add the value of the source to the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def sub(self, source, destination):
        """Subtract the value of the source from the destination.

        Args:
            source (ProcessorRegister): the source register
            destination (ProcessorRegister): the destination register

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def div(self, source, destination):
        """Divide the value of the source by the destination.

        Args:
            source (ProcessorRegister): the dividend register
            destination (ProcessorRegister): the divider register

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError

    def shift(self, register, mode, amount):
        """Shift the register.

        Args:
            register (ProcessorRegister): the register to shift
            mode (ShiftMode): the mode to shift
            amount (int): the shift amount

        Returns:
            bytearray: the machine code
        """
        raise NotImplementedError
