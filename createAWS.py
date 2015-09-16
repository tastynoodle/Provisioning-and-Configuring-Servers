#!/usr/bin/env python

import boto3
from time import sleep

ec2 = boto3.resource('ec2')
instances = ec2.create_instances( 
					ImageId = "ami-5189a661",
					MinCount = 1,
					MaxCount = 1,
					SecurityGroups = [ "launch-wizard-3" ],
					InstanceType='t2.micro',
					KeyName = "key" )
print "AWS server created."

print "Trying to get the server ip, may take few seconds..."
id = instances[0].id
instance = ec2.Instance( id )
while not instance.public_ip_address:	
    instance = ec2.Instance( id )
with open( "inventory_AWS", "w+" ) as f:
    command = "node1 ansible_ssh_host=%s ansible_ssh_user=ubuntu ansible_ssh_private_key_file=node1.key" % instance.public_ip_address
    print >> f, command
print "inventory file created."
