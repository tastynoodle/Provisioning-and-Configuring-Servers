#!/usr/bin/env python

# I used an open-source python sdk for digital ocean
# https://github.com/koalalorenzo/python-digitalocean
# install with "pip install -U python-digitalocean"
from digitalocean import Droplet, Account, Manager
from time import sleep

token = "404b7a26a00b89c7dc85f431e293fd532d68edfaf3268728a95ed38833dee257"
account = Account.get_object( token )
keys_list = account.get_data( "account/keys" )

# get ssh key id
keys_id_list = []
for key in keys_list[ 'ssh_keys' ]:
    keys_id_list.append( key[ 'id' ] )

droplet = Droplet( token = token,
                   ssh_keys = keys_id_list,
                   name = "Server1",
                   region = "nyc2",
                   image = "ubuntu-14-04-x64",
                   size_slug = "512mb",
                   backups = True )
droplet.create()
print "droplet created."

# waiting for server to boot
#print "Waiting for server to boot, this may take a while..."
#actions = droplet.get_actions()
#for action in actions:
#    action.wait()

# reload the droplet and get the ip address
while not droplet.ip_address:
    droplet.load()
with open( "inventory_DO", "w+" ) as f:
    command = "node0 ansible_ssh_host=%s ansible_ssh_user=root ansible_ssh_private_key_file=node0.key" % droplet.ip_address
    print >> f, command
print "inventory file created."
