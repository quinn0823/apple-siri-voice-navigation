# Apple Siri Voice Navigation
# The MIT License (MIT)
# Copyright (c) 2025 Jonathan Chiu

# Under Development...

import os
import shutil
from configparser import ConfigParser
import sys
import json
import re

script_dir = 'scripts'
voice_dir = 'navigation/build'
docs_dir = 'docs/mod'
build_dir = 'build'
config = {}

# Fetch config
def fetch_config():
    print('Fetching config...')

    config = ConfigParser()

    # Check if the config file exists
    if os.path.exists(f'{script_dir}/config.ini'):
        config.read(f'{script_dir}/config.ini')
    elif os.path.exists(f'{script_dir}/config_default.ini'):
        print('config.ini not found, using config_default.ini instead.')
        config.read(f'{script_dir}/config_default.ini')
    else:
        print('config file not found.')
        sys.exit(1)

    # Check if the required sections and options exist
    config_map = {
        'versions.sii': ['package_name'],
        'manifest.sii': ['package_version', 'display_name', 'author', 'category', 'icon', 'description_file'],
    }
    for section, options in config_map.items():
        if not config.has_section(section):
            print(f'Section [{section}] not found in the config file.')
            sys.exit(1)
        for option in options:
            if not config.has_option(section, option):
                print(f'Option "{option}" not found in the section [{section}] in the config file.')
                sys.exit(1)

    print(f'Config: {json.dumps({section: dict(config[section]) for section in config.sections()}, ensure_ascii=False)}')

    return config

# Build Workshop version
def build_workshop():
    print('Building Workshop version...')

    # Create build directory
    build_workshop_dir = f'{build_dir}/workshop'
    os.makedirs(build_workshop_dir)

    # Create versions.sii file
    package_name = config['versions.sii']['package_name']
    versions_sii = f'''SiiNunit {{
    package_version_info : .{package_name} {{
        package_name: "{package_name}"
    }}
}}
'''
    with open(f'{build_workshop_dir}/versions.sii', 'w') as file:
        file.write(versions_sii)
    print('Created versions.sii.')

    # Create {package_name} directory
    build_package_dir = f'{build_workshop_dir}/{package_name}'
    os.makedirs(build_package_dir)

    # Create manifest.sii file
    manifest_sii = f'''SiiNunit {{
    mod_package : .package_name {{
        package_version: {config['manifest.sii']['package_version']}
        display_name: "{config['manifest.sii']['display_name']}"
        author: "{config['manifest.sii']['author']}"
        category[]: "{config['manifest.sii']['category']}"
        icon: "{config['manifest.sii']['icon']}"
        description_file: "{config['manifest.sii']['description_file']}"
    }}
}}
'''
    with open(f'{build_package_dir}/manifest.sii', 'w') as file:
        file.write(manifest_sii)
    print('Created manifest.sii.')

    # Copy icon
    shutil.copy(f'{docs_dir}/images/{config["manifest.sii"]["icon"]}', f'{build_package_dir}')
    print(f'Copied icon: {config["manifest.sii"]["icon"]}.')

    # Copy description files
    docs_descriptions_dir = f'{docs_dir}/descriptions'
    description_file_split = config["manifest.sii"]["description_file"].split('.')
    for file_name in os.listdir(docs_descriptions_dir):
        if re.match(rf'^{description_file_split[0]}(\.[a-z]{{2}}_[a-z]{{2}})?\.{description_file_split[1]}$', file_name):
            shutil.copy(f'{docs_descriptions_dir}/{file_name}', f'{build_package_dir}')
            print(f'Copied description file: {file_name}.')

    # Copy voices
    print('Copying voices...')
    build_voices_dir = f'{build_package_dir}/sound/navigation'
    os.makedirs(build_voices_dir)

    copied_count = 0
    skipped_count = 0
    skipped_list = []
    for dirpath, dirnames, filenames in os.walk(voice_dir):
        dir_name = os.path.basename(dirpath)
        if len(filenames) == 3:
            expected_file_map = [f'{dir_name}.bank', f'{dir_name}.bank.guids', f'{dir_name}.sii']
            illegal_files = []
            for file in filenames:
                if file not in expected_file_map:
                    illegal_files.append(file)

            if illegal_files:
                print(f'Skipped voice: {dir_name}. Has illegal files: {illegal_files}')
                skipped_count += 1
                skipped_list.append(dir_name)
            else:
                for file in filenames:
                    shutil.copy(f'{dirpath}/{file}', build_voices_dir)
                copied_count += 1
        elif len(filenames) != 0:
            print(f'Skipped voice: {dir_name}. Contains {len(filenames)} files, expected 3 files')
            skipped_count += 1
            skipped_list.append(dir_name)
    print(f'Copied {copied_count} voices, skipped {skipped_count} voices: {skipped_list}')

def main():
    global config
    config = fetch_config()

    # Initialize the build directory
    print('Initializing the build directory...')
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Create build directory
    os.makedirs(build_dir)

    build_workshop()

if __name__  == '__main__':
    main()
