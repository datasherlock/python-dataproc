#!/usr/bin/env python

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This sample walks a user through creating a Cloud Dataproc cluster using
# the Python client library.
#
# This script can be run on its own:
#   python delete_cluster.py ${PROJECT_ID} ${REGION} ${DP_CLUSTER_NAME}

import sys

# [START dataproc_delete_gke_gce_cluster]
from google.cloud import dataproc_v1 as dataproc


def delete_cluster(project_id, region, cluster_name) -> None:
    """This sample walks a user through deleting a Cloud Dataproc cluster
    using the Python client library. This method can be used both for Dataproc clusters running on GCE as well as on GKE clusters.

    Args:
        project_id (string): Project where you are deleting resources.
        region (string): Region where the resources currently live.
        cluster_name (string): Name of the Dataproc cluster you are deleting.
    """

    # Create a client with the endpoint set to the desired cluster region.
    cluster_client = dataproc.ClusterControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )

    # Delete your Dataproc cluster.
    operation = cluster_client.delete_cluster(
        request={
            "project_id": project_id,
            "region": region,
            "cluster_name": cluster_name,
        }
    )
    operation.result(60)

    print("Cluster {} successfully deleted.".format(cluster_name))


# [END dataproc_delete_gke_gce_cluster]


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("python create_cluster.py project_id region cluster_name")

    project_id = sys.argv[1]
    region = sys.argv[2]
    cluster_name = sys.argv[3]
    delete_cluster(project_id, region, cluster_name)
