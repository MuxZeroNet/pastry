# Pastry

Here is a sample Pastry implementation. It is written in Python 3. It requires the package `sortedcontainers`.

This is simply a barebone implementation of the Pastry routing table and leaf set. You will need a network protocol to help put this into practical application.

```bash
$ tar -xvf pastry-master.tar.gz
$ cd pastry-master
$ python3 -m venv .
$ source ./bin/activate
$ python3 -m pip install sortedcontainers --upgrade
$ python3 -m pastry.tests
```

## Explore its API

```python
>>> from pastry.routing import Pastry
>>> pastry = Pastry(b'myid1111myid2222', peers={
... b'\x01'*16: ('8.8.8.8', 8080), b'\x02'*16: ('8.8.4.4', 5353)})
>>> pastry
<pastry.routing.Pastry object at 0x7feb39a12668>

# dictionary-like interface
>>> pastry[b'\x01'*16]
('8.8.8.8', 8080)

# internal attributes, read-only; please do not modify them
>>> list(pastry.routing_table.items())
[(b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02', ('8.8.4.4', 5353)), (b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01', ('8.8.8.8', 8080))]
>>> list(pastry.leaf_set.items())
[(b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01', ('8.8.8.8', 8080)), (b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02', ('8.8.4.4', 5353))]

# find the next hop; key does not need to be exact
>>> list(pastry.route(b'\x01'*15 + b'\x00'))
[('8.8.8.8', 8080), ('8.8.4.4', 5353)]
>>> list(pastry.route(b'\x02'*15 + b'\x00'))
[('8.8.4.4', 5353), ('8.8.8.8', 8080)]
>>> list(pastry.route(b'\x00'*16))
[('8.8.8.8', 8080), ('8.8.4.4', 5353)]
>>> list(pastry.route(b''))
[('8.8.8.8', 8080), ('8.8.4.4', 5353)]

# update routing table and leaf set
>>> pastry.update({b'\x03'*16: ('abcdabcdabcdabcd.onion', 12345)})
>>> pastry.route(b'\x03')
(('abcdabcdabcdabcd.onion', 12345), ('8.8.4.4', 5353), ('8.8.8.8', 8080))
```

## Sample usage

```python
from pastry.routing import Pastry

def next_hop(pastry, key):
    peers = pastry.route(key, n=5)
    for peer in peers:
        has_value, more_peers = send_dht_request(peer, key)
        if has_value:
            return peer
        else:
            pastry.update(more_peers)
    raise KeyError(key)

def send_dht_request(peer, key):
    # stub
    if peer.endswith('.onion') and key.startswith(b'\x03'):
        return (True, None)
    else:
        return (False, {b'\x03'*16: 'abcdabcdabcdabcd.onion'})

pastry = Pastry(b'myid'*4, {b'A'*16: '1.2.3.4', b'B'*16: '5.6.7.8'})
print(next_hop(pastry, b'\x03'))  # KeyError
print(next_hop(pastry, b'\x03'))  # got it
```


## Back-porting to Python 2

For those who are too hesitant to write in Python 3.

1. `from __future__ import unicode_literals`
2. `yield from generator` --> `for thing in generator: yield thing`
3. Find alternative methods to `int.from_bytes` and `int.to_bytes`
4. When programming in Python 2, use `dict.viewitems`, `dict.viewkeys` and `dict.viewvalues`. In Python 3, you don't have to type the `view`- or `iter`- prefix.
5. Note the behavior difference of the `bytes.__getitem__` method
    ```
    >>> b = b'abcd'
    >>> b[0]  # python 3
    97

    >>> b = b'abcd'
    >>> b[0]  # python 2
    'a'
    ```
