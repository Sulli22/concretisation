def read(fic):
    
    with open(fic,"r") as f:
        lines = f.readlines()
        
    val=[]
    for line in lines:
        if not line.startswith('c') and not line.startswith('p') and not line.startswith('%'):
            nums = (int(x) for x in line.split() if x!= "0")
            val.extend(nums)
    return val

def arrangement_3(fic):
    list_decomp = []
    val = read(fic)
    for i in range(0,len(read(fic)),3):
        list_decomp.append([val[i],val[i+1],val[i+2]])
    return list_decomp
           
print(arrangement_3("graphe.cnf"))



           

