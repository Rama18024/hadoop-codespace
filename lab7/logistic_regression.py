from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

spark = SparkSession.builder \
    .appName("LogisticRegressionLab7") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("/tmp/student_pass.csv")

print("== Student Pass Data ==")
df.show()

assembler = VectorAssembler(
    inputCols=["StudyHours", "Attendance"],
    outputCol="features"
)

data = assembler.transform(df).select("features", "Pass")

train, test = data.randomSplit([0.8, 0.2], seed=42)

lr = LogisticRegression(
    featuresCol="features",
    labelCol="Pass"
)

model = lr.fit(train)

print("Coefficients:", model.coefficients)
print("Intercept:", model.intercept)

predictions = model.transform(test)

print("== Predictions ==")
predictions.select(
    "features", "Pass", "probability", "prediction"
).show(truncate=False)

evaluator = BinaryClassificationEvaluator(
    labelCol="Pass",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderROC"
)

auc = evaluator.evaluate(predictions)

print("Area Under ROC (AUC):", auc)

print("== Confusion Matrix ==")
predictions.groupBy("Pass", "prediction").count().orderBy("Pass", "prediction").show()

spark.stop()
