import argparse
import sys
import string
import ctypes

horizonal_line = '+----------+------+------+------+------+-------+------+' \
                 '---------+-------+------------+------+------+------' \
                 '+------+' \
                 '------+------+------+-----------------------+'
header = '''+----------+------+------+------+------+-------+------+---------+'\
'-------+------------+------+------+------+------+------+------+------+'\
'-----------------------+
| address  |  0   |  1   |  2   |  3   |  4    |  5   |  6      |   7   |'\
'  8         |  9   |  10  | 11   | 12   | 13   |  14  | 15   '\
'| asccii interpretation |
+==========+======+======+======+======+=======+======+=========+======='\
'+============+======+======+======+======+======+======+======'\
'+=======================+'''

section_types = {
    0x0: 'SHT_NULL',
    0x1: 'SHT_PROGBITS',
    0x2: 'SHT_SYMTAB',
    0x3: 'SHT_STRTAB',
    0x4: 'SHT_RELA',
    0x5: 'SHT_HASH',
    0x6: 'SHT_DYNAMIC',
    0x7: 'SHT_NOTE',
    0x8: 'SHT_NOBITS',
    0x9: 'SHT_REL',
    0xa: 'SHT_SHLIB',
}

section_flags = {
    0x1: 'SHF_WRITE',
    0x2: 'SHF_ALLOC',
    0x4: 'SHF_EXECINSTR',
    0x10: 'SHF_MERGE',
    0x20: 'SHF_STRINGS',
    0x40: 'SHF_INFO_LINK',
    0x80: 'SHF_LINK_ORDER',
    0x100: 'SHF_OS_NONCONFORM',
    0x200: 'SHF_GROUP',
    0x400: 'SHF_TLS',
    0xff00000: 'SHF_MARKOS',
    0xf0000000: 'SHF_MARKPROC'
}


def get_word(data, index, length, signed=False):
    word = data[index]
    if length > 1:
        word += data[index + 1] * 0x100
    if length > 2:
        word += data[index + 2] * 0x10000
    if length > 3:
        word += data[index + 3] * 0x1000000
    if length > 4:
        upper_part = get_word(data, index + 4, length - 4)
        word += upper_part * 0x100000000
    if signed:
        word = ctypes.c_long(word).value
    return word


def get_string(data, index):
    string = ''
    while data[index] != 0:
        string += chr(data[index])
        index += 1

    return string


def parse(input_file_name):
    with open(input_file_name, 'rb') as file:
        data = file.read()
        data = list(data)

    print(f'data length {len(data)}')

    # MAG0 is data[0]
    # MAG1 is data[1]
    # MAG2 is data[2]
    # MAG3 is data[3]
    # CLASS is data[4]
    # DATA is data[5]
    # VERSION is data[6]
    # OSABI is data[7]
    # ABIVERSION is data[8]

    print_elf_header(data)

    shoff = data[0x28] + data[0x29] * 256
    shentsize = data[0x3a] + data[0x3b] * 256
    shnum = data[0x3c] + data[0x3d] * 256
    shstrndx = data[0x3e] + data[0x3f] * 256
    print(f'shoff {shoff}, shentsize {shentsize}, shnum {shnum}, '
          f'shstrndx {shstrndx}')

    string_table_start_index = shoff + (shentsize * shstrndx) + 0x18
    string_table_offset = get_word(data, string_table_start_index, length=8)

    string_table_size_start_index = shoff + (shentsize * shstrndx) + 0x20
    string_table_size = get_word(data, string_table_size_start_index, length=8)

    string_table = data[string_table_offset:
                        string_table_offset + string_table_size]
    for section in range(shnum):
        start_address = shoff + shentsize * section
        section_data = data[start_address:start_address + shentsize]
        print_section(section_data, start_address, shentsize, string_table,
                      data, shoff, shentsize, section)


