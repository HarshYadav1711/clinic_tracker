from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import FollowUp, PublicViewLog
from .forms import FollowUpForm
from django.contrib import messages


# Helper function
def get_user_clinic(request):
    try:
        return request.user.userprofile.clinic
    except AttributeError:
        return None


# Dashboard function
@login_required
def dashboard(request):
    clinic = get_user_clinic(request)
    if not clinic:
        return HttpResponseForbidden("User does not have a clinic profile.")
    
    followups = FollowUp.objects.filter(clinic=clinic)
    
    # Status filter
    status = request.GET.get("status")
    if status:
        followups = followups.filter(status=status)
    
    # Date range filter
    from_date = request.GET.get("from")
    to_date = request.GET.get("to")
    if from_date:
        followups = followups.filter(due_date__gte=from_date)
    if to_date:
        followups = followups.filter(due_date__lte=to_date)
    
    total = followups.count()
    pending = followups.filter(status="pending").count()
    done = followups.filter(status="done").count()

    context = {
        "followups": followups,
        "total": total,
        "pending": pending,
        "done": done,
    }

    return render(request, "followups/dashboard.html", context)


# Follow-up View
@login_required
def followup_create(request):
    clinic = get_user_clinic(request)
    if not clinic:
        return HttpResponseForbidden("User does not have a clinic profile.")
    
    if request.method == "POST":
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.clinic = clinic
            followup.created_by = request.user
            followup.save()
            messages.success(request, "Follow-up created successfully.")
            return redirect("dashboard")
    else:
        form = FollowUpForm()
    return render(request, "followups/followup_form.html", {"form": form})


# Follow-up edit
@login_required
def followup_edit(request, pk):
    clinic = get_user_clinic(request)
    if not clinic:
        return HttpResponseForbidden("User does not have a clinic profile.")
    
    followup = get_object_or_404(FollowUp, pk=pk)
    if followup.clinic != clinic:
        return HttpResponseForbidden()
    form = FollowUpForm(request.POST or None, instance=followup)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard")
    return render(request, "followups/followup_form.html", {"form": form})


# Mark_done
@login_required
def mark_done(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden()
    
    clinic = get_user_clinic(request)
    if not clinic:
        return HttpResponseForbidden("User does not have a clinic profile.")
    
    followup = get_object_or_404(FollowUp, pk=pk)
    if followup.clinic != clinic:
        return HttpResponseForbidden()
    followup.status = "done"
    followup.save()
    return redirect("dashboard")


# Delete follow-up
@login_required
def followup_delete(request, pk):
    if request.method != "POST":
        return HttpResponseForbidden()
    
    clinic = get_user_clinic(request)
    if not clinic:
        return HttpResponseForbidden("User does not have a clinic profile.")
    
    followup = get_object_or_404(FollowUp, pk=pk)
    if followup.clinic != clinic:
        return HttpResponseForbidden()
    
    followup.delete()
    messages.success(request, "Follow-up deleted successfully.")
    return redirect("dashboard")


# Public View
def public_view(request, token):
    followup = get_object_or_404(FollowUp, public_token=token)
    PublicViewLog.objects.create(
        followup=followup,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        ip_address=request.META.get("REMOTE_ADDR", ""),
    )
    if followup.language == "en":
        message = "Please visit the clinic on your due date."
    else:
        message = "कृपया अपनी तय तारीख पर क्लिनिक आएं।"
    return render(request, "followups/public_view.html", {"message": message})

