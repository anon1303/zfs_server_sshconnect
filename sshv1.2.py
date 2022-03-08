# from paramiko import SSHClient, AutoAddPolicy
import paramiko
from getpass import getpass
from docopt import docopt
import logging



def get_args():

	usage = """
	Usage:
		try.py -s <STORAGE> -o <OLDPASSWORD> -n <NEWPASSWORD>
		try.py --version
		try.py -h | --help

	Options:
		-h --help            Show this message and exit
		-s <STORAGE>         ZFS appliance/storage name

	"""

	args = docopt(usage)
	return args	


def logs(message):

	log_message = message

	logger = logging.getLogger('user')

	logging.basicConfig(filename='logs', level= logging.INFO, 
					format='%(asctime)s: %(levelname)s: %(name)s - %(message)s')

	logger.info(message)




def trial(args):

	if args['-s'] == True:
		message = ('New password set on server: '+args['<STORAGE>'])
		logs(message)


def connection():

	
	#LOAD HOST KEYS
	client = paramiko.SSHClient()

	# client.load_host_keys('~/root/.ssh/id_rsa')
	# ssh_key = '~/root/.ssh/known_hosts'
	# ssh = paramiko.RSAKey.from_private_key_file(ssh_key)

	# client.look_for_keys(True)
	# client.load_system_host_keys()

	#Known_host policy
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	host = '192.168.0.114' #Change this into the ipaddress of the machine you want to connect

	password = getpass('Enter password :')
	# client.connect()

	client.connect(hostname = host,
					username='root',
					password = password
					)
	# client.connect('192.168.0.109', username='root')


	# client.exec_command('hostname')
	stdin, stdout, stderr = client.exec_command(command)
	print(type(stdin))
	print(type(stdout))
	print(type(stderr))

	# # Optionally, send data via STDIN, and shutdown when done
	# stdin.write('Hello world')
	# stdin.channel.shutdown_write()

	# # Print output of command. Will wait for command to finish.
	print(f'STDOUT: {stdout.readlines().decode("utf8")}')
	print(f'STDERR: {stderr.readlines().decode("utf8")}')

	# # Get return code from command (0 is default for success)
	print(f'Return code: {stdout.channel.recv_exit_status()}')

	# # Because they are file objects, they need to be closed
	stdin.close()
	stdout.close()
	stderr.close()

	# # Close the client itself
	client.close()

def main(args):

	trial(args)
	# connection()



if __name__ == '__main__':
	try:
		ARGS = get_args()

		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except Exception:
	    ETRACE = traceback.format_exc()
	    print(ETRACE)