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

import unittest
import lazytest
from pastry.routing import *
from ipaddress import IPv4Address
from os import urandom
from random import choice

def make_peer():
    key = []
    for i in range(16):
        digit = choice(b'1234567890abcdef')
        key.append(digit.to_bytes(length=1, byteorder='big'))
    ip = IPv4Address(urandom(4))
    port = int.from_bytes(urandom(2), byteorder='big')
    return (b''.join(key), (ip, port))

class TestRoutingTable(unittest.TestCase):
    @lazytest.docstring
    def test_setitem_impl_detail(self):
        """
        >>> rt = RoutingTable(hash_len=4)
        >>> rt[b'1234'] = 'Test'
        >>> rt._dict
        {b'1': {b'2': {b'3': {b'4': 'Test'}}}}
        >>> rt._key_set
        {b'1234'}

        >>> rt[b'2345'] = 'Test2'
        >>> sorted(rt._dict.items())
        [(b'1', {b'2': {b'3': {b'4': 'Test'}}}), (b'2', {b'3': {b'4': {b'5': 'Test2'}}})]
        >>> sorted(rt._key_set)
        [b'1234', b'2345']

        >>> rt[b'2345'] = 'Test3'
        >>> sorted(rt._dict.items())
        [(b'1', {b'2': {b'3': {b'4': 'Test'}}}), (b'2', {b'3': {b'4': {b'5': 'Test3'}}})]
        >>> rt[b'2345']
        'Test3'
        >>> sorted(rt._key_set)
        [b'1234', b'2345']
        >>> sorted(iter(rt))
        [b'1234', b'2345']
        >>> sorted(rt.keys())
        [b'1234', b'2345']
        >>> sorted(rt.items())
        [(b'1234', 'Test'), (b'2345', 'Test3')]

        >>> 'Test' in rt
        False
        >>> b'1234' in rt
        True
        >>> b'2345' in rt
        True
        >>> b'Test3' in rt
        False

        >>> del rt[b'2345']
        >>> del rt[b'1234']
        >>> rt._dict
        {}
        """

    @lazytest.docstring
    def test_route(self):
        """
        >>> rt = RoutingTable(hash_len=4)
        >>> rt[b'1234'] = 'Test 1234'
        >>> rt[b'1235'] = 'Test 1235!!!'
        >>> rt[b'2980'] = 'Test!! 2980.'
        >>> sorted(rt.items())
        [(b'1234', 'Test 1234'), (b'1235', 'Test 1235!!!'), (b'2980', 'Test!! 2980.')]

        >>> rt.nearest(b'1233')
        'Test 1234'
        >>> rt.nearest(b'1234')
        'Test 1234'

        >>> list(rt.route(b'1233'))
        ['Test 1234', 'Test 1235!!!', 'Test!! 2980.']
        >>> list(rt.route(b'1111'))
        ['Test 1234', 'Test 1235!!!', 'Test!! 2980.']
        >>> list(rt.route(b'1234'))
        ['Test 1234', 'Test 1235!!!', 'Test!! 2980.']

        >>> rt.nearest(b'1235')
        'Test 1235!!!'
        >>> rt.nearest(b'1236')
        'Test 1235!!!'

        >>> list(rt.route(b'1235'))
        ['Test 1235!!!', 'Test 1234', 'Test!! 2980.']
        >>> list(rt.route(b'1236'))
        ['Test 1235!!!', 'Test 1234', 'Test!! 2980.']

        >>> rt.nearest(b'2018')
        'Test!! 2980.'
        >>> rt.nearest(b'2980')
        'Test!! 2980.'

        >>> list(rt.route(b'2018'))
        ['Test!! 2980.', 'Test 1235!!!', 'Test 1234']
        >>> list(rt.route(b'2980'))
        ['Test!! 2980.', 'Test 1234', 'Test 1235!!!']
        """
