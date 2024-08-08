import global_vars 
import gc
def add_var(key,value):
    global_vars.var_dict.update({key:value})

def rm_var(key,dict):
    if key in dict:
        del dict[key]
        gc.collect()

    else:
        pass