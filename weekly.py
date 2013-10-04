import indio
import datetime

USERS_LOGGED_IN_TILL_DATE = """
		SELECT 
		type, count(*) No_Of_Users 
		FROM 
		tbl_user 
		WHERE 
		logindatetime 
		IS NOT NULL
		AND 
		type not in ('TPU_X','STPU_X')
		GROUP BY 
		type
		"""

USERS_LOGGED_IN_THIS_WEEK = """
		SELECT 
		type, count(*) No_Of_Users 
		FROM 
		tbl_user 
		WHERE 
		trunc(logindatetime) > trunc(sysdate) - 7
		AND 
		type not in ('TPU_X','STPU_X')
		GROUP BY 
		type
		"""

TP_PLANNED_ORDERS_THIS_WEEK = """
		SELECT 
		COUNT(DISTINCT distributor_id) TOTAL_TP_PLANNING 
		FROM 
		tbl_order_dtls 
		WHERE 
		trunc(ordered_date) > trunc(sysdate) - 7
		"""

ORDERS_THIS_WEEK = """
		SELECT
		COUNT(*) TOTAL_TP_PLANNING 
		FROM 
		tbl_order_dtls
		WHERE 
		trunc(ordered_date) > trunc(sysdate) - 7
		"""

SIM_SWAPS_THIS_WEEK = """
		SELECT 
		COUNT(DISTINCT serialno) 
		FROM 
		tbl_simswap_trans 
		WHERE 
		trunc(transaction_date) > trunc(sysdate) - 7
		"""

DAMAGED_PIN_TXNS_THIS_WEEK = """
		SELECT 
		COUNT(*) DAMAGED_PIN 
		FROM 
		TBL_DAMAGED_PIN
		WHERE 
		TO_DATE(substr(datetime,1,10), 'YYYY-MM-DD') > trunc(sysdate) - 7
		"""

def weekly_report():
    weekly = indio.Indio(config_file='indio.ini')
    message = weekly.execute_sql('count_logged_in_users_till_date',
	    USERS_LOGGED_IN_TILL_DATE)
    message += '\n\n'
    message += weekly.execute_sql('count_logged_in_users_this_week',
	    USERS_LOGGED_IN_THIS_WEEK)
    message += '\n\n'
    message += weekly.execute_sql('count_tp_planned_orders_this_week',
	    TP_PLANNED_ORDERS_THIS_WEEK)
    message += '\n\n'
    message += weekly.execute_sql('count_orders_this_week', ORDERS_THIS_WEEK)
    message += '\n\n'
    message += weekly.execute_sql('count_simswaps_this_week', SIM_SWAPS_THIS_WEEK)
    message += '\n\n'
    message += weekly.execute_sql('count_damaged_pins_this_week', DAMAGED_PIN_TXNS_THIS_WEEK)

    subject = "TPP Weekly Report - Week ending %s" % str(datetime.date.today())
    weekly.send_email(message, subject)


if __name__ == '__main__':
    weekly_report()
