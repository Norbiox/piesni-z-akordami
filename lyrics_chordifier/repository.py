from typing import Protocol

import boto3


class ApplicationRepository(Protocol):
    """Repository for application data"""

    def get_hymn(self, name) -> str:
        """Returns lyrics hymn"""
        raise NotImplementedError()

    def get_hymns(self) -> list[str]:
        """Returns list of names of all hymns"""
        raise NotImplementedError()

    def get_hymns_with_lyrics(self) -> list[str]:
        """Returns list of names of all hymns with added lyrics"""
        raise NotImplementedError()

    def save_hymn_with_lyrics(self, name: str, body: str):
        """Saves a hymn with added lyrics"""
        raise NotImplementedError()


class S3ApplicactionRepository(ApplicationRepository):
    """Implementation of ApplicationRepository with S3 bucket"""

    bucket: str = "spiewnik-pielgrzyma"
    client: boto3.client

    def __init__(self, client: boto3.client, bucket_name: str | None):
        self.client = client
        self.bucket = bucket_name or self.bucket

    def get_hymn(self, name: str) -> str:
        """Returns lyrics hymn"""
        obj = self.client.get_object(Bucket=self.bucket, Key=f"teksty/{name.strip('.txt')}.txt")
        return obj["Body"].read().decode("utf-8")

    def get_hymns(self) -> list[str]:
        """Returns list of names of all hymns"""
        objects = self.client.list_objects_v2(Bucket=self.bucket, Prefix="teksty/")["Contents"]
        hymns = [obj for obj in objects if obj["Key"].endswith(".txt")]
        return [obj["Key"].split("/")[1] for obj in hymns]

    def get_hymns_with_lyrics(self) -> list[str]:
        objects = self.client.list_objects_v2(Bucket=self.bucket, Prefix="teksty_z_akordami/")[
            "Contents"
        ]
        hymns = [obj for obj in objects if obj["Key"].endswith(".txt")]
        return [obj["Key"].split("/")[1] for obj in hymns]

    def save_hymn_with_lyrics(self, name: str, body: str) -> None:
        self.client.put_object(
            Body=body, Bucket=self.bucket, Key=f"teksty_z_akordami/{name.strip('.txt')}.txt"
        )
