# Copyright DataStax, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

try:
    import unittest2 as unittest
except ImportError:
    import unittest  # noqa

import os
import subprocess

from tests.integration import CLOUD_STARGATE_PATH, USE_CASS_EXTERNAL


def setup_package():
    if CLOUD_STARGATE_PATH and not USE_CASS_EXTERNAL:
        start_cloud_stargate()


def teardown_package():
    if not USE_CASS_EXTERNAL:
        stop_cloud_stargate()


class CloudStargateCluster(unittest.TestCase):

    creds_dir = os.path.join(os.path.abspath(CLOUD_STARGATE_PATH or ''), 'certs/bundles/')
    creds = os.path.join(creds_dir, 'creds-v1.zip')
    creds_no_auth = os.path.join(creds_dir, 'creds-v1-wo-creds.zip')
    creds_unreachable = os.path.join(creds_dir, 'creds-v1-unreachable.zip')
    creds_invalid_ca = os.path.join(creds_dir, 'creds-v1-invalid-ca.zip')

    cluster, connect = None, False
    session = None

    @classmethod
    def connect(cls, creds, **kwargs):
        cloud_config = {
            'secure_connect_bundle': creds,
        }
        cls.cluster = Cluster(cloud=cloud_config, protocol_version=4, **kwargs)
        cls.session = cls.cluster.connect(wait_for_all_pools=True)

    def tearDown(self):
        if self.cluster:
            self.cluster.shutdown()


class CloudStargateServer(object):
    """
    Class for starting and stopping the proxy (stargate_driver_endpoint)
    """

    def __init__(self, cloud_stargate_path):
        self.cloud_stargate_path = cloud_stargate_path
        self.running = False

    def start(self):
        subprocess.call(
            ["uname -a"],
            cwd=self.cloud_stargate_path,
            shell=True)
        subprocess.call(
            ["uname -m"],
            cwd=self.cloud_stargate_path,
            shell=True)
        return_code = subprocess.call(
            ['REQUIRE_CLIENT_CERTIFICATE=true ./run.sh'],
            cwd=self.cloud_stargate_path,
            shell=True)
        if return_code != 0:
            raise Exception("Error while starting stargate server")
        self.running = True

    def stop(self):
        if self.is_running():
            subprocess.call(
                ["docker-compose stop"],
                cwd=self.cloud_stargate_path,
                shell=True)
            self.running = False

    def is_running(self):
        return self.running

    def start_node(self, id):
        command = 'docker-compose start envoy{}'.format(id)
        subprocess.call(
            [command],
            cwd=self.cloud_stargate_path,
            shell=True)

    def stop_node(self, id):
        command = 'docker-compose stop envoy{}'.format(id)
        subprocess.call(
            [command],
            cwd=self.cloud_stargate_path,
            shell=True)


CLOUD_STARGATE_SERVER = CloudStargateServer(CLOUD_STARGATE_PATH)


def start_cloud_stargate():
    """
    Starts and waits for the proxy to run
    """
    CLOUD_STARGATE_SERVER.stop()
    CLOUD_STARGATE_SERVER.start()


def stop_cloud_stargate():
    CLOUD_STARGATE_SERVER.stop()
