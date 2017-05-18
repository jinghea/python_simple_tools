import configparser
import boto3
import subprocess


CONFIG_PATH = '../configurations/python_simple_tools.ini'
CONFIG_SECTION = 'DEFAULT'


def do_with_first_ip(ec2):
	response = ec2.describe_instances()
	reservations = response['Reservations']

	for reservation in reservations:
		for instance in reservation['Instances']:
			yield instance['PublicIpAddress']
			return

def load_config():
	config = configparser.ConfigParser()
	config.read(CONFIG_PATH)
	return config
	

config = load_config()
ec2 = boto3.client('ec2')

for ip in do_with_first_ip(ec2):
	subprocess.call("ssh -i "+config[CONFIG_SECTION]['pem-path']+" "+config[CONFIG_SECTION]['ec2-username']+"@"+ip,shell=True)

