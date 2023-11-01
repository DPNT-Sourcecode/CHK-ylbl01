
# noinspection PyUnusedLocal
# skus = unicode string

from collections import Counter
from collections import defaultdict


def checkout(skus):
    price_info = {
        'A': {'price':50, 'offer':[{'type':'multibuy', 'quantity':3,'discounted_price':130},{'type':'multibuy', 'quantity':5,'discounted_price':200}]},
        'B': {'price':30, 'offer':[{'type':'multibuy','quantity':2,'discounted_price':45}]},
        'C': {'price':20, 'offer':None},
        'D': {'price':15, 'offer':None},
        'E': {'price':40, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]},
        'F': {'price':10, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'F'}]}
    }
    basket_summary = Counter(skus)
    for item, count in basket_summary.items():
        if item not in price_info:
            return -1
    basket_summary = remove_free_items(basket_summary,price_info)
    basket_price = 0

    for item, count in basket_summary.items():
        if item in price_info:
            details = price_info[item]
            if details['offer'] == None:
                basket_addition_from_item = details['price']*count
            else:
                basket_addition_from_item = get_optimal_price_for_item(item,count,details['price'],details['offer'],price_info)
            basket_price += basket_addition_from_item
        else:
            return -1
    return basket_price

def remove_free_items(item_counter,price_info):
    new_counter = defaultdict(int)
    print(item_counter)
    for item, count in item_counter.items():
        if price_info[item]['offer']:
            offer = price_info[item]['offer'][0] #item['offer'][0]
            if offer['type'] == 'buy_x_get_free':
                free_item = offer['free_item']
                if free_item == item:
                    if count <= offer['buy']:
                        new_counter[item] += count
                    else:

                        number_of_free_items= ((count-1) // offer['buy']) * offer['get']
                        new_counter[free_item] = count - number_of_free_items


                else:
                    number_of_free_items= (count // offer['buy']) * offer['get']
                    new_counter[free_item] -= number_of_free_items
                    new_counter[item] += count
            else:
                new_counter[item] += count
        else:
            new_counter[item] += count
    print(new_counter)
    for key, value in new_counter.items():
        if value < 0:
            new_counter[key] = 0
    return new_counter

def get_optimal_price_for_item(item, count,price, offer_list,price_info):

    best_price = count * price
    for i in range(len(offer_list)):

        offer = offer_list[i]
        if offer['type'] == 'multibuy' and count >= offer['quantity']:
            best_price = count * price
            multibuy_instances = count // offer['quantity']
            multibuy_leftover = count % offer['quantity']
            multibuy_price = multibuy_instances * offer['discounted_price']
            remaining_offer_list = offer_list[:i] + offer_list[i+1:]
            if multibuy_leftover != 0:
                left_over_optimal_price = get_optimal_price_for_item(item,multibuy_leftover,price,remaining_offer_list,price_info)
            else:
                left_over_optimal_price = 0
            current_price = multibuy_price + left_over_optimal_price
            best_price = min(best_price,current_price)

    return best_price

