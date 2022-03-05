select StatusDate as PaymentCreateDate,OsmpProviderID, p.ProviderPaymentIDString,
AgentPaymentID as AzeriQazID, ReceiveDate, p."Number", PaySum, Status,ServiceID,
case 
when SUBSTR(split_part(extraparams,'<online_trm_prv_id>',2),0,11) != ''
then SUBSTR(split_part(extraparams,'<online_trm_prv_id>',2),0,11)
else SUBSTR(split_part(extraparams,'<trm_prv_id>',2),0,11) end trm_prv_id
--into test.Zenner_Modenis
	from reckon.gate_payment  p where ServiceID in ( 992)
and StatusDate Between '2022-02-01'and'2022-03-01'
  and status=2
