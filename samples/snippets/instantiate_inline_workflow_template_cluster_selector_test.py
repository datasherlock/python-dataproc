# Copyright 2020 Google LLC
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

import os
import uuid

from google.api_core.exceptions import NotFound
from google.cloud import dataproc_v1 as dataproc
import pytest

import instantiate_inline_workflow_template_cluster_selector


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
LABEL = "demo-pool"
CLUSTER_NAME = "pytest-{}".format(str(uuid.uuid4()))
CLUSTER = {
    "project_id": PROJECT_ID,
    "cluster_name": CLUSTER_NAME,
    "labels": {
        "cluster-pool": LABEL
    },
    "config": {
        "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
        "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
    },
}


@pytest.fixture(autouse=True)
def setup_teardown():
    try:
        cluster_client = dataproc.ClusterControllerClient(
            client_options={
                "api_endpoint": "{}-dataproc.googleapis.com:443".format(REGION)
            }
        )

        # Create the cluster.
        operation = cluster_client.create_cluster(
            request={"project_id": PROJECT_ID, "region": REGION, "cluster": CLUSTER}
        )
        operation.result()

        yield

    finally:
        try:
            operation = cluster_client.delete_cluster(
                request={
                    "project_id": PROJECT_ID,
                    "region": REGION,
                    "cluster_name": CLUSTER_NAME
                }
            )
            operation.result()

        except NotFound:
            print("Cluster already deleted")


def test_submit_job(capsys):
    instantiate_inline_workflow_template_cluster_selector.instantiate_inline_workflow_template_cluster_selector(PROJECT_ID, REGION, LABEL)
    out, _ = capsys.readouterr()

    assert "Workflow ran successfully." in out
