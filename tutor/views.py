from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ----------------- DeepSeek API Setup -----------------
DEEPSEEK_API_KEY = "sk-6c53b3b32271483a9fad09b0fca4c5d1"   # replace with your real key
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

# ----------------- Pages -----------------
def home(request):
    return render(request, 'tutor/home.html')

def primary_school(request):
    grades_dict = {
        "Grade 4": ["Mathematics", "English", "Natural Sciences and Technology", "Social Studies", "Life Skills"],
        "Grade 5": ["Mathematics", "English", "Natural Sciences and Technology", "Social Studies", "Life Skills"],
        "Grade 6": ["Mathematics", "English", "Natural Sciences", "Social Studies", "Technology"],
        "Grade 7": ["Mathematics", "English", "Natural Sciences", "Technology", "Geography", "History", "EMS"],
    }
    return render(request, 'tutor/primary_school.html', {'grades': grades_dict})

def secondary_school(request):
    grades_dict = {
        "Grade 8": ["Mathematics", "English", "Natural Sciences", "Social Sciences", "Technology"],
        "Grade 9": ["Mathematics", "English", "Natural Sciences", "Social Sciences", "Technology"],
        "Grade 10": ["Mathematics", "Physical Science", "Life Sciences", "History", "Geography"],
        "Grade 11": ["Mathematics", "Physical Science", "Life Sciences", "Accounting", "Business Studies"],
        "Grade 12": ["Mathematics", "Physical Science", "Life Sciences", "Accounting", "Business Studies"],
    }
    return render(request, 'tutor/secondary_school.html', {'grades': grades_dict})

# ----------------- CAPS Content Generator (DeepSeek) -----------------
@csrf_exempt
def generate_caps_content(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        grade = request.GET.get('grade', '').strip()
        subject = request.GET.get('subject', '').strip()
        topic = request.GET.get('topic', '').strip()
        content_type = request.GET.get('content_type', '').strip()

        if not grade or not subject or not topic or not content_type:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        prompt = f"Generate a {content_type} for {grade} {subject} on the topic '{topic}' following the South African CAPS curriculum. Make it learner-friendly."

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a CAPS curriculum content generator for South African schools."},
                {"role": "user", "content": prompt},
            ],
        }

        try:
            response = requests.post(
                f"{DEEPSEEK_API_BASE}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Debug: print the raw response in server console
            print("DeepSeek API response:", data)

            if "choices" in data and len(data["choices"]) > 0:
                ai_content = data["choices"][0]["message"]["content"]
                return JsonResponse({'ai_content': ai_content})
            else:
                return JsonResponse({'error': 'No content returned from DeepSeek.'}, status=500)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f'DeepSeek API request error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request. Use AJAX GET.'}, status=400)
