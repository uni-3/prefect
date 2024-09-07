from __future__ import annotations

import tempfile
import warnings
from typing import cast

import airbyte as ab
from airbyte.caches.bigquery import BigQueryCache
from airbyte.secrets.base import SecretString
from airbyte.secrets.google_gsm import GoogleGSMSecretManager

from pathlib import Path
import json


AIRBYTE_INTERNAL_GCP_PROJECT = "free-180413"
SECRET_NAME = "SECRET_DESTINATION-BIGQUERY_CREDENTIALS__CREDS"

# bigquery_destination_secret: dict = cast(
#     SecretString,
#     GoogleGSMSecretManager(
#         project=AIRBYTE_INTERNAL_GCP_PROJECT,
#         #credentials_json=ab.get_secret("GCP_GSM_CREDENTIALS"),
#     ).get_secret(SECRET_NAME),
# ).parse_json()

credentials_path=ab.get_secret("GOOGLE_APPLICATION_CREDENTIALS")
bigquery_destination_secret = SecretString(Path(credentials_path).read_text(encoding="utf-8"))
bigquery_destination_secret = json.loads(bigquery_destination_secret)


import tempfile
from contextlib import contextmanager

class BigQueryCacheWithTempFile:
    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8")
        self.temp_file.write(bigquery_destination_secret["credentials_json"])
        self.temp_file.flush()

        self.cache = BigQueryCache(
            project_name=bigquery_destination_secret["project_id"],
            dataset_name=bigquery_destination_secret.get("dataset_id", "pyairbyte_integtest"),
            credentials_path=self.temp_file.name,
        )
        import atexit
        atexit.register(self.cleanup)

    def __del__(self):
        self.temp_file.close()
        import os
        import atexit
        os.unlink(self.temp_file.name)
        atexit.unregister(self.cleanup)

    def __getattr__(self, name):
        return getattr(self.cache, name)

@contextmanager
def bq_cache():
    cache = BigQueryCacheWithTempFile()
    try:
        yield cache
    finally:
        del cache


# def bq_cache():
#     with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as temp:
#         # Write credentials to the temp file
#         temp.write(bigquery_destination_secret["credentials_json"])
#         temp.flush()
#         temp.close()

#         cache = BigQueryCache(
#             project_name=bigquery_destination_secret["project_id"],
#             dataset_name=bigquery_destination_secret.get(
#                 "dataset_id", "pyairbyte_integtest"
#             ),
#             credentials_path=temp.name,
#         )

#         return cache