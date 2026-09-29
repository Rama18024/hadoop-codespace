from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum, avg, col

spark = SparkSession.builder \
    .appName("EmployeeSalarySQL") \
    .master("local[*]") \
    .getOrCreate()

data = [
    (1, "Amit", "CSE", 50000),
    (2, "Riya", "IT", 62000),
    (3, "Rahul", "CSE", 55000),
    (4, "Neha", "IT", 71000),
    (5, "Ankit", "ECE", 48000),
    (6, "Simran", "CSE", 66000),
    (7, "Rohit", "ECE", 52000)
]

columns = ["Emp_ID", "Name", "Department", "Salary"]

df = spark.createDataFrame(data, columns)

print("== Employee Data ==")
df.show()

print("== Department-wise Salary Analysis ==")

dept_summary = df.groupBy("Department").agg(
    count("*").alias("Employee_Count"),
    sum("Salary").alias("Total_Salary"),
    avg("Salary").alias("Average_Salary")
)

dept_summary.show()

print("== Employees with Salary > 55000 ==")

high_earners = df.filter(col("Salary") > 55000)
high_earners.show()

spark.stop()
