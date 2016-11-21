# Query database for number of ProgramIntervalReporting commands sent in the last 24 hours, and update plotly

import datetime
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go


my_query = """select Count(*)
                        from web_command cm
                        inner join web_communicator c on c.id = communicator_id
                        where status='COMPLETED'
                        and command_type = 'ProgramIntervalReporting'
                        and sent_at > (now() - interval '1 day')
                        and (c.channel_id=12 or c.channel_id=14)
                        group by command_type
                        order by command_type"""


def connect_to_database():

    try:
        db = "commservice"
        conn = psycopg2.connect(host="*",
                                database=db,
                                user="*",
                                password="*")
        return conn
    except psycopg2.DatabaseError as dberr:
        print "Connection error:", dberr


def run_query(connection):
    try:
        cur = connection.cursor()
        cur.execute(my_query)
        for row in cur.fetchall():
            print "Program commands sent:", row[0]
            trace0 = go.Scatter(x=[str(datetime.datetime.now())], y=[row[0]])
        return go.Data([trace0])
    except psycopg2.DatabaseError as query_err:
        print "Query error: ", query_err


def update_plotly(data, filename):
        py.plot(data, filename=filename,  fileopt='extend')


def main():
    my_connection = connect_to_database()
    data = run_query(my_connection)
    #update_plotly(data, 'ProgramCommand-graph')

main()
