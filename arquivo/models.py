from django.db import models
from django.utils.text import slugify
import re
import PyPDF2
import subprocess
from PIL import Image
from django.conf import settings
import os
from django.core.files import File
from io import BytesIO
import mimetypes
# Create your models here.

class Produtor(models.Model):
    nome_produtor = models.CharField(max_length=255, blank=False, null=False, verbose_name='Produtor')
    slug = models.SlugField(max_length=255, default='',blank=True, null=True, unique=True)

    def __str__(self):
        return self.nome_produtor
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug += f'-{slugify(self.nome_produtor)}'

        super().save(*args, **kwargs)

class Categoria(models.Model):
    nome_categoria = models.CharField(max_length=255, blank=False, null=False, verbose_name='Categoria')
    slug = models.SlugField(max_length=255, default='',blank=True, null=True, unique=True)

    
    def __str__(self):
        return self.nome_categoria 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug += f'-{slugify(self.nome_categoria)}'

        super().save(*args, **kwargs)

class Objeto(models.Model):
    arquivo = models.FileField(upload_to=r'arquivos/principal/%Y/%m/%d/', verbose_name='Arquivo')
    thumbnail = models.FileField(upload_to=r'arquivos/thumbnail/%Y/%m/%d/',default='', blank=True, verbose_name='Thumbnail')
    extensao_arquivo = models.CharField(max_length=255, blank=True, verbose_name='Extensão')
    nome_produtor = models.ForeignKey(Produtor, on_delete = models.SET_NULL, blank=True, null=True, verbose_name='Produtor')
    nome_diretor = models.CharField(max_length=255, blank=False, null=False, verbose_name='Diretor')
    titulo = models.CharField(max_length=255, blank=False, null=False, verbose_name='Título')
    slug = models.SlugField(max_length=255, default='',blank=True, null=True, unique=True)
    autor = models.CharField(max_length=255, blank=True, null=False, verbose_name='Autor')
    data = models.DateTimeField(blank=True, null=False, verbose_name='Data')
    created_at = models.DateTimeField(auto_now_add=True)
    dimensao_suporte = models.TextField( blank=True, null=False, verbose_name='Dimensão e suporte')
    entidade_custodiadora = models.CharField(max_length=255, blank=True, null=False, verbose_name='Entidade custoriadora')
    localizacao_fisica = models.CharField(max_length=255, blank=True, null=False, verbose_name='Localização física')
    descricao = models.TextField(default='', blank=True, null=False, verbose_name='Descrição')
    nota_explicativa = models.CharField(max_length=255, blank=True, null=False, verbose_name='Nota explicativa')
    categorias = models.ManyToManyField(Categoria, blank=False, verbose_name='Categorias')
    publicado = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo 
    
    def save(self, *args, **kwargs):

        if not self.slug:
            # Gera o slug a partir do título
            self.slug = slugify(self.titulo)
            self.slug += f'-{slugify(self.nome_produtor)}-{slugify(self.autor)}'

        self.get_extension(self)
        super().save(*args, **kwargs)
        
        self.create_thumbnail(self)
        
    
    @staticmethod
    def create_thumbnail(self):
        ext = os.path.splitext(self.arquivo.url)[1]
        print(ext)
        # Verifica se o arquivo possui uma thumbnail já criada
        if self.thumbnail:
            return
        if ext in ['.jpeg', '.jpg', '.png']:
            # Abre o arquivo
            with Image.open(self.arquivo) as image:
                # Redimensiona a imagem para a thumbnail
                image.thumbnail((500, 500))

                # Cria um arquivo temporário para armazenar a thumbnail
                temp_thumb = BytesIO()

                # Salva a thumbnail no arquivo temporário
                image.save(temp_thumb, 'JPEG')
                temp_thumb.seek(0)

                # Cria um novo Django File usando o arquivo temporário
                django_file = File(temp_thumb)

                # Atribui o Django File criado como thumbnail do objeto
                self.thumbnail.save(self.arquivo.name, django_file)
        

    @staticmethod
    def get_extension(self):
        mimetype = mimetypes.guess_type(self.arquivo.url)[0]
        print(mimetype)
        self.extensao_arquivo = mimetype    
        
    

