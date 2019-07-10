from django.shortcuts import render, redirect, get_object_or_404
from autos.models import Auto, Comment
from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from autos.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from autos.forms import CreateForm, CommentForm


class AutoListView(OwnerListView):
    model = Auto
    template_name = "auto_list.html"

    def get(self, request) :
        auto_list = Auto.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}]  (A list of rows)
            rows = request.user.favorite_autos.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx = {'auto_list' : auto_list, 'autos': autos}
        return render(request, self.template_name, ctx)

#@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Auto, id=pk)
        fav = Fav(user=request.user, auto=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

#@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Auto, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, auto=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


class AutoListView(OwnerListView):
    model = Auto
    template_name = "auto_list.html"

class AutoDetailView(OwnerDetailView):
    model = Auto
    template_name = "auto_detail.html"

    def get(self, request, pk) :
        auto = Auto.objects.get(id=pk)
        comments = Comment.objects.filter(auto=auto).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'auto' : auto, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class AutoCreateView(OwnerCreateView):
    model = Auto
    fields = ['name', 'detail', 'mileage']
    template_name = "auto_form.html"

class AutoUpdateView(OwnerUpdateView):
    model = Auto
    fields = ['name', 'detail', 'mileage']
    template_name = "auto_form.html"

class AutoDeleteView(OwnerDeleteView):
    model = Auto
    template_name = "auto_delete.html"

class CommentCreateView(OwnerCreateView):
    def post(self, request, pk) :
        f = get_object_or_404(Auto, id=pk)
        comment_form = CommentForm(request.POST)
        comment = Comment(text=request.POST['comment'], owner=request.user, auto=f)
        comment.save()
        return redirect(reverse_lazy('auto_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "comment_delete.html"



class PicFormView(LoginRequiredMixin, View):
    template = 'auto_form.html'
    success_url = reverse_lazy('autos')
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            pic = get_object_or_404(Auto, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            pic = get_object_or_404(Auto, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)


def stream_file(request, pk) :
    pic = get_object_or_404(Auto, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response