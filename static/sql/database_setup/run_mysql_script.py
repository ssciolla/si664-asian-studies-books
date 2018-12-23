import argparse
import logging
import MySQLdb
import sys
import yaml


def main(args):
	"""
	This python script is designed to process MySQL scripts.  The script
	requires a valid database connection.  After opening a connection and creating a cursor,
	the script creates a list of SQL statements after splitting the SQL script on each semi-colon
	encountered (;).  The script then loops through the statements, attempting to execute
	each. If successful, the script commits the changes, closes the cursor and then closes the
	connection.  Otherwise, it rolls back the transaction and reports the error encountered.
	"""

	# Setting logging format and default level
	logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

	msg = [
		'Connection created.',
		'Connection closed.',
		'Cursor created.',
		'Cursor closed.',
		'Changes committed.',
		'Statement executed:',
		'Transaction rollback:'
	]

	# Process args
	args = parse_args(args)
	script_path = args.path
	config_path = args.config

	# Read config file
	cfg = read_config(config_path)

	try:
		cnx = connect_to_db(cfg['mysql'])
		logging.info(msg[0])

		# Create cursor
		cursor = cnx.cursor()
		logging.info(msg[2])

		# Open and read the file as a single buffer
		fd = open(script_path, 'r')
		sql_script = fd.read()
		fd.close()

		# Get all SQL statements (split on ';')
		sql_statements = sql_script.split(';')

		# Execute SQL statements
		for statement in sql_statements:
			if not statement.strip():
				continue
			cursor.execute(statement)
			logging.info(msg[5] + ' %s' % str(statement) + '\n')

		# Commit changes
		cnx.commit()
		logging.info(msg[4])

	except MySQLdb.Error as err:
		# Note: catching client.OperationalError as error reports back skipped statements
		# such as CREATE TABLE IF NOT EXISTS [table_name] as errors even though existing
		# table in fact exists.

		cnx.rollback()
		logging.warning(msg[6] + ' %s' % str(err) + '\n')

	finally:
		cursor.close()
		logging.info(msg[3])
		cnx.close()
		logging.info(msg[1])


def connect_to_db(config):

	if not config['local_infile']:
		config['local_infile'] = False

	return MySQLdb.connect(
		host=config['host'],
		port=config['port'],
		user=config['user'],
		passwd=config['passwd'],
		db=config['db'],
		local_infile=config['local_infile'])


def parse_args(args):
	parser = argparse.ArgumentParser(
		description='''This python script is designed to process MySQL scripts.  The script 
		requires a valid database connection.  After opening a connection and creating a cursor, 
		the script creates a list of SQL statements after splitting the SQL script on each semi-colon 
		encountered (;).  The script then loops through the statements, attempting to execute 
		each. If successful, the script commits the changes, closes the cursor and then closes the 
		connection.  Otherwise, it rolls back the transaction and reports the error encountered. '''
	)
	parser.add_argument("-c", "--config", type=str, required=True, help="path to config file")
	parser.add_argument("-p", "--path", type=str, required=True, help="path to script")
	return parser.parse_args(args)


def read_config(path):
	with open(path, 'r') as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as err:
			logging.error(err)


# Execute filename change
if __name__ == '__main__':
	main(sys.argv[1:])
# sys.exit(main())