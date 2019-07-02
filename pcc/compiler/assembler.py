#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum


class ProcessorRegister(enum.Enum):
    frame_pointer = 0
    base_pointer = 1
    accumulator = 2
    single_scalar_0 = 3
    double_scalar_0 = 4


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
