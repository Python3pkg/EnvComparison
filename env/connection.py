from paramiko import SSHClient, SSHConfig, AutoAddPolicy
import re
import pprint





class Connection(object):
    
    def __init__(self, config_location, server_name):


        self.system = {}
        self.system['ssh_hostname'] = server_name
        self.system['system'] = {'ssh_hostname':server_name}

        config = SSHConfig()
        config.parse(open(config_location))
        o = config.lookup(server_name)

        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_client.load_system_host_keys()
        self.ssh_client.connect(o['hostname'], username=o['user'], key_filename=o['identityfile'])


    def _run_command(self, cmd):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.readlines()

        
    def _check_command(self, cmd):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return stdout.channel.recv_exit_status()


    def system_check(self):
        """
        Should do something with this test one day...
        """
        if self._check_command('file') != 1:
            pass
        if self._check_command('which') != 1:
            pass


    def get_platform_family(self):

        # https://github.com/opscode/ohai/blob/master/lib/ohai/plugins/linux/platform.rb
        if self.system['platform'] in ['oracle', 'centos', 'redhat', 'scientific', 'enterpriseenterprise', 'amazon']:
            self.system['platform_family'] = 'rhel'
        if self.system['platform'] in ['debian', 'ubuntu', 'linuxmint']:
            self.system['platform_family'] = 'debian'
        if self.system['platform'] in ['fedora']:
            self.system['platform_family'] = 'fedora'

    def get_packages(self):
        """ 
        print out dpkg -l or parse /var/lib/dpkg/status ??? 
        """
        self.packages = {}
        if self.system['platform_family'] == 'debian':
            for line in self._run_command('dpkg -l'):
                parts = line.split()
                if parts[0] == 'ii':
                    self.packages[parts[1]] = parts[2]

        elif self.system['platform_family'] == 'rhel':
            pass

        elif self.system['platform_family'] == 'arch':
            pass

        #elif self.system['platform_family'] == '':

        #else:
        #    self.system['platform_family'] == 


        self.system['packages'] = self.packages


    def get_platform_details(self):
        """
        is ubuntu? 
        """
        avars = self._run_command('lsb_release -a')

        final = ' '.join(avars).lower()
        output = dict(re.findall(r'(\S[^:]+):\s*(.*\S)', final))
        self.system['platform'] = output['distributor id']
        self.system['codename'] = output['codename']
        self.system['release'] = output['release']



    def get_system_arch(self):
        self.system['arch'] = self._run_command('arch')[0].strip()


        
    def get_fqdn(self):
        self.system['fqdn'] = self._run_command('hostname --fqdn')[0].strip()


    def get_pip_packages(self):
        if self._check_command('which pip') == 0:
            for line in self._run_command('pip freeze'):
                parts = line.strip().split('==')
                self.system[parts[0]] = parts[1] 

        
    def get_php_info(self):
        if self._check_command('which php') == 0:
            for line in self._run_command('php -i | grep -i "version =>"'):
                parts = line.strip().split(' => ')
                self.system[parts[0]] = parts[1]



    def pretty_print(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.system)


