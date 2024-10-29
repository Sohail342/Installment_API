from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.db.models import Q
from rest_framework.response import Response

# Custom pagination class Categories
class CategoryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Filter class
class CategoryFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['search']

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    


# Custom pagination class for Products
class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = Category.objects.filter(name=category_name).first()
        
        if not category:
            return Product.objects.none() 

        # Get the search query
        search = self.request.query_params.get('search', '').strip()

        # Filter products by category and search query
        queryset = Product.objects.filter(category=category)

        if search:
            queryset = queryset.filter(Q(name__icontains=search))

        return queryset.order_by('name')
    

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Get the installment plan
        installment_plan = instance.get_installment_plan()
        
        # Create a response dictionary
        response_data = {
            'product': serializer.data,
            'installments': installment_plan
        }

        return Response(response_data)
