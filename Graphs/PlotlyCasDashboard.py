# Query database for % communicators reporting into cas in the last 24 hours, and update plotly

import datetime
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go


def connect_to_database():

    try:
        db = "cas"
        # print "Connecting to:", db
        conn = psycopg2.connect(host="10.11.30.101",
                                database=db,
                                user="postgres",
                                password="rh81dg5j")
        return conn
    except psycopg2.DatabaseError as dberr:
        print "Connection error: ", dberr


def run_query(connection):

    cur = connection.cursor()

    try:
        cur.execute("""select
                        concat((count
                         (case when (ms.channel_uri = '/api/v1/channel/21') and (last_position_timestamp_gnss > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (ms.channel_uri = '/api/v1/channel/21') then 1 end)),'%')
                         as Honeywell,
                        concat((count
                         (case when (ms.channel_uri = '/api/v1/channel/13') and (last_position_timestamp_gnss > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (ms.channel_uri = '/api/v1/channel/13') then 1 end)),'%')
                         as AIS,
                        concat((count
                         (case when (ms.channel_uri = '/api/v1/channel/12' or ms.channel_uri = '/api/v1/channel/14') and (last_position_timestamp_gnss > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (ms.channel_uri = '/api/v1/channel/12' or ms.channel_uri = '/api/v1/channel/14') then 1 end)),'%')
                         as SatC,
                        concat((count
                         (case when (ms.channel_uri = '/api/v1/channel/17' or ms.channel_uri = '/api/v1/channel/23') and (last_position_timestamp_gnss > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (ms.channel_uri = '/api/v1/channel/17' or ms.channel_uri = '/api/v1/channel/23') then 1 end)),'%')
                         as IsatM2M,
                        concat((count
                         (case when (ms.channel_uri = '/api/v1/channel/15' or ms.channel_uri = '/api/v1/channel/22' or ms.channel_uri = '/api/v1/channel/27') and (last_position_timestamp_gnss > (current_timestamp - interval '24 hours')) then 1 end))
                         * 100
                         / (count(case when (ms.channel_uri = '/api/v1/channel/15' or ms.channel_uri = '/api/v1/channel/22' or ms.channel_uri = '/api/v1/channel/27')then 1 end)),'%')
                         as IsatDataPro
                        from mobile_subscription ms
                        inner join subscription s on s.id = ms.subscription_id
                        inner join ship sh on sh.id = s.ship_id
                        inner join account a on sh.account_id = a.id
                        where ms.status='ACTIVE'
                        and a.company_name not ilike '%trial%'""")
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
        py.plot(data, filename='CAS-Nov16', fileopt='extend')


def main():
    my_connection = connect_to_database()
    rows = run_query(my_connection)
    my_x_value = get_date()
    update_plotly(my_x_value, rows)

main()
