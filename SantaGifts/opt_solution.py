

import numpy as np
import pandas as pd

import itertools


## The number of gits of each type
def init_count():
    return {
        "horse": 1000,
        "ball": 1100,
        "bike": 500,
        "train": 1000,
        "coal": 166,
        "book": 1200,
        "doll": 1000,
        "blocks": 1000,
        "gloves": 200
    }

## The max number of gifts of a certain type to put in a bag
def init_limit():
    return {
        "horse": 6,
        "ball": 8,
        "bike": 2,
        "train": 3,
        "coal": 0,
        "book": 4,
        "doll": 6,
        "blocks": 3,
        "gloves": 4
    }

def generate_sample():
    sample = {}
    sample['ball'] = [max(0, 1 + np.random.normal(1,0.3,1)[0]) for i in range(1000000)]
    sample['bike'] = [max(0, np.random.normal(20,10,1)[0]) for i in range(1000000)]
    sample['blocks'] = [np.random.triangular(5,10,20,1)[0] for i in range(1000000)]
    sample['book'] = [np.random.chisquare(2,1)[0] for i in range(1000000)]
    sample['coal'] = [47 * np.random.beta(0.5,0.5,1)[0] for i in range(1000000)]
    sample['doll'] = [np.random.gamma(5,1,1)[0] for i in range(1000000)]
    sample['gloves'] = [3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0] for i in range(1000000)]
    sample['horse'] = [max(0, np.random.normal(5,2,1)[0]) for i in range(1000000)]
    sample['train'] = [max(0, np.random.normal(10,5,1)[0]) for i in range(1000000)]
    return sample

dispatch = {
    "horse": lambda:max(0, np.random.normal(5,2,1)[0]),
    "ball": lambda:max(0, 1 + np.random.normal(1,0.3,1)[0]),
    "bike": lambda:max(0, np.random.normal(20,10,1)[0]),
    "train": lambda:max(0, np.random.normal(10,5,1)[0]),
    "coal": lambda:47 * np.random.beta(0.5,0.5,1)[0],
    "book": lambda:np.random.chisquare(2,1)[0],
    "doll": lambda:np.random.gamma(5,1,1)[0],
    "blocks": lambda:np.random.triangular(5,10,20,1)[0],
    "gloves": lambda:3.0 + np.random.rand(1)[0] if np.random.rand(1) < 0.3 else np.random.rand(1)[0]
    }


'''
This function yields a generator containing all the different possible combinations possible in a bag for a
given gift type combination and number of gifts.
params:
    a: combination of gifts: e.g. (horse, ball), etc.
    n: Number of different types of gifts in the combination passed
    k: The number of gifts required in bag
'''
def combination_generator(a, n, k):
    if n > k: yield None
    elif n == 0: yield [] #This will never happen as per the parameters passed
    elif n == 1: yield a*k
    elif n == 2:
        for i in range(k-1): yield [a[0]]*(1+i) + [a[1]]*(k-i-1)
    elif k == 3: yield [a[0], a[1], a[2]] ## When there are 3 gifts in the combination and 3 gifts required in the bag
    else:
        generator = itertools.chain(
            combination_generator(a,n,k-2),
            combination_generator(a[1:],n-1,k-2),
            combination_generator(a[:-1],n-1,k-2),
            combination_generator(a[1:-1],n-2,k-2) )
        for iter in generator:
            if iter is not None: yield [a[0]] + iter + [a[-1]]
'''
This function returns the average weight for a given combination of gifts to fill the bag.
params:
    lst: list containing the names of the gifts.
    n: default value fixed to 1
'''
def simulator(lst, n):
    s = 0
    samples = 100000
    for i in range(samples):
        total_w = 0
        for i in range(n):
            w = 0
            for x in lst:
                w += dispatch[x]()
            if w <= 50:
                total_w += w
        s += total_w
    return s*1.0/samples
