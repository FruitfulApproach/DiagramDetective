

def filter_out_gfx_descendents(items:list):
    descendent_free = []
    
    for i in items:
        for j in items:
            if i is not j:
                if j.isAncestorOf(i):
                    break
        else:
            descendent_free.append(i)
            
    return descendent_free