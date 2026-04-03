from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from udltimes.models import StatsWordle, StatsFramed, StatsConnections


# Create your views here.
def wordle_view(request):
    return render(request, 'wordle.html')

def connections_view(request):
    return render(request, 'connections/connections.html')

def framed_view(request):
    return render(request, 'framed.html')

def home(request):
    return render(request, 'home.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

@login_required
def profile_view(request):
    user = request.user

    wordle_stats = StatsWordle.objects.filter(user=user)
    framed_stats = StatsFramed.objects.filter(user=user)
    connections_stats = StatsConnections.objects.filter(user=user)

    context = {
        'user': user,
        'wordle_stats': wordle_stats,
        'framed_stats': framed_stats,
        'connections_stats': connections_stats,
    }
    return render(request, 'registration/profile.html', context)