import os

import getpass
from fabric import Connection, Config
from invoke.util import cd

# sudo_pass = getpass.getpass('password: ')
# config = Config(overrides={'sudo': {'password': sudo_pass}})


def make_connection(user, password, host, port=22):
    connect_kwargs = {}
    if password:
        connect_kwargs['password'] = password

    conn = Connection(user=user, host=host, port=port, connect_kwargs=connect_kwargs)
    return conn


def transfer_files(conn, local_folder, remote_folder):
    with conn:
        # make tar
        base_name = os.path.basename(os.path.normpath(local_folder))
        file_name = '%s.tar.gz' % base_name
        conn.local('tar -czvf ../%s %s' % (file_name, local_folder))
        print('Created %s file at local.' % file_name)

        # upload file
        print('Uploading %s...' % file_name)
        result = conn.put('../%s' % file_name, remote=remote_folder)
        print("Uploaded {0.local} to {0.remote}.".format(result))

        # decompress tar
        conn.run('tar -xzf %s -C %s' % (result.remote, remote_folder))
        print('Unpacked %s in %s.' % (result.remote, result.orig_remote))

        working_folder = os.path.join(remote_folder, base_name)
        with conn.cd(working_folder):
            print('Changed working folder to %s.' % working_folder)

            conn.run('rm -r %s' % os.path.join(working_folder, 'venv'))
            print('Removed venv folder.')

            conn.run('python3 -m venv venv')
            print('Created new venv folder.')

            print('Installing requirements..')
            conn.run('venv/bin/pip install --upgrade pip')
            conn.run('venv/bin/pip install -r requirements.txt')

            print('Setting environment...')
            conn.run('source venv/bin/activate && export FLASK_ENV=production && export FLASK_APP=blog.py && flask deploy')

        # start supervisord
        # supervisord_config = os.path.join(working_folder, 'supervisord.conf')
        # conn.run('cd %s' % working_folder)
        # conn.run('supervisord -c %s' % supervisord_config)
