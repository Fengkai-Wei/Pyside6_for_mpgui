import meep as mp
import numpy as np
from meep.materials import SiO2,cSi,aSi,ITO,Al2O3,GaAs,AlAs,AlN,BK7,Si3N4,Ge,InP,GaN,CdTe,LiNbO3,BaB2O4,CaWO4,CaCO3,Y2O3,YAG,PMMA,PC,PS,CLS,Ag,Au,Cu,Al,Be,Cr,Ni,Pd,Pt,Ti,W
def dummy_src(time):
    return (np.sin(time))


def reverse_dict(from_dict, find_val):
    key = next((k for k, v in from_dict.items() if v == find_val), None)
    return key

def reload_BC(sim, reload_list=[]):
    sim.restart_fields()
    for item in reload_list:
        sim.set_boundary(side = item.side,
                         direction = item.direction,
                         condition = item.condition)

def reload_mnt(reload_list):
    pass





def init():
    global var_dict, current_sim
    current_sim = mp.Simulation(cell_size = mp.Vector3(2,2,2),resolution=50)

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
            'Cylinder': mp.Cylinder,
            'Block': mp.Block,
            'Sphere': mp.Sphere,
            'Wedge': mp.Wedge,
            'Cone': mp.Cone,
            'Ellipsoid': mp.Ellipsoid,
            'Prism': mp.Prism,
                     },
        'geo':{},
        'Sources':{'Continuous Source': mp.ContinuousSource,
                   'Gaussian': mp.GaussianSource,
                   'Custom Source': mp.CustomSource,

        },
        'src':{},

        'Boundary':[],
        'CurrentSim':mp.Simulation(cell_size = mp.Vector3(2,2,2),resolution=50),
        
        'Monitors':{
            'Flux': current_sim.add_flux,
            'Field': current_sim.add_dft_fields,
            'Force': current_sim.add_force,
            'Energy': current_sim.add_energy,
            'Mode': current_sim.add_mode_monitor,
            'Near to Far': current_sim.add_near2far,
        },
        'dft':{},
        'Frequency':1/1.55,

        'direction':{'X': mp.X,
                     'Y': mp.Y,
                     'Z': mp.Z,
                     'R': mp.R,
                     'P': mp.P,
        },

        'side':{'High': mp.High,
                'Low': mp.Low,
        },

        'boundary_condition':{'Metallic': mp.Metallic,
                              'Magnetic': mp.Magnetic,
        },



                }
