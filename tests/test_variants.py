
import test_setup
import unittest

import numpy

import test_utils
from variant.variants import Variants
from variant import GT_FIELD


class VariantsTest(unittest.TestCase):
    def test_init(self):
        from pathlib import Path
        h5_fhand = test_utils.create_temp_h5_file()
        variants = Variants(Path(h5_fhand.name))
        assert GT_FIELD in variants.arrays.keys()
        assert all(numpy.equal(variants.samples,
                               [b'NA00001', b'NA00002', b'NA00003']))
        assert variants.num_variants == 5
        assert variants.ploidy == 2
        print('TODO Variants({})')


if __name__ == '__main__':
    unittest.main()
