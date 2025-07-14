# Apple Siri Voice Navigation
# The GNU General Public License v3.0 (GPL-3.0)
# Copyright (c) 2025 Jonathan Chiu

import os
import shutil
from configparser import ConfigParser
import sys
import json
import re
import zipfile

script_dir = 'scripts'
voice_dir = 'navigation/build'
docs_dir = 'docs/mod'
build_dir = 'build'
temp_dir = f'{build_dir}/temp'
config = None
use_existing_temp = None
keep_temp = None

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
        'versions_sii': ['package_name'],
        'manifest_sii': ['package_version', 'display_name', 'category', 'icon', 'description_file'],
        'build': ['build_mode', 'version', 'skip_voices'],
        'debug': ['keep_temp', 'use_existing_temp']
    }
    for section, options in config_map.items():
        if not config.has_section(section):
            print(f'Section [{section}] not found in the config file.')
            sys.exit(1)
        for option in options:
            if not config.has_option(section, option):
                print(f'Option "{option}" not found in section [{section}] in the config file.')
                sys.exit(1)

    # Convert config to dictionary
    config = {section: dict(config[section]) for section in config.sections()}

    # Convert skip_voices string to list
    config['build']['skip_voices'] = re.findall(r'\w+', config['build']['skip_voices'])

    # Check if temp directory exists when debug.use_existing_temp is not '0'
    if config['debug']['use_existing_temp'] != '0':
        if not os.path.exists(temp_dir):
            print(f'Temp directory not found. use_existing_temp is disabled.')
            config['debug']['use_existing_temp'] = '0'

    print(f'Config: {json.dumps(config, ensure_ascii=False)}')

    return config

# Initialize directory
def initialize_directory():
    if use_existing_temp == '0':
        print('Initializing directory...')
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir)
    else:
        print('Initializing directory... (use_existing_temp is enabled)')
        for file in os.listdir(build_dir):
            file_path = os.path.join(build_dir, file)
            if file != 'temp' and os.path.isdir(file_path):
                shutil.rmtree(file_path)
            elif os.path.isfile(file_path):
                os.remove(file_path)

# Prepare temporary files
def copy_to_temp():
    if use_existing_temp != '0':
        print('Skipped preparing temporary files.')
        return

    print('Preparing temporary files...')

    # Create temp directory
    os.makedirs(temp_dir)

    # Create manifest.sii file
    manifest_sii = f'''SiiNunit {{
    mod_package : .package_name {{
        package_version: "{config['manifest_sii']['package_version']}"
        display_name: "{config['manifest_sii']['display_name']}"
        author: "Jonathan Chiu"
        category[]: "{config['manifest_sii']['category']}"
        icon: "{config['manifest_sii']['icon']}"
        description_file: "{config['manifest_sii']['description_file']}"
    }}
}}
'''
    with open(f'{temp_dir}/manifest.sii', 'w') as file:
        file.write(manifest_sii)
    print('Created manifest.sii.')

    # Copy icon
    shutil.copy(f'{docs_dir}/images/{config['manifest_sii']['icon']}', f'{temp_dir}')
    print(f'Copied icon: {config['manifest_sii']['icon']}.')

    # Copy description files
    docs_descriptions_dir = f'{docs_dir}/descriptions'
    description_file_split = config['manifest_sii']['description_file'].split('.')
    for file_name in os.listdir(docs_descriptions_dir):
        if re.match(rf'^{description_file_split[0]}(\.[a-z]{{2}}_[a-z]{{2}})?\.{description_file_split[1]}$', file_name):
            shutil.copy(f'{docs_descriptions_dir}/{file_name}', f'{temp_dir}')
            print(f'Copied description file: {file_name}.')

    # Copy voices
    print('Copying voices...')
    build_voices_dir = f'{temp_dir}/sound/navigation'
    os.makedirs(build_voices_dir)

    copied_count = 0
    skipped_count = 0
    skipped_list = []
    for dirpath, dirnames, filenames in os.walk(voice_dir):
        dir_name = os.path.basename(dirpath)

        # Remove .DS_Store from filenames if present
        if '.DS_Store' in filenames:
            filenames.remove('.DS_Store')

        if dir_name in config['build']['skip_voices']:
            print(f'Skipped voice: {dir_name}. In skip_voices list. May be deprecated.')
            skipped_count += 1
            skipped_list.append(dir_name)
        elif len(filenames) == 3:
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
            print(f'Skipped voice: {dir_name}. Contains {len(filenames)} files, expected 3 files: {filenames}')
            skipped_count += 1
            skipped_list.append(dir_name)

    print(f'Copied {copied_count} voices, skipped {skipped_count} voices: {skipped_list}')

