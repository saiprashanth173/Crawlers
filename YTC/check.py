from multiprocessing import Pool

pool = Pool(8)

def check(k,b):
    print (k)
    print (b)

k=(1,3)
pool.apply_async(check,(1,3,))
