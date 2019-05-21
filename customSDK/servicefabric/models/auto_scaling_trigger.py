# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AutoScalingTrigger(Model):
    """Describes the trigger for performing auto scaling operation.

    You probably want to use the sub-classes and not this class directly. Known
    sub-classes are: AverageLoadScalingTrigger

    :param kind: Constant filled by server.
    :type kind: str
    """

    _validation = {
        'kind': {'required': True},
    }

    _attribute_map = {
        'kind': {'key': 'kind', 'type': 'str'},
    }

    _subtype_map = {
        'kind': {'AverageLoad': 'AverageLoadScalingTrigger'}
    }

    def __init__(self):
        super(AutoScalingTrigger, self).__init__()
        self.kind = None
