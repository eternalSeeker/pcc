# -*- coding: utf-8 -*-
import enum
import os

# https://www.uclibc.org/docs/elf-64-gen.pdf
# https://0x00sec.org/t/dissecting-and-exploiting-elf-files/7267

# sizes and alignments for the elf words
import pcc
from pcc.AST.compiled_object import CompiledObjectType

Elf64_Addr = 8
Elf64_Off = 8
Elf64_Half = 2
Elf64_Word = 4
Elf64_Sword = 4
Elf64_Xword = 8
Elf64_Sxword = 8


def number_to_bytearray(number, size):
    """Convert a number to a bytearray

    Args:
        number (int): the number to convert
        size (int): the size of the bytearray of the result

    Returns:
        bytearray: the resulting byte array
    """
    array = bytearray()
    for i in range(size):
        num = number >> (i * 8)
        num = num & 0xff
        array.append(num)
    return array


class ObjectFileType(enum.Enum):
    NO_FILE_TYPE = 0
    RELOCATABLE_OBJECT_FILE = 1
    EXECUTABLE_FILE = 2


class ElfHeader:
    # size of the header
    EI_NIDEN = 16
    # header indexes
    EI_MAG0 = 0
    EI_MAG1 = 1
    EI_MAG2 = 2
    EI_MAG3 = 3

    EI_CLASS = 4
    EI_DATA = 5
    EI_VERSION = 6
    EI_OSABI = 7
    EI_ABIVERSION = 8

    # the class options
    ELFCLASSNONE = 0
    ELFCLASS32 = 1
    ELFCLASS64 = 2

    # data format types
    ELFDATANONE = 0
    ELFDATA2LSB = 1
    ELFDATA2MSB = 2

    # version options
    EV_NONE = 0
    EV_CURRENT = 1

    # osabi version options
    ELFOSABI_SYSV = 0
    ELFOSABI_HPUX = 1
    ELFOSABI_STANDALONE = 256

    # Object File Types
    ET_NONE = [0, 0]
    ET_REL = [1, 0]
    ET_EXEC = [2, 0]
    ET_DYN = [3, 0]
    ET_CORE = [4, 0]
    ET_LOOS = [0xfe, 0]
    ET_HIOS = [0xfe, 0xff]
    ET_LOPROC = [0xff, 0]
    ET_HIPROC = [0xff, 0xff]

    def __init__(self, obj_type):
        """Create an object file object

        Args:
            obj_type (ObjectFileType): the type
        """
        # e_ident: identify the file as an ELF object file, and provide
        # information about the data representation
        # of the object file structures.
        self.e_ident = [0] * ElfHeader.EI_NIDEN

        # e_type: identifies the object file type.
        self.e_type = [0] * Elf64_Half
        self.obj_type = obj_type
        # e_machine: identifies the target architecture.
        self.e_machine = [0] * Elf64_Half

        # E-version: identifies the version of the object file format.
        # Currently, this field has the value EV_CURRENT ,
        # which is defined with the value 1
        self.e_version = [0] * Elf64_Word
        self.e_version[0] = 1

        # e_entry contains the virtual address of the program entry point.
        # If there is no entry point, this field contains zero.
        self.e_entry = [0] * Elf64_Addr
        # e_phoff: contains the file offset, in bytes,
        # of the program header table.
        self.e_phoff = [0] * Elf64_Off
        # e_shoff: contains the file offset, in bytes,
        # of the section header table.
        self.e_shoff = [0] * Elf64_Off
        # e_flags: contains processor-specific flags.
        self.e_flags = [0] * Elf64_Word
        # e_ehsize: contains the size, in bytes, of the ELF header.
        self.e_ehsize = [0] * Elf64_Half
        # e_phentsize: contains the size, in bytes,
        # of a program header table entry.
        self.e_phentsize = [0] * Elf64_Half
        # e_phnum :contains the number of entries in the program header table.
        self.e_phnum = [0] * Elf64_Half
        # e_shentsize: contains the size, in bytes,
        # of a section header table entry.
        self.e_shentsize = [0] * Elf64_Half
        # e_shnum: contains the number of entries in the section header table.
        self.e_shnum = [0] * Elf64_Half
        # e_shstrndx: contains the section header table index of the section
        # containing the section name string table.
        # If there is no section name string table,
        # this field has the value SHN_UNDEF .
        self.e_shstrndx = [0] * Elf64_Half

        self.elf_header_size = 0x40

    def set_section_offset(self, offset):
        """Specify the offset of the section table in bytes.

        Args:
            offset (int): the offset from the start of the file in bytes
        """
        self.e_shoff[0] = offset & 0xff
        self.e_shoff[1] = (offset >> 8) & 0xff
        self.e_shoff[2] = (offset >> 16) & 0xff
        self.e_shoff[3] = (offset >> 24) & 0xff

    def set_section_string_index(self, str_sections_index):
        self.e_shstrndx = [str_sections_index & 0xff,
                           (str_sections_index >> 8) & 0xff]

    def set_number_of_sections(self, num_sections):
        """Specify the number of sections

        Args:
            num_sections (int): the number of sections
        """
        self.e_shnum = [num_sections & 0xff,
                        (num_sections >> 8) & 0xff]

    def _fill_in_shentsize(self):
        section_entry_size = 0x40
        self.e_shentsize = [section_entry_size & 0xff,
                            (section_entry_size >> 8) & 0xff]

    def _fill_in_ehsize(self):
        self.e_ehsize = [0x40, 0]  # default size

    def _fill_in_machine(self):
        # http://www.sco.com/developers/gabi/latest/ch4.eheader.html
        em_x86_64 = [62, 0]  # AMD x86-64  architecture
        self.e_machine = em_x86_64

    def _fill_in_type(self, obj_type):
        if obj_type == ObjectFileType.RELOCATABLE_OBJECT_FILE:
            self.e_type = ElfHeader.ET_REL
        elif obj_type == ObjectFileType.EXECUTABLE_FILE:
            self.e_type = ElfHeader.ET_EXEC

    def _fill_in_ident(self):
        self.e_ident[ElfHeader.EI_MAG0] = 0x7f
        self.e_ident[ElfHeader.EI_MAG1] = ord('E')
        self.e_ident[ElfHeader.EI_MAG2] = ord('L')
        self.e_ident[ElfHeader.EI_MAG3] = ord('F')
        self.e_ident[ElfHeader.EI_CLASS] = ElfHeader.ELFCLASS64
        self.e_ident[ElfHeader.EI_DATA] = ElfHeader.ELFDATA2LSB
        self.e_ident[ElfHeader.EI_VERSION] = ElfHeader.EV_CURRENT
        self.e_ident[ElfHeader.EI_OSABI] = ElfHeader.ELFOSABI_SYSV
        self.e_ident[ElfHeader.EI_ABIVERSION] = 0

    def to_binary_array(self):
        """Get the binary representation of the elf header

        Returns:
            bytearray: the binary representation
        """
        self._fill_in_ident()
        self._fill_in_type(self.obj_type)
        self._fill_in_machine()
        self._fill_in_ehsize()
        self._fill_in_shentsize()
        byte_array = bytearray()
        byte_array.extend(self.e_ident)
        byte_array.extend(self.e_type)
        byte_array.extend(self.e_machine)
        byte_array.extend(self.e_version)
        byte_array.extend(self.e_entry)
        byte_array.extend(self.e_phoff)
        byte_array.extend(self.e_shoff)
        byte_array.extend(self.e_flags)
        byte_array.extend(self.e_ehsize)
        byte_array.extend(self.e_phentsize)
        byte_array.extend(self.e_phnum)
        byte_array.extend(self.e_shentsize)
        byte_array.extend(self.e_shnum)
        byte_array.extend(self.e_shstrndx)
        return byte_array


