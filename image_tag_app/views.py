from django.shortcuts import render, HttpResponse, redirect
from .models import Data
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    datas = Data.objects.filter().values()
    taggers = Data.objects.filter().values('taggers')
    tags = Data.objects.filter().values('tags')

    paginator = Paginator(datas, 15) # Show 15 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 把 tag 轉成 distinct
    if tags is not None:
        for tag in tags:
            if tag['tags'] is not None:
                tag['tags'] = list(set(tag['tags']))


    return render(request, 'app/index.html', {'datas': datas, 'tags': tags, 'page_obj': page_obj})


def post(request, slug):
    if request.method == 'POST':

        tags = request.POST.get('tags', '').strip().split(' ')
        taggers = request.POST.get('taggers', '')
        ppt_post = Data.objects.get(slug__contains = slug)

        # 若沒有人標過，把標注者轉成空陣列
        if not ppt_post.taggers:
            ppt_post.taggers = []
        ppt_post.taggers.append(taggers)

        # 若沒有人給過標籤，把標籤轉成空陣列
        if not ppt_post.tags:
            ppt_post.tags = []
        for tag in tags:
            ppt_post.tags.append(tag)

        Data.objects.filter(slug__contains = slug).update(taggers = ppt_post.taggers)
        Data.objects.filter(slug__contains = slug).update(tags = ppt_post.tags)
        return HttpResponse(Data.objects.filter(slug__contains = slug).values())

    if request.method == 'GET':
        datas = Data.objects.filter(slug__contains = slug).values()
        tags = Data.objects.filter().values('tags')

        # 把 tag 轉成 distinct
        if tags is not None:
            for tag in tags:
                if tag['tags'] is not None:
                    tag['tags'] = list(set(tag['tags']))

        return render(request, 'app/post.html', {'datas': datas, 'tags': tags, 'slug': slug })

def delete_img(request, slug, img):
    imgs = Data.objects.filter(slug__contains = slug).values('imgs')[0]['imgs']
    img = imgs.pop(int(img))
    Data.objects.filter(slug__contains = slug).update(imgs = imgs)
    # HttpResponse(img+'has been removed,\n\ncurrent imgs: '+str(imgs))
    return redirect('/post/'+slug)
