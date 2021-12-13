SELECT 
PaymentID,AgentPaymentID,Number,PaySum,ProviderSum,StatusDate,
CAST([PaymentInfo].query('data(r/transactionid)') as nvarchar) transactionid ,
CAST([PaymentInfo].query('data(r/providerpaymentid)') as nvarchar) providerpaymentid ,
CAST([PaymentInfo].query('data(r/batchid)') as nvarchar) batchid
,ExtraParams

FROM gate211.dbo.Payment WHERE ServiceID in (323,324,325,326,556,1123)
 --(323,324,325)

and (StatusDate between '2021-11-01' and '2021-11-02') and Status =2