class SectionType(enum.IntEnum):
    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    SHT_SHLIB = 10
    SHT_DYNSYM = 11
    SHT_LOPROC = 0x70000000
    SHT_HIPROC = 0x7fffffff
    SHT_LOUSER = 0x80000000
    SHT_HIUSER = 0xffffffff


class SectionFlags(enum.IntEnum):
    SHF_NONE = 0x0
    SHF_WRITE = 0x1
    SHF_ALLOC = 0x2
    SHF_EXECINSTR = 0x4
    SHF_MERGE = 0x10
    SHF_STRINGS = 0x20
    SHF_INFO_LINK = 0x40
    SHF_LINK_ORDER = 0x80
    SHF_OS_NONCONFORMING = 0x100
    SHF_GROUP = 0x200
    SHF_TLS = 0x400
    SHF_MASKOS = 0x0ff00000
    SHF_AMD64_LARGE = 0x10000000
    SHF_ORDERED = 0x40000000
    SHF_EXCLUDE = 0x80000000
    SHF_MASKPROC = 0xf0000000


class Section:
    def __init__(self, name, name_offset, section_type, flags):
        """Create a section for an object file.

        Args:
            name (str): the canonical name of this section
            name_offset (int): the index of the name of the section
                in the section string table
            section_type (SectionType): the type of the section
            flags (list[SectionFlags]): the list off all flags of the section
        """
        self.name = name
        self.name_offset = name_offset
        self.section_type = section_type
        self.flags = flags
        self.address = 0
        self.offset = 0
        self.size = 0
        self.link = 0
        self.info = 0
        self.alignment = 1
        self.entry_size = 0

        self.section_content = bytearray()

    def set_offset(self, offset):
        """Specify the section offset from the start of the file.

        Args:
            offset (int): the offset in bytes from the start of the file
        """
        self.offset = offset

    def clear(self):
        """Clear the section contents.

        """
        self.section_type = 0
        self.name_offset = 0
        self.flags = [SectionFlags.SHF_NONE]
        self.address = 0
        self.offset = 0
        self.size = 0
        self.link = 0
        self.info = 0
        self.alignment = 0
        self.entry_size = 0

    def to_binary_array(self):
        """Get the binary representation of the section

        Returns:
            bytearray: the binary representation
        """
        byte_array = bytearray()
        flags = 0
        for flag in self.flags:
            flags += flag
        if self.section_content:
            self.size = len(self.section_content)
        byte_array += number_to_bytearray(self.name_offset, 4)
        byte_array += number_to_bytearray(self.section_type, 4)
        byte_array += number_to_bytearray(flags, 8)
        byte_array += number_to_bytearray(self.address, 8)
        byte_array += number_to_bytearray(self.offset, 8)
        byte_array += number_to_bytearray(self.size, 8)
        byte_array += number_to_bytearray(self.link, 4)
        byte_array += number_to_bytearray(self.info, 4)
        byte_array += number_to_bytearray(self.alignment, 8)
        byte_array += number_to_bytearray(self.entry_size, 8)
        return byte_array

    def fill(self, data):
        """Fill the section with the data.

        Args:
            data (bytearray): the data for the section
        """
        self.section_content = data
        self.size = len(self.section_content)


