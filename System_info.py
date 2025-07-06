import configparser
import os
import sys
from datetime import timedelta, datetime

import wmi

from common import get_current_time, log_print

CONFIG_PATH = '_internal/system_info.ini'
MAX_RETRIES = 5

DEFAULT_VALUES = {
    'version': '4.3',
    'error_sound': 'True',
    'net_time': 'False',
    'auto_update': 'True',
    'close_option': 'True',
    'membership': 'Free',
    'motherboardsn': 'LEAF AUTO',
    'membership_class': '0',
    'language': 'cn',
    'serve_lock': 'False',
    'add_timestep': 10,
    'reply_delay': 0
}


def get_motherboard_serial_number():
    log_print('Getting motherboard serial number...')
    c = wmi.WMI()
    for board_id in c.Win32_BaseBoard():
        log_print(f'Motherboard SN found: {board_id.SerialNumber}')
        return str(board_id.SerialNumber).strip()
    log_print('Motherboard SN not found, returning Null')
    return 'Null'


def read_config():
    log_print(f'Reading config from {CONFIG_PATH}')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    log_print(f'Config sections: {config.sections()}')
    return config


def ensure_config_file_exists():
    global config
    log_print('Ensuring config file exists...')
    retries = 0
    while retries < MAX_RETRIES:
        log_print(f'Retry {retries + 1}/{MAX_RETRIES}')
        if not os.path.exists(CONFIG_PATH):
            log_print(f'Config file {CONFIG_PATH} does not exist, creating...')
            create_config_file()
            retries += 1
            continue

        try:
            log_print('Reading existing config file...')
            config = read_config()

            log_print('Checking for missing keys...')
            missing_keys = any(not config.has_option('SystemInfo', key) for key in
                               ['membership', 'expiration_time', 'motherboardsn'])
            if missing_keys:
                log_print('Missing required keys, deleting config file')
                os.remove(CONFIG_PATH)
                retries += 1
                continue

            membership = config.get('SystemInfo', 'membership', fallback='Free')
            expiration_time_str = config.get('SystemInfo', 'expiration_time', fallback=None)
            motherboard_sn = config.get('SystemInfo', 'motherboardsn', fallback=None)
            current_motherboard_sn = get_motherboard_serial_number()

            log_print(f'Membership: {membership}')
            log_print(f'Expiration Time: {expiration_time_str}')
            log_print(f'Config Motherboard SN: {motherboard_sn}')
            log_print(f'Current Motherboard SN: {current_motherboard_sn}')

            if membership != 'Free':
                if expiration_time_str and get_current_time('mix') > datetime.strptime(expiration_time_str,
                                                                                       '%Y-%m-%d %H:%M:%S'):
                    log_print('Membership expired, resetting to Free')
                    write_key_value('membership', 'Free')
                    write_key_value('motherboardsn', 'LEAF AUTO')
                    write_key_value('membership_class', str(int(read_key_value('membership_class')) + 1))
                    continue

                if current_motherboard_sn is None or (motherboard_sn and motherboard_sn != current_motherboard_sn):
                    log_print('Motherboard SN mismatch, deleting config file')
                    os.remove(CONFIG_PATH)
                    retries += 1
                    continue

            log_print('Config file is valid')
            return True

        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            log_print(f'Config parsing error: {str(e)}, deleting config file')
            os.remove(CONFIG_PATH)
            retries += 1

    log_print(f'Max retries ({MAX_RETRIES}) exceeded, exiting')
    if retries >= MAX_RETRIES:
        sys.exit()


def create_config_file():
    log_print('Creating new config file...')
    config = configparser.ConfigParser()
    config['SystemInfo'] = {
        'version': '4.3',
        'error_sound': 'True',
        'net_time': 'False',
        'auto_update': 'True',
        'close_option': 'True',
        'expiration_time': (get_current_time('net') + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
        'membership': 'Free',
        'motherboardsn': 'LEAF AUTO',
        'membership_class': '0',
        'language': 'cn',
        'serve_lock': 'False',
        'add_timestep': '10',
        'reply_delay': 0
    }
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    log_print(f'Writing config to {CONFIG_PATH}')
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    log_print('Config file created successfully')


def read_key_value(key):
    log_print(f'Reading key: {key}')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    try:
        value = config.get('SystemInfo', key, fallback=DEFAULT_VALUES.get(key))
        log_print(f'Key {key} value: {value}')
        return value
    except configparser.Error as e:
        log_print(f'Error reading key {key}: {str(e)}, returning default')
        return DEFAULT_VALUES.get(key)


def write_key_value(key, value):
    log_print(f'Writing key {key} = {value}')
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    if not config.has_section('SystemInfo'):
        log_print('Adding SystemInfo section')
        config.add_section('SystemInfo')
    config.set('SystemInfo', key, value)
    log_print(f'Writing updated config to {CONFIG_PATH}')
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    log_print(f'Key {key} updated successfully')
