# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:50:52 2016

@author: Morgan
"""

source_file = SOME_PATH

for i, energy in enumerate(range(1, 100, 5)):

    # edit source file
    f1 = open('souce_file', 'r')
    f2 = open('souce_file', 'w')
    for line in f1:
        f2.write(line)
    f1.close()
    f2.close()

    # change directory
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

    # run cosima
    run("cosima" "filename")