class SymbolType(enum.IntEnum):
    STT_NOTYPE = 0
    STT_OBJECT = 1
    STT_FUNC = 2
    STT_SECTION = 3
    STT_FILE = 4
    STT_COMMON = 5
    STT_LOOS = 10
    STT_HIOS = 12
    STT_LOPROC = 13
    STT_SPARC_REGISTER = 13
    STT_HIPROC = 15


class SymbolBinding(enum.IntEnum):
    STB_LOCAL = 0
    STB_GLOBAL = 1
    STB_WEAK = 2
    STB_LOOS = 10
    STB_HIOS = 12
    STB_LOPROC = 13
    STB_HIPROC = 15


class SpecialSymbolIndex(enum.IntEnum):
    SHN_UNDEF = 0
    SHN_LORESERVE = 0xff00
    SHN_LOPROC = 0xff00
    SHN_HIPROC = 0xff1f
    SHN_LOOS = 0xff20
    SHN_HIOS = 0xff3f
    SHN_ABS = 0xfff1
    SHN_COMMON = 0xfff2
    SHN_XINDEX = 0xffff
    SHN_HIRESERVE = 0xffff


class Symbol:
    def __init__(self, name, value, size, symbol_type, relocation_objects):
        """Create a compiled symbol object

        Args:
            name (str): the name of the symbol
            value (bytearray): the value of the symbol
            size (int): the size of the symbol, if value is empty,
                it represents the size of the actual symbol
            symbol_type (SymbolType): the type
            relocation_objects(List[RelocationObject]): the relocation objects
                if applicable
        """
        self.name = name
        self.value = value
        self.size = size
        self.type = symbol_type
        self.relocation_objects = relocation_objects


