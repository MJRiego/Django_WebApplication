from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Count
from scholars.models import Members, Grades, Requirements_list, Requirements, Allowances
from django.db.models import Case, When, F, Count
from .forms import MembersForm, ReqsForm, ReqsListForm, AllowanceForm, GradesForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import json
from django.db.models.functions import ExtractYear



# Create your views here.
class Dashboard(ListView):
    model = Members
    template_name = 'dashboard.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        yearlevel = Members.objects.values('yearlevel').annotate(total=Count('memberID'))
        total_members = Members.objects.count()

        for year in yearlevel:
            year['percentage'] = round((year['total'] / total_members) * 100)

        context = {
            'yearlevel': yearlevel,
        }

        batch_numbers = Members.objects.values('batchnum').annotate(total_members=Count('memberID')).order_by('batchnum')
        labels_batchnum = [batch_number['batchnum'] for batch_number in batch_numbers]
        data_totalmembers = [batch_number['total_members'] for batch_number in batch_numbers]
        batchnum = json.dumps(labels_batchnum)
        totalmembers = json.dumps(data_totalmembers)

        context['batchnum'] = batchnum
        context['totalmembers'] = totalmembers

        accept_date = Members.objects.annotate(accept_year=ExtractYear('acceptdate')).values('accept_year').annotate(accept_total=Count('memberID')).order_by('accept_year')
        labels_acceptyear = [accept_data['accept_year'] for accept_data in accept_date]
        data_totalaccept = [accept_data['accept_total'] for accept_data in accept_date]
        acceptyear = json.dumps(labels_acceptyear)
        totalaccept = json.dumps(data_totalaccept)

        context['acceptyear'] = acceptyear
        context['totalaccept'] = totalaccept

        return context

class MembersView(ListView):
    model = Members
    context_object_name = 'members'
    template_name = 'members.html'
    paginate_by = 15

    def get(self, request):
        members_list = Members.objects.all() 
        paginator = Paginator(members_list, self.paginate_by)

        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)

        return render(request, self.template_name, {'members': members})

class ProfileView(ListView):
    model = Members
    context_object_name = 'member'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.kwargs['memberID']
        member = Members.objects.get(memberID=member_id)
        member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"
        context['member'] = member
        return context

class GradesPageView(ListView):
    model = Members
    context_object_name = 'members'
    template_name = 'grades-page.html'
    paginate_by = 15

    def get(self, request):
        members_list = Members.objects.all() 
        paginator = Paginator(members_list, self.paginate_by)

        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)
        
        for member in members:
            member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"
            
        return render(request, self.template_name, {'members': members})

class MemberGradesView(ListView):
    model = Grades
    template_name = 'grades.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.kwargs['memberID']
        member = Members.objects.get(memberID=member_id)
        member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"
        context['member'] = member

        year = self.request.POST.get('year')
        sem = self.request.POST.get('sem')
        if year and sem:
            context['grades'] = Grades.objects.filter(memberID=member_id, yearlevel=year, semester=sem).order_by(
        Case(
            When(yearlevel='1st Year', then=1),
            When(yearlevel='2nd Year', then=2),
            When(yearlevel='3rd Year', then=3),
            When(yearlevel='4th Year', then=4),
        ),
        Case(
            When(semester='1st Sem', then=1),
            When(semester='2nd Sem', then=2),
        ),
        'gradeID'
            )
        elif year:
            context['grades'] = Grades.objects.filter(memberID=member_id, yearlevel=year).order_by(
        Case(
            When(semester='1st Sem', then=1),
            When(semester='2nd Sem', then=2),
        ),
        'gradeID'
            )
        elif sem:
            context['grades'] = Grades.objects.filter(memberID=member_id, semester=sem).order_by(
        Case(
            When(yearlevel='1st Year', then=1),
            When(yearlevel='2nd Year', then=2),
            When(yearlevel='3rd Year', then=3),
            When(yearlevel='4th Year', then=4),
        ),
        'gradeID'
            )
        else:
            context['grades'] = Grades.objects.filter(memberID=member_id).order_by(
        Case(
            When(yearlevel='1st Year', then=1),
            When(yearlevel='2nd Year', then=2),
            When(yearlevel='3rd Year', then=3),
            When(yearlevel='4th Year', then=4),
        ),
        Case(
            When(semester='1st Sem', then=1),
            When(semester='2nd Sem', then=2),
        ),
        'gradeID'
            )

        context['year'] = year
        context['sem'] = sem
        return context
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class ReqsPageView(ListView):
    model = Members
    context_object_name = 'members'
    template_name = 'reqs-page.html'
    paginate_by = 15

    def get(self, request):
        members_list = Members.objects.all() 
        paginator = Paginator(members_list, self.paginate_by)

        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)

        for member in members:
            member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"

        context = {
            'members': members,
            'requirements': Requirements_list.objects.all(),
        }

        return render(request, self.template_name, context)

