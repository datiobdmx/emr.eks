import argparse
from pyspark.sql import SparkSession
def rate_movies(movie_catalog, movie_ratings, user_catalog, output_uri):

    with SparkSession.builder.appName("Movie Rater").getOrCreate() as spark:
        # Load the restaurant violation CSV data
        movie_catalog_df = spark.read.parquet(movie_catalog)
        movie_ratings_df = spark.read.parquet(movie_ratings)
        user_catalog_df = spark.read.parquet(user_catalog)

        # print schemas
        # movie_catalog_df.printSchema()
        # movie_ratings_df.printSchema()
        # user_catalog_df.printSchema()

        # Create an in-memory DataFrame to query
        users_ratings_df = user_catalog_df.join(movie_ratings_df,on='User_id').join(movie_catalog_df,on='Movie_id').select('Firstname','Lastname','Rating','Title')

        rated_movies_df = users_ratings_df.groupBy('Title').avg().orderBy('avg(Rating)',ascending=False)

        
        # Write the results to the specified output URI
        rated_movies_df.repartition(1).write.option("header", "true").mode("overwrite").csv(output_uri)

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--movie_catalog', help="The URI for you data, like an S3 bucket location.")
    parser.add_argument(
        '--movie_ratings', help="The URI for you data, like an S3 bucket location.")
    parser.add_argument(
        '--user_catalog', help="The URI for you data, like an S3 bucket location.")

    parser.add_argument(
        '--output_uri', help="The URI where output is saved, like an S3 bucket location.")
    args = parser.parse_args()
    rate_movies(args.movie_catalog, args.movie_ratings, args.user_catalog, args.output_uri)

