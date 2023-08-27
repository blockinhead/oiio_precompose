__author__ = "Ilya Radovilsky"
__license__ = "MIT"

import argparse
import bisect
import glob
import os.path
from typing import List, Sequence

import clique
from OpenImageIO import ImageBuf, ImageBufAlgo


def _get_by_index(self: clique.Collection, index: int) -> str:
    return self.head + str(index).rjust(self.padding, '0') + self.tail


def get_by_index(self: clique.Collection, index: int) -> str:
    if index not in self.indexes:
        raise Exception(f'index {index} is not in collection {self}')
    return self._get_by_index(index)


def get_nearest_by_index(self: clique.Collection, index: int) -> str:
    indices = self.indexes._members

    pos = bisect.bisect_left(indices, index)

    if pos == 0:
        index = indices[0]
    elif pos == len(indices):
        index = indices[-1]
    else:

        val_before, val_after = indices[pos - 1], indices[pos]

        if val_after - index < index - val_before:
            index = val_after
        else:
            index = val_before

    return self._get_by_index(index)


clique.Collection._get_by_index = _get_by_index
clique.Collection.get_by_index = get_by_index
clique.Collection.get_nearest_by_index = get_nearest_by_index


def compose_sequences(src_pics: Sequence, start_index: int, end_index: int, target_name_prefix: str, padding: int = 4):

    os.makedirs(os.path.dirname(target_name_prefix), exist_ok=True)

    collections: List[clique.Collection] = []
    for s in src_pics:
        c, _ = clique.assemble(glob.glob(s), patterns=[clique.PATTERNS['frames']], minimum_items=1)
        collections.append(c[0])

    for c in collections:
        print(c.head, c.tail, c.padding)

    for i in range(start_index, end_index + 1):

        res = None

        for c in collections:
            current_pic = c.get_nearest_by_index(i)
            print(current_pic)
            if not res:
                res = ImageBuf(current_pic)
            else:
                tmp = ImageBuf()
                ok = ImageBufAlgo.over(tmp, ImageBuf(current_pic), res)
                if not ok:
                    raise Exception(f'error merging images: {tmp.geterror()}')
                res = tmp
        res.write(rf'{target_name_prefix}.{str(i).rjust(padding, "0")}.exr')
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='precompose sequences')
    parser.add_argument('--src', type=str, action='append', required=True,
                        help=r'paths with mask to a sequence. like c:\tmp\sq1.*.exr. use --src key as much as needed')
    parser.add_argument('--start', type=int, required=True,
                        help='start frame. for some layers may have less frames')
    parser.add_argument('--end', type=int, required=True,
                        help='end frame')
    parser.add_argument('--target', type=str, required=True,
                        help=r'target prefix of exr sequence. like c:\tmp\res')

    args = parser.parse_args()

    compose_sequences(src_pics=args.src,
                      start_index=args.start,
                      end_index=args.end,
                      target_name_prefix=args.target_pics_prefix)
