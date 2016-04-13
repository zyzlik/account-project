import json

from django.http import HttpResponse
from django.views.generic.edit import FormView

from .forms import MoneyTransferForm


class MoneyTransferView(FormView):
    template_name = 'index.html'
    form_class = MoneyTransferForm
    success_url = '/'

    def form_valid(self, form):
        form.transfer_process()
        super(MoneyTransferView, self).form_valid(form)
        return HttpResponse("ok")

    def form_invalid(self, form):
        data = []
        for k, v in form._errors.iteritems():
            text = {
                'desc': ', '.join(v),
            }
            if k == '__all__':
                text['key'] = '#%s' % self.request.POST.get('form')
            else:
                text['key'] = '#id_%s' % k
            data.append(text)
        return HttpResponse(json.dumps(data))
