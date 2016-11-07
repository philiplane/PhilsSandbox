# Query database for number of ProgramIntervalReporting command sent in the last 24 hours, and update plotly

import datetime
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go


def connect_to_database():

    try:
        db = "commservice"
        # print "Connecting to:", db
        conn = psycopg2.connect(host="*.*.*.*",
                                database=db,
                                user="*",
                                password="*")
        return conn
    except psycopg2.DatabaseError as dberr:
        print "Connection error:", dberr


def run_query(connection):

    try:
        cur = connection.cursor()
        cur.execute("""select command_type,
                        Count(case when c.channel_id=12 then 1 end) as Airbus,
                        Count(case when c.channel_id=14 then 1 end) as Inmarsat
                        from web_command cm
                        inner join web_communicator c on c.id = communicator_id
                        where status='COMPLETED' and c.channel_id=12 and sent_at > (now() - interval '1 day')
                        group by command_type
                        order by command_type""")
        return cur.fetchall()
    except psycopg2.DatabaseError as query_err:
        print "Query error: ", query_err


def get_y_value(rows):
    y_value = -1
    for row in rows:
        if row[0] == "ProgramIntervalReporting":
            y_value = row[1]

    return y_value


def get_date():
    return str(datetime.date.today())


def update_plotly(x_value, y_value):
    trace0 = go.Scatter(x=[x_value], y=[y_value])
    data = go.Data([trace0])
    py.plot(data, filename='ProgramCommand-graph',  fileopt='extend')


def main():
    my_connection = connect_to_database()
    rows = run_query(my_connection)
    my_x_value = get_date()
    my_y_value = get_y_value(rows)
    print "Date:", my_x_value
    print "Commands sent:", my_y_value
    update_plotly(my_x_value, my_y_value)

main()
