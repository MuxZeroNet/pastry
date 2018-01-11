# Copyright 2018 MuxZeroNet
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import doctest

def docstring(func):
    def test_runner(self, *args, **kwargs):
        tests = doctest.DocTestFinder().find(func)
        runner = doctest.DocTestRunner()
        for t in tests:
            runner.run(t)
        runner.summarize()
        self.assertEquals(runner.failures, 0)
        return func(self, *args, **kwargs)
    return test_runner
