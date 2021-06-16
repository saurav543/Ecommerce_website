from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.inventory.models import Product
from django.conf import settings


class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, quantity):
        """
        adding and updating users basket data
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id] = {'price': float(
                product.regular_price), 'quantity': int(quantity)}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['total_price'] = item['price']*item['quantity']
            yield item
        
    def basket_update_delivery(self,deliveryprice=0):
        subtotal = sum((item['price'])*item['quantity'] for item in self.basket.values())
        total = int(subtotal) + int(deliveryprice)
        # print(total)
        return int(total)

    def delete(self, product):
        """
            delete the basket data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]

        self.session.modified = True

    def update(self, product_id, product_qty):
        """
            Update the basket data
        """
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['quantity'] = int(product_qty)
        self.session.modified = True

    def __len__(self):
        """
        get the basket data and the qunatity of products
        """
        return int(sum(item['quantity'] for item in self.basket.values()))

    def get_subtotal_price(self):
        a=0
        a = sum(item['price']*item['quantity']
                for item in self.basket.values())
        return int(a)
    def delivery_price(self):
        newprice = 0
        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
        return newprice
    def get_total_price(self):
        newprice = 0.00
        a = sum(item['price']*item['quantity']
                for item in self.basket.values())
        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price
        
        total = int(a)+int(newprice)
        return total

    def clear(self):
        del self.session['skey']
        self.session.modified = True
