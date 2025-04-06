import dbutils  # available only on databricks : https://docs.databricks.com/aws/en/dev-tools/databricks-utils
import spark


catalog = dbutils.widgets.get("catalog_name")
schema = dbutils.widgets.get("schema_name")


def create_table():
    # Read CSV, create Spark DataFrame
    sdf = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", True)
        .load(f"/Volumes/{catalog}/{schema}/volume_name/file_name.csv")
    )

    # Create delta table
    (sdf.write.mode("overwrite").format("delta").saveAsTable(f"table_name"))


def crud_files():
    # List content of volume
    files = dbutils.fs.ls(f"/Volumes/{catalog}/{schema}/volume_name/")
    print(files)

    # Delete file
    dbutils.fs.rm(f"/Volumes/{catalog}/{schema}/volume_name/file_name.csv")


def run_sql():
    spark.sql("DROP TABLE IF EXISTS catalog.schema.table_name")
