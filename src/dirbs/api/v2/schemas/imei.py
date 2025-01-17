"""
DIRBS REST-ful IMEI API Schema module.

SPDX-License-Identifier: BSD-4-Clause-Clear

Copyright (c) 2018-2019 Qualcomm Technologies, Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
limitations in the disclaimer below) provided that the following conditions are met:

    - Redistributions of source code must retain the above copyright notice, this list of conditions and the following
      disclaimer.
    - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
      following disclaimer in the documentation and/or other materials provided with the distribution.
    - All advertising materials mentioning features or use of this software, or any deployment of this software,
      or documentation accompanying any distribution of this software, must display the trademark/logo as per the
      details provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
    - Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or
      promote products derived from this software without specific prior written permission.



SPDX-License-Identifier: ZLIB-ACKNOWLEDGEMENT

Copyright (c) 2018-2019 Qualcomm Technologies, Inc.

This software is provided 'as-is', without any express or implied warranty. In no event will the authors be held liable
for any damages arising from the use of this software. Permission is granted to anyone to use this software for any
purpose, including commercial applications, and to alter it and redistribute it freely, subject to the following
restrictions:

    - The origin of this software must not be misrepresented; you must not claim that you wrote the original software.
      If you use this software in a product, an acknowledgment is required by displaying the trademark/logo as per the
      details provided here: https://www.qualcomm.com/documents/dirbs-logo-and-brand-guidelines
    - Altered source versions must be plainly marked as such, and must not be misrepresented as being the original
      software.
    - This notice may not be removed or altered from any source distribution.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
import re
from enum import Enum

from flask import abort
from marshmallow import Schema, fields, validate, post_dump


class StolenStatus(Schema):
    """Defines schema for StolenList status."""

    status = fields.String()
    provisional_only = fields.Boolean()


class RegistrationStatus(Schema):
    """Defines schema for checking RegistrationList Status."""

    status = fields.String()
    provisional_only = fields.Boolean()


class RealtimeChecks(Schema):
    """Defines schema for realtime checks associated with IMEI."""

    ever_observed_on_network = fields.Boolean()
    invalid_imei = fields.Boolean()
    is_paired = fields.Boolean()
    is_exempted_device = fields.Boolean()


class ClassificationState(Schema):
    """Define schema for status of configured conditions."""

    blocking_conditions = fields.List(fields.Dict())
    informative_conditions = fields.List(fields.Dict())


class IMEI(Schema):
    """Define schema for IMEI API."""

    SKIP_VALUES = {None}

    imei_norm = fields.String(required=True)
    block_date = fields.Date(required=False)
    classification_state = fields.Nested(ClassificationState, required=True)
    realtime_checks = fields.Nested(RealtimeChecks, required=True)
    registration_status = fields.Nested(RegistrationStatus, required=True)
    stolen_status = fields.Nested(StolenStatus, required=True)

    @post_dump
    def skip_missing_block_date(self, data):
        """
        Skip block date if it is missing.

        :param data: dumped data
        :return: modified dumped data
        """
        if data.get('block_date') in self.SKIP_VALUES:
            del data['block_date']
        return data


class BatchIMEI(Schema):
    """Defines schema for Batch-IMEIs API (version 2.0)."""

    results = fields.List(fields.Nested(IMEI, required=True))


class Validators:
    """Defines custom validators for schema fields."""

    @staticmethod
    def validate_imei(val):
        """
        Validates IMEI format.

        :param val: IMEI value
        """
        if len(val) > 16:
            abort(400, 'Bad IMEI format (too long).')

        if re.match(r'\s+', val):
            abort(400, 'Bad IMEI format (whitespces not allowed).')

        if re.match(r'\t+', val):
            abort(400, 'Bad IMEI format (tabs not allowed).')

        if len(val) == 0:
            abort(400, 'Bad IMEI format (empty imei).')

    @staticmethod
    def validate_imei_list(val):
        """
        Validates IMEI list.

        :param val: list of IMEIs
        """
        if len(val) == 0:
            abort(400, 'Bad Input format (imei list cannot be empty).')

        if len(val) > 1000:
            abort(400, 'Bad Input format (max allowed imeis are 1000).')


class IMEIBatchArgs(Schema):
    """Input args for Batch-IMEI POST API (version 2)."""

    # noinspection PyProtectedMember
    imeis = fields.List(fields.String(required=True, validate=Validators.validate_imei),
                        validate=Validators.validate_imei_list)

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class Subscribers(Schema):
    """Defines schema for Subscribers Info for IMEI API."""

    imsi = fields.String()
    msisdn = fields.String()
    last_seen = fields.String()


class Pairings(Schema):
    """Defines schema for Pairings Info for IMEI API."""

    imsi = fields.String()
    last_seen = fields.String()


class SortingOrders(Enum):
    """Enum for supported sorting orders."""

    ASC = 'Ascending'
    DESC = 'Descending'


class SubscriberArgs(Schema):
    """Defines schema for IMEI-Subscriber API arguments."""

    offset = fields.Integer(required=False, description='Offset the results on the current page '
                                                        'by the specified imsi-msisdn pair. It should be the value of '
                                                        'imsi-msisdn pair for the last result on the previous page')
    limit = fields.Integer(required=False, description='Number of results to return on the current page')
    order = fields.String(required=False, validate=validate.OneOf([f.value for f in SortingOrders]),
                          description='The sort order for the results using imsi-msisdn as the key')

    @property
    def fields_dict(self):
        """Convert declared fields to dictionary."""
        return self._declared_fields


class IMEIKeys(Schema):
    """Defines schema for keys of paginated result set."""

    previous_key = fields.String()
    next_key = fields.String()
    result_size = fields.Integer()


class IMEISubscribers(Schema):
    """Defines schema for IMEI-Subscribers."""

    _keys = fields.Nested(IMEIKeys, required=True)
    imei_norm = fields.String()
    subscribers = fields.List(fields.Nested(Subscribers, required=True))


class IMEIPairings(Schema):
    """Defines schema for IMEI-Pairings."""

    _keys = fields.Nested(IMEIKeys, required=True)
    imei_norm = fields.String()
    pairs = fields.List(fields.Nested(Pairings, required=True))


class IMEIInfo(Schema):
    """Response schema for IMEI-Info API."""

    imei_norm = fields.String(required=True)
    status = fields.String(required=False)
    make = fields.String(required=False)
    model = fields.String(required=False)
    model_number = fields.String(required=False)
    brand_name = fields.String(required=False)
    device_type = fields.String(required=False)
    radio_interface = fields.String(required=False)