class RelocationTableEntry:
    def __init__(self, offset, info, addend):
        """Create a relocation table entry

        Args:
            offset (int): offset into the section
            info (int): the encoded info
            addend (int): the addend
        """
        self.offset = offset
        self.addend = addend
        self.info = info

    def to_binary_array(self):
        """Get the byte array representation of the relocation table entry

        Returns:
            bytearray: the binary representation
        """
        byte_array = bytearray()
        byte_array += number_to_bytearray(self.offset, 8)
        byte_array += number_to_bytearray(self.info, 8)
        byte_array += number_to_bytearray(self.addend, 8)

        return byte_array


class SymbolTableEntry:
    def __init__(self, name_index, symbol_type, binding,
                 section_index, symbol_size, offset_in_section=0):
        """Create a symbol table entry

        Args:
            name_index (int): the start index of the name string
            symbol_type (SymbolType): the type of the symbol
            binding (SymbolBinding): the binding of the symbol
            section_index (int): The index of the section of this symbol
            symbol_size (int): the size of the symbol
            offset_in_section (int, optional): The offset in the section
        """
        self.st_name = name_index
        self.st_info = (symbol_type & 0xf) + (binding << 4)
        self.st_other = 0
        self.st_shndx = section_index
        self.st_value = offset_in_section
        self.st_size = symbol_size

    def update_info(self, symbol_type, binding):
        """Update the info field

        Args:
            symbol_type (SymbolType): the type
            binding (SymbolBinding): the binding
        """
        self.st_info = symbol_type + (binding << 4)

    def to_binary_array(self):
        """Get the byte array representation of the symbol table entry

        Returns:
            bytearray: the binary representation
        """
        byte_array = bytearray()
        byte_array += number_to_bytearray(self.st_name, 4)
        byte_array += number_to_bytearray(self.st_info, 1)
        byte_array += number_to_bytearray(self.st_other, 1)
        byte_array += number_to_bytearray(self.st_shndx, 2)
        byte_array += number_to_bytearray(self.st_value, 8)
        byte_array += number_to_bytearray(self.st_size, 8)

        return byte_array

    def __str__(self):
        string = 'SymbolTableEntry '
        string += f'name offset in string table {self.st_name} '
        string += f'info {self.st_info} '
        string += f'other {self.st_other} '
        string += f'section header index {self.st_shndx} '
        string += f'value {self.st_value} '
        string += f'size {self.st_size} '

        return string


def add_to_table(name, table):
    """Add a string to the table

    Args:
        name (str): the same to add to the table
        table (bytearray): the table to add to

    Returns:
        int: the start index of the name in the table
    """
    start_point = len(table)
    for character in name:
        table.append(ord(character))
    # closing \0' character
    table.append(0)
    return start_point


