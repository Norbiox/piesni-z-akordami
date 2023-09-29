import boto3


def get_s3_client(app) -> boto3.client:
    return boto3.client(
        "s3",
        endpoint_url=app.config["BUCKET_ENDPOINT_URL"],
        aws_access_key_id=app.config["BUCKET_ACCESS_KEY_ID"],
        aws_secret_access_key=app.config["BUCKET_SECRET_ACCESS_KEY"],
    )
