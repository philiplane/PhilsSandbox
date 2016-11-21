# Query database for % communicators reporting into cas in the last 24 hours, and update plotly

import datetime
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go

communicators_reporting_query = """select
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
                        and a.company_name not ilike '%trial%'"""
total_communicators_query = """select
                         count(case when ms.channel_uri = '/api/v1/channel/21' then 1 end) as Honeywell,
                         count(case when ms.channel_uri = '/api/v1/channel/13' then 1 end) as AIS,
                         count(case when ms.channel_uri = '/api/v1/channel/12' or ms.channel_uri = '/api/v1/channel/14' then 1 end) as SatC,
                         count(case when ms.channel_uri = '/api/v1/channel/17' or ms.channel_uri = '/api/v1/channel/23' then 1 end) as DAP,
                         count(case
                          when ms.channel_uri = '/api/v1/channel/15'
                          or ms.channel_uri = '/api/v1/channel/22'
                          or ms.channel_uri = '/api/v1/channel/27'
                          then 1 end) as IGWS
                        from mobile_subscription ms
                        inner join subscription s on s.id = ms.subscription_id
                        inner join ship sh on sh.id = s.ship_id
                        inner join account a on sh.account_id = a.id
                        where ms.status='ACTIVE'
                         and a.company_name not ilike '%trial%' """
reports = [[communicators_reporting_query, 'CAS-Nov16'],
           [total_communicators_query, 'TotalCommunicatorsInCAS']]
network_name = ['Honeywell IsatM2M', 'AIS', 'Inmarsat-C', 'Skywave DAP-XML', 'Skywave IGWS']


def connect_to_database():
    try:
        conn = psycopg2.connect(host="*.*.*.*",
                                database="cas",
                                user="*",
                                password="*")
        return conn
    except psycopg2.DatabaseError as dberr:
        print "Connection error: ", dberr


def run_query(connection, query):

    cur = connection.cursor()

    try:
        cur.execute(query)
        return cur.fetchall()
    except psycopg2.DatabaseError as query_err:
        print "Query error: ", query_err


def update_plotly(rows, filename):
    date_time_now = str(datetime.datetime.now())
    print "Date & time:", date_time_now
    for row in rows:
        print "Query data:", row
        trace = []
        for n in range(0, 5):
            trace.append(go.Scatter(x=[date_time_now], y=[row[n]], name=network_name[n]))
        data = go.Data([trace[0], trace[1], trace[2], trace[3], trace[4]])
        done = py.plot(data, filename=filename, fileopt='extend')
        print "Plotly response:", done
    return


def main():
    db_connection = connect_to_database()
    for report_info in reports:
        query_response = run_query(db_connection, report_info[0])
        update_plotly(query_response, report_info[1])

main()
