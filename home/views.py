from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class HomeView(TemplateView):
    template_name = 'home/home.html'

home = HomeView.as_view()


class CompareDetailView(TemplateView):
    template_name = 'home/compare.html'

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(CompareDetailView, self).dispatch(request=request)

compare_detail_view = CompareDetailView.as_view()