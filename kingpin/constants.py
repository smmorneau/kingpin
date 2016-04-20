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
# limitations under the License.
#
# Copyright 2014 Nextdoor.com, Inc

__author__ = 'Mikhail Simin <mikhail@nextdoor.com>'


class REQUIRED(object):

    """Meta class to identify required arguments for actors."""


class StringCompareBase(object):

    """Meta class to identify the desired state for a resource.

    This basic type of constant allows someone to easily define a set of valid
    strings for their option and have the base actor class automatically
    validate the inputs against those strings.
    """

    valid = None

    @classmethod
    def validate(self, option):
        if option in self.valid:
            return True


class STATE(StringCompareBase):

    """Meta class to identify the desired state for a resource.

    Simple tester for 'present' or 'absent' on actors. Used for any actor thats
    idempotent and used to ensure some state of a resource.
    """

    valid = ('present', 'absent')
