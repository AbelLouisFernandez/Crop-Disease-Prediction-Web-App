from django.shortcuts import render
from .forms import SignUpForm
from django.contrib import messages
from .models import CustomUser
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser


from google import genai

from django.conf import settings
from django.http import JsonResponse




client = genai.Client(api_key=settings.GEMINI_API_KEY)

def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():

            enteredemail = form.cleaned_data['email']

            users = CustomUser.objects.filter(email=enteredemail).first()

            if users:
                messages.error(request, 'This email has already been registered')

            else:
                form.save()

                messages.success(request, "Signup successful! You can now login.")

                return redirect('login')

    else:
        form = SignUpForm()

    return render(request, 'base/signup.html', {'form': form})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ✅ Correct usage of authenticate()
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {'page': page}
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

import os
from django.shortcuts import render
from .utils import predict_disease


from .models import PredictionHistory
@login_required
def predict_view(request):

    results = None
    image_url = None

    if request.method == "POST" and request.FILES.get("leaf_image"):

        img = request.FILES["leaf_image"]

        file_path = "media/" + img.name

        with open(file_path,"wb+") as f:
            for chunk in img.chunks():
                f.write(chunk)

        results = predict_disease(file_path)

        image_url = "/media/" + img.name

        if results and request.user.is_authenticated:

            top = results[0]

            PredictionHistory.objects.create(
                user=request.user,
                image=img,
                crop=top["crop"],
                disease=top["disease"],
                confidence=top["confidence"]
            )

    return render(request,"base/predict.html",{
        "results":results,
        "image_url":image_url
    })



@login_required
def edit_profile(request):

    if request.method == "POST":

        form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():

            user = form.save(commit=False)

            current_password = form.cleaned_data.get("current_password")
            new_password = form.cleaned_data.get("new_password")
            confirm_password = form.cleaned_data.get("confirm_password")

            if new_password:

                if not user.check_password(current_password):
                    messages.error(request, "Current password is incorrect.")
                    return redirect("edit_profile")

                if new_password != confirm_password:
                    messages.error(request, "New passwords do not match.")
                    return redirect("edit_profile")

                user.set_password(new_password)
                update_session_auth_hash(request, user)

            user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("home")

    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "base/edit_profile.html", {"form": form})


from django.contrib.auth.decorators import login_required
from .models import PredictionHistory


@login_required
def prediction_history(request):

    history = PredictionHistory.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request,"base/history.html",{
        "history":history
    })


from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def generate_report(request):

    if request.method == "POST":

        data = json.loads(request.body)
        crop = data.get("crop")
        disease = data.get("disease")

        prompt = f"""
A plant disease has been detected.
Crop: {crop}
Disease: {disease}

Return ONLY a valid JSON object with exactly these two keys, nothing else:
{{
  "description": "A 1-2 sentence simple explanation of what this disease is, written for a farmer with no technical background.",
  "prevention": [
    "First prevention or management tip",
    "Second prevention or management tip",
    "Third prevention or management tip",
    "Fourth prevention or management tip"
  ]
}}

Rules:
- "description" must be plain text, 1-2 sentences only, no markdown.
- "prevention" must be a JSON array of 4-6 short, practical bullet points, plain text only, no markdown, no bullet symbols.
- Do NOT include any text outside the JSON object.
- Do NOT use markdown code fences.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()
        # Strip markdown code fences if Gemini wraps them anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        import json as json_lib
        try:
            parsed = json_lib.loads(raw)
            return JsonResponse({
                "description": parsed.get("description", ""),
                "prevention":  parsed.get("prevention", [])
            })
        except Exception:
            # Fallback: return raw text so the frontend can still display something
            return JsonResponse({
                "description": raw,
                "prevention": []
            })