class MemberRequirementsView(ListView):
    model = Requirements
    template_name = 'reqs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.kwargs['memberID']
        member = Members.objects.get(memberID=member_id)
        member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"
        context['member'] = member

        requirements = Requirements.objects.filter(memberID=member_id).select_related('reqs_listID')
        context['requirements'] = requirements
        return context

class AllowancePageView(ListView):
    model = Members
    context_object_name = 'members'
    template_name = 'allowance-page.html'
    paginate_by = 15

    def get(self, request):
        members_list = Members.objects.all() 
        paginator = Paginator(members_list, self.paginate_by)

        page_number = request.GET.get('page')
        members = paginator.get_page(page_number)
        
        for member in members:
            member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"
            
        return render(request, self.template_name, {'members': members})

class MemberAllowancesView(ListView):
    model = Allowances
    template_name = 'allowance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member_id = self.kwargs['memberID']
        member = Members.objects.get(memberID=member_id)
        member.fullname = f"{member.firstname} {member.midinitial} {member.lastname}"
        context['member'] = member

        year = self.request.POST.get('year')
        sem = self.request.POST.get('sem')
        if year and sem:
            context['allowances'] = Allowances.objects.filter(memberID=member_id, yearlevel=year, semester=sem).order_by(
        Case(
            When(yearlevel='1st Year', then=1),
            When(yearlevel='2nd Year', then=2),
            When(yearlevel='3rd Year', then=3),
            When(yearlevel='4th Year', then=4),
        ),
        Case(
            When(semester='1st Sem', then=1),
            When(semester='2nd Sem', then=2),
        ),
        Case(
            When(month='1st Month', then=1),
            When(month='2nd Month', then=2),
            When(month='3rd Month', then=3),
            When(month='4th Month', then=4),
            When(month='5th Month', then=5),
        ),
        'allowanceID'
            )
        elif year:
            context['allowances'] = Allowances.objects.filter(memberID=member_id, yearlevel=year).order_by(
        Case(
            When(semester='1st Sem', then=1),
            When(semester='2nd Sem', then=2),
        ),
        Case(
            When(month='1st Month', then=1),
            When(month='2nd Month', then=2),
            When(month='3rd Month', then=3),
            When(month='4th Month', then=4),
            When(month='5th Month', then=5),
        ),
        'allowanceID'
            )
        elif sem:
            context['allowances'] = Allowances.objects.filter(memberID=member_id, semester=sem).order_by(
        Case(
            When(yearlevel='1st Year', then=1),
            When(yearlevel='2nd Year', then=2),
            When(yearlevel='3rd Year', then=3),
            When(yearlevel='4th Year', then=4),
        ),
        Case(
            When(month='1st Month', then=1),
            When(month='2nd Month', then=2),
            When(month='3rd Month', then=3),
            When(month='4th Month', then=4),
            When(month='5th Month', then=5),
        ),
        'allowanceID'
            )
        else:
            context['allowances'] = Allowances.objects.filter(memberID=member_id).order_by(
        Case(
            When(yearlevel='1st Year', then=1),
            When(yearlevel='2nd Year', then=2),
            When(yearlevel='3rd Year', then=3),
            When(yearlevel='4th Year', then=4),
        ),
        Case(
            When(semester='1st Sem', then=1),
            When(semester='2nd Sem', then=2),
        ),
        Case(
            When(month='1st Month', then=1),
            When(month='2nd Month', then=2),
            When(month='3rd Month', then=3),
            When(month='4th Month', then=4),
            When(month='5th Month', then=5),
        ),
        'allowanceID'
            )

        context['year'] = year
        context['sem'] = sem
        return context
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


# ALL ADD FUNCTIONS

