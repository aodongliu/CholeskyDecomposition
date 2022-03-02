import os
import subprocess
import shutil

algs = ['dynamiceri'] #, 'traditional', 'dynamicall']
taus = ['1e-8', '1e-6', '1e-4']
sigmas = ['1e-2']
b4Is = [False]#, True]
maxquals = [1000]#, 500, 2000, 200, 5000, 100, 50, 20, 1, 20000]
nsmps = [28,1,14,1,2,4,7,10,20]

input_template = """[Molecule]
charge = 0
mult = 1
geom:
  Au 0.000000 1.301287 3.455717
 Au 0.000000 -1.301287 3.455717
 Au 0.000000 -2.411924 1.122548
 Au 0.000000 -3.442601 -1.385463
 Au 0.000000 -1.299933 -3.054007
 Au 0.000000 1.299933 -3.054007
 Au 0.000000 3.442601 -1.385463
 Au 0.000000 2.411924 1.122548
 Au 1.289497 0.000000 1.495924
 Au 1.338260 -1.268643 -0.817359
 Au 1.338260 1.268643 -0.817359
 Au -1.289497 0.000000 1.495924
 Au -1.338260 -1.268643 -0.817359
 Au -1.338260 1.268643 -0.817359

[QM]
reference = GPBE0
job = SCF
x2ctype = OneE
atomicx2c = ALH


[SCF]
guess = core
damp = false
nkeep = 10
maxiter = 12800
ENETOL = 1e-8

[INTS]
alg = incore
ri  = RIALG
rithreshold = RITAU
risigma = RISIGMA
ribuild4index = RIB4I
rimaxqual = RIMAXQUAL

[MISC]
nsmp = RINSMP
mem = 240 GB

[BASIS]
definebasis = true
basisdef :
 ****
 Au     0
 S   8   1.00
 20162259.58330972            0.0035038
 3070855.39820743             0.0099910
  728175.48979388             0.0212369
  223539.37274308             0.0396609
   82113.74582179             0.0720153
   32730.86613529             0.1300336
   13145.26241266             0.2696207
    5338.79545761             0.4539375
 S   3   1.00
    2243.10985958            -0.4725186
     986.09034544            -0.3723481
     453.26974469            -0.1551332
 S   3   1.00
      37.80244178            -0.5907388
      20.15005714            -0.3940365
       8.27623094            -0.0152246
 S   2   1.00
     195.94631681            -0.6932958
      92.55850653            -0.3067041
 S   1   1.00
       4.24755314            -1.0000000
 S   1   1.00
       1.34336664             1.0000000
 S   1   1.00
       0.59529825            -1.0000000
 S   1   1.00
       0.08994935             1.0000000
 S   1   1.00
       0.03343767             1.0000000
 P   8   1.00
   73383.54251702             0.0020347
   17472.50869505             0.0059899
    5638.93703523             0.0195357
    2098.19025069             0.0613422
     851.53864397             0.1596535
     368.70358160             0.3281625
     168.00266115             0.3049154
      78.46531818             0.1183659
 P   2   1.00
      38.03978273            -0.9924652
      18.76567430            -0.0075347
 P   2   1.00
       8.59064706             0.7437797
       4.07645406             0.2562202
 P   1   1.00
       1.46203761             1.0000000
 P   1   1.00
       0.54164607             1.0000000
 P   1   1.00
       0.20129280             1.0000000
 D   5   1.00
    1515.76145260             0.0080822
     455.90133736             0.0496076
     173.87649659             0.1950572
      73.92719918             0.3733694
      33.19874243             0.3738834
 D   2   1.00
      14.34491022            -0.5068337
       6.21807304            -0.4931662
 D   1   1.00
       2.45352195             1.0000000
 D   1   1.00
       0.91871833             1.0000000
 D   1   1.00
       0.36349181             1.0000000
 F   4   1.00
      86.55080722             0.0540446
      27.62667451             0.2308307
       9.86249821             0.3955567
       3.32239166             0.3195678
 F   1   1.00
       2.57279125             1.0000000
 F   1   1.00
       0.92170017             1.0000000
 G   1   1.00
       1.98804717             1.0000000
 ****
"""



for nsmp in nsmps:
    for b4I in b4Is:
        for tau in taus:
            for alg in algs:
                sigmaCount = 0
                for sigma in sigmas:
                    for maxqual in maxquals:
                        if sigmaCount > 0: # This statement is used to skip sigma and maxqual iterations for traditional and dynamicall algorithms
                            continue

                        if 'spanfactor' not in alg and 'dynamiceri' != alg:
                            sigmaCount += 1

                        fname = 'Au14_jorge_tzp_dkh_%s_t%s_%s' % (alg, tau, 'B' if b4I else 'D')
                        if 'spanfactor' in alg or 'dynamiceri' == alg:
                            fname += '_s%s_m%d' % (sigma,maxqual)

                        fname += '_n%d' % (nsmp,)

                        if os.path.exists(fname+'.out'):
                            continue

                        fname += '.inp'

                        fin = input_template.replace('RIALG', alg)\
                                            .replace('RITAU', tau)\
                                            .replace('RISIGMA', sigma)\
                                            .replace('RIMAXQUAL', str(maxqual))\
                                            .replace('RIB4I', str(b4I))\
                                            .replace('RINSMP', str(nsmp))

                        f = open(fname, 'w')

                        f.write(fin)

                        f.close()

                        subprocess.call("/gscratch/chem/tzhang93/Source/chronusq_dev/build/chronusq "+fname, shell=True)

