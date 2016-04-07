# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:50:52 2016

@author: Morgan
"""

import os
import subprocess

source_file = 'SOME_PATH'

for i, energy in enumerate(range(1, 100, 5)):

    # edit source file
    with open(souce_file, 'r') as in_file, open(souce_file, 'w') as out_file:
        for line in in_file:
            out_file.write(line)


    # change directory
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    os.chdir(path)

    # run cosima
    subprocess.run("cosima" "filename")
