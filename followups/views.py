from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import FollowUp, PublicViewLog
from .forms import FollowUpForm


# Dashboard function
@login_required
def dashboard(request):
    clinic = request.user.userprofile.clinic
    followups = FollowUp.objects.filter(clinic=clinic)
    status = request.GET.get("status")
    if status:
        followups = followups.filter(status=status)
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
    if request.method == "POST":
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.clinic = request.user.userprofile.clinic
            followup.created_by = request.user
            followup.save()
            return redirect("dashboard")
    else:
        form = FollowUpForm()
    return render(request, "followups/followup_form.html", {"form": form})


# Follow-up edit
@login_required
def followup_edit(request, pk):
    followup = get_object_or_404(FollowUp, pk=pk)
    if followup.clinic != request.user.userprofile.clinic:
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
    followup = get_object_or_404(FollowUp, pk=pk)
    if followup.clinic != request.user.userprofile.clinic:
        return HttpResponseForbidden()
    followup.status = "done"
    followup.save()
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
