import os
import sys
import settings
from azure.storage.blob import BlobServiceClient


class AzureBlobCopier:
    def __init__(self):
        print("Intialising AzureBlobCopier")

        self.src_blob_srv_client = BlobServiceClient.from_connection_string(settings.src_conn_str)
        self.src_containers = self.src_blob_srv_client.list_containers()
        self.src_containers_info = {c.name for c in self.src_containers}
        self.dst_blob_srv_client = BlobServiceClient.from_connection_string(settings.dst_conn_str)

    def save_blob(self, file_name, file_content):
        download_file_path = os.path.join(settings.tmp_dir, file_name)
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, "wb") as file:
            file.write(file_content)

    def list_blob(self, client, container_name, prefix=None):
        container_client = client.get_container_client(container_name)
        blobs = {bolb.name for bolb in container_client.list_blobs(name_starts_with=prefix)}

        return blobs

    def download_blob(self, container_name=settings.src_container_name, prefix=None):
        for container in self.src_containers_info:
            if container == container_name:
                container_client = self.src_blob_srv_client.get_container_client(container)
                my_blobs = self.diff_containers()
                for blob in my_blobs:
                    bytes = container_client.get_blob_client(blob).download_blob().readall()
                    self.save_blob(blob, bytes)

    def upload_file(self, file_path, blob_path):
        blob_client = self.dst_blob_srv_client.get_blob_client(container=settings.dst_container_name, blob=blob_path)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data=data)

    def upload_dir(self, source):
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = "" if dir_part == "." else dir_part + "/"
                file_path = os.path.join(root, name)
                blob_path = "media/" + dir_part + name
                self.upload_file(file_path, blob_path)
                os.remove(file_path)

    def diff_containers(self):
        src_list = self.list_blob(self.src_blob_srv_client, settings.src_container_name)
        dst_list = self.list_blob(self.dst_blob_srv_client, settings.dst_container_name, prefix=settings.dst_prefix)
        dst_list_prefix = {str(i).removeprefix(settings.dst_prefix) for i in dst_list}
        diff = src_list.difference(dst_list_prefix)

        return diff


def run():
    azure_blob_copier = AzureBlobCopier()
    azure_blob_copier.download_blob(prefix=settings.dst_prefix)
    azure_blob_copier.upload_dir(settings.tmp_dir)


run()
