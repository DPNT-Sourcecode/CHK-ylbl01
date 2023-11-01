
# noinspection PyUnusedLocal
# skus = unicode string

from collections import Counter

def checkout(skus):
    price_info = {
        'A': {'price':150, 'offer':{'quantity':3,'discounted_price':130}},
        'B': {'price':30, 'offer':{'quantity':2,'discounted_price':45}},
        'C': {'price':20, 'offer':None},
        'D': {'price':15, 'offer':None}
    }
    basket_summary = Counter(skus)
    for item, count in basket_summary.items():
        if item in price_info:
            details = price_info[item]
            if details['offer'] and count >= details['offer'][]
        else:
            return -1










