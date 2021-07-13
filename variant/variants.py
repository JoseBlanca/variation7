
import functools
from pathlib import Path

import h5py

from delayed_array.delayed_array import DelayedArray, DsetInfo

from variant._config import (SCIKIT_ALLEL_VARIANTS_GROUP_NAME,
                             SCIKIT_ALLEL_CALL_GROUP_NAME,
                             FIELDS_FROM_SCIKIT_ALLEL_FIELD_PATHS,
                             SCIKIT_ALLEL_FIELD_PATHS)
from variant import SAMPLE_FIELD, GT_FIELD


class Variants:
    @functools.singledispatchmethod
    def __init__(self):
        raise NotImplementedError('')

    @__init__.register
    def _(self, h5_path:Path, ignore_unknown_fields=True):
        self.arrays = {}
        self.h5 = h5py.File(h5_path, 'r')
        self.ignore_unknown_fields = ignore_unknown_fields
        self._register_h5_dsets()

    @__init__.register
    def _(self, numpy_arrays:dict, ignore_unknown_fields=True):
        self.arrays = {}
        self.ignore_unknown_fields = ignore_unknown_fields
        print(f'{numpy_arrays=}')

    def _register_h5_dsets(self):
        h5_path = Path(self.h5.filename)

        for group_name in [SCIKIT_ALLEL_VARIANTS_GROUP_NAME,
                           SCIKIT_ALLEL_CALL_GROUP_NAME]:
            for dset_name, dset in self.h5[group_name].items():
                dset_path = f'{group_name}/{dset_name}'
                try:
                    field = FIELDS_FROM_SCIKIT_ALLEL_FIELD_PATHS[dset_path]
                except KeyError:
                    if self.ignore_unknown_fields:
                        continue
                    else:
                        raise
                dset_info = DsetInfo(h5_path, dset_path)
                self.arrays[field] = DelayedArray(dset_info)
        self._samples = DelayedArray(DsetInfo(h5_path,
                                     SCIKIT_ALLEL_FIELD_PATHS[SAMPLE_FIELD]))

    @property
    def samples(self):
        return self._samples[:]

    @property
    def num_samples(self):
        return len(self.samples)

    @property
    def num_variants(self):
        shape = self.arrays[GT_FIELD].shape
        if shape:
            return shape[0]
        raise RunTimeError('num_variants is still not available')

    @property
    def ploidy(self):
        shape = self.arrays[GT_FIELD].shape
        return shape[2]