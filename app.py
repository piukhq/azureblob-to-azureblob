import os
import sys
from azure.storage.blob import BlobServiceClient

tmp_dir = "/tmp/downloads/"

try:
    src_conn_str = os.environ["SRC_CONN_STR"]
except KeyError as e:
    print("SRC_CONN_STR environment variable undefined")
    sys.exit(1)

try:
    dst_conn_str = os.environ["DST_CONN_STR"]
except KeyError as e:
    print("DST_CONN_STR environment variable undefined")
    sys.exit(1)

try:
    src_container_name = os.environ["SRC_CON_NAME"]
except KeyError as e:
    print("SRC_CON_NAME - source container name environment variable undefined")
    sys.exit(1)

try:
    dst_container_name = os.environ["DST_CON_NAME"]
except KeyError as e:
    print("DST_CON_NAME - destination container name environment variable undefined")
    sys.exit(1)


src_storage_key = [key for key in src_conn_str.split(";") if key.startswith("AccountKey")][0][11:]
src_storage_name = [name for name in src_conn_str.split(";") if name.startswith("AccountName")][0][12:]

dst_storage_key = [key for key in dst_conn_str.split(";") if key.startswith("AccountKey")][0][11:]
dst_storage_name = [name for name in dst_conn_str.split(";") if name.startswith("AccountName")][0][12:]


class AzureBlobCopier:
    def __init__(self):
        print("Intialising AzureBlobCopier")

        self.src_blob_srv_client = BlobServiceClient.from_connection_string(src_conn_str)
        self.src_containers = self.src_blob_srv_client.list_containers()
        self.src_containers_info = {c.name: {"last_modified": c.last_modified} for c in self.src_containers}
        self.dst_blob_srv_client = BlobServiceClient.from_connection_string(dst_conn_str)

    def save_blob(self, file_name, file_content):
        download_file_path = os.path.join(tmp_dir, file_name)
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, "wb") as file:
            file.write(file_content)

    def list_blob(self, client, container_name):
        container_client = client.get_container_client(container_name)
        blobs = {bolb.name for bolb in container_client.list_blobs()}

        return blobs

    def download_blob(self, container_name=src_container_name):
        for container in self.src_containers_info.keys():
            if container == container_name:
                container_client = self.src_blob_srv_client.get_container_client(container)
                my_blobs = self.diff_containers()
                for blob in my_blobs:
                    bytes = container_client.get_blob_client(blob).download_blob().readall()
                    self.save_blob(blob, bytes)

    def upload_file(self, file_path, blob_path):
        blob_client = self.dst_blob_srv_client.get_blob_client(container=dst_container_name, blob=blob_path)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data=data)

    def upload_dir(self, source):
        for root, dirs, files in os.walk(source):
            for name in files:
                dir_part = os.path.relpath(root, source)
                dir_part = "" if dir_part == "." else dir_part + "/"
                file_path = os.path.join(root, name)
                blob_path = dir_part + name
                self.upload_file(file_path, blob_path)
                os.remove(file_path)

    def diff_containers(self):
        src_list = self.list_blob(self.src_blob_srv_client, src_container_name)
        dst_list = self.list_blob(self.dst_blob_srv_client, dst_container_name)
        diff = src_list.difference(dst_list)

        return diff


def run():
    azure_blob_copier = AzureBlobCopier()
    azure_blob_copier.download_blob()
    azure_blob_copier.upload_dir(tmp_dir)


run()
