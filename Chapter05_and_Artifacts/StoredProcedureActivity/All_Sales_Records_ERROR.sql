SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[All_Sales_Records_ERROR](
	[SalesOrderID] [int] NULL,
	[StoreId] [int] NULL,
	[OrderDate] [date] NULL,
	[SubTotal] [decimal](18, 0) NULL,
	[Taxperc] [int] NULL,
	[TaxAmt] [decimal](18, 0) NULL,
	[Freightperc] [int] NULL,
	[Freight] [decimal](18, 0) NULL,
	[TotalDue] [decimal](18, 0) NULL,
	[SalesOrderDetailID] [int] NULL,
	[PName] [varchar](max) NULL,
	[OrderQty] [int] NULL,
	[UnitPrice] [decimal](18, 0) NULL,
	[UnitPriceDiscount] [decimal](18, 0) NULL,
	[LineTotal] [decimal](18, 0) NULL,
	[Remark] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

