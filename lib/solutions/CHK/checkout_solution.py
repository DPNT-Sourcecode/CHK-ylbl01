
# noinspection PyUnusedLocal
# skus = unicode string

from collections import Counter
def checkout(skus):
    price_info = {
        'A': {'price':50, 'offer':[{'type':'multibuy', 'quantity':3,'discounted_price':130},{'type':'multibuy', 'quantity':5,'discounted_price':200}]},
        'B': {'price':30, 'offer':[{'type':'multibuy','quantity':2,'discounted_price':45}]},
        'C': {'price':20, 'offer':None},
        'D': {'price':15, 'offer':None},
        'E': {'price':60, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]}
    }
    basket_summary = Counter(skus)
    basket_price = 0
    for item, count in basket_summary.items():
        if item in price_info:
            details = price_info[item]
            if details['offer'] == None:
                basket_addition_from_item = details['price']*count
            else:
                basket_addition_from_item = get_optimal_price_for_item(item,count,details['price'],details['offer'],price_info)
            basket_price += basket_addition_from_item

            # best_price = count * details['price']
            # for offer in details.get('offer',[]):
            #     if offer['type'] == 'multibuy' and count >= offer['quantity']:
            #         multibuy_instances = count // offer['quantity']
            #         multibuy_leftover = count % details['offer']['quantity']
            # if details['offer'] and count >= details['offer']['quantity']:
            #     multibuy_instances = count // details['offer']['quantity']
            #     multibuy_leftover = count % details['offer']['quantity']
            #     basket_price += multibuy_instances * details['offer']['discounted_price']
            #     basket_price += multibuy_leftover * details['price']
            # else:
            #     basket_price += count * details['price']
        else:
            return -1
    return basket_price

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
        elif offer['type'] == 'buy_x_get_free' and count >= offer['buy']:
            offer_instances = count // offer['buy']
            free_item = price_info[offer['free_item']]
            number_free_items = offer_instances*offer['get']
            leftover_value = get_optimal_price_for_item(free_item,number_free_items,free_item['price'],free_item.get('offer',[]),price_info)
            best_price = count * price + leftover_value



    return best_price

# price_info = {
#     'A': {'price':50, 'offer':[{'type':'multibuy', 'quantity':3,'discounted_price':130},{'type':'multibuy', 'quantity':5,'discounted_price':200}]},
#     'B': {'price':30, 'offer':[{'type':'multibuy','quantity':2,'discounted_price':45}]},
#     'C': {'price':20, 'offer':None},
#     'D': {'price':15, 'offer':None},
#     'E': {'price':60, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]}
# }
# offer_list = [{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]
# #offer_list = [{'type': 'multibuy', 'quantity': 2, 'discounted_price': 45}]
#print(get_optimal_price_for_item("C",9,20,offer_list,price_info))
# 380 + 75 + 60
basket =   ['C']*3 #+ ['A']*9 + ['B']*3 #+
print(checkout(basket))

