from datetime import datetime
import streamlit as st
import psycopg2
import psycopg2.extras as extras
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table


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


# Email module


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def send_email(sender, mail_receiver, cc, body, subject, kochurme_sum,  df):
    mail_receiver = str(mail_receiver)
    if cc is not None:
        cc = str(cc)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = mail_receiver
    if cc is not None:
        message["CC"] = cc

    html = """\
<html>
  <body>
    <p>
    %s
    </p>
    <p>
    Yekun:
    </p>

    %s

    <p>
    Yekun kochurme mbelegi: %s azn
    </p>

  </body>
</html>
 """ % (body,  build_table(df, 'blue_light'), kochurme_sum)

    part2 = MIMEText(html, "html")

    message.attach(part2)
    toaddr = []

    if ',' in mail_receiver:
        mail_receiver = mail_receiver.split(',')
        for i in mail_receiver:
            toaddr.append(i)

    elif ',' not in mail_receiver:
        toaddr.append(mail_receiver)

    if cc is not None:
        if ',' in cc:
            cc = cc.split(',')
            for i in cc:
                toaddr.append(i)
        else:
            toaddr.append(cc)
    else:
        toaddr = toaddr
    with smtplib.SMTP(host='172.23.0.15', port=25) as server:
        server.sendmail(
            sender, toaddr, message.as_string()
        )


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table(df):
    mydate = datetime.now()
    month = mydate.strftime("%B")
    commands = (
        """
        DROP TABLE IF EXISTS public.modenis_email_file_{0}
        """.format(month),
        """
        CREATE TABLE public.modenis_email_file_{0} (
            osmpproviderid int4 PRIMARY KEY,
            providername varchar(500),
            servicename varchar(500),
            ProviderAmount float,
            Count int4
        )
        """.format(month)


    )
    conn = None
    table = 'public.modenis_email_file_{0}'.format(month)
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

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def create_table_mpay(df):
    mydate = datetime.now()
    month = mydate.strftime("%B")
    commands = (
        """
        DROP TABLE IF EXISTS public.mpay_email_file_{0}
        """.format(month),
        """
        CREATE TABLE public.mpay_email_file_{0} (
            id_service int4 PRIMARY KEY,
            name_legal varchar(500),
            service_name varchar(500),
            ProviderAmount float,
            Count int4
        )
        """.format(month)


    )
    conn = None
    table = 'public.mpay_email_file_{0}'.format(month)
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

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_single(osmpId, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.modenis_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s , cc = %(cc)s where osmpproviderid = {}"""
    cursor.execute(sql.format(osmpId[0]), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_double(osmpId, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.modenis_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s , cc = %(cc)s where osmpproviderid in {}"""
    cursor.execute(sql.format(osmpId), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_single_mpay(id_service, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.mpay_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s, cc=%(cc)s where id_service = {}"""
    cursor.execute(sql.format(id_service[0]), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()


@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def update_double_mpay(id_service, subject, mail_receiver, cc, body, comment, is_prv, conn):
    DSN = "dbname='DWH' user='acavidan' host='172.20.10.181' port='5432' password='dwh@2022!@'"
    conn = psycopg2.connect(DSN)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """ UPDATE public.mpay_email SET subject = %(subject)s , mail_receiver=%(mail_receiver)s , body=%(body)s , "comment"=%(comment)s , is_prv=%(is_prv)s, cc=%(cc)s where id_service in {}"""
    cursor.execute(sql.format(id_service), {"subject": subject,
                   "mail_receiver": mail_receiver, "body": body, "comment": comment, "is_prv": is_prv, "cc": cc})

    conn.commit()

    conn.close()
