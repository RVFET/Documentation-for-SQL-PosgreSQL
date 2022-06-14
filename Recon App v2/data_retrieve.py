import streamlit as st
import pandas as pd
import psycopg2
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


@st.cache(allow_output_mutation=True)
def todataframe(result):
    resultpd = pd.DataFrame(result)
    resultpd.index += 1
    resultpd.to_numpy()
    return resultpd


@st.cache()
def to_excel(result):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    result.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


@st.cache()
def convert_df(result):
    result = result.to_csv(
        index=False, date_format='%Y/%m/%d %H:%M:%S', encoding='utf-8')
    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_mpay_provider(conn, providerId, startdate, enddate, statusM):

    if statusM == 'All':
        if providerId.iloc[0]['id_legal'] == 15:
            sql = """ SELECT m.id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number,b.value customer, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service left join work.operation_attributes b on m.id_operation = b.id_operation where time_server between %(startdate)s and %(enddate)s and b."name" = 'customer' and m.id_provider = %(providerId)s """

            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
        else:
            sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where time_server between %(startdate)s and %(enddate)s and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})

    elif statusM == 'Success':
        if providerId.iloc[0]['id_legal'] == 15:
            sql = """ SELECT m.id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number,b.value customer, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service left join work.operation_attributes b on m.id_operation = b.id_operation where state = 60 and substate = 0 and time_server between %(startdate)s and %(enddate)s and b."name" = 'customer' and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
        else:
            sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 60 and substate = 0 and time_server between %(startdate)s and %(enddate)s and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        if providerId.iloc[0]['id_legal'] == 15:
            sql = """ SELECT m.id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number,b.value customer, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service left join work.operation_attributes b on m.id_operation = b.id_operation where state = 80 and time_server between %(startdate)s and %(enddate)s and b."name" = 'customer' and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})
        else:
            sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 80 and time_server between %(startdate)s and %(enddate)s and m.id_provider = %(providerId)s """
            result = pd.read_sql(sql,
                                 conn, params={"providerId": str(providerId.iloc[0]['id_legal']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_mpay_service(conn, serviceId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate,  time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where time_server between  %(startdate)s and %(enddate)s and m.id_service =%(serviceid)s  """
        result = pd.read_sql(sql,
                             conn, params={"serviceid": str(serviceId.iloc[0]['id_service']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate,  time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 60 and substate = 0 and time_server between  %(startdate)s and %(enddate)s and m.id_service =%(serviceid)s  """
        result = pd.read_sql(sql,
                             conn, params={"serviceid": str(serviceId.iloc[0]['id_service']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate,  time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 80 and time_server between  %(startdate)s and %(enddate)s and m.id_service =%(serviceid)s  """
        result = pd.read_sql(sql,
                             conn, params={"serviceid": str(serviceId.iloc[0]['id_service']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_mpay_multiselect(conn, serviceId, startdate, enddate, statusM):
    s = ','.join([str(x) for x in serviceId['id_service'].unique().tolist()])
    if statusM == 'All':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where time_server between  %(startdate)s and %(enddate)s and m.id_service in ({}) """
        result = pd.read_sql(sql.format(s), conn, params={
                             "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 60 and substate = 0 and time_server between  %(startdate)s and %(enddate)s and m.id_service in ({}) """
        result = pd.read_sql(sql.format(s), conn, params={
                             "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT id_operation,provider_trans, id_point, account, account2, case when state = 60 then 'Ugurlu' when state = 80 then 'Ugursuz' when state = 40 then 'Novbede' end Status, substate, time_server, sum_income/100 as paysum, sum_outcome/100 as paysum_outcome, operation_number, ws.service_name FROM reckon.work_master m full join reckon.work_services ws on m.id_service = ws.id_service where state = 80 and time_server between  %(startdate)s and %(enddate)s and m.id_service in ({}) """
        result = pd.read_sql(sql.format(s), conn, params={
                             "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_provider(conn, providerId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """ SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and paydate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s  """
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """  SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s"""
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """  SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and a.ProviderID = %(providerId)s """
        result = pd.read_sql(sql, conn, params={
            "providerId": str(providerId.iloc[0]['providerid']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_service(conn, serviceId, startdate, enddate, statusM):
    if statusM == 'All':
        sql = """  SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid = %(serviceid)s  """
        result = pd.read_sql(sql, conn, params={
            "serviceid": str(serviceId.iloc[0]['serviceid']), "startdate": startdate, "enddate": enddate})

    return result


@with_connection
@st.cache(hash_funcs={psycopg2.extensions.connection: id}, allow_output_mutation=True)
def result_modenis_multiselect(conn, serviceId, startdate, enddate, statusM):
    s = ','.join([str(x) for x in serviceId['serviceid'].unique().tolist()])
    if statusM == 'All':
        sql = """ SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid in ({}) """
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})
    elif statusM == 'Success':
        sql = """ SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=2 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid in ({})"""
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})
    elif statusM == 'Rejected':
        sql = """ SELECT AgentPaymentID as agentpaymentid, case when ProviderPaymentIDString is null then concat((LEFT(cast(transactionid as varchar),10)),(RIGHT(concat('0000000000',cast(AgentTerminalID as varchar)),10))) else providerpaymentidstring end providerpaymentidstring,transactionid, p.ServiceID, statusdate, "Number" as number, AgentTerminalID as agentterminalid, PaySum as paysum,providersum,case when Status = 2 then 'Ugurlu' when Status = 3 then 'Ugursuz' when Status = 1 then 'Novbede' end Status, Agent,s.servicename,case when s.serviceid in ( 546,987,1242)   then SUBSTR(split_part(extraparams,'<sessionid>',2),0,8) when s.serviceid in (1237,1238,1239,1240,1251,1252,1253) then SUBSTR(split_part(extraparams,'<rabita_session>',2),0,8)  when s.serviceid = 1144 then SUBSTR(split_part(extraparams,'<xazri_sessionid>',2),0,20) when s.serviceid in ( 1021,1022) then cast(paymentid as varchar) when s.serviceid in (126,127,439,590,776,1120) then SUBSTR(split_part(extraparams,'<rrn>',2),0,10) else null end ExtraParam FROM reckon.gate_payment p join reckon.gate_service s on p.ServiceID=s.ServiceID join reckon.gate_provider a on a.ProviderID=s.ProviderID where status=3 and duplicate=1 and paydate  between %(startdate)s and %(enddate)s and p.serviceid in ({})"""
        result = pd.read_sql(sql.format(
            s), conn, params={"startdate": startdate, "enddate": enddate})

    return result