'''
params:
    n: The number of gifts required in the combination.
    lst_candidate: The types of gifts with quantity left > 0
    limit: The limit for each type of Gift
    thres1: The threshold based on the number of types of gifts in lst_candidate
    thres2: The threshold based on the number of types of gifts in lst_candidate
'''
def simulator_wrapper(n, lst_candidate, limit, percentileAvg, thres=50):
    combs = []
    cnt = 0
    print(lst_candidate);
    for i in range(1,n+1):
        for lst in itertools.combinations(lst_candidate, i):
            ## lst is a possible combination of gift to fill the bag
            for iter in combination_generator(list(lst), i, n):

                ## iter is a list of gifts for a bag for the given combination
                ## Calculating the average weight for this bag
                w = sum([percentileAvg[cate] for cate in iter])
                flag = True

                c = {}
                for x in iter:
                    c[x] = c.get(x, 0) + 1
                for x in iter:
                    if c[x] > limit[x]:
                        flag = False
                        break
                if flag and w <= thres:
                    cnt += 1
                    ###w = simulator(iter,1)
                    combs.append({'bag': iter, 'weight': w})
    return cnt, combs

def filterBags(percentileUpper, percentileLower, threshUp, threshLow, bags):
    filtered_bags = []
    for bag in bags:
        w_up = sum([percentileUpper[cate] for cate in bag['bag']])
        w_low = sum([percentileLower[cate] for cate in bag['bag']])
        if w_up < threshUp and w_low >= threshLow:
            filtered_bags.append(bag)
    return filtered_bags;

def fillBags(UPValue, LPValue):
    lst_all = ['horse', 'ball','train', 'book', 'doll', 'blocks', 'gloves', 'coal', 'bike']
    sample = generate_sample()
    percentileAvg = {}

    for cate in lst_all:
        percentileAvg[cate] = np.average(sample[cate]);

    count = init_count()
    shuffle_map = {}
    ## Creating a random set of the gift samples
    for k,v in count.items():
        shuffle_map[k] = np.random.permutation(np.arange(v))

    limit = init_limit()
    n_bags = 0
    w_bags = 0

    lst_candidate = [x for x in lst_all if count[x] > 0]
    combos = []
    # The range specifies the lower and upper limit of gits in a bag
    for i in range(3,15):
        c, combs = simulator_wrapper(i, lst_candidate, count, percentileAvg, 47);
        print ('Got a total of %s combinations for %s # of gifts' % (c, i) );
        for com in combs:
            combos.append(com);

    for upLimit in UPValue:
        for lowLimit in LPValue:
            percentileUpper = {}
            percentileLower = {}
            for cate in lst_all:
                percentileUpper[cate] = np.percentile(sample[cate], upLimit)
                percentileLower[cate] = np.percentile(sample[cate], lowLimit)
            filtered_bags = filterBags(percentileUpper, percentileLower, upLimit, lowLimit, combos);
            filename = 'Tests/submission_up_'+ str(upLimit) +'_low_'+str(lowLimit)+'.csv';
            f_out = open(filename, 'w')
            f_out.write('Gifts\n')
            filtered_bags = sorted(filtered_bags, key = lambda x: x['weight'], reverse = True);
            print 'Running for UpperLimit', upLimit, 'and lowerLimit', lowLimit, len(filtered_bags);
            count = init_count();
            n_bags = 0
            w_bags = 0
            while n_bags < 1000:
                best_comb = filtered_bags[0]
                ##print('Packaging...', best_comb['bag'])
                while n_bags < 1000:
                    bag = []
                    tmp_count = {}
                    flag = True
                    for x in best_comb['bag']:
                        if count[x] - tmp_count.get(x, 0) <= 0:
                            flag = False
                            del filtered_bags[0]
                            break
                        else:
                            tmp_count[x] = tmp_count.get(x, 0) + 1
                            idx = count[x] - tmp_count[x]
                            bag.append('%s_%s' % (x, shuffle_map[x][idx]))
                            #bag.append('%s_%s' % (x, idx))
                    if flag:
                        for x, c in tmp_count.items():
                            count[x] = count[x] - c
                        bag = ' '.join(bag) + '\n'
                        f_out.write(bag)
                        n_bags += 1
                        w_bags += best_comb['weight']
                    else:
                        break
                ##print('\tn_bags=%s, w_bags=%s' % (n_bags, w_bags))

            f_out.close()
            ##print 'The remaing gifts are', count


upperLimits = np.linspace(65, 75, 11)
lowerLimits = np.linspace(20, 25, 6)

fillBags(upperLimits, lowerLimits);
