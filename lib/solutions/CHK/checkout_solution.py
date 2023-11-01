
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
        'F': {'price':10, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'F'}]},
        'G': {'price':20, 'offer':None},
        'H': {'price':10, 'offer':[{'type':'multibuy', 'quantity':5,'discounted_price':45},{'type':'multibuy', 'quantity':10,'discounted_price':80}]},
        'I': {'price':35, 'offer':None},
        'J': {'price':60, 'offer':None},
        'K': {'price':80, 'offer':[{'type':'multibuy','quantity':2,'discounted_price':150}]},
        'L': {'price':90, 'offer':None},
        'M': {'price':15, 'offer':None},
        'N': {'price':40, 'offer':[{'type':'buy_x_get_free','buy':3,'get':1,'free_item':'M'}]},
        'O': {'price':10, 'offer':None},
        'P': {'price':50, 'offer':[{'type':'multibuy','quantity':5,'discounted_price':200}]},
        'Q': {'price':30, 'offer':[{'type':'multibuy','quantity':3,'discounted_price':80}]},
        'R': {'price':50, 'offer':[{'type':'buy_x_get_free','buy':3,'get':1,'free_item':'Q'}]},
        'S': {'price':20, 'offer':[{'type':'group','quantity':3,'discounted_price':45}]},
        'T': {'price':20, 'offer':[{'type':'group','quantity':3,'discounted_price':45}]},
        'U': {'price':40, 'offer':[{'type':'buy_x_get_free','buy':3,'get':1,'free_item':'U'}]},
        'V': {'price':50, 'offer':[{'type':'multibuy', 'quantity':2,'discounted_price':90},{'type':'multibuy', 'quantity':3,'discounted_price':130}]},
        'W': {'price':20, 'offer':None},
        'X': {'price':17, 'offer':[{'type':'group','quantity':3,'discounted_price':45}]},
        'Y': {'price':20, 'offer':[{'type':'group','quantity':3,'discounted_price':45}]},
        'Z': {'price':21, 'offer':[{'type':'group','quantity':3,'discounted_price':45}]},
    }


    basket_summary = Counter(skus)
    for item, count in basket_summary.items():
        if item not in price_info:
            return -1
    basket_summary = remove_free_items(basket_summary,price_info)
    print('before' ,basket_summary)
    basket_summary, number_group_offers = remove_group_items(basket_summary,price_info)
    print('after' ,basket_summary)
    basket_price = 45 * number_group_offers

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

def extract_group_offer_items(price_info):
    extracted_prices = {}
    for item, details in price_info.items():
        if details['offer'] and any(offer['type']=='group' for offer in details['offer']):
            extracted_prices[item] = details['price']
    return extracted_prices

def remove_group_items(item_counter,price_info):
    group_prices = extract_group_offer_items(price_info)
    group_items = list(group_prices.keys())

    group_items_count = {item: item_counter[item] for item in group_items if item in item_counter}
    sorted_group_items = sorted(group_items_count.keys(), key=lambda item: group_prices[item], reverse=True)

    total_group_item_count = sum(group_items_count.values())
    number_group_offers = total_group_item_count // 3
    items_to_deduct = (total_group_item_count // 3) * 3

    for item in sorted_group_items:
        while item_counter[item] > 0 and items_to_deduct > 0:
            item_counter[item] -= 1
            items_to_deduct -= 1
    return item_counter , number_group_offers

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