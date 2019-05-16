# Bundlewrap - Mediawiki Bundle

Install MediaWiki (version 1.31.0 tested) to /home/mediawiki/mediawiki/.
- Create User mediawiki
- Install PHP
- Setup Database
- Setup MediaWiki tables

## Dependencies
- MySQL-Bundle (not published yet)
- [apt-Bundle](https://github.com/sHorst/bw.bundle.apt)

## Suggestion
PHP-FPM Bundle (https://github.com/DasLampe/bw.bundle.php-fpm/tree/development)

## Config
'mediawiki': {
    'version': '1.31.0',
    'name': 'My Wiki',
    'admin_user': 'root',
    'admin_pass': "change-and-encrypt-me",
    'language': 'en',
    'server': '',
    'db': {
        'host': 'localhost',
        'db': 'wiki',
        'user': 'wiki',
        'password': 'without->generated',
    }
},