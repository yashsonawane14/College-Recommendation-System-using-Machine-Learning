from django.shortcuts import render, redirect
from django.http import JsonResponse
import pandas as pd
import json
import requests
import joblib

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

from .forms import LoginForm, RegisterForm, RecommendationForm

# Ollama API URL (Mistral)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Load trained models and encoders
knn = joblib.load('knn_model.pkl')
label_encoder_category = joblib.load('label_encoder_category.pkl')
label_encoder_gender = joblib.load('label_encoder_gender.pkl')
label_encoder_branch = joblib.load('label_encoder_branch.pkl')


# CSV paths
CSV_PATH = r"F:/College Recommendation System/College Recommendation System/Be_project1/compare_clg.csv"
MHT_CET_CSV = r"F:/College Recommendation System/College Recommendation System/Be_project1/mht_cet2.csv"

# ---------------- Views ---------------- #

def home(request):
    return render(request, 'home.html')

def recommendation(request):
    return JsonResponse({'message': 'Welcome to College Recommendation'})

def compare(request):
    return JsonResponse({'message': 'Let’s compare colleges'})

def search_college(request):
    if request.method == "POST":
        college_name = request.POST.get("college_name", "").strip().lower()
        df = pd.read_csv(CSV_PATH)
        df.columns = df.columns.str.strip()
        college = df[df["College Name"].str.strip().str.lower() == college_name]

        if not college.empty:
            def safe_value(value):
                return "null" if pd.isna(value) or value == "" else value

            data = {
                "established_year": safe_value(college.iloc[0].get("Established Year")),
                "rating": safe_value(college.iloc[0].get("Rating")),
                "average_fees": safe_value(college.iloc[0].get("Average Fees"))
            }
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "College not found"}, status=404)
    return render(request, "search.html")

# 💡 Added from code1
def display_college(request, college_name):
    df = pd.read_csv(CSV_PATH)
    college = df[df['College Name'].str.lower().str.strip() == college_name.lower().strip()]
    if not college.empty:
        data = college.iloc[0].to_dict()
        return render(request, 'display_college.html', {'college': data})
    else:
        messages.error(request, 'College not found.')
        return redirect('home')

def recommend_colleges(rank, percentile, category, gender,branch, y, n_neighbors=20):
    try:
        category_encoded = label_encoder_category.transform([category])[0]
    except ValueError:
        category_encoded = -1
    try:
        gender_encoded = label_encoder_gender.transform([gender])[0]
    except ValueError:
        gender_encoded = -1
    try:
        branch_encoded = label_encoder_branch.transform([branch])[0]
    except ValueError:
        branch_encoded = -1


    input_data = [[rank, percentile, category_encoded, gender_encoded,branch_encoded]]
    distances, indices = knn.kneighbors(input_data, n_neighbors=n_neighbors)
    recommended_colleges = y.iloc[indices[0]]
    return recommended_colleges.tolist()

def services(request):
    return render(request, 'services.html')  # Make sure services.html exists

def recommendation_view(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            rank = form.cleaned_data['rank']
            percentile = form.cleaned_data['percentile']
            category = form.cleaned_data['category']
            gender = form.cleaned_data['gender']
            branch = form.cleaned_data['branch']  # New branch data


            request.session['rank'] = rank
            request.session['percentile'] = percentile
            request.session['category'] = category
            request.session['gender'] = gender
            request.session['branch'] = branch  # Save branch in session


            dataframe = pd.read_csv(MHT_CET_CSV)
            y = dataframe['college_name']

            all_recommendations = recommend_colleges(rank, percentile, category, gender,branch, y, n_neighbors=20)
            request.session['all_recommendations'] = all_recommendations
            recommendations = all_recommendations[:10]
            request.session['recommendations'] = recommendations
            request.session['next_recommendation_index'] = 10

            return render(request, 'results.html', {'recommendations': recommendations})
    else:
        form = RecommendationForm()
    return render(request, 'form.html', {'form': form})

# 💡 Added from code1
def clear_recommendations(request):
    request.session.pop('recommendations', None)
    request.session.pop('all_recommendations', None)
    request.session.pop('next_recommendation_index', None)
    return redirect('home')

def get_college_names(request):
    df = pd.read_csv(CSV_PATH)
    college_names = df["College Name"].dropna().unique().tolist()
    return JsonResponse({"colleges": college_names})

def discard_college(request):
    """
    Handle the discard request and return a new recommendation.
    """
    if request.method == 'POST':

        print("Discarded College:", request.POST.get('college'))
        print("Current Recommendations:", request.session.get('recommendations', []))
        print("All Recommendations:", request.session.get('all_recommendations', []))
        print("Next Recommendation Index:", request.session.get('next_recommendation_index', 10))
        
        # Get the discarded college from the request
        discarded_college = request.POST.get('college')

        # Get the current list of displayed recommendations from the session
        recommendations = request.session.get('recommendations', [])

        # Get the list of all fetched recommendations from the session
        all_recommendations = request.session.get('all_recommendations', [])

        # Get the index of the next recommendation to use
        next_recommendation_index = request.session.get('next_recommendation_index', 10)
        
        
        # Remove the discarded college from the displayed list
        if discarded_college in recommendations:
            recommendations.remove(discarded_college)

            # Check if there are more recommendations available
            if next_recommendation_index < len(all_recommendations):
                # Get the next recommendation
                new_recommendation = all_recommendations[next_recommendation_index]

                # Add the new recommendation to the end of the displayed list
                recommendations.append(new_recommendation)

                # Increment the index for the next recommendation
                request.session['next_recommendation_index'] = next_recommendation_index + 1

                # Save the updated displayed recommendations in the session
                request.session['recommendations'] = recommendations

                # Return the new recommendation as JSON
                return JsonResponse({
                    'status': 'success',
                    'new_recommendation': new_recommendation
                })
            else:
                # No more recommendations available
                return JsonResponse({'status': 'error', 'message': 'No more recommendations available'})

        return JsonResponse({'status': 'error', 'message': 'College not found'})
        
@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"response": "Please enter a message."}, status=400)

            payload = {
                "model": "mistral",
                "prompt": user_message,
                "stream": False
            }

            response = requests.post(OLLAMA_API_URL, json=payload)
            ollama_response = response.json()
            bot_reply = ollama_response.get("response", "Sorry, I couldn't understand that.")

            return JsonResponse({"response": bot_reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, 'You have successfully logged in!')
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful! You are now logged in.')
#             return redirect('home')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})

# @login_required
# def logout_view(request):
#     logout(request)
#     messages.success(request, 'You have been logged out.')
#     return redirect('home')
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Profile

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('home')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'login.html')


def register_view(request):

    if request.method =="POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_obj= User.objects.filter(username=email)

        if user_obj.exists():
            messages.warning(request , "email already taken")
            return HttpResponseRedirect(request.path_info)
        
        user_obj=User.objects.create(first_name=first_name, last_name=last_name,email=email,username=email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request , "An email has been sent on your mail")
        return HttpResponseRedirect(request.path_info)


    return render(request, "register.html")


@login_required
def logout_view(request):
    logout(request)
    #messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home page after logout

def activate_email(request, email_token):
    try:

        user=Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token.')