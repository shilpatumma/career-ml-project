from django.shortcuts import render
import sys
import os
import json

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from .models import CareerResult

# Add ML folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml')))

from predict import predict_career

# -----------------------------
# HOME PAGE
# -----------------------------
def home(request):
    return render(request, 'form.html')

# -----------------------------
# PREDICTION VIEW
# -----------------------------
# def predict_view(request):
#     if request.method == 'POST':
#         skills = request.POST['skills']
#         experience = int(request.POST['experience'])
#         education = request.POST['education']

#         result = predict_career(skills, experience, education)

#         # ✅ Convert missing skills to JSON
#         skills_json = json.dumps(result['missing_skills'])

#         return render(request, 'result.html', {
#             'result': result,
#             'skills_json': skills_json   # ✅ ADD THIS
#         })

#     return render(request, 'form.html')

def predict_view(request):
    if request.method == 'POST':
        skills = request.POST['skills']
        experience = int(request.POST['experience'])
        education = request.POST['education']

        result = predict_career(skills, experience, education)

        # ✅ SAVE RESULT HERE (INSIDE FUNCTION)
        if request.user.is_authenticated:
            CareerResult.objects.create(
                user=request.user,
                role=result["Role"],
                salary=result["Salary_LPA"],
                cluster=result["Cluster"]
            )

        return render(request, 'result.html', {
            'result': result,
            'user_skills': skills,
            'experience': experience,
            'education': education
        })

    return render(request, 'form.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def history(request):
    data = CareerResult.objects.filter(user=request.user)
    return render(request, "history.html", {"data": data})


