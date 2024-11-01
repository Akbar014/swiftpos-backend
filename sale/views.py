from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from . import models
from . import serializers
from history import models as sale_models
from person import models as person
import random
import uuid

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse , HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from sslcommerz_lib import SSLCOMMERZ 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import string
import json
# Create your views here.
# class PurchaseViewSet(viewsets.ModelViewSet):
    
#     queryset = models.Purchase.objects.all()
#     serializer_class = serializers.PurchaseSerializer
#     permission_classes = [permissions.AllowAny]

# class PurchaseItemsViewSet(viewsets.ModelViewSet):
   
#     queryset = models.PurchaseItems.objects.all()
#     serializer_class = serializers.PurchaseItemsSerializer
#     permission_classes = [permissions.AllowAny]


# class SaleViewSet(viewsets.ModelViewSet):
#     queryset = models.Sale.objects.all()
#     serializer_class = serializers.SaleSerializer
#     permission_classes = [permissions.AllowAny]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         print("Validation Errors:", serializer.errors)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SaleViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all().order_by('-id')
    serializer_class = serializers.SaleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def generate_purchase_code(self):
    #     return str(uuid.uuid4()).split('-')[0].upper()

    def generate_sale_code(self):
        return random.randint(100000, 999999)

    # def perform_create(self, serializer):
    #     generated_code = self.generate_purchase_code()
    #     sale = serializer.save(user=self.request.user, code=generated_code)
        
    #     # Create a single history entry
    #     sale_models.SaleHistory.objects.create(
    #         sale=sale,
    #         sale_code=sale.code,
    #         user=self.request.user,
    #         total_amount=sale.total_amount,
    #     )   

    # def perform_create(self, serializer):
    #     generated_code = self.generate_sale_code()
    #     sale = serializer.save(user=self.request.user, code=generated_code)

    #     sale_history = sale_models.SaleHistory.objects.create(
    #         sale=sale,
    #         sale_code=sale.code,
    #         user=self.request.user,
    #         total_amount=sale.total_amount,
    #     ) 

    #     for item in sale.items.all():
    #         product = item.product
    #         # quantity = int(item.quantity)
    #         product.stock_quantity -= item.quantity  # Increase product stock by purchase quantity
    #         product.save()


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate the sale code
        generated_code = self.generate_sale_code()
        
        # Save the sale with the generated code
        sale = serializer.save(user=self.request.user, code=generated_code)

        # Create the sale history entry
        sale_history = sale_models.SaleHistory.objects.create(
            sale=sale,
            sale_code=sale.code,
            user=self.request.user,
            total_amount=sale.total_amount,
        ) 

        # Update product stock for each item in the sale
        for item in sale.items.all():
            product = item.product
            product.stock_quantity -= item.quantity
            product.save()

        # Customize the response data
        response_data = {
            "message": "Sale created successfully",
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
 


@api_view(['GET', 'POST'])
def salePayment(request):
    items = request.data.get('items', [])
    customer = request.data.get('customer')
    discount = request.data.get('discount')

    settings = { 'store_id': 'abc671f28ecabcb6', 'store_pass': 'abc671f28ecabcb6@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = request.data.get('total_amount')
    post_body['currency'] = "BDT"
    post_body['tran_id'] = unique_transaction_id_generator()
    post_body['success_url'] = f"http://127.0.0.1:8000/salesapp/success_payment/{request.user.username}/{post_body['tran_id']}/{customer}/{discount}/success?redirect=true"
    post_body['fail_url'] = "https://fabulous-trifle-8657b5.netlify.app/dashboard.html?success=false"
    post_body['cancel_url'] = "https://fabulous-trifle-8657b5.netlify.app/dashboard.html?success=cancel"
    post_body['emi_option'] = 0
    post_body['cus_name'] = request.user.username
    post_body['cus_email'] = request.user.email
    post_body['cus_phone'] = "01401277707"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['custom_items'] = json.dumps(items) 
    # post_body['num_of_item']: len(items)  # Number of items in the sale
    # post_body['product_name'] = ", ".join([item['product'] for item in items]) # Example: concatenate product names
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    # print(response)
    # Need to redirect user to response['GatewayPageURL']
    # return redirect(response['GatewayPageURL'])
    return JsonResponse({'url': response['GatewayPageURL']})

@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([permissions.AllowAny])

def payment_success(request, username, tran_id,customer, discount):
    payment_data = request.POST
    print(payment_data[total_amount])
    customer = person.Customer.objects.get(id=customer)
    user = User.objects.filter(username = username).first()
    # print(request)
    # print(request.data.get('total_amount'))

    if request.data.get('status') == 'VALID' and request.data.get('tran_id') == tran_id:

        # print(request.data.get('total_amount'))
    
        code = random.randint(100000, 999999)
        
        # sale = models.Sale.objects.create(
        #     code=code,
        #     customer=customer,
        #     total_amount=request.data.get('total_amount'),
        #     discount=discount,
        #     user=user
        # )

        # items = request.data.get('items', [])  # Assuming items are sent in the request body
        items = json.loads(request.data.get('custom_items', '[]'))
        print(items)

        for item in items:
            models.SaleItems.objects.create(
                sale=sale,
                product_id=item['product'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )

        sale_models.SaleHistory.objects.create(
            sale=sale,
            sale_code=code,
            user=user,
            total_amount=total_amount,
        )

        # Update stock quantities for products in the sale
        for item in items:
            product = item['product']
            product.stock_quantity -= item['quantity']
            product.save()

        # # Create sale items
        # for item in items:
        #     sale_models.SaleItems.objects.create(
        #         sale=sale,
        #         product_id=item['product'],
        #         quantity=item['quantity'],
        #         unit_price=item['unit_price']
        #     )
        
        # sale_models.SaleHistory.objects.create(
        #     sale=sale,
        #     sale_code=generated_code,
        #     user=user,
        #     total_amount=request.data.get('total_amount'),
        # )

        # # Update stock quantities for products in the sale
        # for item in sale.items.all():
        #     product = item.product
        #     product.stock_quantity -= item.quantity
        #     product.save()

        # return Response({"message": "Sale created successfully after payment."}, status=status.HTTP_201_CREATED)
        if request.GET.get('redirect') == 'true':
            # return HttpResponseRedirect ("https://fabulous-trifle-8657b5.netlify.app/")
            return HttpResponseRedirect ("http://127.0.0.1:5501/allSale.html?success=true")
        return Response ({'message': 'Paymeny successfull'}, status = status.HTTP_200_OK)
    return Response ({'message': 'Payment Failed'}, status= status.HTTP_400_BAD_REQUEST)