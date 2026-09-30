from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder \
    .appName("DecisionTreeLab7") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("/tmp/iris.csv")

print("== Iris Data ==")
df.show()

assembler = VectorAssembler(
    inputCols=[
        "SepalLength",
        "SepalWidth",
        "PetalLength",
        "PetalWidth"
    ],
    outputCol="features"
)

data = assembler.transform(df).select("features", "Species")

train, test = data.randomSplit([0.7, 0.3], seed=42)

dt = DecisionTreeClassifier(
    featuresCol="features",
    labelCol="Species",
    maxDepth=5
)

model = dt.fit(train)

predictions = model.transform(test)

print("== Predictions ==")
predictions.select(
    "features",
    "Species",
    "prediction"
).show(truncate=False)

evaluator = MulticlassClassificationEvaluator(
    labelCol="Species",
    predictionCol="prediction",
    metricName="accuracy"
)

accuracy = evaluator.evaluate(predictions)

print("Accuracy:", accuracy)

print("== Feature Importances ==")
print(model.featureImportances)

spark.stop()