def print_section(data, address, section_size, string_table, object_file,
                  shoff, shentsize, section_index):
    off = address % 16
    padded = [None] * off + data + [None] * (32 - off)
    lines = int(section_size / 16)

    if off == 0:
        section_first = '|          | sh_name                   | sh_type   ' \
                        '                     |   sh_flags                 ' \
                        '                                 |                 ' \
                        '      |'
        second_line = '|          | sh_addr              ' \
                      '                    ' \
                      '                  | sh_offset               ' \
                      '          ' \
                      '                          |                       |'
        third_line = '|          |sh_size                       ' \
                     '             ' \
                     '                 |   sh_link                       | ' \
                     '  sh_info                 |                       |'
        fourth_line = '|          |sh_addralign                            ' \
                      '                    |   sh_entsize                  ' \
                      '                              |                       |'
        explanation_lines = [
            section_first,
            second_line,
            third_line,
            fourth_line
        ]
    else:
        section_first = '|          |                                     ' \
                        '                       | sh_name                  ' \
                        '       | sh_type                   |              ' \
                        '         |'
        second_line = '|          | sh_flags                               ' \
                      '                    | sh_addr                      ' \
                      '                               |         ' \
                      '              |'
        third_line = '|          | sh_offset                               ' \
                     '                   | sh_size                         ' \
                     '                            |                       |'
        fourth_line = '|          | sh_link                   |   sh_info  ' \
                      '                    | sh_addralign                  ' \
                      '                              |                       |'
        fifth_line = '|          | sh_entsize                              ' \
                     '                   |                                 ' \
                     '                            |                       |'
        explanation_lines = [
            section_first,
            second_line,
            third_line,
            fourth_line,
            fifth_line
        ]

    name_offset = get_word(data, 0, length=4)
    section_offset = get_word(data, 0x18, length=8)
    section_size = get_word(data, 0x20, length=8)
    section_entry_size = get_word(data, 0x38, length=8)
    section_link = get_word(data, 0x28, length=4)
    section_type = get_word(data, 0x4, length=4)
    section_type = section_types[section_type]
    section_flag = get_word(data, 0x8, length=8)

    section_data = object_file[section_offset: section_offset + section_size]

    flags = ''
    for key in section_flags:
        if key & section_flag:
            flags += section_flags[key] + ','

    section_name = get_string(string_table, name_offset)
    print(f'\nthis section index: {section_index} section_name {section_name}'
          f', type {section_type}, flags [{flags}]'
          f', linked to section: {section_link}\n')

    print(header)
    if off != 0:
        lines += 1
    for line in range(lines):
        print(explanation_lines[line])
        print(horizonal_line)
        print_data(padded[line * 16:(line + 1) * 16],
                   address - off + line * 16)
        print(horizonal_line)

    if section_name == '.symtab':
        start_address = shoff + shentsize * section_link
        linked_section_data = object_file[
                              start_address:start_address + shentsize]
        symbol_names_offset = get_word(linked_section_data, 0x18, length=8)
        symbol_names_size = get_word(linked_section_data, 0x20, length=8)
        symbol_names = object_file[symbol_names_offset:
                                   symbol_names_offset + symbol_names_size]
        print_symbol_table(section_data, section_entry_size,
                           section_offset, symbol_names)

    if section_name == '.rela.text':
        print_relocatable_text(section_data, section_entry_size,
                               section_offset, section_type, section_link)


def print_relocatable_text(section_data, entry_size,
                           address, relocatable_type, section_link):
    print_section_data(section_data, address)

    number_of_entries = len(section_data) // entry_size
    print(f'entries for to linked section{section_link}, ')
    for i in range(number_of_entries):
        line = section_data[i * entry_size:(i + 1) * entry_size]
        offset = get_word(line, index=0, length=8)
        info = get_word(line, index=8, length=8)
        entry_symbol = info >> 32
        entry_type = info & 0xffffffff
        if relocatable_type == 'SHT_REL':
            print(f'relocatable entry at offset {offset}, '
                  f'with info {info:#X} (symbol {entry_symbol}, '
                  f'type {entry_type})')
        elif relocatable_type == 'SHT_RELA':
            addend = get_word(line, index=16, length=8, signed=True)
            print(f'relocatable entry at offset {offset}, '
                  f'with info {info:#X} (symbol {entry_symbol}, '
                  f'type {entry_type})'
                  f' and addend {addend:#X}')
        if entry_type == 2:
            pass


def print_section_data(section_data, address):
    off = address % 16
    padding = [None] * off + section_data + [None] * (16 - off)
    num_of_lines = len(padding) // 16
    padded_address = address - off

    print('\n')

    print(header)
    for i in range(num_of_lines):
        line = padding[i * 16:(i + 1) * 16]
        print_data(line, padded_address)
        padded_address += 16
        print(horizonal_line)


