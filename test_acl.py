import json
import logging
import os
import requests
import sys
import yaml

from fabric.api import env, run, settings, task

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)

logger.info('Running as: %s' % env.user)

with open('hosts.yml', 'r') as host_file:
hosts = yaml.load(host_file)
print '\n%s\n' % hosts
env.roledefs = hosts

if 'out' in env:
out_path = env['out']
logger.info('Logging results to: %s' % out_path)
try:
os.remove(out_path)
except OSError as e:
pass
file_handler = logging.FileHandler(out_path)
logger.addHandler(file_handler)

class HostFetchError(ValueError):
pass

@task(default = True)
def check_acls(in_path = 'acls.yml'):
print ''

with open(in_path, 'r') as in_file:
acls = yaml.load(in_file)

for acl in acls:
print 'Checking "%(name)s" ACLs\n' % acl

if 'command' in acl:
command = acl['command']
else:
raise ValueError('No command specified')

if 'port' in acl:
dst_port = acl['port']
else:
raise ValueError('No destination port specified')

if 'hosts' in acl:
dst_hosts = acl['hosts']
elif 'hosts_url' in acl:
dst_hosts = fetch_hosts(acl['hosts_url'])
else:
raise ValueError('No destination hosts specified')

for dst_host in dst_hosts:
result = check_acl(command, dst_host, dst_port)
result_str = 'Success' if result else 'Fail'
logger.info('%s -> %s:%d: %s' % (env.host, dst_host, dst_port, result_str))

@task
def check_acl(command, dst_host, dst_port):
with settings(warn_only = True):
result = run(command % {'host': dst_host, 'port': dst_port})

return result.succeeded

def fetch_hosts(url):
response = requests.get(url)

if 200 <= response.status_code < 300:
return json.loads(response.text)
else:
raise HostFetchError('Invalid response: %d' % response.status_code)
