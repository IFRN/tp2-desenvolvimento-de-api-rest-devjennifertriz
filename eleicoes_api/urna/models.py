from django.db import models
from django.core.exceptions import ValidationError
 
class Eleitor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} ({self.cpf})'

class Eleicao(models.Model):
    TIPO_CHOICES = [
        ('estudantil', 'Estudantil'),
        ('sindical', 'Sindical'),
        ('associacao', 'Associacao'),
        ('condominio', 'Condomínio'),
        ('conselho', 'Conselho'),
        ('outra', 'Outra'),
    ]
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('aberta', 'Aberta'),
        ('encerrada', 'Encerrada'),
        ('apurada', 'Apurada'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='rascunho')
    permite_branco = models.BooleanField(default=True)
    criada_por = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='eleicoes_criadas')

    def __str__(self):
        return self.titulo
    
    def clean(self):
        if self.data_inicio > self.data_fim:
            raise ValidationError('Data de início deve ser anterior à data de fim.')

class Candidato(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='candidatos')
    numero = models.PositiveIntegerField()
    nome = models.CharField(max_length=150)
    nome_urna = models.CharField(max_length=50)
    partido_ou_chapa = models.CharField(max_length=100, blank=True)
    proposta = models.TextField(blank=True)
    foto_url = models.URLField(blank=True)

    class Meta:
        unique_together = [('eleicao', 'numero')]

    def __str__(self):
        return f'{self.nome_urna} (#{self.numero}) — {self.eleicao.titulo}'


class AptidaoEleitor(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='aptidoes')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='aptos')
    data_inclusao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('eleitor', 'eleicao')]

    def __str__(self):
        return f'{self.eleitor.nome} apto em {self.eleicao.titulo}'


class RegistroVotacao(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='registros_votacao')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='registros_votacao')
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('eleitor', 'eleicao')]

    def __str__(self):
        return f'{self.eleitor.nome} votou em {self.eleicao.titulo}'


class Voto(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='votos')
    candidato = models.ForeignKey(Candidato, on_delete=models.PROTECT, related_name='votos', null=True, blank=True)
    em_branco = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    comprovante_hash = models.CharField(max_length=64, unique=True)

    def __str__(self):
        if self.em_branco:
            return f'Voto em branco — {self.eleicao.titulo}'
        return f'Voto em {self.candidato.nome_urna} — {self.eleicao.titulo}'