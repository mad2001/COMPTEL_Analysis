Author: Morgan A. Daly
Created: Summer 2015


This folder contains the modules necessary to transform a computer
simulated set of data into data resembling the output of the COMPTEL
telescope.

Simulation data is generated as a text file by the Medium Energy Gamma
Ray library (MEGAlib). Specifically, the output used is from Cosima, the
MEGAlib interface for CERN's Geant4 package. Cosima was used to recreate
the subatomic events involved in the neutron interactions within COMPTEL.

This program turns a text file into data that can be used to construct a
response matrix for COMPTEL's response to neutrons.


General process is as follows:
1) Parses simulation's text file, organizes data into ndarray
2) Identifies the module that each interaction occurred in
3) Converts the kinetic energy loss into its electron equivalent
4) Creates COMPTEL's interpretation of the interactions by taking
    the energy weighted average of the data for each module
5) Broadens that data by an experimentally determined and accepted
    Gaussian distribution
6) Identifies the hits that would have triggered COMPTEL

* note that unless explicitly stated otherwise units should be assumed
    to be centimeters (cm) and kilo electron volts (keV).





###########################################################################
#######              MEGAlib Documentation Snippets                 #######
###########################################################################

GEOMEGA
--------
    SPHE (a sphere, which can be hollow, or a segment of it)
    2: inner radius in cm 3: outer radius in cm 4: theta min in deg
    5: theta max in deg 6: phi min in deg 7: phi max in deg

    TUBS (a cylinder, which can be hollow, or a section of it)
    2: inner radius in cm 3: outer radius in cm 4: half height in cm
    5: phi min in deg 6: phi max in deg

    PCON (a polycone – round corners)
    2: the azimuthal angle phi at which the volume begins
    (angles are counted counterclockwise) 3: opening angle of the volume
    4: number of sections
    (number of time the following three arguments are repeated),
    the number should be at least 2
    The following three arguments are repeated accordingly:
    M1: height (full not half) M2: inner radius M3: outer radius

    PGON (a polygon)
    2: the azimuthal angle phi at which the volume begins
    (angles are counted counterclockwise) 3: opening angle of the volume
    4: number of sides of the cross section between the given phi limits
    5: number of sections (number of time the following three
    arguments are repeated), number should be at least 2
    The following three arguments are repeated accordingly
    M1: height (full not half) M2: inner radius M3: outer radius



These are measurements that correspond with those used in the construction
of geometry for MEGAlib simulations.
They may vary slightly from actual COMPTEL measurements.

GEOMETRY FILE NOTES:
    SurroundingSphere 250.0 0.0 0.0 0.0 250.0


Could store size and position seperate and calculate it for copies
    store "(0, 0, 0)" position
    store dimensions
    then relate

