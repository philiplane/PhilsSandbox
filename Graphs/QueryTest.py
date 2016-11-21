# Testing Pyscopg to connect to database
#

import psycopg2

try:
    print ("Trying to connect..")
    conn = psycopg2.connect(host="*.*.*.*",
                            database=db,
                            user="*",
                            password="*")
except psycopg2.DatabaseError as dberr:
    print "DatabaseError: ", dberr

cur = conn.cursor()

try:
    cur.execute("""select command_type,
                    Count(case when c.channel_id=12 then 1 end) as Airbus,
                    Count(case when c.channel_id=14 then 1 end) as Inmarsat
                    from web_command cm
                    inner join web_communicator c on c.id = communicator_id
                    where status='COMPLETED' and c.channel_id=12 and sent_at > (now() - interval '1 day')
                    group by command_type
                    order by command_type""")
except psycopg2.DatabaseError as dberr:
    print "DatabaseError: ", dberr

rows = cur.fetchall()
#print "\nRows: \n"
for row in rows:
    print "   ", row[0],":", row[1]
