from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("DeptAverageRDD").getOrCreate()
sc = spark.sparkContext

lines = sc.textFile("hdfs://172.18.0.1:9000/user/lab6/input/student.csv")

def parse(line):
    fields = line.split(",")
    if len(fields) < 4 or fields[0] == "Student_ID":
        return None
    try:
        return (fields[2], (float(fields[3]), 1))
    except ValueError:
        return None

pairs = lines.map(parse).filter(lambda x: x is not None)

totals = pairs.reduceByKey(
    lambda a, b: (a[0] + b[0], a[1] + b[1])
)

averages = totals.mapValues(lambda v: v[0] / v[1])

print("== Department-wise Student Count & Average Marks ==")

for dept, (total, count) in totals.collect():
    avg = total / count
    print(f"{dept}: Count = {count}, Average Marks = {avg:.2f}")

spark.stop()
