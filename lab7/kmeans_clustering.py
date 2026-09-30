from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

spark = SparkSession.builder \
    .appName("KMeansLab7") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("/tmp/customers.csv")

print("== Customer Data ==")
df.show()

assembler = VectorAssembler(
    inputCols=["Age", "AnnualIncome"],
    outputCol="features"
)

data = assembler.transform(df)

kmeans = KMeans(
    featuresCol="features",
    k=3,
    seed=42
)

model = kmeans.fit(data)

print("== Cluster Centers ==")
for center in model.clusterCenters():
    print(center)

predictions = model.transform(data)

print("== Cluster Assignments ==")
predictions.select(
    "CustomerID",
    "Age",
    "AnnualIncome",
    "prediction"
).show()

print("== Cluster Counts ==")
predictions.groupBy("prediction") \
    .count() \
    .orderBy("prediction") \
    .show()

spark.stop()
