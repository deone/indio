import indio
import unittest
import commands

class TestIndio(unittest.TestCase):
    def setUp(self):
	self.indio_obj = indio.Indio(config_file='../indio.ini')
	self.action = 'count_employees'
	self.results = self.indio_obj.execute_sql(self.action, '''select
		employee_id, first_name from employees where rownum < 6''')

	""" self.action = 'count_orders'
	self.results = self.indio_obj.execute_sql(self.action, '''
		SELECT 
		usr.distributor_id, decode(od.status, 'C', 'Cancelled', 
		'R', 'Rejected', 'PTTP', 'Posted to TP', 'PTTPSA', 
		'Posted to TPSA', 'PTIFS', 'Posted to IFS') order_status, 
		count(od.status) order_count
		FROM
		tbl_order_dtls od, tbl_user usr
		WHERE
		od.INITIATED_BY=usr.USER_NAME and trunc(od.LAST_UPDATED_DATE)
		=trunc(sysdate)
		GROUP BY
		od.status, usr.distributor_id 
		ORDER BY distributor_id''')"""

    def test_initialize(self):
	""" Check if Indio initializes correctly """
	self.assertEquals(hasattr(self.indio_obj, 'db_params'), True)
	self.assertEquals(hasattr(self.indio_obj, 'email_params'), True)
	self.assertEquals(hasattr(self.indio_obj, 'cursor'), True)
	self.assertEquals(hasattr(self.indio_obj, 'action_dict'), True)

	self.assertEquals(type(self.indio_obj.email_params['to_addrs']).__name__,
	    'list')
	self.assertEquals(hasattr(self.indio_obj, 'execute_sql'), True)
	self.assertEquals(hasattr(self.indio_obj, 'send_email'), True)

    def test_execute_sql(self):
	""" Check if Indio executes SQL statements properly, formats and returns results accurately """
	self.assertEquals(self.indio_obj.action_dict[self.action]['title'] in self.results, True)

    def test_send_email(self):
	""" Check if Indio sends email """
	# retval = self.indio_obj.send_email(self.results, subject='Oracle XE Sample Database Report')
	# self.assertEquals(retval, {})
	pass


if __name__ == "__main__":
    unittest.main()
