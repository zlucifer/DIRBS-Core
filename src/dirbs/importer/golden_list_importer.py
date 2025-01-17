"""
Code for importing golden list data into DIRBS Core.

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
from dirbs.importer.base_delta_importer import BaseDeltaImporter


class GoldenListImporter(BaseDeltaImporter):
    """Golden list data importer."""

    def __init__(self,
                 *args,
                 prehashed_input_data=False,
                 **kwargs):
        """Constructor."""
        super().__init__(*args, **kwargs)
        self._prehashed_input_data = prehashed_input_data

    @property
    def _import_type(self):
        """Overrides AbstractImporter._import_type."""
        return 'golden_list'

    @property
    def _import_relation_name(self):
        """Overrides AbstractImporter._import_relation_name."""
        return 'golden_list'

    @property
    def _schema_file(self):
        """Overrides AbstractImporter._schema_file."""
        if self._delta:
            if self._prehashed_input_data:
                return 'GoldenListDeltaSchemaPreHashedData.csvs'
            else:
                return 'GoldenListDeltaSchemaData.csvs'

        schema_file = 'GoldenListSchemaPreHashedData.csvs' \
            if self._prehashed_input_data else 'GoldenListSchemaData.csvs'
        return schema_file

    @property
    def _owner_role_name(self):
        """Overrides AbstractImporter._owner_role."""
        return 'dirbs_core_import_golden_list'

    @property
    def _staging_tbl_ddl(self):
        """Overrides BaseImporter._staging_tbl_ddl."""
        return """CREATE UNLOGGED TABLE {0} (
                                             row_id             BIGSERIAL NOT NULL,
                                             imei               TEXT,
                                             hashed_imei_norm   UUID NOT NULL
                                            ) WITH (autovacuum_enabled = false)"""

    @property
    def _pk_field_names(self):
        """Overrides BaseImporter._pk_field_names."""
        return ['hashed_imei_norm']

    @property
    def _input_csv_field_names(self):
        """Overrides BaseImporter._input_csv_field_names."""
        return ['imei']

    @property
    def _staging_data_insert_trigger_name(self):
        """Overrides BaseImporter._staging_data_insert_trigger_name."""
        # If data hasn't already been hashed, normalize the IMEI values,
        # hash them with MD5 and cast them to UUID, to make their value normalized and unique.
        if self._prehashed_input_data:
            return '{0}_prehashed_imei_staging_data_insert_trigger_fn'.format(self._import_type)
        return '{0}_unhashed_imei_staging_data_insert_trigger_fn'.format(self._import_type)

    @property
    def _import_metadata(self):
        """Overrides BaseImporter._import_metadata."""
        md = super()._import_metadata
        md.update({
            'pre_hashed': self._prehashed_input_data
        })
        return md
