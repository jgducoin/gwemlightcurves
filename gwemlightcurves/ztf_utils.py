
import os, sys
from matplotlib import pyplot as plt
import requests
import numpy as np
from astropy.time import Time

try:
    from penquins import Kowalski
except:
    print('Please install penquins')
    pass

def get_ztf(filename, name, username, password):

    k = Kowalski(username=username, password=password, verbose=True)

    q = {"query_type": "general_search",
     "query": "db['ZTF_alerts'].find({'objectId': {'$eq': '"+name+"'}})"
     }
    r = k.query(query=q,timeout=10)
    if len(r['result_data']['query_result']) >0:
        candidate = r['result_data']['query_result'][0]
        prevcandidates= r['result_data']['query_result'][0]['prv_candidates']

        jd = [candidate['candidate']['jd']]
        mag = [candidate['candidate']['magpsf']]
        magerr = [candidate['candidate']['sigmapsf']]
        filt = [candidate['candidate']['fid']]

        for candidate in prevcandidates:
            jd.append(candidate['jd'])
            if not candidate['magpsf'] == None:
                mag.append(candidate['magpsf'])
            else:
                mag.append(candidate['diffmaglim'])
            if not candidate['sigmapsf'] == None:
                magerr.append(candidate['sigmapsf'])
            else:
                magerr.append(np.inf)

            filt.append(candidate['fid'])
        filtname = []
        for f in filt:
            if f == 1:
                filtname.append('g')
            elif f == 2:
                filtname.append('r')
            elif f == 3:
                filtname.append('i')
    idx = np.argsort(jd)

    fid = open(filename,'w')
    for ii in idx:
        t = Time(jd[ii], format='jd').isot
        fid.write('%s %s %.5f %.5f\n'%(t,filtname[ii],mag[ii],magerr[ii]))
    fid.close()

