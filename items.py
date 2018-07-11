users = {
    'mediawiki': {
        'shell': '/usr/sbin/nologin',
    }
}

pkg_apt = {
    'php': {},
    'php-mbstring': {},
    'php-xml': {},
    'php-mysql': {},
    'php-imagick': {},
}

wikiversion = node.metadata.get('mediawiki', {}).get('version', '1.31.0')
wiki = node.metadata.get('mediawiki', {})
mysql_db = wiki.get('mediawiki', {}).get('db', {}).get('db', 'wiki')
mysql_host = wiki.get('mediawiki', {}).get('db', {}).get('host', 'localhost')
mysql_user = wiki.get('db', {}).get('user', 'wiki')
mysql_password = wiki.get('db', {}).\
    get('password', repo.libs.pw.get("mysql_{}_user_{}".format(mysql_user, node.name)))

directories = {
    '/home/mediawiki': {
        'owner': 'mediawiki',
        'group': 'mediawiki',
    },
}

downloads = {
    '/home/mediawiki/mediawiki-{}.tar.gz'.format(wikiversion): {
        'url': 'https://releases.wikimedia.org/mediawiki/' \
                '{version_short}/mediawiki-{version}.tar.gz' \
            .format(
                version_short='.'.join(wikiversion.split('.')[:2]),
                version=wikiversion
            ),
        'sha256': wiki.get('sha256', \
                 'f2273eac60ba5e141143c27caaed1eb3505c339455f5834b757c0e34c1782077'),
        'needs': [
            'directory:/home/mediawiki',
        ],
        'unless': 'test -f /home/mediawiki/mediawiki-{}.tar.gz' \
            .format(wikiversion),
    },
}

symlinks = {
    '/home/mediawiki/mediawiki': {
        'target': '/home/mediawiki/mediawiki-{}'.format(wikiversion),
        'triggered': True,
    },

}

actions = {
    'unpack_mediawiki': {
        'command': 'tar xfvz /home/mediawiki/mediawiki-{}.tar.gz ' \
                   '-C /home/mediawiki/'.format(wikiversion),
        'unless': 'test -f /home/mediawiki/mediawiki-{}/index.php'.format(wikiversion),
        'needs': [
            'download:/home/mediawiki/mediawiki-{}.tar.gz'.format(wikiversion),
        ],
        'triggers': [
            'action:chown_mediawiki',
            'symlink:/home/mediawiki/mediawiki',
        ],
    },
    'chown_mediawiki': {
        'command': 'chown -R mediawiki:mediawiki /home/mediawiki',
        'triggered': True,
    },
    'run_mediawiki_install': {
        'command': 'php /home/mediawiki/mediawiki-{version}/maintenance/install.php ' \
            '"{name}" "{admin_user}" --pass="{admin_pass}" ' \
            '--dbname={db_name} --dbserver={db_server} --dbtype=mysql ' \
            '--dbuser={db_user} --dbpass={db_pass} --installdbpass={db_pass} ' \
            '--installdbuser={db_user} --lang={lang} ' \
            '--server={server} --scriptpath=' \
            .format(
            version=wikiversion,
            name=wiki.get('name', 'My Wiki'),
            admin_user=wiki.get('admin_user', 'root'),
            admin_pass=wiki.get('admin_pass', 'changeme'),
            db_name=mysql_db,
            db_server=mysql_host,
            db_user=mysql_user,
            db_pass=mysql_password,
            lang=wiki.get('language', 'en'),
            server=wiki.get('server', ''),
        ),
        'unless': 'test -f /home/mediawiki/mediawiki-{}/LocalSettings.php' \
            .format(wikiversion),
        'needs': [
            'action:unpack_mediawiki',
            'action:chown_mediawiki',
        ]
    }
}

if mysql_host == 'localhost':
    mysql_users = {
        mysql_user: {
            'password': mysql_password,
            'hosts': ['127.0.0.1', '::1', 'localhost'].copy(),
            'db_priv': {
                mysql_db: 'all',
            },
        }
    }

    mysql_dbs = {
        mysql_db: {
        }
    }