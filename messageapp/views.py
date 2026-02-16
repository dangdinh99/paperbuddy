import json
import os
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

MESSAGES_FILE = os.path.join(settings.BASE_DIR, 'messages.json')


def _load_messages():
    """Load messages from JSON file."""
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as f:
            return json.load(f)
    return []


def _save_messages(messages):
    """Save messages to JSON file."""
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=2)


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def send_message(request):
    """Endpoint that receives messages and saves them to a JSON file."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '')

            # Create message entry
            entry = {
                'message': message_text,
                'timestamp': datetime.now().isoformat(),
            }

            # Load existing messages, append, and save
            messages = _load_messages()
            messages.append(entry)
            _save_messages(messages)

            return JsonResponse({
                'status': 'success',
                'message': 'Message received and saved!',
                'received': message_text,
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests allowed',
    }, status=405)


@csrf_exempt
def get_messages(request):
    """Endpoint that returns all saved messages."""
    if request.method == 'GET':
        messages = _load_messages()
        return JsonResponse({
            'status': 'success',
            'messages': messages,
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Only GET requests allowed',
    }, status=405)
