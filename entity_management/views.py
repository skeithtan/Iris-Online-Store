from django.shortcuts import render
from django.views import View
from .models import *
from django.shortcuts import Http404
from django.http import HttpResponse
import json


class EntityManagementView(View):
    @staticmethod
    def get(request):
        stalls = Stall.objects.all()
        products = Product.objects.all()
        return render(request, 'entity_management.html', {
            "stalls": stalls,
        })

class ProductView(View):
    @staticmethod
    def post(request,stall_id):

        if 'photo' not in request.FILES:
            return HttpResponse(status=400)

        dict = {
            "product_name":request.POST.get('name'),
            "description":request.POST.get('description'),
            "price":request.POST.get('price'),
            "quantity":request.POST.get('quantity')
        }

        new_product = Product()
        new_product.name = dict["product_name"]
        new_product.description = dict["description"]
        new_product.photo = request.FILES.get('photo')
        new_product.price = dict["price"]
        new_product.stall = Stall.objects.get(pk=stall_id)
        new_product.quantity = dict["quantity"]

        new_product.save()

        data = {
            "new_product": new_product.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

class StallView(View):
    # noinspection PyBroadException
    @staticmethod
    def get(request, stall_id):
        try:
            stall = Stall.objects.get(id=stall_id)
            products = Product.objects.all().filter(stall=stall)
        except:
            raise Http404("Stall does not exist")

        stalls = Stall.objects.all()
        return render(request, 'entity_management.html', {
            "stalls": stalls,
            "active_stall": stall,
            "products":products,

        })

    @staticmethod
    def post(request):
        dict = json.loads(request.body)
        new_stall = Stall()
        new_stall.name = dict["stall_name"]
        new_stall.save()

        data = {
            "new_stall": new_stall.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    @staticmethod
    def put(request, stall_id):
        dict = json.loads(request.body)
        try:
            stall = Stall.objects.get(pk=stall_id)
            print(stall)
            old_name = stall.name # old name stored for debugging purposes (sent in JSON response)
            stall.name = dict["modified_name"]
            stall.save()

        except:
            raise Http404("Stall does not exist")
        data = {
            "old_name": old_name,
            "new_name": stall.name
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


    @staticmethod
    def delete(self, stall_id):

        try:
            Stall.objects.get(pk=stall_id).delete()

        except:
            raise Http404("Stall does not exist")

        data = {

        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
