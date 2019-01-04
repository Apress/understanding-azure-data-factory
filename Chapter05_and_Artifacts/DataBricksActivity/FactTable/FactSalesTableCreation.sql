CREATE TABLE [dbo].[FactStoreSales](
	[SalesOrderID] [int] NULL,
	[StoreId] [int] NULL,
	[OrderDate] [date] NULL,
	[SubTotal] [decimal](18, 2) NULL,
	[Taxperc] [int] NULL,
	[TaxAmt] [decimal](18, 2) NULL,
	[Freightperc] [int] NULL,
	[Freight] [decimal](18, 2) NULL,
	[TotalDue] [decimal](18, 2) NULL,
	[SalesOrderDetailID] [int] NULL,
	[ProductKey] [bigint] NULL,
	[OrderQty] [int] NULL,
	[UnitPrice] [decimal](18, 2) NULL,
	[UnitPriceDiscount] [decimal](18, 2) NULL,
	[LineTotal] [decimal](18, 2) NULL
)