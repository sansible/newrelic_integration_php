import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_packages(host):
    packages = [
        'newrelic-daemon', 'newrelic-php5',
        'newrelic-php5-common',
    ]
    for package in packages:
        assert host.package(package).is_installed


def test_config(host):
    php_ini = host.file('/etc/php/7.3/mods-available/newrelic.ini')
    assert 'newrelic.daemon.loglevel = error' in php_ini.content_string


def test_extension_loaded_in_cli(host):
    cmd = host.run('php -m | grep newrelic')
    assert "newrelic" in cmd.stdout


def test_extension_loaded_in_fpm(host):
    cmd = host.run('curl http://127.0.0.1/phpinfo.php | grep module_newrelic')
    assert "module_newrelic" in cmd.stdout
