from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Gig
from .forms import GigForm

# Create your views here.

def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request, 'home.html', {"gigs": gigs})

def test(request):
    return render(request, 'test.html', {})

def gig_detail(request, id):
    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')
    return render(request, 'gig_detail.html', {"gig": gig})


@login_required(login_url="/")
def create_gig(request):
    error = ''
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        # If form submit is valid
        if gig_form.is_valid():
            # Create new gig from form data
            gig = gig_form.save(commit=False)
            # Then set user FK to user id
            gig.user = request.user
            # Save to database
            gig.save()
            # Once saved, redirect to my gigs page
            return redirect('my_gigs')
        else:
            error = "Something went wrong"

    gig_form = GigForm()
    return render(request, 'create_gig.html', {"gig_form": gig_form, "error": error})

@login_required(login_url="/")
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs})
