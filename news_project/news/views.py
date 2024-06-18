from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import logout
from .forms import NewsForm
from .models import News

def is_admin(user):
    return user.is_superuser


@login_required
def news_list(request):
    news = News.objects.all()
    paginator = Paginator(news, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/news_list.html', {'page_obj': page_obj})


@login_required
def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news_item': news_item})


@user_passes_test(is_admin)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form})


@user_passes_test(is_admin)
def news_edit(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'news/news_form.html', {'form': form})


@user_passes_test(is_admin)
def news_delete(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news_item.delete()
        return redirect('news_list')
    return render(request, 'news/news_confirm_delete.html', {'news_item': news_item})


def logout_view(request):  # Функция для выхода из аккаунта
    logout(request)
    return redirect('login')