class ObjectFile:

    def __init__(self, input_file_name):
        """Create an object file.

        Args:
            input_file_name (str): the name of the source file corresponding
                                   to this object file
        """
        self.input_file_name = input_file_name
        self.section_string_table = bytearray()
        self.string_table = bytearray()
        self.dot_data_content = bytearray()
        self.text_rela_table = []

        none = add_to_table('', self.string_table)
        # only add the base name of the file to the object file
        name = os.path.basename(self.input_file_name)
        file_name = add_to_table(name, self.string_table)
        self.symbol_table = [
            SymbolTableEntry(none, SymbolType.STT_NOTYPE,
                             SymbolBinding.STB_LOCAL, section_index=0,
                             symbol_size=0),
            SymbolTableEntry(file_name, SymbolType.STT_FILE,
                             SymbolBinding.STB_LOCAL,
                             SpecialSymbolIndex.SHN_ABS, 0),
            SymbolTableEntry(none, SymbolType.STT_SECTION,
                             SymbolBinding.STB_LOCAL, section_index=1,
                             symbol_size=0),
            SymbolTableEntry(none, SymbolType.STT_SECTION,
                             SymbolBinding.STB_LOCAL, section_index=2,
                             symbol_size=0),
            SymbolTableEntry(none, SymbolType.STT_SECTION,
                             SymbolBinding.STB_LOCAL, section_index=3,
                             symbol_size=0),
            SymbolTableEntry(none, SymbolType.STT_SECTION,
                             SymbolBinding.STB_LOCAL, section_index=4,
                             symbol_size=0),
            SymbolTableEntry(none, SymbolType.STT_SECTION,
                             SymbolBinding.STB_LOCAL, section_index=5,
                             symbol_size=0),
            SymbolTableEntry(none, SymbolType.STT_SECTION,
                             SymbolBinding.STB_LOCAL, section_index=6,
                             symbol_size=0),

        ]

        self.elf_header = ElfHeader(ObjectFileType.RELOCATABLE_OBJECT_FILE)
        no_flags = [SectionFlags.SHF_NONE]
        ax_flags = [SectionFlags.SHF_ALLOC, SectionFlags.SHF_EXECINSTR]
        wa_flags = [SectionFlags.SHF_ALLOC, SectionFlags.SHF_WRITE]
        ms_flags = [SectionFlags.SHF_MERGE, SectionFlags.SHF_STRINGS]
        link_flags = [SectionFlags.SHF_INFO_LINK]

        none = add_to_table('', self.section_string_table)
        dot_symtab = add_to_table('.symtab', self.section_string_table)
        dot_strtab = add_to_table('.strtab', self.section_string_table)
        dot_shstrtab = add_to_table('.shstrtab', self.section_string_table)
        dot_text = add_to_table('.text', self.section_string_table)
        dot_data = add_to_table('.data', self.section_string_table)
        dot_bss = add_to_table('.bss', self.section_string_table)
        dot_rela_text = add_to_table('.text.rela', self.section_string_table)
        dot_comment = add_to_table('.comment', self.section_string_table)
        dot_note_gnu_stack = add_to_table('.note.GNU-stack',
                                          self.section_string_table)

        self.sections = [
            # the first section header is all zero
            Section('none', none, SectionType.SHT_NULL, no_flags),
            Section('.text', dot_text, SectionType.SHT_PROGBITS, ax_flags),
            Section('.data', dot_data, SectionType.SHT_PROGBITS, wa_flags),
            Section('.bss', dot_bss, SectionType.SHT_NOBITS, wa_flags),
            Section('.text.rela', dot_rela_text, SectionType.SHT_RELA,
                    link_flags),
            Section('.comment', dot_comment, SectionType.SHT_PROGBITS,
                    ms_flags),
            Section('.note.GNU-stack', dot_note_gnu_stack,
                    SectionType.SHT_PROGBITS, no_flags),
            Section('.symtab', dot_symtab, SectionType.SHT_SYMTAB, no_flags),
            Section('.strtab', dot_strtab, SectionType.SHT_STRTAB, no_flags),
            Section('.shstrtab', dot_shstrtab, SectionType.SHT_STRTAB,
                    no_flags)
        ]
        # first section needs to be all 0's
        self.get_section('none').clear()

        # the symbol table entry size is 0x18
        self.get_section('.symtab').entry_size = 0x18
        # make the link from the symbol table to the string table
        self.get_section('.symtab').link = self.get_section_index('.strtab')
        self.get_section('.symtab').info = self.get_section_index('.strtab')
        # the symbol table needs to be 8 bytes aligned
        self.get_section('.symtab').alignment = 8

        self.get_section('.comment').entry_size = 1

        self.get_section('.text.rela').link = self.get_section_index('.symtab')
        self.get_section('.text.rela').info = self.get_section_index('.text')
        self.get_section('.text.rela').alignment = 8
        # create a dummpy entry to calculate the size of the entry
        dummy_entry = RelocationTableEntry(0, 0, 0)
        self.get_section('.text.rela').entry_size = \
            len(dummy_entry.to_binary_array())

        str_index = self.get_section_index('.shstrtab')
        self.elf_header.set_section_string_index(str_index)

        # add custom information to the comment section
        content = bytearray()
        content.append(0)
        content.extend(map(ord, 'PCC: (Ubuntu 7.3.0-27ubuntu1~18.04) 7.3.0'))
        content.append(0)
        self.get_section('.comment').fill(content)

        self.get_section('.strtab').fill(self.string_table)

        self.program_headers = []

    def add_symbol(self, symbol):
        """Add a compiled symbol to the object file.

        Args:
            symbol (Symbol): the symbol to add
        """
        for sym in self.symbol_table:
            name = self.get_name_at_offset_of_string_table(sym.st_name)
            if name == symbol.name:
                # name = self.symbol_table.index(sym)
                self.update_symbol(sym, symbol)
                return
        else:
            self.add_new_symbol(symbol)

    def handle_symbol(self, symbol):
        size = len(symbol.value)
        original_section_size = 0
        symbol_binding = SymbolBinding.STB_GLOBAL
        symbol_type = SymbolType.STT_OBJECT
        if symbol.type == CompiledObjectType.code:
            if symbol.size > 0:
                section_index = self.get_section_index('.text')
                section_content = self.get_section('.text').section_content
                original_section_size = len(section_content)
                section_content += symbol.value
                symbol_type = SymbolType.STT_FUNC
            else:
                section_index = self.get_section_index('none')
                section_content = self.get_section('none').section_content
                original_section_size = len(section_content)
                symbol_type = SymbolType.STT_NOTYPE
                symbol_binding = SymbolBinding.STB_WEAK

        elif symbol.type == CompiledObjectType.data:
            if size == 0:
                size = symbol.size
                if size != 0:
                    section_index = self.get_section_index('.bss')
                else:
                    # undefined section
                    section_index = 0
                    symbol_binding = SymbolBinding.STB_GLOBAL
                    symbol_type = SymbolType.STT_NOTYPE
            else:
                section_index = self.get_section_index('.data')
                original_section_size = len(self.dot_data_content)
                self.dot_data_content += symbol.value
        elif symbol.type == CompiledObjectType.none_type:
            section_index = 0
            size = symbol.size
        else:
            message = f'Could not identify type of {symbol.name}, ' \
                      f'got {symbol.type}\nIgnoring this symbol'
            pcc.utils.warning.error(self.input_file_name, line_number=-1,
                                    message=message)
            return
        if symbol.relocation_objects:
            self.handle_relocation_objects(original_section_size, symbol)
        return symbol_type, symbol_binding, \
            section_index, size, original_section_size

    def update_symbol(self, original_symbol, updated_symbol):
        """Update the symbol in the symbol table.

        Args:
            original_symbol(SymbolTableEntry): the entry to update
            updated_symbol (Symbol): the updated symbol
        """
        symbol_type, symbol_binding, \
            section_index, size, original_section_size = \
            self.handle_symbol(updated_symbol)
        original_symbol.update_info(symbol_type, symbol_binding)
        original_symbol.st_shndx = section_index
        original_symbol.st_size = size
        original_symbol.st_value = original_section_size

    def add_new_symbol(self, symbol):
        """Add a new symbol.

        Args:
            symbol (Symbol): the symbol to add

        """
        name = add_to_table(symbol.name, self.string_table)
        symbol_type, symbol_binding, \
            section_index, size, original_section_size = \
            self.handle_symbol(symbol)

        entry = SymbolTableEntry(name_index=name,
                                 symbol_type=symbol_type,
                                 binding=symbol_binding,
                                 section_index=section_index,
                                 symbol_size=size,
                                 offset_in_section=original_section_size)
        if symbol.name == 'putchar':
            entry.st_other = 0x0
            entry.st_info = 0x10
        self.symbol_table.append(entry)

    def handle_relocation_objects(self, original_section_size, symbol):
        """Handle the relocation objects

        Args:
            original_section_size (int): the original size of the section
            symbol (Symbol): The symbol that has the objects

        Raises:
            NotImplementedError: for comiled object types not yet supported
        """
        for rela_object in symbol.relocation_objects:
            offset = rela_object.offset
            offset += original_section_size
            # info is the encoding of the type of the relocated object and
            # the index of the symbol in the symbol table, which after
            # addition will be the length before addition
            if rela_object.type == CompiledObjectType.data:
                info = 2
            elif rela_object.type == CompiledObjectType.code:
                info = 4
            else:
                raise NotImplementedError
            index = -1
            for sym in self.symbol_table:
                name = self.get_name_at_offset_of_string_table(sym.st_name)
                if name == rela_object.name:
                    index = self.symbol_table.index(sym)
                    break
            if index == -1:
                message = f'Could not find the referenced symbol ' \
                          f'{sym.st_name}'
                pcc.utils.warning.error(self.input_file_name,
                                        line_number=-1,
                                        message=message)
            info += index << 32
            obj = RelocationTableEntry(offset, info, rela_object.addend)
            self.text_rela_table.append(obj)

    def get_name_at_offset_of_string_table(self, offset):
        name = ''

        working_offset = offset
        while working_offset < len(self.string_table) and \
                self.string_table[working_offset] != 0:
            name += chr(self.string_table[working_offset])
            working_offset += 1

        return name

    def get_section(self, name):
        """Get the section from the name.

        Args:
            name (str): the section name

        Returns:
            Section: the requested section if found, else None
        """
        for section in self.sections:
            if section.name == name:
                return section
        return None

    def get_section_index(self, name):
        """Get the section index from the name.

        Args:
            name (str): the section name

        Returns:
            int: the requested section index if found, else -1
        """
        for i in range(len(self.sections)):
            if self.sections[i].name == name:
                return i
        return -1

    def to_binary_array(self):
        """Get the byte array representation.

        Returns:
            bytearray: the binary representation
        """

        self.get_section('.shstrtab').fill(self.section_string_table)
        self.get_section('.data').fill(self.dot_data_content)

        text_rela_content = bytearray()
        for rela in self.text_rela_table:
            text_rela_content += rela.to_binary_array()
        self.get_section('.text.rela').fill(text_rela_content)

        byte_array = bytearray()
        for i in range(len(self.symbol_table)):
            byte_array += self.symbol_table[i].to_binary_array()

        self.get_section('.symtab').fill(byte_array)

        offset = self.elf_header.elf_header_size
        self.elf_header.set_number_of_sections(len(self.sections))

        section_content = bytearray()
        for section in self.sections:
            if section.alignment:
                padding = offset % section.alignment
                if padding != 0:
                    additional = section.alignment - padding
                    offset += additional
                    for _ in range(additional):
                        section_content.append(0)
            if section.name != 'none':
                section.set_offset(offset)
            offset += len(section.section_content)
            section_content += section.section_content

        # align the section headers on a 8 byte boundary
        padding = offset % 8
        padding = (8 - padding)
        offset += padding
        for _ in range(padding):
            section_content.append(0)
        self.elf_header.set_section_offset(offset)
        byte_array = self.elf_header.to_binary_array()
        byte_array += section_content

        for i in range(len(self.sections)):
            section = self.sections[i]
            tmp = section.to_binary_array()
            byte_array += tmp
        return byte_array
