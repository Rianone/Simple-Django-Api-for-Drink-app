from .models import Drink
from django.http import JsonResponse
from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','POST']) # This is a decorator, it is typically something you put above your function to describe its functionality
def drink_list(request):
    if request.method == 'GET':
        #get all the drinks
        drinks = Drink.objects.all()

        #serialize them
        drinks_serialized = DrinkSerializer(drinks, many=True)

         #return json
        return JsonResponse({"drinks" : drinks_serialized.data}, safe=False)
    
    if request.method == 'POST':
        #create a new drink
        serializer = DrinkSerializer(data=request.data)

        #verify if data is correct
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id):

    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return JsonResponse({"error" : "Drink does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        #serialize it
        drink_serialized = DrinkSerializer(drink)
        #return json
        return JsonResponse(drink_serialized.data, safe=False)
    
    elif request.method == 'PUT':
        #update the drink
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == 'DELETE':
        #delete the drink
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
