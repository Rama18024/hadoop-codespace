from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("LogFileAnalysis") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext

# Read log file
lines = sc.textFile("/tmp/access.log")

# -------------------------------
# 1. Count requests per IP
# -------------------------------

ip_counts = (
    lines
    .map(lambda line: line.split()[0])
    .map(lambda ip: (ip, 1))
    .reduceByKey(lambda a, b: a + b)
)

print("== Request Count per IP ==")

for ip, count in ip_counts.collect():
    print(f"{ip}: {count}")

# -------------------------------
# 2. Top 5 visitors
# -------------------------------

top_visitors = ip_counts \
    .map(lambda x: (x[1], x[0])) \
    .sortByKey(ascending=False) \
    .take(5)

print("\n== Top 5 Visitors ==")

for count, ip in top_visitors:
    print(f"{ip}: {count} requests")

# -------------------------------
# 3. Count HTTP status codes
# -------------------------------

status_counts = (
    lines
    .map(lambda line: line.split()[-1])
    .map(lambda status: (status, 1))
    .reduceByKey(lambda a, b: a + b)
)

print("\n== HTTP Status Code Counts ==")

for status, count in status_counts.collect():
    print(f"{status}: {count}")

spark.stop()
