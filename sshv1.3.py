# from paramiko import SSHClient, AutoAddPolicy

"""
version 1.3

Updated the script,
- removed redundant scripts
- added error handlings E.i(error when server is not found)
- updated the logging
(When command is not successful it will send the error to the logs)

"""
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

	logger = logging.getLogger()

	logging.basicConfig(filename='zfs_changelog', level= logging.INFO, 
					format='%(asctime)s: %(levelname)s: %(name)s - %(message)s')

	logger.info(message)



def connection(args):

	command = 0
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
					# password = password
					)
	# sample client.connect('192.168.0.109', username='root')


	# client.exec_command('hostname')
	if args['-o'] == False:
		command = 1
		stdin, stdout, stderr = client.exec_command('configuration users select ' +args['<OUT>']+ ' show' ) 
		
	else:
		stdin, stdout, stderr = client.exec_command('configuration users select ' +args['<USER>']+' set initial_password='
											+args['<OLDPASSWD>']+' initial_password='+args['<NEWPASSWD>'] )
	
	# print(type(stdin))
	# print(type(stdout))
	# print(type(stderr))

	# # Optionally, send data via STDIN, and shutdown when done
	# stdin.write('Hello world')
	# stdin.channel.shutdown_write()

	# # Print output of command. Will wait for command to finish.
	# print(f'STDOUT: {stdout.read().decode("utf8")}')
	output = stdout.read().decode("utf8")
	print('\n'+'-'*60)
	print(output)


	print(f'STDERR: {stderr.read().decode("utf8")}')

	# # Get return code from command (0 is default for success)
	
	# response=(f'Return code: {stdout.channel.recv_exit_status()}')
	response = stdout.channel.recv_exit_status()
	
	if response == 0:
		if command == 1:
			message = ('View user '+args['<OUT>'])
			logs(message)
		elif command == 0:
			message = ('Updated password on the user '+args['<USER>'])
			logs(message)
	else:
		message = (output)
		logs(message)

	# # Because they are file objects, they need to be closed
	stdin.close()
	stdout.close()
	stderr.close()

	# # Close the client itself
	client.close()



def main(args):

	connection(args)

	
	#print(args)
	# connection()



if __name__ == '__main__':
	try:
		ARGS = get_args()

		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except paramiko.ssh_exception.AuthenticationException:
		print('\nAuthentication problem....')
	except paramiko.ssh_exception.NoValidConnectionsError:
		print('\nServer problem....')

	except Exception:
	    ETRACE = traceback.format_exc()
	    print(ETRACE)