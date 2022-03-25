import os.path
import math

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.ticker import NullLocator

#------------------------------------------------------------------------------------------------------------------------------------
#Useful functions
#------------------------------------------------------------------------------------------------------------------------------------

# This function parses the output and returns a directionary of lists (that store the progress of each variable during CD) and a dictionary of values (the cumulative values)
def parseOutput(fname):

    if not os.path.exists(fname):
        return None
    f = open(fname)

    # dynamicERIProgress is a dictionary object that holds the step-by-step data obtained during the CD progress
    dynamicERIProgress = {}
    # dynamicERITotal is a dictionary object that holds cumulataive data
    dynamicERITotal = {}


    # Initialize the following keys for dynamicERIProgress to hold lists:

    # Pivot candidates. This corresponds to P in the paper
    dynamicERIProgress['D_size']= []

    # The current batch selected based on sigma and msigma. This corresponds to Q in the paper
    dynamicERIProgress['lenQ']= []

    # The number of computed ERI vectors (of length D) stored in memory. This corresponds to Epsilon in the paper
    dynamicERIProgress['ERI_vec']= []

    # The time used for shrinking of the current batch. This corresponds to line 39
    dynamicERIProgress['shrink_count']= []

    # Time used to do transpose for the current batch
    dynamicERIProgress['ERI_trans']= []

    # The number of ERIs calculated for current batch. This corresponds to line 20
    dynamicERIProgress['ERI_count']= []

    # Time used to calculate ERI for current batch, all threads added together. This corresponds to line 20
    dynamicERIProgress['ERI_duration_all']= []

    # Time used to calculate ERI for current batch, wall clock. This corresponds to line 20
    dynamicERIProgress['RI_duration_wall']= []

    # Time used to copy for the current batch. This corresponds to line 22
    dynamicERIProgress['ERI_copy']= []

    # Time used to do CD for the current batch. This corresponds to line 22
    dynamicERIProgress['CDalgMM']= []

    # Time used to do CD for the current batch in the innerloop. This corresponds to line 30
    dynamicERIProgress['innerloop_CDalgMM']= []

    # Time used for the current batch in the innerloop. This corresponds to line 27-33
    dynamicERIProgress['innerloop_dur']= []




    for line in f:

        # Add cumulative data key-value pairs into dynamicERITotal
        if 'Cholesky-RI-Pivots-ERI count' in line:
            dynamicERITotal['N1ERI'] = int(line.split('= ')[-1])

        if 'Cholesky-RI-Pivots-ERI duration' in line:
            dynamicERITotal['T1ERI_AllThreads'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-ERIvec duration     =' in line:
            dynamicERITotal['T1ERI_WC'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-ERIcopy duration    =' in line:
            dynamicERITotal['ERIcopy'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-ERItrans duration   =' in line:
            dynamicERITotal['ERItrans'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-CDalgMM duration    =' in line:
            dynamicERITotal['CDalgMM'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-CDalgMV duration    =' in line:
            dynamicERITotal['CDalgMV'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-Shrink count        =' in line:
            dynamicERITotal['NShrink'] = int(line.split('= ')[-1])

        if 'Cholesky-RI-Shrink duration     =' in line:
            dynamicERITotal['TShrink'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-misc duration       =' in line:
            dynamicERITotal['misc'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-Dynamic-ERI-Pivots duration =' in line:
            dynamicERITotal['T1'] = float(line.split('= ')[-1].split()[0])

        if 'Cholesky-RI-auxiliary dimension =' in line:
            dynamicERITotal['NPivots'] = int(line.split('= ')[-1])



        # Append values of each step into corresponding list in dynamicERIProgress
        if 'D size =' in line:
            dynamicERIProgress['D_size'].append(float(line.split('= ')[-1]))

        if 'lenQ:' in line:
            dynamicERIProgress['lenQ'].append(int(line.split(':')[-1]))

        if 'ERI size =' in line:
            dynamicERIProgress['ERI_vec'].append(int(line.split('= ')[-1]))

        if 'Current Shrink =' in line:
            dynamicERIProgress['shrink_count'].append(float(line.split('= ')[-1].split()[0]))

        if 'Current ERItrans =' in line:
            dynamicERIProgress['ERI_trans'].append(float(line.split('= ')[-1].split()[0]))

        if 'Current ERI count    =' in line:
            dynamicERIProgress['ERI_count'].append(int(line.split('= ')[-1]))

        if 'Current ERI duration =' in line:
            dynamicERIProgress['ERI_duration_all'].append(float(line.split('= ')[-1].split()[0]))

        if 'Current ERIvec =' in line:
            dynamicERIProgress['RI_duration_wall'].append(float(line.split('= ')[-1].split()[0]))

        if 'Current ERIcopy =' in line:
            dynamicERIProgress['ERI_copy'].append(float(line.split('= ')[-1].split()[0]))

        if 'Current CDalgMM =' in line:
            dynamicERIProgress['CDalgMM'].append(float(line.split('= ')[-1].split()[0]))

        if 'InnerLoop CDalgMV  =' in line:
            dynamicERIProgress['innerloop_CDalgMM'].append(float(line.split('= ')[-1].split()[0]))

        if 'InnerLoop duration =' in line:
            dynamicERIProgress['innerloop_dur'].append(float(line.split('= ')[-1].split()[0]))


    f.close()
    return dynamicERIProgress, dynamicERITotal


#------------------------------------------------------------------------------------------------------------------------------------

# Construct output filenames
root = '/Users/aodongliu/LiGroup/cholesky/study_param/H1000/libint_seg/'
system = 'H1000'
basis = 'sto3g'
integral_engine = 'libint'
contraction_type = 's'
taus = ['1e-8', '1e-6', '1e-4']
sigmas = ['1','5e-1','1e-1','5e-2','1e-2','5e-3','1e-3','5e-4','1e-4','5e-5','1e-5']
maxquals = [20000,5000,2000,1500,1250,1000,750,500,250,100,50,20,1]


for tau in taus:
    for sigma in sigmas:
        for maxqual in maxquals:

            fname = root + system

            fname += '_%s_%s%s' % (basis,integral_engine,contraction_type)

            fname += '_t%s_s%s_m%d' % (tau,sigma,maxqual)

            fname += '.out'

            #print(fname)

# Testing if parseOutput function works
progress, total = parseOutput('/Users/aodongliu/LiGroup/cholesky/study_param/H1000/libint_seg/H1000_sto3g_libints_t1e-6_s1e-5_m20.out')
progress.keys()
for key in progress.keys():
    print(key, len(progress[key]))
