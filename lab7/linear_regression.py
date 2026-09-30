from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

spark = SparkSession.builder \
    .appName("LinearRegressionLab7") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("/tmp/house.csv")

print("== House Price Data ==")
df.show()

assembler = VectorAssembler(
    inputCols=["Area", "Bedrooms"],
    outputCol="features"
)

data = assembler.transform(df).select("features", "Price")

train, test = data.randomSplit([0.8, 0.2], seed=42)

lr = LinearRegression(
    featuresCol="features",
    labelCol="Price"
)

model = lr.fit(train)

print("Coefficients:", model.coefficients)
print("Intercept:", model.intercept)

predictions = model.transform(test)

print("== Predictions ==")
predictions.select(
    "features", "Price", "prediction"
).show()

evaluator = RegressionEvaluator(
    labelCol="Price",
    predictionCol="prediction",
    metricName="rmse"
)

rmse = evaluator.evaluate(predictions)

print("Root Mean Squared Error (RMSE):", rmse)

spark.stop()
