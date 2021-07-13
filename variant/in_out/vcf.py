
import allel

from variant._config import SCIKIT_ALLEL_FIELD_PATHS


def vcf_to_hdf5(vcf_path, h5_path, fields=None):

    if fields is None:
        scikit_allel_fields = None
    else:
        scikit_allel_fields = [SCIKIT_ALLEL_FIELD_PATHS[field] for field in fields]
        if 'samples' not in scikit_allel_fields:
            scikit_allel_fields.append('samples')

    allel.vcf_to_hdf5(str(vcf_path), str(h5_path), fields=scikit_allel_fields)
