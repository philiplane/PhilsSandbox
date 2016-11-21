# Query database for % communicators reporting into commservice in the last 24 hours, and update plotly

import datetime
import psycopg2
import plotly.plotly as py
import plotly.graph_objs as go

program_commands_query = """select Count(*)
                        from web_command cm
                        inner join web_communicator c on c.id = communicator_id
                        where status='COMPLETED'
                        and command_type = 'ProgramIntervalReporting'
                        and sent_at > (now() - interval '1 day')
                        and (c.channel_id=12 or c.channel_id=14)
                        group by command_type
                        order by command_type"""
communicators_reporting_query = """select
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
                        inner join web_communicator c on s.communicator_id = c.id"""
total_communicators_query = """select
                          count(case when protocol = 'Honeywell IsatM2M' then 1 end) as Honeywell,
                          count(case when protocol = 'Pole Star AIS' then 1 end) as AIS,
                          count(case when protocol = 'SatC (Thrane LES)' then 1 end) as SatC,
                          count(case when protocol = 'Skywave DAP-XML' then 1 end) as DAP,
                          count(case when protocol = 'Skywave IGWS' then 1 end) as IGWS
                          from communicator_reporting_status s
                          inner join web_communicator c on s.communicator_id = c.id
                          where c.id in (select communicator_id from web_subscriber)"""
reports = [[program_commands_query, 'ProgramCommand-graph'],
           [communicators_reporting_query, 'Comms-Nov16'],
           [total_communicators_query, 'TotalCommunicatorsInCommservice']]
network_name = ['Honeywell IsatM2M', 'AIS', 'Inmarsat-C', 'Skywave DAP-XML', 'Skywave IGWS']


def connect_to_database():
    try:
        conn = psycopg2.connect(host="10.11.30.101",
                                database="commservice",
                                user="postgres",
                                password="rh81dg5j")
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
        if filename == 'ProgramCommand-graph':
            trace = go.Scatter(x=[date_time_now], y=[row[0]])
            data = go.Data([trace])
        else:
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
