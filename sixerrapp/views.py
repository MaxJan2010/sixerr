from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Gig, Profile, Purchase, Review
from .forms import GigForm

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                    merchant_id="kjrhyjymp2cg3nvz",
                                    public_key="6vq8f4n2gpw8hfgj",
                                    private_key="9f2f8ba30e9c60cf9805340f53bb91ef")

# Create your views here.

def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request, 'home.html', {"gigs": gigs})

def test(request):
    return render(request, 'test.html', {})

def gig_detail(request, id):
    # If a form is submitted AND user is logged in AND there is stuff in review content and that content isnt empty
    if request.method == 'POST' and \
        not request.user.is_anonymous() and \
        Purchase.objects.filter(gig_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
        # then create new review object
        Review.objects.create(content=request.POST['content'], gig_id=id, user=request.user, star=request.POST['star'])


    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')

    # 1. First check if user is logged in
    # 2. If current user has never made any purchase for this gig
    # 3. If current user has already made a review for this gig

    if request.user.is_anonymous() or \
        Purchase.objects.filter(gig=gig, buyer=request.user).count() == 0 or \
        Review.objects.filter(gig=gig, user=request.user).count() > 0:
        # Then hide the review form
        show_post_review = False
    else:
        # then check if user has purchased this gig
        show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0
    # Get all reviews belonging to this gig id
    reviews = Review.objects.filter(gig=gig)
    # generate a client token for braintree
    client_token = braintree.ClientToken.generate()
    return render(request, 'gig_detail.html', {"show_post_review": show_post_review, "reviews": reviews, "gig": gig, "client_token": client_token})


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
    return render(request, 'create_gig.html', {"error": error})


@login_required(login_url="/")
def edit_gig(request, id):
    try:
        # find all gig objects equal to gig id and user id
        gig = Gig.objects.get(id=id, user=request.user)
        error = ''
        if request.method == 'POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
            else:
                error = "Something went wrong"
        return render(request, 'edit_gig.html', {"gig": gig, "error": error})
    except Gig.DoesNotExist:
        return redirect('/')

    return render(request, 'edit_gig.html', {})


@login_required(login_url="/")
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs})


@login_required(login_url="/")
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')
    gigs = Gig.objects.filter(user=profile.user, status=True)


    # First we must get all gigs created by profile user - both active and inactive as we
    # want to display ALL reviews for ALL gigs, not jsut active ones for the above list
    gig = Gig.objects.filter(user=profile.user)
    # Then we create a list of review objects based on the profile user
    reviews = Review.objects.filter(gig=gig)


    return render(request, 'profile.html', {"profile": profile, "gigs": gigs, "reviews": reviews})


@login_required(login_url="/")
def create_purchase(request):
    if request.method == 'POST':
        try:
            gig = Gig.objects.get(id=request.POST['gig_id'])
        except Gig.DoesNotExist:
            return redirect('/')
        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": gig.price,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            Purchase.objects.create(gig=gig, buyer=request.user, seller=gig.user.username)
        else:
            print("Something went wrong")

    return redirect('/my_orders/')

@login_required(login_url="/")
def my_sales(request):
    purchases = Purchase.objects.filter(gig__user=request.user)
    return render(request, 'my_sales.html', {"purchases": purchases})

@login_required(login_url="/")
def my_orders(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'my_orders.html', {"purchases": purchases})


def category(request, link):
    categories = {
        "graphics-design": "GD",
        "digital-marketing": "DM",
        "video-animation": "VA",
        "music-audio": "MA",
        "programming-tech": "PT"
    }
    try:
        gigs = Gig.objects.filter(category=categories[link])
        return render(request, 'home.html', {"gigs": gigs})
    except KeyError:
        return redirect('home')

def search(request):
    gigs = Gig.objects.filter(title__contains=request.GET['title'])
    return render(request, 'home.html', {"gigs": gigs})
