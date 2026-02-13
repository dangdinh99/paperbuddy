from django.shortcuts import render
def index(request):
    return render(request, 'index.html')

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_message(request):
    """
    Endpoint that receives messages
    """
    if request.method == 'POST':
        try:
            # Get the message from request
            data = json.loads(request.body)
            message_text = data.get('message', '')
            
            # Send response back
            return JsonResponse({
                'status': 'success',
                'message': 'Message received!',
                'received': message_text
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests allowed'
    }, status=405)
