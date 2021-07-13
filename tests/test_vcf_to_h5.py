
import unittest
import tempfile
from pathlib import Path

import numpy
import h5py

import test_setup
import test_utils
from variant.in_out import vcf_to_hdf5
from variant.in_out.vcf import SCIKIT_ALLEL_FIELD_PATHS
from variant import CHROM_FIELD, POS_FIELD


class H5CreationTest(unittest.TestCase):

    def test_h5_creation(self):
        vcf_fhand = test_utils.create_temp_vcf_file()
        h5_fhand = tempfile.NamedTemporaryFile(suffix='.h5')
        vcf_to_hdf5(Path(vcf_fhand.name), Path(h5_fhand.name))

        h5 = h5py.File(h5_fhand.name, 'r')
        assert all(numpy.equal(h5['samples'][:],
                               [b'NA00001', b'NA00002', b'NA00003']))
        assert all(numpy.equal(h5[SCIKIT_ALLEL_FIELD_PATHS[CHROM_FIELD]][:],
                               [b'20', b'20', b'20', b'20', b'20']))
        assert all(numpy.equal(h5[SCIKIT_ALLEL_FIELD_PATHS[POS_FIELD]][:],
                               [14370, 17330, 1110696, 1230237, 1234567]))


if __name__ == '__main__':
    unittest.main()
