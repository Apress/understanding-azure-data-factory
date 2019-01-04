from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HDISpark-ADF")\
    .enableHiveSupport()\
    .getOrCreate()

from pyspark.sql import *
from pyspark.sql.types import *
from pyspark.sql.functions import *

salesData = spark.read.csv('wasb://hdisparkactivity@adbooksparkstorage.blob.core.windows.net/All_Sales_Records.csv', header=True, inferSchema=True)

resultData = salesData.select(col('StoreId') , col('TotalDue') ).groupBy('StoreId').avg('TotalDue')

resultData.repartition(1).write.csv('wasb://hdisparkactivity@adbooksparkstorage.blob.core.windows.net/SalesAvg' , header=True)







