#!/usr/bin/env python3

def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

def unzip_file(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)

def update_distro(distro):
    if distro == "ubuntu":
        run(["sudo","apt-get","update"])

def install_packages(distro):
    if distro == "ubuntu":
        base = ["sudo", "apt-get", "-y", "install"]
        packages = ["python3", "python3-pip", "firefox"]
        for package in packages:
            base.append(package)
        run(base)
        run(["pip3", "install", "-r", "requirements.txt"])

import sys
import os
import urllib.request

from subprocess import run

if sys.platform.startswith('win'):
    cwd = os.getcwd()
    GECKO_DIR = cwd + '\geckodriver'
    if not os.path.exists(GECKO_DIR):
        os.mkdir(GECKO_DIR)
    if not os.path.isfile(GECKO_DIR + '\geckodriver.exe'):
        os.chdir(GECKO_DIR)
        urllib.request.urlretrieve("https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-macos.tar.gz", filename='geckodriver.zip')
        import zipfile
        unzip_file(GECKO_DIR + '\geckodriver.zip', GECKO_DIR)
        os.chdir(cwd)
    GECKO_PATH = GECKO_DIR + '\geckodriver.exe'

elif sys.platform.startswith('darwin'):
    cwd = os.getcwd()
    GECKO_DIR = cwd + '/geckodriver'
    if not os.path.exists(GECKO_DIR):
        os.mkdir(GECKO_DIR)
    if not os.path.isfile(GECKO_DIR + '/geckodriver'):
        os.chdir(GECKO_DIR)
        urllib.request.urlretrieve("https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-macos.tar.gz", filename='geckodriver.tar.gz')
        import tarfile
        tar = tarfile.open('geckodriver.tar.gz', "r:gz")
        tar.extractall()
        tar.close()
        os.chdir(cwd)
    GECKO_PATH = GECKO_DIR + '/geckodriver'

else:
    cwd = os.getcwd()
    GECKO_DIR = cwd + '/geckodriver'
    if not os.path.exists(GECKO_DIR):
        os.mkdir(GECKO_DIR)
    if not os.path.isfile(GECKO_DIR + '/geckodriver'):
        os.chdir(GECKO_DIR)
        urllib.request.urlretrieve("https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz", filename='geckodriver.tar.gz')
        import tarfile
        tar = tarfile.open('geckodriver.tar.gz', "r:gz")
        tar.extractall()
        tar.close()
        os.chdir(cwd)
    GECKO_PATH = GECKO_DIR + '/geckodriver'
    """
    import platform
    platf = platform.platform().strip().lower()
    if "manjaro" in platf:
        PKGM = "pacman"
        opt = "--noconfirm"
    elif "ubuntu" in platf:
        PKGM = "apt"
    elif "arch" in platf:
        PKGM = "pacman"
        opt = "--noconfirm"
    elif "debian" in platf:
        PKGM = "apt-get"
    elif "centos" in platf:
        PKGM = "yum"
    if PKGM == "yum":
        run([PKGM, "-y", "install", "firefox", "pypy", "python"])
    elif PKGM == "pacman":
        run([PKGM, "-S", "firefox", "pypy", "python", opt])
    else:
        run([PKGM, "install", "-y", "firefox", "pypy", "python"])

run(["pip3", "install", "-r", "requirements.txt"])
"""

# Now install all packages in the machine
update_distro("ubuntu")
install_packages("ubuntu")
