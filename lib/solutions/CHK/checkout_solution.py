
# noinspection PyUnusedLocal
# skus = unicode string

from collections import Counter
def checkout(skus):
    price_info = {
        'A': {'price':50, 'offer':[{'type':'multibuy', 'quantity':3,'discounted_price':130},{'type':'multibuy', 'quantity':5,'discounted_price':200}},
        'B': {'price':30, 'offer':[{'type':'multibuy','quantity':2,'discounted_price':45}]},
        'C': {'price':20, 'offer':None},
        'D': {'price':15, 'offer':None},
        'E': {'price':60, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]}
    }
    # basket_summary = Counter(skus)
    # basket_price = 0
    # for item, count in basket_summary.items():
    #     if item in price_info:
    #         details = price_info[item]
    #         if details['offer'] and count >= details['offer']['quantity']:
    #             multibuy_instances = count // details['offer']['quantity']
    #             multibuy_leftover = count % details['offer']['quantity']
    #             basket_price += multibuy_instances * details['offer']['discounted_price']
    #             basket_price += multibuy_leftover * details['price']
    #         else:
    #             basket_price += count * details['price']
    #
    #     else:
    #         return -1
    # return basket_price








