import re

from rest_framework import serializers
from .models import AptidaoEleitor, Candidato, Eleicao, Eleitor, RegistroVotacao, Voto

class EleitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleitor
        fields = '__all__'

    def validate_cpf(self, value):
        cpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(cpf, value):
            raise serializers.ValidationError('CPF deve estar no formato XXX.XXX.XXX-XX')
    
class EleicaoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_candidatos = serializers.IntegerField(source='candidatos.count', read_only=True)
    total_aptos = serializers.IntegerField(source='aptos.count', read_only=True)

    class Meta:
        model = Eleicao
        fields = '__all__'
        extra_fields = ['status_display', 'total_candidatos', 'total_aptos']

class CandidatoSerializer(serializers.ModelSerializer):
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)

    class Meta:
        model = Candidato
        fields = '__all__'
        extra_fields = ['eleicao_titulo']

class AptidaoEleitorSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.CharField(source='eleitor.nome', read_only=True)
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)

    class Meta:
        model = AptidaoEleitor
        fields = '__all__'
        read_only_fields = ['eleitor_nome', 'eleicao_titulo']

class RegistroVotacaoSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.CharField(source='eleitor.nome', read_only=True)
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)

    class Meta:
        model = RegistroVotacao
        fields = '__all__'
        read_only_fields = ['eleitor_nome', 'eleicao_titulo']

class VotoSerializer(serializers.ModelSerializer):
    candidato_nome_urna = serializers.CharField(source='candidato.nome_urna', read_only=True, allow_null=True)
    em_branco_display = serializers.SerializerMethodField()

    class Meta:
        model = Voto
        fields = '__all__'
        extra_kwargs = {'comprovante_hash': {'write_only': True}}

    def get_em_branco_display(self, obj):
        return 'BRANCO' if obj.em_branco else None
    
class VotacaoInputSerializer(serializers.Serializer):
    candidato_id = serializers.IntegerField(required=False)
    em_branco = serializers.BooleanField(default=False)

    def validate(self, data):
        if not data.get('em_branco') and not data.get('candidato_id'):
            raise serializers.ValidationError('Deve fornecer candidato_id ou marcar como em_branco.')
        if data.get('em_branco') and data.get('candidato_id'):
            raise serializers.ValidationError('Não pode fornecer candidato_id se for em_branco.')
        return data