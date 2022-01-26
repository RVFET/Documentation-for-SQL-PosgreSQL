select LEFT(pb.ID,10),pb.ServiceName, SUM(pb.PaySum) Amount,SUM(pb.ProviderSum) ProviderAmount,
SUM(pb.CommissionSum) CommissionAmount, SUM(pb.CardCommissionAmount) CardCommissionAmount, count(*)

 Count,
pb.Agent ,pb.ProviderName  
from (select 
  case when s.ProviderID=51 
  then Cast(p.OsmpProviderID as nvarchar(30))+
    CASE
     WHEN LEFT(p.Number, 2) in ('01','02','03','04','05','06','07','08','09','10','11','13','15','18','22','31','32','33','34','35','36','37','38','39','40',
    '41','42','43','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','65','66','67','68','69','70','71','72',
    '73','74','75','76','77','78','79','81','82','83','84','85','86') THEN N'01'
     WHEN LEFT(p.Number, 2) = '27' THEN N'02'
     WHEN LEFT(p.Number, 2) = '80' THEN N'05'
     WHEN LEFT(p.Number, 2) in ('28','29','44','64') THEN N'06'
     ELSE ' 00' END
  when p.ServiceID  in(291)
  then CASE WHEN p.PaySum<200 THEN 
    CAST(p.OsmpProviderID as nvarchar)+'200'
    ELSE CAST(p.OsmpProviderID as nvarchar) END
  when p.ServiceID in(312,1242)
  then CASE WHEN p.PaySum<500 THEN 
    CAST(p.OsmpProviderID as nvarchar)+'500'
    ELSE CAST(p.OsmpProviderID as nvarchar) END
  when p.ServiceID  in (254,255,257,258,259,260,261,262,263,264)
  then CAST(p.[PaymentInfo].query('data(r/id)') as nvarchar) 
  else CAST(p.OsmpProviderID as nvarchar) end  as ID 
,pp.ProviderName
, case when  s.ProviderID=51 
  then s.ServiceName+CASE 
    WHEN LEFT(p.Number, 2) in ('01','02','03','04','05','06','07','08','09','10','11','13','15','18','22','31','32','33','34','35','36','37','38','39','40',
    '41','42','43','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','65','66','67','68','69','70','71','72',
    '73','74','75','76','77','78','79','81','82','83','84','85','86') THEN N' Azersu ASC'
    WHEN LEFT(p.Number, 2) = '27' THEN N' Seki TSC'
    WHEN LEFT(p.Number, 2) = '80' THEN N' Gence TSC'
    WHEN LEFT(p.Number, 2) in ('28','29','44','64') THEN N' Birlesmis sukanal MMC'
    ELSE ' Unknown'END
  when p.ServiceID  in(291)
  then CASE WHEN p.PaySum<200 THEN s.ServiceName+' 200 az' ELSE s.ServiceName END 
  when p.ServiceID in(312,1242)
  then CASE WHEN p.PaySum<500 THEN 
    CAST(p.OsmpProviderID as nvarchar)+'500'
    ELSE CAST(p.OsmpProviderID as nvarchar) END
  when p.ServiceID  in (254,255,257,258,259,260,261,262,263,264)
  then CAST(p.[PaymentInfo].query('data(r/serviceName)') as nvarchar(MAX))
  else s.ServiceName end  ServiceName


,  case when p.ServiceID in(618)
	then  CAST(CAST (p.[PaymentInfo].query('data(root/paid)') as nvarchar) as float) 
	else p.PaySum end PaySum 
, 
--adding providersum to agent 17 and 18

CASE
    when CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) in ('17', '18')
	then 
	--checking null values
	case
	when sd.chargecommission is null or sd.purchasecommission is null
	then PaySum
	else PaySum - sd.chargecommission - sd.purchasecommission
	end
    when p.ServiceID in(618) 
	then CAST(CAST (p.[PaymentInfo].query('data(root/payable)') as nvarchar) as float)
	when  p.OsmpProviderID in (18106,18107)
	then (CAST(CAST (p.[PaymentInfo].query('data(root/debt)') as nvarchar) as float))
	when p.ServiceID  in (254,255)
    then p.[ProviderSum] - CAST(CAST(p.PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))
	else p.ProviderSum end ProviderSum
,
--adding cardcommissionsum to agent 17 and 18

CASE
when CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) in ('17', '18')
then CAST((CASE when sd.chargecommission is null then 0.00 else sd.chargecommission end) as float)
 else 0.00 end as CardCommissionAmount
,
--adding commissionsum to agent 17 and 18

