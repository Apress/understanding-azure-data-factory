CREATE TABLE [dbo].[DimProduct](
	[ProductKey] [int] IDENTITY(1,1) NOT NULL,
	[ProductAlternateKey] [varchar](255) NULL,
	[EnglishProductName] [varchar](255) NULL,
	[StandardCost] [decimal](18, 2) NULL,
	[Size] [int] NULL,
	[StartDate] [datetime] NULL,
	[EndDate] [datetime] NULL,
	[Status] [varchar](50) NULL
) 
GO