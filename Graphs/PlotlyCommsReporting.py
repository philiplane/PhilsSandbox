# Query database for % communicators reporting into commservice in the last 24 hours, and update plotly

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
                        concat((count
                         (case when (protocol = 'Honeywell IsatM2M') and (last_timestamp > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (protocol = 'Honeywell IsatM2M') and (c.id in (select communicator_id from web_subscriber)) then 1 end)),'%')
                         as Honeywell,
                        concat((count
                         (case when (protocol = 'Pole Star AIS') and (last_timestamp > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (protocol = 'Pole Star AIS') and (c.id in (select communicator_id from web_subscriber)) then 1 end)),'%')
                         as AIS,
                        concat((count
                         (case when (protocol = 'SatC (Thrane LES)') and (last_timestamp > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (protocol = 'SatC (Thrane LES)') and (c.id in (select communicator_id from web_subscriber)) then 1 end)),'%')
                         as SatC,
                        concat((count
                         (case when (protocol = 'Skywave DAP-XML') and (last_timestamp > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (protocol = 'Skywave DAP-XML') and (c.id in (select communicator_id from web_subscriber)) then 1 end)),'%')
                         as IsatM2M,
                        concat((count
                         (case when (protocol = 'Skywave IGWS') and (last_timestamp > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (protocol = 'Skywave IGWS') and (c.id in (select communicator_id from web_subscriber)) then 1 end)),'%')
                         as IsatDataPro
                        from communicator_reporting_status s
                        inner join web_communicator c on s.communicator_id = c.id""")
    except psycopg2.DatabaseError as query_err:
        print "Query error:", query_err

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
        py.plot(data, filename='Comms-Nov16', fileopt='extend')


def main():
    my_connection = connect_to_database()
    rows = run_query(my_connection)
    my_x_value = get_date()
    update_plotly(my_x_value, rows)

main()