# Build standard mod
def build_standard():
    print('Building standard mod...')

    # Create standard directory
    build_standard = f'{build_dir}/standard'
    os.makedirs(build_standard)

    # Create manifest.sii file
#     manifest_sii = f'''SiiNunit {{
#     mod_package : .package_name {{
#         package_version: "{config['manifest_sii']['package_version']}"
#         display_name: "{config['manifest_sii']['display_name']}"
#         author: "Jonathan Chiu"
#         category[]: "{config['manifest_sii']['category']}"
#         icon: "{config['manifest_sii']['icon']}"
#         description_file: "{config['manifest_sii']['description_file']}"
#     }}
# }}
#     '''

    # Create zip file
    zip_name = f'{config['manifest_sii']['display_name']}_{config['build']['version']}.zip'.lower().replace(" ", "-")
    zip_path = f'{build_standard}/{zip_name}'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for dirpath, dirnames, filenames in os.walk(temp_dir):
            for file in filenames:
                temp_file_path = os.path.join(dirpath, file)
                zip_file.write(temp_file_path, os.path.relpath(temp_file_path, temp_dir))
        # zip_file.writestr('manifest_sii', manifest_sii)
        # print('Created manifest.sii.')
    print(f'Created zip file: {zip_name}')

    return zip_name, zip_path

# Build Workshop mod
def build_workshop():
    print('Building Workshop mod...')

    # Create build directory
    build_workshop_dir = f'{build_dir}/workshop'
    os.makedirs(build_workshop_dir)

    # Create versions.sii file
    package_name = config['versions_sii']['package_name']
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

    if keep_temp == '0':
        print('Moving files from temp to workshop...')
        for dirpath, dirnames, filenames in os.walk(temp_dir):
            for file in filenames:
                temp_file_path = os.path.join(dirpath, file)
                build_package_file_path = os.path.join(build_package_dir, os.path.relpath(temp_file_path, temp_dir))
                os.makedirs(os.path.dirname(build_package_file_path), exist_ok=True)
                shutil.move(temp_file_path, build_package_file_path)
    else:
        print('Copying files from temp to workshop... (keep_temp is enabled)')
        for dirpath, dirnames, filenames in os.walk(temp_dir):
            for file in filenames:
                src_path = os.path.join(dirpath, file)
                dest_path = os.path.join(build_package_dir, os.path.relpath(src_path, temp_dir))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(src_path, dest_path)

    return build_workshop_dir

def clean_temp():
    if keep_temp == '0':
        shutil.rmtree(temp_dir)
        print('Cleaning temp directory...')
    else:
        print(f'Skipped cleaning temp directory.')

# Build mod
def build_mod():
    copy_to_temp()

    standard_name = None
    standard_path = None
    workshop_path = None
    if 's' in config['build']['build_mode']:
        print('\n')
        standard_name, standard_path = build_standard()
    if 'w' in config['build']['build_mode']:
        print('\n')
        workshop_path = build_workshop()

    print('\n')

    clean_temp()

    print('\n')

    if workshop_path:
        print(f'Workshop mod built at: {workshop_path}')
    if standard_name:
        usage = f'''0. Move {standard_name} to the mod folder
    - Windows
        - ETS2: %UserProfile%\Documents\Euro Truck Simulator 2\mod
        - ATS: %UserProfile%\Documents\American Truck Simulator\mod
    - macOS (Press Shift-Command-G to open a Go to Folder window)
        - ETS2: ~/Library/Application Support/Euro Truck Simulator 2/mod
        - ATS: ~/Library/Application Support/American Truck Simulator/mod
    - Linux
        - ETS2: ~/.local/share/Euro Truck Simulator 2/mod
        - ATS: ~/.local/share/American Truck Simulator/mod
1. Click Mods on the title screen to open the mod manager.
2. Double-click Apple Siri Voice Navigation to activate this mod.
3. Open Options.
4. Navigate to Audio > Voice Navigation > Language and voice and select a voice you like.'''
        print(f'Standard mod built at: {standard_path}\n\n{usage}')

def main():
    copyright = '''Apple Siri Voice Navigation
The GNU General Public License v3.0 (GPL-3.0)
Copyright (c) 2025 Jonathan Chiu'''
    print(copyright)

    print('\n')

    global config, use_existing_temp, keep_temp
    config = fetch_config()
    use_existing_temp = config['debug']['use_existing_temp']
    keep_temp = config['debug']['keep_temp']

    print('\n')

    initialize_directory()

    print('\n')

    build_mod()

    print('\nBuild completed!')

if __name__  == '__main__':
    main()
