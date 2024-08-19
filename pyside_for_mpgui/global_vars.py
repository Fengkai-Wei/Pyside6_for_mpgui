import meep as mp
import numpy as np
from meep.materials import SiO2,cSi,aSi,ITO,Al2O3,GaAs,AlAs,AlN,BK7,Si3N4,Ge,InP,GaN,CdTe,LiNbO3,BaB2O4,CaWO4,CaCO3,Y2O3,YAG,PMMA,PC,PS,CLS,Ag,Au,Cu,Al,Be,Cr,Ni,Pd,Pt,Ti,W
def dummy_src(time):
    return (np.sin(time))





def init():
    global var_dict
    var_dict = {
        'Material':{'c-Si':cSi,
                    'a-Si':aSi,
                    'Al':Al,
                    'SiO2':SiO2,
                    'Vaccum':mp.air,
                    'ITO': ITO,
                    'Al2O3': Al2O3,
                    'GaAs': GaAs,
                    'AlAs': AlAs,
                    'AlN': AlN,
                    'BK7': BK7,         
                    'Si3N4': Si3N4,
                    'Ge': Ge,
                    'InP': InP,
                    'GaN': GaN,
                    'CdTe': CdTe,
                    'LiNbO3': LiNbO3,
                    'BaB2O4': BaB2O4,
                    'CaWO4': CaWO4,
                    'CaCO3': CaCO3,
                    'Y2O3': Y2O3,
                    'YAG': YAG,
                    'PMMA': PMMA,
                    'PC': PC,
                    'PS': PS,
                    'CLS': CLS,
                    'Ag': Ag,
                    'Au': Au,
                    'Cu': Cu,
                    'Be': Be,
                    'Cr': Cr,
                    'Ni': Ni,
                    'Pd': Pd,
                    'Pt': Pt,
                    'Ti': Ti,
                    'W': W,
                    },

        'Structure':{
            'Cylinder': mp.Cylinder(radius=0.2,height=1.0,material = aSi),
            'Block': mp.Block(size=(0.2,0.2,0.2),),
            'Sphere': mp.Sphere(radius=0.2),
            'Wedge': mp.Wedge(radius=0.2),
            'Cone': mp.Cone(radius=0.2),
            'Ellipsoid': mp.Ellipsoid(size = (0.2,0.2,0.2)),
            'Prism': mp.Prism(vertices=[mp.Vector3(-0.1,-0.1,0),mp.Vector3(-0.1,0.1,0),mp.Vector3(0.1,0.1,0),mp.Vector3(0.1,-0.1,0)], height=0.2),
                     },
        'geo':{},
        'Sources':{'Continuous Source': mp.ContinuousSource,
                   'Gaussian': mp.GaussianSource,
                   'Custom Source': mp.CustomSource,

        },
        'src':{},

        'Boundary':[],
        'CurrentSim':mp.Simulation(cell_size = mp.Vector3(2,2,2),resolution=50),
        'Monitors':{},
        'dft':{},
        'Frequency':1/1.55


                }
