import indio
import datetime

TP_PLANNED_ORDERS_COUNT = """ 
	SELECT 
	COUNT(DISTINCT(distributor_id))TP_PLANNED 
	FROM 
	tbl_order_dtls 
	WHERE 
	trunc(ordered_date) = trunc(sysdate)
	"""

ORDERS_COUNT = """
	SELECT 
	COUNT(*) PLANNED_ORDERS_COUNT 
	FROM 
	tbl_order_dtls od 
	WHERE 
	trunc(od.ORDERED_DATE) = trunc(sysdate)
	"""

TODAYS_ORDERS_APPROVED_TODAY_COUNT = """
	SELECT 
	COUNT(*) TODAYS_ORDERS_APPROVED 
	FROM tbl_order_dtls od
	WHERE 
	trunc(od.ORDERED_DATE) = trunc(sysdate)
	AND 
	trunc(od.LAST_UPDATED_DATE) = trunc(sysdate)
	AND 
	od.ifs_order_no <> 0
	"""

OLD_ORDERS_APPROVED_TODAY_COUNT = """
	SELECT 
	COUNT(*) PREVIOUS_ORDERS_APPROVED 
	FROM 
	tbl_order_dtls 
	WHERE 
	trunc(ORDERED_DATE) < trunc(sysdate)
	AND 
	trunc(LAST_UPDATED_DATE) = trunc(sysdate)
	AND 
	ifs_order_no <> 0
	"""

SIM_SWAPS_TXN_COUNT = """
	SELECT 
	COUNT(DISTINCT serialno) 
	FROM 
	tbl_simswap_trans 
	WHERE 
	trunc(transaction_date) = trunc(sysdate)
	"""

DAMAGED_PIN_TXN_COUNT = """
	SELECT 
	COUNT(*) DAMAGED_PIN 
	FROM 
	TBL_DAMAGED_PIN
	WHERE 
	TO_DATE(SUBSTR(datetime,1,10), 'YYYY-MM-DD') = trunc(sysdate)
	"""


def daily_report():
    daily = indio.Indio(config_file='indio.ini')
    message = daily.execute_sql('count_tp_planned_orders', TP_PLANNED_ORDERS_COUNT)
    message += '\n\n'
    message += daily.execute_sql('count_orders', ORDERS_COUNT)
    message += '\n\n'
    message += daily.execute_sql('count_orders_approved', TODAYS_ORDERS_APPROVED_TODAY_COUNT)
    message += '\n\n'
    message += daily.execute_sql('count_old_orders_approved', OLD_ORDERS_APPROVED_TODAY_COUNT)
    message += '\n\n'
    message += daily.execute_sql('count_simswaps', SIM_SWAPS_TXN_COUNT)
    message += '\n\n'
    message += daily.execute_sql('count_damaged_pins', DAMAGED_PIN_TXN_COUNT)

    subject = "TPP Daily Report - %s" % str(datetime.date.today())
    daily.send_email(message, subject)


if __name__ == '__main__':
    daily_report()
