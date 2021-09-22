from administrador.models import Plato, Comedor
# from django.contrib.auth.models import Group
from rest_framework import serializers
from account.models import User


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

#Serializer de Platos
class PlatoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plato
        fields = ['id','nombre_plato', 'dia_plato', 'hora_plato', 'precio_plato','comedor_id_comedor']

#Serializer de Platos
class ComedorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comedor
        fields = ['id','servicio_comedor']