CASE 
    when CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) in ('17', '18')
	then CAST((CASE when sd.purchasecommission is null then 0.00 else sd.purchasecommission end) as float)
	WHEN p.OsmpProviderID in (17217, 17218, 17219, 17220) THEN 1.00	  
	when p.ServiceID in(126,127)
	then CAST(CAST(p.[PayFields].query('data(fields/field4)') as nvarchar) as float) 
	when p.ServiceID in(355)
	then CAST(CAST (p.[PaymentInfo].query('data(r/qaliq)') as nvarchar) as float)
	when p.ServiceID in(618)
	then CAST(CAST (p.[PaymentInfo].query('data(root/residual)') as nvarchar) as float)
	when  p.ServiceID in(631,632,649)
	then (p.CommissionSum+CAST(CAST (p.[PaymentInfo].query('data(root/overpaid)') as nvarchar) as float))
	when pp.ProviderID = 135
	then 0.236
	when p.ServiceID  in (254,255)
    then (p.[CommissionSum] + CAST(CAST(p.PaymentInfo.query('data(r/overpaid)') as nvarchar) as decimal(7,2))) 
	when p.CommissionSum is null then 0.00
	ELSE p.CommissionSum  END AS CommissionSum

,CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) as  agent,

 ROW_NUMBER()OVER(PARTITION BY    case 
	  when len(CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar))>0
  then CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar) 
      when len( CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar) )>0 
  then CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar) 
   when len( CAST([ExtraParams].query('data(r/receipt_num)') as nvarchar) )>0 
  then CAST([ExtraParams].query('data(r/receipt_num)') as nvarchar)end, p.agentterminalid,p.serviceid ORDER BY (case 
	  when len(CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar))>0
  then CAST([ExtraParams].query('data(r/trm_prv_id)') as nvarchar) 
      when len( CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar) )>0 
  then CAST([ExtraParams].query('data(r/online_trm_prv_id)') as nvarchar) 
   when len( CAST([ExtraParams].query('data(r/receipt_num)') as nvarchar) )>0 
  then CAST([ExtraParams].query('data(r/receipt_num)') as nvarchar)end)) as rn

  FROM [DWHTEST].[dbo].[paymentupg] p with (nolock) 
join [DWHTEST].[dbo].gate_Service s with (nolock) on p.ServiceID=s.ServiceID join [DWHTEST].[dbo].gate_Provider pp with (nolock) on s.ProviderID=pp.ProviderID 

--joining sdk and upg through main base

join [DWHTEST].[dbo].[Paymentmain] m with (nolock) on p.AgentPaymentID = m.PaymentID left join [DWHTEST].[dbo].[sdk_provider_trnsaction] sd with (nolock) on m.TransactionID = sd.p_id

where (StatusDate between '2021-12-01' and '2022-01-01' ) 
and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) not in ( '3','10','14','20')
and p.Status=2 
)pb 
--where pb.rn=1

group by pb.ID, pb.ServiceName, pb.Agent ,pb.ProviderName

--adding kartdan balansin artirilmasi

UNION  all

SELECT s.[id] as ID,s.[servicename]  as ServiceName, s.[total] as Amount, s.[amount] as ProviderAmount,
s.[purchascomission] as CommissionAmount, s.[chargecomission] as CardCommissionAmount, s.[count ] as Count,
s.[agent] as Agent ,'MPAY MMC'  as ProviderName  

from [DWHTEST].[dbo].[sdk_report_by_services] s

where s.id = 1018

union all

--adding agent 20

SELECT LEFT(p.OsmpProviderId,10) as ID,
       s.ServiceName as ServiceName,
	   SUM(mm.mpaysum) as Amount,
	   SUM(mm.mpayprovsum) as ProviderAmount,
	   SUM(mm.mpaycommsum) as CommisionAmount,
	   0.00 as CardComissionAmount,
	   mm.count as Count,
	   '20' as Agent,
	   pp.ProviderName as ProviderName
from
(select [id_service],sum([sum_income]/100)mpaysum ,sum([sum_outcome]/100) mpayprovsum,
sum([sum_comm]/100)mpaycommsum,count(m.id_operation) as count from [DWHTEST].dbo.master m join [dbo].[work_legals] l on m.id_legal=l.id_legal
where state = 60       
       and substate = 0
       and time_process >= '2021-12-01' 
       and time_process < '2022-01-01' 
       and time_server >= DATEADD(DAY,-7,'2021-12-01')
       and time_server < DATEADD(DAY,+7,'2022-01-01' )   and l.id_legal=1  --or l.id_legal=23
group by [id_service]) mm 
left join [DWHTEST].[dbo].[Relationship] r
on mm.id_service=r.eManatID
 left join [DWHTEST].[dbo].[paymentupg] p
on p.OsmpProviderId=r.ModenisID 
 join [DWHTEST].[dbo].gate_Service s with (nolock) on p.ServiceID=s.ServiceID join [DWHTEST].[dbo].gate_Provider pp with (nolock) on s.ProviderID=pp.ProviderID 
 group by p.OsmpProviderID, s.ServiceName,pp.ProviderName,mm.count

order by pb.ProviderName,pb.ServiceName



