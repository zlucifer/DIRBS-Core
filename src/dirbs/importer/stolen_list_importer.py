"""
Code for importing local stolen list data into DIRBS Core.

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


class StolenListImporter(BaseDeltaImporter):
    """Local stolen list data importer."""

    @property
    def _import_type(self):
        """Overrides AbstractImporter._import_type."""
        return 'stolen_list'

    @property
    def _import_relation_name(self):
        """Overrides AbstractImporter._import_relation_name."""
        return 'stolen_list'

    @property
    def _schema_file(self):
        """Overrides AbstractImporter._schema_file."""
        if self._delta:
            return 'StolenListDeltaSchema.csvs'
        return 'StolenListSchema.csvs'

    @property
    def _owner_role_name(self):
        """Overrides AbstractImporter._owner_role."""
        return 'dirbs_core_import_stolen_list'

    @property
    def _pk_field_names(self):
        """Overrides BaseImporter._pk_field_names."""
        return ['imei_norm']

    @property
    def _extra_field_names(self):
        """Overrides BaseImporter._extra_field_names."""
        return ['reporting_date', 'status']

    @property
    def _input_csv_field_names(self):
        """Overrides BaseImporter._input_csv_field_names."""
        return ['imei', 'reporting_date', 'status']

    @property
    def _staging_tbl_ddl(self):
        """Overrides BaseImporter._staging_tbl_ddl."""
        return """CREATE UNLOGGED TABLE {0} (
                      row_id           BIGSERIAL NOT NULL,
                      imei             TEXT,
                      imei_norm        TEXT NOT NULL,
                      reporting_date   DATE,
                      status           TEXT
                  )"""

    @property
    def _supports_imei_shards(self):
        """Overrides AbstractImporter._supports_imei_shards."""
        return True
