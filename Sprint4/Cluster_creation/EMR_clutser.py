
'''
mkdir ~/sample-data
echo -e "apple\nbanana\napple\norange\nbanana\napple" > ~/sample-data/fruit.txt
nano ~/wordcount.py
spark-submit wordcount.py
these steps i have done inside ssh EMR

'''

from pyspark import SparkContext

# Hardcode S3 input and output paths
input_path = "s3://s3-partioning/fruit.txt"
output_path = "s3://s3-partioning/output"

sc = SparkContext()

# Read file from S3
rdd = sc.textFile(input_path)

# Perform word count
counts = rdd.flatMap(lambda line: line.split(" ")) \
            .map(lambda word: (word, 1)) \
            .reduceByKey(lambda a, b: a + b)

# Collect and print results in SSH
result = counts.collect()
for word, count in result:
    print(f"{word}: {count}")

# Save clean results to S3
counts.map(lambda x: f"{x[0]} {x[1]}").saveAsTextFile(output_path)

sc.stop()
