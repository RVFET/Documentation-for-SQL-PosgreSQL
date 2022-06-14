import streamlit as st
import pandas as pd
import psycopg2


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




# Status Check


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gatePaymentAcc(conn, account, startdate, enddate):
    sql = """ SELECT p.paymentid FROM main.payment p, gate.payment p2 where p.paymentid = cast(p2.agentpaymentid as int) and p2."Number" = %(number)s and p2.paydate >= %(start)s and p2.paydate< %(end)s"""

    paymentSql = pd.read_sql(sql, conn, params={
                             "number": account, "start": startdate, "end": enddate})
    paymentid = []

    if len(paymentSql) == 0:
        pid = ''
    elif len(paymentSql) == 1:
        pid = paymentSql.iloc[0]['paymentid']
    else:
        for i in range(len(paymentSql)):
            paymentid.append(paymentSql.iloc[i]['paymentid'])
        paymentid = tuple(paymentid)
        pid = ', '.join([str(i) for i in paymentid])

    return pid


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gatePaymentTrnBulk(conn, trn, startdate, enddate):
    sql = """SELECT distinct paymentid FROM main.payment p where  statustime between %(start)s and %(end)s and transactionid in ({})"""
    paymentSql = pd.read_sql(sql.format(trn), conn, params={
        "start": startdate, "end": enddate})
    paymentid = []
    if len(paymentSql) == 0:
        pid = ''
    elif len(paymentSql) == 1:
        pid = paymentSql.iloc[0]['paymentid']
    else:

        for i in range(len(paymentSql)):
            paymentid.append(paymentSql.iloc[i]['paymentid'])

        paymentid = tuple(paymentid)
        pid = ', '.join([str(i) for i in paymentid])

    return pid


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayPaymentAcc(conn, account, startdate, enddate):
    sql = """SELECT distinct id_operation FROM reckon.work_master p where account = %(number)s and time_process between %(start)s and %(end)s"""
    paymentSql = pd.read_sql(sql, conn, params={
                             "number": account, "start": startdate, "end": enddate})
    paymentid = []

    if len(paymentSql) == 0:
        pid = ''
    elif len(paymentSql) == 1:
        pid = paymentSql.iloc[0]['id_operation']
    else:
        for i in range(len(paymentSql)):
            paymentid.append(paymentSql.iloc[i]['id_operation'])
        paymentid = tuple(paymentid)
        pid = ', '.join([str(i) for i in paymentid])

    return pid


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gateStatus(conn, paymentid):

    gateStatus = pd.read_sql(
        'SELECT Status FROM gate.payment p where AgentPaymentID in ({})'.format(paymentid), conn)
    status = []
    for i in range(len(gateStatus)):
        if gateStatus.iloc[i]['status'] == 1:
            statusa = 'Novbede'
        elif gateStatus.iloc[i]['status'] == 2:
            statusa = 'Ugurlu'
        elif gateStatus.iloc[i]['status'] == 3:
            statusa = 'Ugursuz'
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getDate(conn, paymentid):

    datex = pd.read_sql(
        'SELECT paydate FROM gate.payment p where AgentPaymentID in ({})'.format(paymentid), conn)

    return datex


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getPaymentId(conn, paymentid):

    payment = pd.read_sql(
        'SELECT distinct AgentPaymentID FROM gate.payment p where AgentPaymentID in ({})'.format(paymentid), conn)

    return payment


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mainStatus(conn, paymentid):
    mainStatus = pd.read_sql(
        'SELECT Status FROM main.payment p where PaymentID in ({})'.format(paymentid), conn)
    status = []
    for i in range(len(mainStatus)):
        if mainStatus.iloc[i]['status'] == 1:
            statusa = 'Novbede'
        elif mainStatus.iloc[i]['status'] == 2:
            statusa = 'Ugurlu'
        elif mainStatus.iloc[i]['status'] == 3:
            statusa = 'Ugursuz'
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def PortalComment(conn, paymentid):
    portalcomment = pd.read_sql(
        'SELECT portalcomment FROM main.payment p where PaymentID in ({})'.format(paymentid), conn)
    status = []
    for i in range(len(portalcomment)):
        statusa = portalcomment.iloc[i]['portalcomment']
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def gateStatusTRN(conn, transactionId, terminalId):
    sql = """ SELECT g.Status FROM main.payment p full join gate.payment g on p.paymentid = g.agentpaymentid where p.transactionid  = %(transactionId)s and p.pointid = %(terminalId)s """
    gateStatus = pd.read_sql(sql, conn, params={
                             "transactionId": transactionId, "terminalId": terminalId})
    status = ''

    if gateStatus.iloc[0]['status'] == 1:
        status = 'Novbede'
    elif gateStatus.iloc[0]['status'] == 2:
        status = 'Ugurlu'
    elif gateStatus.iloc[0]['status'] == 3:
        status = 'Ugursuz'
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getTRN(conn, transactionId, terminalId):
    mainTrn = pd.read_sql('SELECT transactionid FROM main.payment p where transactionid ={0} and pointid = {1}'.format(
        transactionId, terminalId), conn)

    return mainTrn


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def getTRNdate(conn, transactionId, terminalId):
    mainTrnDate = pd.read_sql('SELECT paytime FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
        "transactionId": transactionId, "terminalId": terminalId})

    return mainTrnDate


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mainStatusTRN(conn, transactionId, terminalId):
    mainStatus = pd.read_sql('SELECT Status FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
                             "transactionId": transactionId, "terminalId": terminalId})
    status = ''
    if mainStatus.iloc[0]['status'] == 1:
        status = 'Novbede'
    elif mainStatus.iloc[0]['status'] == 2:
        status = 'Ugurlu'
    elif mainStatus.iloc[0]['status'] == 3:
        status = 'Ugursuz'
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def PortalCommentTRN(conn, transactionId, terminalId):
    portalcomment = pd.read_sql('SELECT portalcomment FROM main.payment p where transactionid = %(transactionId)s and pointid = %(terminalId)s', conn, params={
                                "transactionId": transactionId, "terminalId": terminalId})
    return portalcomment.iloc[0]['portalcomment']


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayIdOper(conn, mpayid):
    mpayID = pd.read_sql(
        'SELECT id_operation FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)

    return mpayID


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayDate(conn, mpayid):
    mpayDt = pd.read_sql(
        'SELECT time_server FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)

    return mpayDt


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayStatus(conn, mpayid):
    mpaystatus = pd.read_sql(
        'SELECT state FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)
    status = []
    for i in range(len(mpaystatus)):
        if mpaystatus.iloc[i]['state'] == 40:
            statusa = 'Novbede'
        elif mpaystatus.iloc[i]['state'] == 60:
            statusa = 'Ugurlu'
        elif mpaystatus.iloc[i]['state'] == 80:
            statusa = 'Ugursuz'
        status.append(statusa)
    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpaySubstatus(conn, mpayid):
    mpaystatus = pd.read_sql(
        'SELECT substate FROM reckon.work_master p where id_operation in ({})'.format(mpayid), conn)
    status = []
    for i in range(len(mpaystatus)):
        if mpaystatus.iloc[i]['substate'] == 0:
            statusa = 'Ugurlu'
        elif mpaystatus.iloc[i]['substate'] == 1:
            statusa = 'Cancelled by user / Istifadeci terefinden legv edildi'
        elif mpaystatus.iloc[i]['substate'] == 2:
            statusa = 'Funds return / Vesait geri qaytarilib'
        elif mpaystatus.iloc[i]['substate'] == 3:
            statusa = 'Cancelled by support / Destek terefinden legv edilib'
        elif mpaystatus.iloc[i]['substate'] == 5:
            statusa = 'Rejected by provider / Provayder terefinden redd edilib'
        elif mpaystatus.iloc[i]['substate'] == 6:
            statusa = 'Corrected / Duzelis edilib'
        elif mpaystatus.iloc[i]['substate'] == 12:
            statusa = 'Blocked by user  / Istifadeci terefinden bloklanib'
        elif mpaystatus.iloc[i]['substate'] == 7:
            statusa = 'Uncorrectable error / Duzelish edilmeyen xeta'
        else:
            statusa = 'None'

        status.append(statusa)

    return status


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def mpayComment(conn, mpayid):
    id_oper = pd.read_sql(
        'SELECT id_operation FROM reckon.work_master where id_operation in ({})'.format(mpayid), conn)
    status = []

    for i in range(len(id_oper)):
        mpaycomment = pd.read_sql(
            'SELECT  "comment" FROM reckon.work_operation_comments where id_operation = {}'.format(id_oper.iloc[i]['id_operation']), conn)
        if len(mpaycomment) == 0:
            statusa = 'None'
        else:
            statusa = mpaycomment.iloc[0]['comment']
        status.append(statusa)

    return status
