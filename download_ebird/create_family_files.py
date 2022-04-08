import pandas as pd
import numpy as np
ec = pd.read_csv('eBird_Taxonomy_v2019.csv', sep='\t')

ec = ec[ec.CATEGORY=='species']

fams = np.unique(ec.FAMILY.values)
for fam in fams:
    sps = ec[ec.FAMILY == fam][['SCI_NAME']]
    sps.to_csv('./target_list/%s.txt' % fam.strip(), index=False)

