"""
Simplistic library for chunk level mutations of PNG.
For encoding or decoding PNG images checkout PurePNG.

+------------------+
|  Length (u32be)  |
+------------------+
|     Name (4B)    |
+------------------+
|   Data (Length)  |
+------------------+
|   CRC32 (u32be)  |
+------------------+

* 4B    = four bytes
* u32be = 32bit big-endian
"""

from zlib   import crc32
from struct import unpack, pack
from types  import SimpleNamespace

class PNGChunk(SimpleNamespace):
    """PNG file consists of many chunks, this is to make
    the format very robust and flexible."""
    name:     bytes
    size:     int
    data:     bytes
    checksum: int

    def __init__(self, name: bytes, data: bytes, size= None, checksum= None):
        if not isinstance(name, bytes):
            raise TypeError('name must be bytes')
        self.name = name[:4]
    
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError('data must be a series of bytes')
        self.data = data
        
        self.size = len(data) if size is None else abs(int(size))
        self.checksum = crc32(data) if size is None else abs(int(checksum))

class PNGChunkReader:
    """
    A reader that iterates over chunks of a given PNG filestream.

    ```py
    >>> f = open('test01.png', 'rb')
    >>> pcr = PNGChunkReader(f)
    >>> for chunk in pcr:
    ...     print(chunk.name)
    ```
    """

    class DataCorruption(Exception): pass
    class PartialData(Exception): pass
    class PartialChecksum(Warning): pass

    def __init__(self, file):
        if not hasattr(file, 'read') and not isinstance(file.read(0), bytes):
            raise TypeError('unreadable binary file')

        self.fs = file
        assert b'\x89PNG\r\n\x1a\n' == file.read(8), \
                'invalid PNG signature of file truncated'
    
    def __iter__(self):
        while True:
            if len(_header:= self.fs.read(8)) < 8:
                break

            size = unpack('>I', _header[:4])[0]
            name = _header[4:]

            if len(data:= self.fs.read(size)) < size:
                raise self.PartialData(f'expected size of {size + 4} but got {len(data)}')

            if len(_checksum:= self.fs.read(4)) < 4:
                raise self.PartialChecksum(f'length of {len(_checksum)}')

            # exception isn't raised if checksum is partial.
            if len(_checksum) == 4 and (checksum:= crc32(name + data)) != unpack('>I', _checksum)[0]:
                raise self.DataCorruption('data in chunk does not match with its checksum')

            yield PNGChunk(name, data, size= size, checksum= checksum)

class PNGChunkWriter:
    """
    A writer that writes PNG chunks into a given PNG filestream.
    ```py
    >>> f = open('test1.png', 'wb')
    >>> pcw = PNGChunkWriter(f)
    >>> pcw << PNGChunk('tEXt', b'\x00' * 28)
    ```
    """

    def __init__(self, file):
        if not hasattr(file, 'write'):
            raise TypeError('unwritable binary file')

        self.fs = file
        file.write(b'\x89PNG\r\n\x1a\n')

    def __lshift__(self, chunk: PNGChunk):
        if not isinstance(chunk, PNGChunk):
            raise TypeError(f'invalid operands type: {type(chunk)}')

        self.fs.write(pack('>I4s', chunk.size, chunk.name))
        self.fs.write(chunk.data)
        self.fs.write(pack('>I', chunk.checksum))
