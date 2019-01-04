CREATE PROCEDURE adfstoredprocactivity
AS
BEGIN

BEGIN TRANSACTION;  
BEGIN TRY 

--insert duplicate recrds into ERROR Table
Insert into All_Sales_Records_ERROR
  Select [SalesOrderID], [StoreId] ,[OrderDate],[SubTotal],[Taxperc],[TaxAmt],[Freightperc],[Freight],[TotalDue],[SalesOrderDetailID],[PName]
      ,[OrderQty],[UnitPrice],[UnitPriceDiscount],[LineTotal], 'Duplicate Record. In dataset by ' + Cast (number_times as varchar) + ' time' as remark from (
  SELECT *, ROW_NUMBER() 
   OVER (PARTITION BY SalesOrderId,StoreId,OrderDate,SalesOrderDetailID ORDER BY SalesOrderId,StoreId,OrderDate,SalesOrderDetailID desc) AS number_times 
   FROM [dbo].[All_Sales_Records_Raw]
   ) B Where B.number_times>1 

--Insert correct data into Production table 
Insert into All_Sales_Records_Production
  Select [SalesOrderID], [StoreId] ,[OrderDate],[SubTotal],[Taxperc],[TaxAmt],[Freightperc],[Freight],[TotalDue],[SalesOrderDetailID],[PName]
      ,[OrderQty],[UnitPrice],[UnitPriceDiscount],[LineTotal] from (
  SELECT *, ROW_NUMBER() 
   OVER (PARTITION BY SalesOrderId,StoreId,OrderDate,SalesOrderDetailID ORDER BY SalesOrderId,StoreId,OrderDate,SalesOrderDetailID desc) AS number_times 
   FROM [dbo].[All_Sales_Records_Raw]
   ) B Where B.number_times=1 

Truncate table [dbo].[All_Sales_Records_Raw]

END TRY  

BEGIN CATCH  
    SELECT   
         ERROR_NUMBER() AS ErrorNumber  
        ,ERROR_SEVERITY() AS ErrorSeverity  
        ,ERROR_STATE() AS ErrorState  
        ,ERROR_PROCEDURE() AS ErrorProcedure  
        ,ERROR_LINE() AS ErrorLine  
        ,ERROR_MESSAGE() AS ErrorMessage;  

    IF @@TRANCOUNT > 0  
        ROLLBACK TRANSACTION;  
END CATCH;  

IF @@TRANCOUNT > 0  
    COMMIT TRANSACTION;  
END
GO 
