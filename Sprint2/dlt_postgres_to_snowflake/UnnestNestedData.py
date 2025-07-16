#in this task we are going to unnest nested data from postgres and load it into snowflake
import dlt

# Source: Postgres
@dlt.source
def postgres_source():
    @dlt.resource(write_disposition="replace")
    def orders_flattened():
        return """
        SELECT
            o.id AS order_id,
            o.customer_name,
            o.order_date,
            o.shipping_address ->> 'street' AS street,
            o.shipping_address ->> 'city' AS city,
            o.shipping_address ->> 'zip' AS zip,
            item.value ->> 'product' AS product,
            (item.value ->> 'quantity')::INT AS quantity,
            (item.value ->> 'price')::DECIMAL AS price
        FROM
            orders o,
            LATERAL jsonb_array_elements(o.items) AS item(value);
        """

    return orders_flattened

# Pipeline
pipeline = dlt.pipeline(
    pipeline_name="postgres_to_snowflake",
    destination="snowflake",
    dataset_name="orders_dataset"
)

info = pipeline.run(postgres_source())
print(info)
