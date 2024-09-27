from django.db import transaction
from django.http import HttpRequest, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import AssignmentForm, FileForm
from .models import File, Assignment


def main_page(request):
    return render(request, 'base.html')


class AssignmentView(ListView):
    template_name = 'assignment/assignment_list.html'
    model = Assignment
    context_object_name = 'assignments'
    paginate_by = 5

    def get(self, request: HttpRequest, *args, **kwargs):
        request.GET = request.GET.copy()
        if not request.GET.get('page'):
            request.GET['page'] = 1
        paginate_by = request.GET.get('paginate_by', self.paginate_by)
        if paginate_by != str(self.paginate_by) and paginate_by in {'5', '10', '20', '50'}:
            self.paginate_by = int(paginate_by)
        request.GET['paginate_by'] = self.paginate_by
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_color_labels'] = Assignment.Status.COLOR_LABELS
        context['priority_color_labels'] = Assignment.PRIORITY_COLOR_LABELS
        if not context.get('paginate_by'):
            context['paginate_by'] = self.paginate_by
        paginator = context.get('paginator')
        number = context.get('page_obj').number
        context['pages'] = paginator.get_elided_page_range(number=number, on_each_side=1, on_ends=1)
        filters = ''
        for param, value in self.request.GET.items():
            if param != 'page':
                filters += '&' + param + '=' + str(value)
        context['filters'] = filters
        return context


class AssignmentInfo(DetailView):
    template_name = 'assignment/assignment_info.html'
    model = Assignment
    context_object_name = 'assignment'
    slug_url_kwarg = 'assignment_uuid'
    slug_field = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['assignment'].subject
        context['status_color_labels'] = Assignment.Status.COLOR_LABELS
        context['priority_color_labels'] = Assignment.PRIORITY_COLOR_LABELS
        return context

    @staticmethod
    def download(request, assignment_uuid, file_uuid):
        file = get_object_or_404(File, uuid=file_uuid)
        response = FileResponse(file.file, 'rb', as_attachment=True)
        return response


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
