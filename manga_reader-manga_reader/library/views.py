from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import Book, Purchase, Chapter, ChapterImage
from .forms import ChapterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)
    new_manga = books.order_by('-id')[:10]

    # Get the latest chapter for each book
    latest_chapter_ids = (
        Chapter.objects.values('book')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )
    latest_updates = Chapter.objects.filter(id__in=latest_chapter_ids).select_related('book').order_by('-id')

    # Prepare top lists (replace with your own logic)
    top_manga = books.order_by('-id')[:10]
    top_week = books.order_by('-id')[:10]
    top_day = books.order_by('-id')[:10]
    for book in new_manga:
        book.latest_chapter = book.chapters.order_by('-number').first()
    for top in top_manga:
        top.latest_chapter = top.chapters.order_by('-number').first()
    for top in top_week:
        top.latest_chapter = top.chapters.order_by('-number').first()
    for top in top_day:
        top.latest_chapter = top.chapters.order_by('-number').first()
    return render(request, 'dashboard.html', {
        'new_manga': new_manga,
        'latest_updates': latest_updates,
        'top_manga': top_manga,
        'top_week': top_week,
        'top_day': top_day,
        'query': query,
    })

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    has_access = book.is_free or Purchase.objects.filter(user=request.user, book=book).exists()
    return render(request, 'book_detail.html', {'book': book, 'has_access': has_access})

@login_required
def purchase_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not Purchase.objects.filter(user=request.user, book=book).exists():
        Purchase.objects.create(user=request.user, book=book)
    return redirect('dashboard')

@staff_member_required
def add_chapter(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ChapterForm(request.POST, request.FILES)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.book = book
            chapter.save()
            for img in request.FILES.getlist('images'):
                ChapterImage.objects.create(chapter=chapter, image=img)
            # Save PDF
            if 'pdf' in request.FILES:
                chapter.pdf = request.FILES['pdf']
                chapter.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ChapterForm()
    return render(request, 'add_chapter.html', {'form': form, 'book': book})

@login_required
def read_chapter(request, book_id, chapter_id):
    book = get_object_or_404(Book, id=book_id)
    chapter = get_object_or_404(Chapter, id=chapter_id, book=book)
    chapters = list(book.chapters.order_by('number'))
    idx = chapters.index(chapter)
    prev_chapter = chapters[idx-1] if idx > 0 else None
    next_chapter = chapters[idx+1] if idx < len(chapters)-1 else None
    return render(request, 'read_chapter.html', {
        'book': book,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    })

