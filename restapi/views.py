from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from .services import *


@api_view(['GET'])
def get_application(request):
    result_dict =  get_applications_service()
    return  Response(result_dict, status=201)


@api_view(['POST'])
def create_application(request):
    #Body for request
    # {
    # "amount": number,
    # "uin": string,
    # "programm_name": string
    # }
    data = request.data
    try:
        result_dict, status = create_application_service(data["uin"],data["programm_name"],data["amount"])
        return Response(result_dict, status=status)
        
    except Exception as e:
        return Response({"error": str(e)}, status=500)