def print_symbol_table(table, entry_size, start_address, string_table):
    off = start_address % 16
    number_of_entries = int(len(table) / entry_size)
    alligned = True if off == 0 else False
    start_address -= off

    unalligned_line_0 = '|          |                                     ' \
                        '                       | st_name           ' \
                        '| st_info' \
                        '     | st_other    | st_shndx    |                 ' \
                        '      |'
    unalligned_line_1 = '|          | st_value                              ' \
                        ' ' \
                        '                    | st_size                      ' \
                        '                               |                ' \
                        '       |'

    alligned_line_0 = '|          | st_name     | st_info     | st_other ' \
                      '    | st_shndx        | st_value                   ' \
                      '                                 |                  ' \
                      '     |'
    alligned_line_1 = '|          | st_size                               ' \
                      '                     |                             ' \
                      '                                |                 ' \
                      '      |'

    print('')
    print('')

    for i in range(number_of_entries):
        print(header)
        data = table[i * entry_size: (i + 1) * entry_size]

        name = get_word(data, index=0, length=2)
        name = get_string(string_table, name)
        info = get_word(data, index=2, length=2)
        other = get_word(data, index=4, length=2)
        shndx = get_word(data, index=6, length=2)
        if shndx == 0xfff1:
            shndx = 'SHN_ABS'

        value = get_word(data, 8, length=8)
        size = get_word(data, 16, length=8)

        if alligned:
            data = data + [None] * 8
        else:
            data = [None] * 8 + data
        line_1 = data[:16]
        line_2 = data[16:32]
        if alligned:
            print(alligned_line_0)
        else:
            print(unalligned_line_0)
        print(horizonal_line)
        print_data(line_1, start_address)
        print(horizonal_line)
        if alligned:
            print(alligned_line_1)
        else:
            print(unalligned_line_1)
        print(horizonal_line)
        print_data(line_2, start_address + 16)
        print(horizonal_line)

        print('')
        symbol_entry = f'{name} (index {i}), info: {info}, other: {other},' \
                       f' referenced section: {shndx},' \
                       f'value (offset in its section): {value}, size: {size}'
        print(symbol_entry)
        print('')

        alligned = not alligned
        start_address += 32


def print_elf_header(data):
    elf_header_first_line = '|          | MAG0 | MAG1 | MAG2 | MAG3 | CLASS ' \
                            '| DATA | VERSION | OSABI | ABIVERSION |      | ' \
                            '     |      |      |      |      |      |      ' \
                            '                 |'
    elf_header_second_line = '|          | type        | machine     | ' \
                             'version                        | entry    ' \
                             '                                          ' \
                             '         |                       |'
    elf_header_third_line = '|          | phoff                         ' \
                            '                             | shoff       ' \
                            '                                           ' \
                            '     |                       |'
    elf_header_fourth_line = '|          | flags                     |  ' \
                             'ehsize      | phentsize       | phnum     ' \
                             '        | shentsize   |  shnum      |   ' \
                             'shstrndx  |                       |'
    print(header)
    print(elf_header_first_line)
    print(horizonal_line)
    print_data(data[0:16], 0)
    print(horizonal_line)
    print(elf_header_second_line)
    print(horizonal_line)
    print_data(data[16:32], 16)
    print(horizonal_line)
    print(elf_header_third_line)
    print(horizonal_line)
    print_data(data[32:48], 32)
    print(horizonal_line)
    print(elf_header_fourth_line)
    print(horizonal_line)
    print_data(data[48:64], 48)
    print(horizonal_line)


def print_data(data, address):
    ascii_str = ''
    for char in data:
        if char and char in bytes(string.digits + string.ascii_letters +
                                  string.punctuation, 'ascii'):
            ascii_str += chr(char)
        else:
            ascii_str += '.'
    data = [f'{x:02X}' if x is not None else '  ' for x in data]
    try:
        data_line_format = f'| {address:08X} | {data[0]}   | {data[1]}   ' \
                           f'| {data[2]}   | {data[3]}   | {data[4]}    ' \
                           f'| {data[5]}   | {data[6]}      | {data[7]}    ' \
                           f'| {data[8]}         | {data[9]}   |  {data[10]}' \
                           f'  | {data[11]}   | {data[12]}   | {data[13]}   ' \
                           f'| {data[14]}   | {data[15]}   | ' \
                           f'*{ascii_str}*   ' \
                           f' |'
        print(data_line_format)
    except Exception as e:
        raise e


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-i',
        type=str,
        help='input file name',
        action='store')
    arguments = arg_parser.parse_args(args=sys.argv[1:])

    input_file = arguments.i

    parse(input_file)


if __name__ == '__main__':
    main()
