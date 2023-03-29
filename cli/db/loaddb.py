from cli.loger import main_logger


def get_events_loaddb(name: str, con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT  full_description, display_name, event_description_id, time \
    FROM (SELECT * FROM tsk_event_descriptions tes \
    INNER JOIN tsk_events te on tes.event_description_id = te.event_description_id \
    INNER JOIN tsk_event_types tet on te.event_type_id = tet.event_type_id) \
    WHERE full_description like '/etc%' and full_description not like '%/usr/share%' \
    ORDER BY time DESC".format(name))
  return res.fetchall()


def input_values_contentdb(name: str, values ,con):
  cur = con.cursor()
  main_logger.debug('Inserting values into Database: {0}_loaddb_events'.format(name))
  cur.executemany("INSERT INTO {0}_loaddb_events VALUES(?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()
 