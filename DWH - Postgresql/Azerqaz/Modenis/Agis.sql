SELECT --top 120-- AzerQazDirect 
p.OsmpProviderID,
p.AgentPaymentID as AzeriQazID, p.ReceiveDate, p."Number", p.PaySum, p.Status
  INTO   test.Agis_Modenis
  FROM   reckon.gate_payment p
where  ServiceID = 275 and 
  StatusDate Between '2022-02-01'and'2022-03-01'
    order by agentdate
