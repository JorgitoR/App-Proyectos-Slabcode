from rest_framework import pagination

class ResultadoStandarPaginacion(pagination.PageNumberPagination):
	page_size = 3
	page_size_query_param = 'page_size'
	maz_page_size = 4