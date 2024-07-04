from rest_framework.permissions import IsAuthenticated
from utils.check_perm import CustomAuthentication
from utils.views import GenericListView, GenericDetailView
from . import models
from . import serializers



class CsListView(GenericListView):
    model = models.Inquiry
    # pagination_class = GenericPaginator
    serializer_class = serializers.InquirySerializer
    create_serializer_class = serializers.InquiryCreateSerializer
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    # search_fields = ['name','phone','email']
    #transction_savepoint = True
    # select_related_fields = ['size','manufacturer',
    #                          'unit1','unit2','category','promotion']
    #prefilter_param = {'is_active':True }
    #ordering = ['-created_on']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제외 쿼리파라미터 ex) ['search', 'user', 'id']
        # self.excluded_params.extend(['category'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
          
class CsDetailView(GenericDetailView):
    model = models.Inquiry
    serializer_class = serializers.InquirySerializer

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)