def MembersAdd(request):
    if request.method == 'POST':
        form = MembersForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Member has been added successfully.'
            return render(request, 'members-add.html', {'form': MembersForm(), 'success_message': success_message})
    else:
        form = MembersForm()
    
    return render(request, 'members-add.html', {'form': form})

def MemberGradesAdd(request, memberID):
    member = get_object_or_404(Members, memberID=memberID)
    if request.method == 'POST':
        form = GradesForm(request.POST)
        memberID = request.POST.get('memberID')
        if form.is_valid():
            grade = form.save(commit=False)
            grade.memberID = member
            grade.save()
            return redirect('grades', memberID=memberID)
    else:
        form = GradesForm()
    
    return render(request, 'grades-add.html', {'form': form, 'memberID': memberID})

def ReqListAdd(request):
    if request.method == 'POST':
        form = ReqsListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reqs-page') 
    else:
        form = ReqsListForm()
    
    return render(request, 'reqs_list-add.html', {'form': form})

def MemberReqsAdd(request, memberID):
    member = get_object_or_404(Members, memberID=memberID)
    if request.method == 'POST':
        form = ReqsForm(request.POST)
        memberID = request.POST.get('memberID')
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.memberID = member
            requirement.save()
            return redirect('requirements', memberID=memberID)
        else:
            messages.error(request, 'Requirements Not added.')
            print(form.errors)
    else:
        form = ReqsForm()
    
    return render(request, 'reqs-add.html', {'form': form, 'memberID': memberID})

def MemberAllowanceAdd(request, memberID):
    member = get_object_or_404(Members, memberID=memberID)
    if request.method == 'POST':
        form = AllowanceForm(request.POST)
        memberID = request.POST.get('memberID')
        if form.is_valid():
            allowance = form.save(commit=False)
            allowance.memberID = member
            allowance.save()
            return redirect('allowances', memberID=memberID)
    else:
        form = AllowanceForm()
    
    return render(request, 'allowance-add.html', {'form': form, 'memberID': memberID})

# ALL UPDATE FUNCTIONS

class ProfileEdit(UpdateView):
    model = Members
    form_class = MembersForm
    template_name = 'profile-edit.html'
    success_url = "/members"

    def get_success_url(self):
        memberID = self.object.pk
        return reverse('profile', kwargs={'memberID':memberID})

    def form_valid(self, form):
      super().form_valid(form)
      return redirect(self.get_success_url())


class GradesEdit(UpdateView):
    model = Grades
    form_class = GradesForm
    template_name = 'grades-edit.html'

    def get_success_url(self):
        memberID = self.kwargs['memberID']
        return f"/grades/memberID={memberID}"

    def form_valid(self, form):
      super().form_valid(form)
      return redirect(self.get_success_url())

class ReqsListEdit(UpdateView):
    model = Requirements_list
    form_class = ReqsListForm
    template_name = 'reqs_list-edit.html'
    success_url = "/reqs-page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
      super().form_valid(form)
      return redirect(self.get_success_url())

class AllowanceEdit(UpdateView):
    model = Allowances
    form_class = AllowanceForm
    template_name = 'allowance-edit.html'

    def get_success_url(self):
        memberID = self.kwargs['memberID']
        return f"/allowance/memberID={memberID}"

    def form_valid(self, form):
      super().form_valid(form)
      return redirect(self.get_success_url())


# ALL DELETE FUNCTIONS
def ProfileDelete(request, memberID):
  member = Members.objects.get(memberID=memberID)
  member.delete()
  return redirect('members')

def GradesDelete(request, memberID, gradeID):
  get_object_or_404(Members, memberID=memberID)
  grade = Grades.objects.get(gradeID=gradeID)
  grade.delete()
  return redirect('grades', memberID=memberID)

def ReqsListDelete(request, reqs_listID):
  reqs_list = Requirements_list.objects.get(reqs_listID=reqs_listID)
  reqs_list.delete()
  return HttpResponseRedirect(reverse('reqs-page'))

def ReqsDelete(request, memberID, reqsID):
  get_object_or_404(Members, memberID=memberID)
  reqs = Requirements.objects.get(reqsID=reqsID)
  reqs.delete()
  return redirect('requirements', memberID=memberID)

def AllowanceDelete(request, memberID, allowanceID):
  get_object_or_404(Members, memberID=memberID)
  allowance = Allowances.objects.get(allowanceID=allowanceID)
  allowance.delete()
  return redirect('allowances', memberID=memberID)


