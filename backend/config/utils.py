import traceback
from django.db import connections
from collections import namedtuple

def raw_sql_select(query, connection):
  cn = connections[connection].cursor()
  cn.execute(query)
  fields = cn.description
  rows = cn.fetchall()
  resultFields = namedtuple("resultFields", [col[0] for col in fields])
  finalResult = [resultFields(*row) for row in rows]
  return [fields, finalResult]

def raw_sql_select_enhanced(query, connection, values):
  cn = connections[connection].cursor()
  cn.execute(query, values)
  fields = cn.description
  rows = cn.fetchall()
  resultFields = namedtuple("resultFields", [col[0] for col in fields])
  finalResult = [resultFields(*row) for row in rows]
  return [fields, finalResult]

def raw_sql_insert(query, connection, values):
	cn = connections[connection].cursor()
	try:
		cn.execute(query, values)
		return True
	except Exception as e:
		traceback.print_exc()
		return False

def raw_sql_update(query, connection, values):
	cn = connections[connection].cursor()
	try:
		cn.execute(query, values)
		return True
	except Exception as e:
		traceback.print_exc()
		return False

def raw_sql_destroy(query, connection, values):
	cn = connections[connection].cursor()
	try:
		cn.execute(query, values)
		return True
	except Exception as e:
		traceback.print_exc()
		return False

def raw_sql_commit(connection):
	cn = connections[connection].cursor()
	try:
		cn.execute('COMMIT; END TRANSACTION;')
		return True
	except Exception as e:
		traceback.print_exc()
		return False
	return False

def raw_sql_rollback(connection):
	cn = connections[connection].cursor()
	try:
		cn.execute('ROLLBACK; END TRANSACTION;')
		return True
	except Exception as e:
		traceback.print_exc()
		return False
	return False