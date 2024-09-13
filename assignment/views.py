from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views import View

from .forms import AssignmentForm


def main_page(request):
    return render(request, 'base.html')


class Assignment(View):

    def get(self, request):
        context = {'assignment_list': ''}
        return render(request, 'assignment/assignment_list.html', context=context)

    def post(self, request):
        return HttpResponse('post method')


class CreateAssignment(View):

    def get(self, request):
        form = AssignmentForm()
        context = {'form': form}
        return render(request, 'assignment/create_assignment.html', context=context)

    def post(self, request: HttpRequest):
        form = AssignmentForm(request.POST)
        context = {'form': form}
        print(form.is_valid())
        print(form.errors)
        return render(request, 'assignment/create_assignment.html', context=context)
