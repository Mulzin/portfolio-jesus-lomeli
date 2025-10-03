from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json
import os

def english_home(request):
    return render(request,'en/home.html')

def spanish_home(request):
    return render(request,'sp/home.html')

@require_GET
def get_portfolio(request):
    json_path = os.environ.get('JSON_PATH')
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)