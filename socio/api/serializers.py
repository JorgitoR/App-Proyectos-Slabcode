from rest_framework import serializers
from socio.models import Socio

class SocioSerializer(serializers.ModelSerializer):

	class Meta:
		model = Socio
		fields = (

			'nombre',
			'email',
			'website',


		)