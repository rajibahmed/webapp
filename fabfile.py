from fabric.api import env
from fabric.api import *

from fabric.contrib import files
from datetime import datetime

def setup():
    development()
    ssh()

def production():
    env.hosts = ['10.100.0.70',]
    env.remote_admin = 'sysadmin'

def development():
    env.hosts = ['172.16.195.11']
    env.remote_admin = 'rajib'


def ssh():
    for host in env.hosts:
        local("ssh-copy-id %s@%s" % (env.remote_admin, host))


def hostconfig():
    apt_upgrade()
    install_git()
    install_nodejs()
    install_nginx()

def cmd_exists(cmd):
    return files.exists("/usr/bin/%s" % cmd)


#######################
# Server initialization
#######################

def apt_upgrade():
    apt("update -y")
    apt("upgrade")

def apt(cmd):
    sudo("apt-get %s" % cmd)

def install_git():
    if not cmd_exists('git'):
        apt("install -y git-core")
        run("git config --global color.ui true")

def install_nodejs():
    if not cmd_exists('nodejs'):
        apt("install -y nodejs")
        apt("install -y npm")

def install_nginx():
    if not cmd_exists('nginx'):
        apt("install -y nginx")

#######################
# Code deployment
#######################

def deploy():
    with cd('/var/www'):
        run("mkdir %s" % datetime.datetime.now().strftime('%Y%m%d%H%M%S'))