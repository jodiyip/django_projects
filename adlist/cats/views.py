from django.shortcuts import render, redirect, get_object_or_404
from cats.models import Cat, Comment
from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from cats.util import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from cats.forms import CreateForm, CommentForm


class CatListView(OwnerListView):
    model = Cat
    template_name = "cat_list.html"

    def get(self, request) :
        cat_list = Cat.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}]  (A list of rows)
            rows = request.user.favorite_cats.values('id')
            favorites = [ row['id'] for row in rows ]
        ctx = {'cat_list' : cat_list, 'cats': cats}
        return render(request, self.template_name, ctx)

#@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(Cat, id=pk)
        fav = Fav(user=request.user, cat=t)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

#@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Cat, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, cat=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()


class CatListView(OwnerListView):
    model = Cat
    template_name = "cat_list.html"

class CatDetailView(OwnerDetailView):
    model = Cat
    template_name = "cat_detail.html"

    def get(self, request, pk) :
        cat = Cat.objects.get(id=pk)
        comments = Comment.objects.filter(cat=cat).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'cat' : cat, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class CatCreateView(OwnerCreateView):
    model = Cat
    fields = ['name', 'foods', 'weight']
    template_name = "cat_form.html"

class CatUpdateView(OwnerUpdateView):
    model = Cat
    fields = ['name', 'foods', 'weight']
    template_name = "cat_form.html"

class CatDeleteView(OwnerDeleteView):
    model = Cat
    template_name = "cat_delete.html"

class CommentCreateView(OwnerCreateView):
    def post(self, request, pk) :
        f = get_object_or_404(Cat, id=pk)
        comment_form = CommentForm(request.POST)
        comment = Comment(text=request.POST['comment'], owner=request.user, cat=f)
        comment.save()
        return redirect(reverse_lazy('cat_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "comment_delete.html"



class PicFormView(LoginRequiredMixin, View):
    template = 'cat_form.html'
    success_url = reverse_lazy('cats')
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            pic = get_object_or_404(Cat, id=pk, owner=self.request.user)
            form = CreateForm(instance=pic)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            pic = get_object_or_404(Cat, id=pk, owner=self.request.user)
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
    pic = get_object_or_404(Cat, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response