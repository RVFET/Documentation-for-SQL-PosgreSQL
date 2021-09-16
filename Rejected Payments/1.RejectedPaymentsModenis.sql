EXECUTE  [dbo].[GetNewPayment] 
 @Login = N'aqammadzadae'
,@PasswordMD5 = N'c2caea1c32db0492a967feb3743fb168'
,@DealerID=16 --5
  --,@TransactionID
  --,@PaymentID=189250177
  --,@ServiceID=1276
  --,@ProviderID
  ,@CreateTimeFrom='2021-06-01'
  ,@CreateTimeTo='2021-07-01'
  ,@Status=3
  ,@RetryStatus=1
  ,@PointType=1
  ,@RevokeStatus=1 --4
  --,@WithRetry=1
  --,@WithRevoke=1
  --,@IsRetried

GO
