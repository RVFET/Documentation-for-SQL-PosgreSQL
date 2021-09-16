Declare @DateFrom date
Declare @DateTo date
set @DateFrom = '2021-04-01'
set @DateTo = '2021-05-01'

SELECT AgentPaymentID, PaymentID, ProviderPaymentIDString, OsmpProviderID,
s.ServiceName,
case when len(CAST([ExtraParams].query('data(r/asanpaydate)') as nvarchar)) <> 0
then CAST([ExtraParams].query('data(r/asanpaydate)') as nvarchar) else AgentReceipteDate end AgentReceipteDate,
StatusDate,
CASE WHEN OsmpProviderID in (18106,18107) THEN PaySum ELSE CAST([PaymentInfo].query('data(root/debt)') as nvarchar(max)) END as PaySum,
Status, GateErrorMessage,
case when len(CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar)) <> 0
then
LEFT(CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar(10))+'00000',10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10)

when len(CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar)) <> 0
then
LEFT(CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar(10))+'00000',10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10)
else
LEFT(CAST([ExtraParams].query('data(r/online_txnid)') as nvarchar(10))+'00000',10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10) end transactionid,



LEFT(CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar(10))+'00000',10)+RIGHT('0000000000'+cast(AgentTerminalID as varchar(10)),10) as transactionid,
Number
FROM Payment p with(nolock) join Service s on p.ServiceID=s.ServiceID
WHERE p.GateServiceID in (635, 636,653,676,692,693,702,708,709,710,711,712,713,716,717,718,730, 731, 751,752,753,754,755,756,757,758,759,760,761,762,763,764, 768,882,883,884,885,886,887,888,889,971,1004,1020,1021,1035,1041,1076,1077,1078,1079,1080,1081,1082,1106, 1121, 1122)
and StatusDate BETWEEN @DateFrom and @DateTo
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
and PaySum>0.99
