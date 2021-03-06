#!/usr/bin/python -tt
# by: Anoop Chaurasiya

import argparse
import os
import sys

def get_parser():
    utility_description = 'Execute a shell command recursively in a directory at each level.'
    parser = argparse.ArgumentParser(description=utility_description)

    parser.add_argument('command',
                        help='command to be executed at each level')

    parser.add_argument('directory',
                        help='destination directory')

    parser.add_argument('--include_hidden', action='store_true',
                        help='includes hidden directories (Excludes by Default)')

    parser.add_argument('--filter_target',
                        help='only include directories which have a specified file/directory in it')

    parser.add_argument('--dry_run', action='store_true',
                        help='prints out what is it going to do, doesn\'t do anything')

    return parser

def should_execute_command_in_Directory(directory, input_settings):
    if input_settings.filter_target:
        return input_settings.filter_target in os.listdir(directory)
    return True

def should_process_file(absolute_filepath, base_filename, input_settings):
    # do not follow symlinks
    if os.path.islink(absolute_filepath):
        return False

    if os.path.isdir(absolute_filepath):
        #check for hidden files
        if base_filename.startswith('.'):
            return input_settings.include_hidden
        return True

    return False

def execute_command_in_directory(directory, input_settings):
    command_list = []
    switch_to_directory_command = 'cd "{}"'.format(directory)
    command_list.append(switch_to_directory_command)
    command_list.append(input_settings.command)

    final_execution_command = ';'.join(command_list)
    print '\n\n' + "-" * 80 + '\nWill Execute command: ' + final_execution_command
    if input_settings.dry_run:
        print '[DRY_RUN (Not Executing))]'
    else:
        os.system(final_execution_command)

def process_directory(directory, input_settings):
    if should_execute_command_in_Directory(directory, input_settings):
        execute_command_in_directory(directory, input_settings)

    for filename in os.listdir(directory):
        absolute_filename = os.path.join(directory, filename)
        if should_process_file(absolute_filename, filename, input_settings):
            process_directory(absolute_filename, input_settings)

def solve(input_settings):
    destination_directory = input_settings.directory
    if os.path.isdir(destination_directory):
        destination_directory = os.path.abspath(destination_directory)
        process_directory(destination_directory, input_settings)
    else:
        print 'ERROR: destination \'{}\' is not an existing directory.'.format(destination_directory)
        sys.exit(1)
    return

def main():
    parser = get_parser()
    input_settings = parser.parse_args()
    print 'Executing with arguments:{}'.format(input_settings)
    solve(input_settings)

if __name__ == '__main__':
    main()
