from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from .forms import AssignmentForm, FileForm
from .models import File, Assignment


def main_page(request):
    return render(request, 'base.html')


class AssignmentView(View):

    def get(self, request):
        context = {'assignment_list': ''}
        return render(request, 'assignment/assignment_list.html', context=context)

    def post(self, request):
        return HttpResponse('post method')


class CreateAssignment(View):

    def get(self, request):
        assignment_form = AssignmentForm()
        file_form = FileForm()
        context = {'assignment_form': assignment_form,
                   'file_form': file_form}
        return render(request, 'assignment/create_assignment.html', context=context)

    def post(self, request: HttpRequest):
        assignment_form = AssignmentForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)
        if assignment_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                assignment = assignment_form.save()
                File.objects.bulk_create([
                    File(file=file, assignment=assignment) for file in file_form.files.getlist('file')
                ])
        else:
            context = {'assignment_form': assignment_form,
                       'file_form': file_form}
            return render(request, 'assignment/create_assignment.html', context=context)
        return redirect('assignment_list')



