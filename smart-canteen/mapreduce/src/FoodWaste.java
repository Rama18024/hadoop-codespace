import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class FoodWaste {

    public static class FoodMapper
            extends Mapper<LongWritable, Text, Text, Text> {

        private Text food = new Text();
        private Text quantities = new Text();

        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            String line = value.toString();

            // Skip CSV header
            if (line.startsWith("date,")) {
                return;
            }

            String[] fields = line.split(",");

            if (fields.length == 6) {
                String foodItem = fields[1];

                int prepared = Integer.parseInt(fields[2]);
                int sold = Integer.parseInt(fields[3]);
                int leftover = Integer.parseInt(fields[4]);

                food.set(foodItem);
                quantities.set(prepared + "," + sold + "," + leftover);

                context.write(food, quantities);
            }
        }
    }

    public static class FoodReducer
            extends Reducer<Text, Text, Text, Text> {

        public void reduce(Text key, Iterable<Text> values,
                           Context context)
                throws IOException, InterruptedException {

            long totalPrepared = 0;
            long totalSold = 0;
            long totalLeftover = 0;

            for (Text value : values) {
                String[] quantities = value.toString().split(",");

                totalPrepared += Long.parseLong(quantities[0]);
                totalSold += Long.parseLong(quantities[1]);
                totalLeftover += Long.parseLong(quantities[2]);
            }

            double wastePercentage =
                    totalPrepared == 0 ? 0 :
                    (totalLeftover * 100.0 / totalPrepared);

            String result = totalPrepared + "\t" +
                            totalSold + "\t" +
                            totalLeftover + "\t" +
                            String.format("%.2f", wastePercentage);

            context.write(key, new Text(result));
        }
    }

    public static void main(String[] args) throws Exception {

        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "Smart Canteen Food Waste Analysis");

        job.setJarByClass(FoodWaste.class);

        job.setMapperClass(FoodMapper.class);
        job.setReducerClass(FoodReducer.class);

        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