SETU

    CGRO_MOTH: (0, 0, 0)

    Volume SETU
    SETU.Shape PCON 0. 360. 2. 0. 0. 85. 254.9 0. 85.
    // this position brings D1 to same height as in simplified CGRO_COMPTEL model
    SETU.Position 0 0 -117.4
    SETU.Mother CGRO_MOTH

    D1
        Volume DET1
        DET1.Shape PCON 0. 360. 4   20.5 0. 73.  -5.4 0. 73. -5.4 0. 66.5 -20.5  0. 66.5
        DET1.Material VACUUM
        DET1.Position 0 0 209.45
        DET1.Rotation 0 0 0
        DET1.Mother SETU

            Volume D1MD
            D1MD.Shape TUBS 0 24.6 5.6 0 360
            D1MD.Material VACUUM

                D1MD_Copy1.Position 0 0 10.3
                D1MD_Copy1.Rotation 90 0 90 90 0 0
                D1MD_Copy1.Mother DET1

                D1MD_Copy2.Position -42.3 0 10.3
                D1MD_Copy2.Rotation 90 22.5 90 112.5 4.9614e-15 -112.5
                D1MD_Copy2.Mother DET1

                D1MD_Copy3.Position -26 39.1 10.3
                D1MD_Copy3.Rotation 90 0 90 90 0 0
                D1MD_Copy3.Mother DET1

                D1MD_Copy4.Position 26 39.1 10.3
                D1MD_Copy4.Rotation 90 0 90 90 0 0
                D1MD_Copy4.Mother DET1

                D1MD_Copy5.Position 42.3 0 10.3
                D1MD_Copy5.Rotation 90 22.5 90 112.5 4.9614e-15 -112.5
                D1MD_Copy5.Mother DET1

                D1MD_Copy6.Position 26 -39.1 10.3
                D1MD_Copy6.Rotation 90 0 90 90 0 0
                D1MD_Copy6.Mother DET1

                D1MD_Copy7.Position -26 -39.1 10.3
                D1MD_Copy7.Rotation 90 0 90 90 0 0
                D1MD_Copy7.Mother DET1

                    Volume D1SN
                    D1SN.Shape PGON 0. 360. 16 2 -4.25 0. 13.47 4.25 0. 13.47
                    D1SN.Material LIQNE213A

                    D1SN.Copy D1SN_Copy1
                    D1SN_Copy1.Position 0 0 0
                    D1SN_Copy1.Rotation 0. 0. 11.25
                    D1SN_Copy1.Mother D1MD


    D2
        Volume DET2
        DET2.Shape PCON 0. 360. 6  -26.1 0. 68.158  0.5 0. 68.158  0.5 0. 66.5  13.5 0. 66.5 13.5 0. 72.75  26.1 0 72.75
        DET2.Material VACUUM
        DET2.Many true
        DET2.Position 0 0 52.1
        DET2.Rotation 0 0 0
        DET2.Mother SETU

            Volume D2MD
            D2MD.Shape TUBS 0 15 20.75 0 360
            D2MD.Material VACUUM

                D2MD.Copy D2MD_Copy1
                D2MD_Copy1.Position 30.2 -41.254 -4.6875
                D2MD_Copy1.Rotation 90 -150 90 -60 4.9614e-15 75
                D2MD_Copy1.Mother DET2

                Volume D2SN
                D2SN.Shape TUBS 0 14.085 3.7625 0 360
                D2SN.Material NaITl

                D2SN.Copy D2SN_Copy1
                D2SN_Copy1.Position 0 0 14.3375
                D2SN_Copy1.Rotation 90 0 90 90 0 0
                D2SN_Copy1.Mother D2MD

                D2MD.Copy D2MD_Copy2
                D2MD_Copy2.Position 0 -41.254 -4.6875
                D2MD_Copy2.Rotation 90 -150 90 -60 4.9614e-15 75
                D2MD_Copy2.Mother DET2

                D2MD.Copy D2MD_Copy3
                D2MD_Copy3.Position -30.2 -41.254 -4.6875
                D2MD_Copy3.Rotation 90 -150 90 -60 4.9614e-15 75
                D2MD_Copy3.Mother DET2

                D2MD.Copy D2MD_Copy4
                D2MD_Copy4.Position 45.3 -15.1 -4.6875
                D2MD_Copy4.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy4.Mother DET2

                D2MD.Copy D2MD_Copy5
                D2MD_Copy5.Position 15.1 -15.1 -4.6875
                D2MD_Copy5.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy5.Mother DET2

                D2MD.Copy D2MD_Copy6
                D2MD_Copy6.Position -15.1 -15.1 -4.6875
                D2MD_Copy6.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy6.Mother DET2

                D2MD.Copy D2MD_Copy7
                D2MD_Copy7.Position -45.3 -15.1 -4.6875
                D2MD_Copy7.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy7.Mother DET2

                D2MD.Copy D2MD_Copy8
                D2MD_Copy8.Position 45.3 15.1 -4.6875
                D2MD_Copy8.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy8.Mother DET2


                D2MD.Copy D2MD_Copy9
                D2MD_Copy9.Position 15.1 15.1 -4.6875
                D2MD_Copy9.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy9.Mother DET2


                D2MD.Copy D2MD_Copy10
                D2MD_Copy10.Position -15.1 15.1 -4.6875
                D2MD_Copy10.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy10.Mother DET2


                D2MD.Copy D2MD_Copy11
                D2MD_Copy11.Position -45.3 15.1 -4.6875
                D2MD_Copy11.Rotation 90 -165 90 -75 4.9614e-15 60
                D2MD_Copy11.Mother DET2

                D2MD.Copy D2MD_Copy12
                D2MD_Copy12.Position 30.2 41.254 -4.6875
                D2MD_Copy12.Rotation 90 -150 90 -60 4.9614e-15 75
                D2MD_Copy12.Mother DET2

                D2MD.Copy D2MD_Copy13
                D2MD_Copy13.Position 0 41.254 -4.6875
                D2MD_Copy13.Rotation 90 -150 90 -60 4.9614e-15 75
                D2MD_Copy13.Mother DET2

                D2MD.Copy D2MD_Copy14
                D2MD_Copy14.Position -30.2 41.254 -4.6875
                D2MD_Copy14.Rotation 90 -150 90 -60 4.9614e-15 75
                D2MD_Copy14.Mother DET2


    Veto Dome 1
        Volume V1TP
        V1TP.Shape SPHE 140.168 141.668 0 33.176 0 360
        V1TP.Material NE110_V1DOME
        V1TP.Position 0 0 113
        V1TP.Rotation 90 0 90 90 0 0
        V1TP.Mother SETU

        Volume V1SD
        V1SD.Shape PCON 0. 360. 4   -31.732 75.694 77.194   30.08 75.694 77.194   30.08 76.71 77.194  30.78 77.1935 77.194
        V1SD.Material NE110_V1DOME
        V1SD.Position 0 0 200.232
        V1SD.Rotation 0 0 0
        V1SD.Mother SETU

    Veto Dome 2
        Volume V2TP
        V2TP.Shape SPHE 147.94 149.34 152.274 180 0 360
        V2TP.Material NE110_V2a4DOME
        V2TP.Position 0 0 295.5
        V2TP.Rotation 90 0 90 90 0 0
        V2TP.Mother SETU

        Volume V2SD
        V2SD.Shape PCON 0. 360. 4 -13.86 69.5575 69.558  -12.492 68.85 69.558 -12.492 68.158 69.558 13.961 68.158 69.558
        V2SD.Material NE110_V2a4DOME
        V2SD.Position 0 0 177.039
        V2SD.Rotation 0. 0 0
        V2SD.Mother SETU

    Veto Dome 3
        Volume V3TP
        V3TP.Shape SPHE 140.24 141.74 0 33.176 0 360
        V3TP.Material NE110_V3DOME
        V3TP.Position 0 0 -23
        V3TP.Rotation 90 0 90 90 0 0
        V3TP.Mother SETU

        Volume V3SD
        V3SD.Shape PCON 0. 360. 4  -31.732 76.148 77.648  30.14 76.148 77.648   30.14 76.75 77.648  31.5 77.6475 77.648
        V3SD.Material NE110_V3DOME
        V3SD.Position 0 0 64.232
        V3SD.Rotation 0 0 0
        V3SD.Mother SETU

    Veto Dome 4
        Volume V4TP
        V4TP.Shape SPHE 147.94 149.34 152.274 180 0 360
        V4TP.Material NE110_V2a4DOME
        V4TP.Position 0 0 157.1
        V4TP.Rotation 90 0 90 90 0 0
        V4TP.Mother SETU

        Volume V4SD
        V4SD.Shape PCON 0. 360. 4 -13.86 69.5575 69.558  -12.492 68.85 69.558 -12.492 68.158 69.558 13.961 68.158 69.558
        V4SD.Material NE110_V2a4DOME
        V4SD.Position 0 0 38.639
        V4SD.Rotation 0 0 0
        V4SD.Mother SETU