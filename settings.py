import os
import sys

src_conn_str = os.getenv("source_connection_string")

dst_conn_str = os.getenv("destination_connection_string")

src_container_name = os.getenv("source_container_name")

dst_container_name = os.getenv("destination_container_name")

dst_prefix = os.getenv("destination_prefix", src_container_name + '/')

tmp_dir = "/tmp/downloads/"
