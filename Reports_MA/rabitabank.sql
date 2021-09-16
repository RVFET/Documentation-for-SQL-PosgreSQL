select   [AgentPaymentID]
		,[ServiceName]
		,[MONTH]
		,[AgentTerminalID]
		,SUM([PaySum]) Sum
		,Count(*) Count
		,sessionid from 
(SELECT 
		[AgentPaymentID]  
		,s.[ServiceName]
		,MONTH(StatusDate) Month
		,[Number]
		,[AgentTerminalID]
		,[PaySum]
		,CAST([ExtraParams].query('data(r/sessionid)') as nvarchar) as sessionid
  FROM [dbo].[Payment] p 
  JOIN Service s ON s.ServiceID=p.ServiceID
	WHERE s.ProviderID in (63) and Status=2 
	and StatusDate between '2021-06-01' and '2021-06-02' 
	and CAST([ExtraParams].query('data(r/agt_id)') as nvarchar) <> '3'
	) a 
	GROUP BY MONTH
		,[AgentPaymentID]
		,[ServiceName]
		,[AgentTerminalID]
		,[sessionid];
