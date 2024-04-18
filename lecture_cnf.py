def lecture(fic):
    
    with open(fic,"r") as f:
        lines = f.readlines()
        
    val=[]
    
    
    for line in lines:
        if not line.startswith('c') and not line.startswith('p') and not line.startswith('%'):
            nums = (int(x) for x in line.split() if x!= "0")
            val.extend(nums)
    return val

for i in lecture("graphe.cnf"):
    
           



           

