
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
            best_price = count * details['price']
            for offer in details.get('offer',[]):
                if offer['type'] == 'multibuy' and count >= offer['quantity']:
                    multibuy_instances = count // offer['quantity']
                    multibuy_leftover = count % details['offer']['quantity']
            if details['offer'] and count >= details['offer']['quantity']:
                multibuy_instances = count // details['offer']['quantity']
                multibuy_leftover = count % details['offer']['quantity']
                basket_price += multibuy_instances * details['offer']['discounted_price']
                basket_price += multibuy_leftover * details['price']
            else:
                basket_price += count * details['price']

        else:
            return -1
    return basket_price

def get_optimal_price_for_item(item, count,price, offer_list,price_info):
    best_price = count * price
    for i in range(len(offer_list)):
        offer = offer_list[i]
        current_price = 0
        if offer['type'] == 'multibuy' and count >= offer['quantity']:
            multibuy_instances = count // offer['quantity']
            multibuy_leftover = count % offer['quantity']
            multibuy_price = multibuy_instances * offer['discounted_price']
            remaining_offer_list = offer_list[:i] + offer_list[i+1:]
            left_over_optimal_price = get_optimal_price_for_item(item,multibuy_leftover,price,remaining_offer_list,price_info)
            current_price = multibuy_price + left_over_optimal_price
            best_price = min(best_price,current_price)
        elif offer['type'] == 'buy_x_get_free' and count >= offer['buy']:
            offer_instances = count // offer['buy']
            offer_leftover = count % offer['buy']
            free_item = price_info[offer['free_item']]
            leftover_value = get_optimal_price_for_item(free_item,offer_instances,free_item['price'],free_item.get('offer',[]),price_info)
            current_price += count * price
            current_price += leftover_value#offer_instances*offer['get']*price_info[offer['free_item']['price']]
            best_price = min(best_price,current_price)

    return best_price

price_info = {
    'A': {'price':50, 'offer':[{'type':'multibuy', 'quantity':3,'discounted_price':130},{'type':'multibuy', 'quantity':5,'discounted_price':200}]},
    'B': {'price':30, 'offer':[{'type':'multibuy','quantity':2,'discounted_price':45}]},
    'C': {'price':20, 'offer':None},
    'D': {'price':15, 'offer':None},
    'E': {'price':60, 'offer':[{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]}
}
offer_list = [{'type':'buy_x_get_free','buy':2,'get':1,'free_item':'B'}]
print(get_optimal_price_for_item("E",9,60,offer_list,price_info))