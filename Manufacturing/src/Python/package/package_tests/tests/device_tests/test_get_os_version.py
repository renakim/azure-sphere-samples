# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azuresphere_device_api import device
from packaging import version
import pytest
from tests.helpers import utils


def test__get_os_version__returns_correct_format():
    """Getting the OS version returns the os version contained in a JSON object"""

    rest_version = device.get_device_rest_api_version()

    if version.parse(rest_version["REST-API-Version"]) < version.parse("4.5.0"):
        # os_version is not supported before 4.5.0 and should raise an exception
        with pytest.raises(Exception) as e_info:
            device.get_device_os_version()
    else:
        response = device.get_device_os_version()
        osversion_schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                'osversion': {'osversion': {'type': 'string'}}
            }
        }
        assert utils.validate_json(response, osversion_schema)
        assert type(version.parse(response["osversion"])).__name__ == "Version"
