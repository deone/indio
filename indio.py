from smtplib import SMTP
import ConfigParser

import cx_Oracle

class Indio(object):
    def __init__(self, config_file):
	""" Read configuration file, initialize database connectivity """
	self.config = ConfigParser.ConfigParser()
	self.config.readfp(open(config_file))

	self.db_params = dict(self.config.items('db'))

	action_dict = {}
	for section in self.config.sections():
	    if section.startswith('count'):
		action_dict[section] = {}
		action_dict[section].update(dict(self.config.items(section)))

	self.action_dict = action_dict
	self.email_params = dict(self.config.items('email'))
	self.email_params['to_addrs'] = self.email_params['to_addrs'].split(', ')

	dsn = cx_Oracle.makedsn(self.db_params['host'], self.db_params['port'],
		self.db_params['sid'])
	connection = cx_Oracle.connect(self.db_params['username'],
		self.db_params['password'], dsn)

	self.cursor = connection.cursor()

    def __format_rows(self, rows):
	formatted_rows = ''
	for row in rows:
	    if len(row) == 2:
		formatted_rows += '\n' + str(row[0]) + '\t\t\t\t' + str(row[1])
	    elif len(row) == 3:
		formatted_rows += '\n' + str(row[0]) + '\t\t\t' + str(row[1]) +\
		'\t\t\t' + str(row[2])
	    elif len(row) == 1:
		formatted_rows += '\n' + str(row[0])

	return formatted_rows

    def execute_sql(self, action, sql):	
	""" Execute SQL statement and format results according to the specified
	action """
	results_title = self.action_dict[action]['title']

	header_items = self.action_dict[action]['table_header'].split('|')

	if len(header_items) == 2:
	    results_table_header = '\n' + header_items[0] + '\t' + '|' + '\t' +\
		header_items[1]
	elif len(header_items) == 3:
	    results_table_header = '\n' + header_items[0] + '\t' + '|' +\
		'\t' + header_items[1] + '\t' + '|' + '\t' +  header_items[2]
	elif len(header_items) == 1:
	    results_table_header = '\n' + header_items[0]

	if action.endswith('this_week') or action.endswith('till_date'):
	    self.email_params['to_addrs'] = self.config.get('email',
	    'to_addrs_weekly').split(', ')

	results = '\n' + results_title

	self.cursor.execute(sql)
	rows = self.cursor.fetchall()

	if not rows:
	    results += '\n' + '0'
	else:
	    results += '\n' + results_table_header
	    results += self.__format_rows(rows)

	return results

    def send_email(self, msg, subject):
	mail_headers = 'Subject: ' + subject + '\r\n' + 'From: ' +\
	    self.email_params['from_addr'] + '\r\n' + 'To: ' + ',\
	    '.join(self.email_params['to_addrs']) +\
	    '\r\n\r\n'

	message = mail_headers + msg

	print message

	server = SMTP(self.email_params['host'])
	retval = server.sendmail(self.email_params['from_addr'], self.email_params['to_addrs'], message)

	server.quit()
	return retval
