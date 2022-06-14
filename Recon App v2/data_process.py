import streamlit as st
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from io import BytesIO


@st.cache(allow_output_mutation=True)
def with_connection(func):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"

    def connection(*args, **kwargs):
        # Here, you may even use a connection pool
        conn = psycopg2.connect(DSN)
        try:
            rv = func(conn, *args, **kwargs)
        except Exception as e:
            conn.rollback()
            raise e
        else:
            # Can decide to see if you need to commit the transaction or not
            conn.commit()
        finally:
            conn.close()
        return rv
    return connection


# Compare Module


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_modenis_emanat(startdate, enddate, serviceid):

    if isinstance(serviceid, tuple):
        commands = (
            """ DROP TABLE IF EXISTS public.compare_emanat_{0}
        """.format(serviceid[0]),
            """ select "Number" as number,statusdate,paysum into public.compare_emanat_{0} from reckon.gate_payment where duplicate = 1 and statusdate between '{1}' and '{2}' and status = 2 and serviceid in {3}
        """.format(serviceid[0], startdate, enddate, serviceid)
        )

    else:
        commands = (
            """ DROP TABLE IF EXISTS public.compare_emanat_{0}
        """.format(serviceid),
            """ select "Number" as number,statusdate,paysum into public.compare_emanat_{0} from reckon.gate_payment where duplicate = 1 and statusdate between '{1}' and '{2}' and status = 2 and serviceid = {3}
        """.format(serviceid, startdate, enddate, serviceid)


        )

    conn = None

    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_modenis(df, serviceid):
    if isinstance(serviceid, tuple):
        serviceid = serviceid[0]
    else:
        serviceid = serviceid

    commands = (
        """
        DROP TABLE IF EXISTS public.compare_prv_{0}
        """.format(serviceid),
        """
        CREATE TABLE public.compare_prv_{0} (
            number varchar(500),
            statusdate timestamp(500),
            paysum numeric(20,2)
            
        )
        """.format(serviceid)


    )

    conn = None
    table = 'public.compare_prv_{0}'.format(serviceid)
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        extras.execute_values(cur, query, tuples)
        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_mpay_emanat(startdate, enddate, serviceid):

    if isinstance(serviceid, tuple):
        commands = (
            """ DROP TABLE IF EXISTS public.compare_mpay_{0}
        """.format(serviceid[0]),
            """ select account, time_server, sum_income/100 as paysum into public.compare_mpay_{0} from reckon.work_master where time_server between '{1}' and '{2}' and state = 60 and substate = 0 and id_service in {3}
        """.format(serviceid[0], startdate, enddate, serviceid)
        )

    else:
        commands = (
            """ DROP TABLE IF EXISTS public.compare_mpay_{0}
        """.format(serviceid),
            """ select account, time_server, sum_income/100 as paysum into public.compare_mpay_{0} from reckon.work_master where time_server between '{1}' and '{2}' and state = 60 and substate = 0 and id_service = {3}
        """.format(serviceid, startdate, enddate, serviceid)


        )

    conn = None

    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_account_mpay(df, serviceid):
    if isinstance(serviceid, tuple):
        serviceid = serviceid[0]
    else:
        serviceid = serviceid

    commands = (
        """
        DROP TABLE IF EXISTS public.compare_mpay_prv_{0}
        """.format(serviceid),
        """
        CREATE TABLE public.compare_mpay_prv_{0} (
            account varchar(500),
            time_server timestamp(500),
            paysum numeric(20,2)
            
        )
        """.format(serviceid)


    )

    conn = None
    table = 'public.compare_mpay_prv_{0}'.format(serviceid)
    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ','.join(list(df.columns))
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    try:
        params = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
        conn = psycopg2.connect(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        extras.execute_values(cur, query, tuples)
        cur.close()
        conn.commit()
        print('inserted successfully')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_to_excel_multiple(df1, df2, df3, df4, df5):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name="Modenisde_var_prvda_yox")
        df2.to_excel(writer, sheet_name="Prvda_var_modenisde_yox")
        df3.to_excel(writer, sheet_name="Dublikatlar")
        df4.to_excel(writer, sheet_name="Qaytarilmish_odenishler")
        df5.to_excel(writer, sheet_name="Final")

    writer.save()
    processed_data = output.getvalue()
    return processed_data
