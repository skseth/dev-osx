from distutils import spawn
import subprocess
import os
import logging
import urllib2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HOME = os.path.expanduser("~")
DEV = "%s/.dev" % (HOME) 
PWD_CLIENT="%s/pwd-client.sh" % (DEV)
BIN_DIR="%s/bin" % (DEV)
INV_DIR="%s/inventory" % (DEV)
GRP_DIR="%s/inventory/group_vars" % (DEV)
ALL_YML="%s/all.yml" % (GRP_DIR)
KEYCHAIN_SERVICE="devsetup"
KEYCHAIN_ACCOUNT="master"

PWD_CLIENT_SCRIPT='''
PWD=$(security find-generic-password -s %s -a %s -w 2>/dev/null)
RC=$?
if [ $RC -eq 0 ] ; then
    echo $PWD
fi
exit $RC
''' % (KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)

class KeychainPassword:
    def __init__(self,service,account):
        self.service = service
        self.account = account
        self.init_state()
    
    def init_state(self):
        try:
            self.value = subprocess.check_output(['/usr/bin/security', 'find-generic-password',
                            '-s', self.service,
                            '-a', self.account,
                            '-w'])
            self.exists = True
        except subprocess.CalledProcessError:
            self.exists = False
            self.value = ""

    def set_pwd(self, pwd):
        subprocess.call(['/usr/bin/security', 'add-generic-password',
                    '-s', self.service,
                    '-a', self.account,
                    '-w', pwd])
        self.value = pwd
        self.exists = True
    
    def clear_pwd(self):
        try:
            subprocess.call(['/usr/bin/security', 'delete-generic-password',
                            '-s', self.service,
                            '-a', self.account])
        except:
            return

    def ensure_pwd(self):
        if not self.exists:
            master_pwd = raw_input("Your Master Password: ")
            self.set_pwd(master_pwd)
    
    def encrypt(self, plainval):
        if self.exists:
            return subprocess.check_output([
                '/usr/local/bin/ansible-vault',
                'encrypt_string',
                plainval
            ])    

class DevConfig:
    def __init__(self, path, master):
        self.path = path
        self.master = master
        try:
            with open(path, 'r') as f:
                self.content = f.read()
        except:
            self.content = ""
            logger.info("%s file does not exist", self.path)
    
    def paramexists(self, paramname):
        paramstr = paramname + ": "
        return (paramstr in self.content)

    def add_param(self, paramname, paramval):
        self.content += "\n%s: %s\n" % (paramname, paramval)
        logger.info("Param %s added" % paramname)

    def add_param_prompt(self, paramname, prompt, isencrypted = False):
        if self.paramexists(paramname):
            logger.info("Param %s exists" % paramname)
        else:
            paramval = raw_input(prompt)
            if isencrypted:
                paramval = self.master.encrypt(paramval)
            self.add_param(paramname, paramval)
        
    def save(self):
        with open(self.path, 'w+') as f:
            f.write(self.content)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def find_command(cmd):
    return spawn.find_executable(cmd)

def download_url(url):
    response = urllib2.urlopen(url)
    script = response.read()
    logger.debug("downloaded url %s" % (script))
    return script

def write_to_file(path, script):
    f = open(path,"w+")
    f.write(script)
    f.close()
    logger.debug("File %s created" % (path))

def read_file(path):
    f = open(path, 'r')
    return f.read()

def file_exists(path):
    return os.path.isfile(path)

def write_to_file_if_missing(path, script):
    if file_exists(path):
        logger.info("%s exists" % path)
    else:
        write_to_file(path, script)

def make_dir_if_missing(path):
    if not os.path.isdir(path):
        make_dir_if_missing(path)
        logging.info("directory %s created" % (path))
    else:
        logging.debug("directory %s exists" % (path))

def brew_install():
    if find_command("brew") is None:
        logger.info(msg="installing brew")
        script = download_url('https://raw.githubusercontent.com/Homebrew/install/master/install')
        subprocess.call(['/usr/bin/ruby', '-e', script])
        logger.info("Done installing brew")
    else:
        logger.info("brew is installed")

def ansible_install():
    if find_command("ansible") is None:
        logger.info(msg="installing ansible")
        subprocess.call(['/usr/local/bin/brew', 'install', 'ansible'])
        logger.info("Done installing ansible")
    else:
        logger.info("ansible is installed")

def create_dirs():
    make_dir_if_missing(DEV)
    make_dir_if_missing(BIN_DIR)
    make_dir_if_missing(INV_DIR)
    make_dir_if_missing(GRP_DIR)


def capture_input(master):
    config = DevConfig(ALL_YML, master)
    config.add_param("dev_user_home", HOME)
    config.add_param("dev_config_root", DEV)
    config.add_param_prompt("dev_name", "Your Name: ")
    config.add_param_prompt("dev_login_id", "Your login id: ")
    config.add_param_prompt("dev_email", "Your Email: ")
    config.add_param_prompt("dev_git_user_name", "Your Git user name: ")
    config.add_param_prompt("ansible_become_pass", "Sudo password for ansible: ", True)
    config.add_param_prompt("dev_email_pwd", "Your Email Password: ", True)
    config.add_param_prompt("dev_ssh_passphrase", "Your SSH Password: ", True)
    config.add_param_prompt("dev_github_token", "Your Github token: ", True)
    config.add_param_prompt("dev_brew_github_token", "Your Homebrew Github token: ", True)
    config.save()

def main():
    
    brew_install()
    ansible_install()
    masterpwd = KeychainPassword(KEYCHAIN_SERVICE, KEYCHAIN_ACCOUNT)
    masterpwd.ensure_pwd()
    create_dirs()
    capture_input(masterpwd)
    write_to_file_if_missing(PWD_CLIENT, PWD_CLIENT_SCRIPT)

if __name__ == '__main__':
    main()

