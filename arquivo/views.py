from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from .models import *
import os
import math
from django.core.paginator import Paginator
# Create your views here.


def home(request):
    return render(request, 'arquivo/pages/home.html')

def files(request):
    objetos = Objeto.objects.filter(
        publicado=True
    ).order_by('-id')
    
    
    page_object, pagination_range = make_pagination(request,objetos, 8)

    return render(request, 'arquivo/pages/files.html', context={
        'objetos': page_object,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
        'pagination_range': pagination_range
    })


def images(request):
    objetos = Objeto.objects.filter(
        publicado=True,
        extensao_arquivo__icontains='image'
    ).order_by('-id')
    
    return render(request, 'arquivo/pages/files-type.html', context={
        'objetos': objetos,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
    })

def documents(request):
    objetos = Objeto.objects.filter(
        publicado=True,
        extensao_arquivo__icontains='application'
    ).order_by('-id')
    
    return render(request, 'arquivo/pages/files-type.html', context={
        'objetos': objetos,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
    })
    
def videos(request):
    objetos = Objeto.objects.filter(
        publicado=True,
        extensao_arquivo__icontains='video'
    ).order_by('-id')
    
    return render(request, 'arquivo/pages/files-type.html', context={
        'objetos': objetos,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
    })




def detail(request, id):

    objeto = get_object_or_404(Objeto, pk=id, publicado=True)
    objetos = Objeto.objects.all()
    categoria = objeto.categorias.all()
    

    return render(request, 'arquivo/pages/detail.html', context={
        'objeto': objeto,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'categoria': categoria,
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
    })


def categorys(request, categoria):
    objeto = Objeto.objects.all()
    print('////////////')
    # for i in objeto:
    #     print(i)
    print(categoria)
    cat_objetos = objeto.filter(
            Q(categorias__slug=categoria) |
            Q(titulo__icontains=categoria) |
            Q(categorias__nome_categoria=categoria) |
            Q(nome_produtor__slug__icontains=categoria) |
            Q(slug__icontains=categoria),
        publicado=True,
    )
    
    print('*********************')
    for i in cat_objetos:
        print(i)

    print(len(cat_objetos))
    return render(request, 'arquivo/pages/related-categorys.html', context={
        'objetos': cat_objetos,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
    })


def search(request):
    query = request.GET.get('query', '').strip()

    found_objects = Objeto.objects.filter(
        Q(
            Q(categorias__nome_categoria__icontains=query) |
            Q(titulo__icontains=query) |
            Q(nome_produtor__nome_produtor__icontains=query) |
            Q(nome_diretor__icontains=query) |
            Q(autor__icontains=query) |
            Q(entidade_custodiadora__icontains=query) |
            Q(descricao__icontains=query)
        ),
        publicado=True,
    )

    print(len(found_objects))

    return render(request, 'arquivo/pages/search_objects.html', context={
        'objetos': found_objects,
        'qtd': len(found_objects),
        'query': query,
        'num_img': get_num_img(Objeto, 'image'),
        'num_video': get_num_img(Objeto, 'video'),
        'num_document': get_num_img(Objeto, 'application'),
        'titulos': get_titles(Objeto),
        'categorias': get_categorys(Categoria),
        'produtores': get_producers(Produtor),
    })


def get_categorys(model):
    categorias = model.objects.all().order_by('-id')[:5]
    return categorias


def get_producers(model):
    produtores = model.objects.all().order_by('-id')[:5]
    return produtores


def get_titles(model):
    titulos = model.objects.all().order_by('-id')[:5]
    return titulos


def get_all_objects(objeto):
    objetos = objeto.objects.filter(
        publicado=True
    ).order_by('-id')
    return objetos


def get_num_img(objeto, tipo):
    tipos = objeto.objects.filter(
        extensao_arquivo__icontains = tipo
    )
    tipes = len(tipos)
    return tipes


def make_pagination_range( page_range, qty_pages, current_page ):
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)
    
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - start_range)
    
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_is_out_of_range': current_page > middle_range,
        'last_page_is_out_of_range': stop_range < total_pages
    }


def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1
    
    paginator = Paginator(queryset, per_page)
    page_object = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return page_object, pagination_range