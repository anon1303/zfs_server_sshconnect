# from paramiko import SSHClient, AutoAddPolicy
import paramiko
from getpass import getpass
from docopt import docopt
import logging



def get_args():

	usage = """
	Usage:
		zfs_changepaswd.py -s <STORAGE> -u <USER> -o <OLDPASSWD> -n <NEWPASSWD> 
		zfs_changepaswd.py -s <STORAGE> -p <OUT> 
		zfs_changepaswd.py --version
		zfs_changepaswd.py -h | --help

	Options:
		-h --help            Show this message and exit
		-s <STORAGE>         ZFS appliance/storage name

	"""

	args = docopt(usage)
	return args	


def logs(message):

	log_message = message

	logger = logging.getLogger('user')

	logging.basicConfig(filename='zfs_changelog', level= logging.INFO, 
					format='%(asctime)s: %(levelname)s: %(name)s - %(message)s')

	logger.info(message)



def connection(args):

	
	#LOAD HOST KEYS
	client = paramiko.SSHClient()

	client.load_host_keys('/root/.ssh/id_rsa')
	 #ssh_key = '~/root/.ssh/known_hosts'
	 #ssh = paramiko.RSAKey.from_private_key_file(ssh_key)

	#client.look_for_keys(True)
	client.load_system_host_keys()

	#Known_host policy
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# host = '192.168.0.114' #sample 

	# password = getpass('Enter password :')
	# client.connect()

	client.connect(hostname = args['<STORAGE>'],
					username='root',
					)
	# sample client.connect('192.168.0.109', username='root')


	# client.exec_command('hostname')
	stdin, stdout, stderr = client.exec_command('configuration users select ' +args['<USER>']+' set initial_password='+args['<OLDPASSWD>']+' initial_password='+args['<NEWPASSWD>'] )
	print(type(stdin))
	print(type(stdout))
	print(type(stderr))

	# # Optionally, send data via STDIN, and shutdown when done
	# stdin.write('Hello world')
	# stdin.channel.shutdown_write()

	# # Print output of command. Will wait for command to finish.
	print(f'STDOUT: {stdout.read().decode("utf8")}')
	print(f'STDERR: {stderr.read().decode("utf8")}')

	# # Get return code from command (0 is default for success)
	print(f'Return code: {stdout.channel.recv_exit_status()}')

	# # Because they are file objects, they need to be closed
	stdin.close()
	stdout.close()
	stderr.close()

	# # Close the client itself
	client.close()
	message = ('log message : '+args['<STORAGE>'])
	logs(message)



def  usercat(args):

	
	#LOAD HOST KEYS
	client = paramiko.SSHClient()

	client.load_host_keys('/root/.ssh/id_rsa')
	 #ssh_key = '~/root/.ssh/known_hosts'
	 #ssh = paramiko.RSAKey.from_private_key_file(ssh_key)

	#client.look_for_keys(True)
	client.load_system_host_keys()

	#Known_host policy
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# host = '192.168.0.114' #sample 

	# password = getpass('Enter password :')
	# client.connect()

	client.connect(hostname = args['<STORAGE>'],
					username='root',
					)
	# sample client.connect('192.168.0.109', username='root')


	# client.exec_command('hostname')
	stdin, stdout, stderr = client.exec_command('configuration users select ' +args['<OUT>']+ ' show' ) 
	print(type(stdin))
	print(type(stdout))
	print(type(stderr))

	# # Optionally, send data via STDIN, and shutdown when done
	# stdin.write('Hello world')
	# stdin.channel.shutdown_write()

	# # Print output of command. Will wait for command to finish.
	print(f'STDOUT: {stdout.read().decode("utf8")}')
	print(f'STDERR: {stderr.read().decode("utf8")}')

	# # Get return code from command (0 is default for success)
	print(f'Return code: {stdout.channel.recv_exit_status()}')

	# # Because they are file objects, they need to be closed
	stdin.close()
	stdout.close()
	stderr.close()

	# # Close the client itself
	client.close()
	message = ('log message : '+args['<STORAGE>'])
	logs(message)





def main(args):

	if args['-o'] == False:
		usercat(args)
	else:
		connection(args)

	
	#print(args)
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