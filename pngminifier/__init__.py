"""pngminifier: reduces PNG size by stripping out unwanted chunks (eg. EXIF, pHYs)."""

from argparse import ArgumentParser, FileType
from ._pngc   import PNGChunkReader, PNGChunkWriter
from sys      import stdin, stdout

critical_chunks = [b'IHDR', b'IDAT', b'PLTE', b'IEND']
useful_chunks = [b'gAMA', b'tRNS', b'iCCP']

class PNGMinifier(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.add_argument('INPUT',
            nargs= '?',
            type= FileType('rb'),
            default= stdin.buffer,
            help= "input PNG file to read from, "
                  "by default stdin")

        self.add_argument('-o',
            dest= 'output',
            type= FileType('wb'),
            default= stdout.buffer,
            help= "output PNG file to write to, "
                  "by default stdout")

        self.add_argument('--include-useful',
            dest= 'allow_useful',
            action= 'store_true',
            help= "include useful chunks too (not recommended)")

        self.argv = self.parse_args()

    def main(self):
        pr = PNGChunkReader(self.argv.INPUT)
        pw = PNGChunkWriter(self.argv.output)

        for chk in pr:
            if chk.name in critical_chunks:
                pw << chk
            elif self.argv.allow_useful and chk.name in useful_chunks:
                pw << chk
        
        self.argv.output.flush()

if __name__ == "__main__":
    PNGMinifier().main()
