# Query database for % communicators reporting into cas in the last 24 hours, and update plotly

import datetime
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go


def connect_to_database():

    try:
        db = "commservice"
        # print "Connecting to:", db
        conn = psycopg2.connect(host="*",
                                database=db,
                                user="*",
                                password="*")
        return conn
    except psycopg2.DatabaseError as dberr:
        print "Connection error: ", dberr


def run_query(connection):

    cur = connection.cursor()

    try:
        cur.execute("""select
                          count(case when protocol = 'Honeywell IsatM2M' then 1 end) as Honeywell,
                          count(case when protocol = 'Pole Star AIS' then 1 end) as AIS,
                          count(case when protocol = 'SatC (Thrane LES)' then 1 end) as SatC,
                          count(case when protocol = 'Skywave DAP-XML' then 1 end) as DAP,
                          count(case when protocol = 'Skywave IGWS' then 1 end) as IGWS
                          from communicator_reporting_status s
                          inner join web_communicator c on s.communicator_id = c.id
                          where c.id in (select communicator_id from web_subscriber)""")
    except psycopg2.DatabaseError as query_err:
        print "Query error: ", query_err

    return cur.fetchall()


def get_y_value(rows):
    column = -1
    for row in rows:
        for column in row:
            print column
    return column


def get_date():
    return str(datetime.datetime.now())


def update_plotly(x_value, rows):
    print "Date:", x_value
    for row in rows:
        print "Y values:", row
        trace0 = go.Scatter(x=[x_value], y=[row[0]], name='Honeywell IsatM2M')
        trace1 = go.Scatter(x=[x_value], y=[row[1]], name='AIS')
        trace2 = go.Scatter(x=[x_value], y=[row[2]], name='Inmarsat-C')
        trace3 = go.Scatter(x=[x_value], y=[row[3]], name='Skywave DAP-XML')
        trace4 = go.Scatter(x=[x_value], y=[row[4]], name='Skywave IGWS')
        data = go.Data([trace0, trace1, trace2, trace3, trace4])
        py.plot(data, filename='TotalCommunicatorsInCommservice', fileopt='extend')


def main():
    my_connection = connect_to_database()
    rows = run_query(my_connection)
    my_x_value = get_date()
    update_plotly(my_x_value, rows)

main()
