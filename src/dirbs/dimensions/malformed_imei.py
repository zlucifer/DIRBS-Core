"""
DIRBS dimension function for malformed IMEIs.

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

from psycopg2 import sql

import dirbs.partition_utils as partition_utils
from .base import Dimension


class MalformedIMEI(Dimension):
    """Implementation of the MalformedIMEI classification dimension."""

    def _matching_imeis_sql(self, conn, app_config, virt_imei_range_start, virt_imei_range_end, curr_date=None):
        """
        Overrides Dimension._matching_imeis_sql.

        :param conn: database connection
        :param app_config: dirbs config obj
        :param virt_imei_range_start: virtual imei shard range start
        :param virt_imei_range_end: virtual imei shard range end
        :param curr_date: user defined current analysis
        :return: SQL
        """
        network_imeis_shard = partition_utils.imei_shard_name(base_name='network_imeis',
                                                              virt_imei_range_start=virt_imei_range_start,
                                                              virt_imei_range_end=virt_imei_range_end)

        return sql.SQL("""SELECT imei_norm
                            FROM {network_imeis_shard}
                           WHERE imei_norm !~ '^\d{{14}}$'""") \
            .format(network_imeis_shard=sql.Identifier(network_imeis_shard)).as_string(conn)


dimension = MalformedIMEI
