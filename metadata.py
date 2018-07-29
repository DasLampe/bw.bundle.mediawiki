@metadata_processor
def add_php_fpm_pool(metadata):
    if node.has_bundle('php-fpm'):
        if 'php-fpm' not in metadata:
            metadata['php-fpm'] = {}

        if 'pools' not in metadata['php-fpm']:
            metadata['php-fpm']['pools'] = {}

        metadata['php-fpm']['pools']['mediawiki'] = {
            'disable_functions': True,
            'user': 'mediawiki',
            'group': 'mediawiki',
        }

    return metadata, DONE

@metadata_processor
def add_mediawiki_user(metadata):
    metadata['users']['mediawiki'] = {
        'shell': '/usr/sbin/nologin',
        'ssh_pubkeys': [],
    }

    return metadata, DONE