#!/usr/bin/env python3
import argparse,pathlib
import configparser
import subprocess
import shutil
import sys

try:
    import distro
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "distro"])
    import distro
    pass

def check_os():
    operating_system = sys.platform
    return(operating_system)

def check_linux_distro():
    distribution = distro.like()
    if distribution == '':
        distribution = distro.id()
    return(distribution)

def check_bin(binary):
    exec('global ' + binary + '_path', globals())
    exec(binary + '_path = shutil.which("' + binary + '")', globals())

def check_package_manager(operating_system):
    if operating_system == 'darwin':
        check_bin("brew")
        check_bin("nix")

    if 'freebsd' in operating_system:
        global pkg_path
        pkg_path = '/usr/sbin/pkg'
        check_bin("nix")

    if operating_system == 'alpine':
        global apk_path
        apk_path = '/sbin/apk'
        check_bin("nix")
        check_bin("brew")

    if operating_system == 'debian':
        global apt_path
        apt_path = '/usr/bin/apt'
        check_bin("nix")
        check_bin("brew")

    if 'rhel' in operating_system or operating_system == 'fedora':
        global dnf_path
        dnf_path = '/usr/bin/dnf'
        check_bin("nix")
        check_bin("brew")

    if operating_system == 'arch':
        global pacman_path
        pacman_path = '/usr/sbin/pacman'
        check_bin("nix")
        check_bin("brew")

def package_manage(package_manager, package_name, action):
    cache_update = 'no'
    if package_manager == 'apk':
        cache_update_cmd = 'apk update'
        if action == 'uninstall':
            action = 'del'

        if action == 'install':
            action = 'add'
            cache_update = 'yes'
        
        if action == 'upgrade':
            cache_update = 'yes'

    if package_manager == 'apt':
        cache_update_cmd = 'apt update'
        if action == 'uninstall':
            action = 'remove'

        if action == 'install':
            cache_update = 'yes'
        
        if action == 'upgrade':
            cache_update = 'yes'

    if package_manager == 'brew':
        cache_update_cmd = 'brew update'
        
        if action == 'install':
            cache_update = 'yes'
        
        if action == 'upgrade':
            cache_update = 'yes'


    if package_manager == 'dnf':
        cache_update_cmd = 'dnf check-update'
        if action == 'uninstall':
            action = 'remove'

        if action == 'install':
            cache_update = 'yes'
        
        if action == 'upgrade':
            cache_update = 'yes'


    if package_manager == 'nix':
        cache_update_cmd = 'nix-channel --update'
        package_manager = 'nix-env'
        if action == 'uninstall':
            action = '--uninstall'
        if action == 'install':
            action = '--install'
            cache_update = 'yes'
        if action == 'upgrade':
            action = '--upgrade'
            cache_update = 'yes'


    if package_manager == 'pacman':
        cache_update_cmd = 'pacman -Sy'
        if action == 'uninstall':
            action = '-R'

        if action == 'install':
            cache_update = 'yes'
            action = '--noconfirm -S'
        
        if action == 'upgrade':
            cache_update = 'yes'
            action = '--noconfirm -Su'


    if package_manager == 'pkg':
        cache_update_cmd = 'pkg update'
        if action == 'uninstall':
            action = 'delete'

        if action == 'install':
            cache_update = 'yes'
        
        if action == 'upgrade':
            cache_update = 'yes'
    
    
    if cache_update == 'yes':
        subprocess.run(cache_update_cmd, shell=True)

    subprocess.run(package_manager + ' ' + action + ' ' + package_name, shell=True)

def ManagePackages(action, package) -> bool:
    operating_system = check_os()
    global linux
    if operating_system == 'linux':
        linux = 'true'
        operating_system = check_linux_distro()
        print(operating_system)
    else:
        linux = 'false'

    if operating_system == 'windows':
        print('Windows not supported!')
    else:
        check_package_manager(operating_system)

    installed = False
    if linux == 'true' or operating_system == 'darwin' or 'freebsd' in operating_system:

        try:
            if apk_path:
                package_manage("apk", package, action)
                installed = True
        except NameError:
            pass

        try:
            if apt_path:
                package_manage("apt", package, action)
                installed = True
        except NameError:
            pass
        
        try:
            if dnf_path:
                package_manage("dnf", package, action)
                installed = True
        except NameError:
            pass
        
        try:
            if pacman_path:
                package_manage("pacman", package, action)
                installed = True
        except NameError:
            pass
        try:
            if pkg_path:
                package_manage("pkg", package, action)
                installed = True
        except NameError:
            pass
    
        try:
            if brew_path and installed == 'false':
                package_manage("brew", package, action)
                installed = True
        except NameError:
            pass
        try:
            if nix_path and installed == 'false':
                package_manage("nix", package, action)
                installed = True
        except NameError:
            pass

    return installed
# if __name__ == "__main__":
#     A= subprocess.call(["which", "fusermount3"])
#     print(A)
#     A=subprocess.call(["which", "fusermount321"])
#     print(A)
#     ManagePackages("remove", ["fuse-zip"])
