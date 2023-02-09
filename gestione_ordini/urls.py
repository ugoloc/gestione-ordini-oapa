from django.conf.urls import url
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from gestione_ordini import views

urlpatterns = [
    # ex: /gestione_ordini/*****			Redirect everything to a work-in-progress page
	#url(r'^.*', views.workinprogress, name='workinprogress'),
	
	# ex: /gestione_ordini/
	#url(r'^$', login_required(views.OrdersIndex.as_view()), name='index'),
	url(r'^$', views.OrderSearch, name='index'),


	# ex: /gestione_ordini/trasparenza
	url(r'^trasparenza/$', views.Trasparenza, name='trasparenza'),
	url(r'^trasparenza/(?P<anno>\d+)/$', views.Trasparenza, name='trasparenza'),
    # ex: /gestione_ordini/5/
    url(r'^(?P<order_id>\d+)/$', views.OrderChange, {'change': False}, name='detail'),
	# ex: /gestione_ordini/5/edit
	url(r'^(?P<order_id>\d+)/edit/$', views.OrderChange, name='edit'),
	# ex: /gestione_ordini/5/editAdmin
	url(r'^(?P<order_id>\d+)/editAdmin/$', views.OrderChange, {'editAdmin': True},name='editAdmin'),
	# ex: /gestione_ordini/5/openSection/collaudo
	url(r'^(?P<order_id>\d+)/openSection/(?P<section>\w+)/$', views.openSection, name='openSection'),
	# ex: /gestione_ordini/5/edit/verifyAttachment
	url(r'^(?P<order_id>\d+)/edit/verifyAttachment/(?P<section>\w+)/$', views.VerifyAttachment, name='verifyAttach'),
	# ex: /gestione_ordini/5/pdf
	url(r'^(?P<order_id>\d+)/(edit(Admin)?/)?pdf/$', views.OrderPdf, {'type': 'modulo'}, name='pdf'),
	# ex: /gestione_ordini/5/funds
	url(r'^(?P<order_id>\d+)/(edit(Admin)?/)?funds/$', views.loadFunds, name='funds'),
	# ex: /gestione_ordini/5/pdfDetermina
	url(r'^(?P<order_id>\d+)/(edit(Admin)?/)?pdfDetermina/$', views.OrderPdf, {'type': 'determina_contrarre'}, name='pdfDetermina'),
	# ex: /gestione_ordini/5/pdfDeterminaSC
	url(r'^(?P<order_id>\d+)/(edit(Admin)?/)?pdfDeterminaSC/$', views.OrderPdf, {'type': 'determina_aggiudicazione'}, name='pdfDeterminaSC'),
	# ex: /gestione_ordini/5/addfile/Sez_proposta
	url(r'^(?P<order_id>\d+)/addfile/(?P<section>\w+)(/(?P<sec_label>\w+))?/$', views.OrderAddfile, name='addfile'),
	# ex: /gestione_ordini/5/deletefile/3
	url(r'^(?P<order_id>\d+)/deletefile/(?P<file_id>\d+)$', views.OrderDeletefile, name='deletefile'),
	# ex: /gestione_ordini/5/delete
	url(r'^(?P<order_id>\d+)/delete/$', views.OrderDelete, name='delete'),
	# ex: /gestione_ordini/5/cancel
	url(r'^(?P<order_id>\d+)/cancel/$', views.OrderCancel, name='cancel'), # set order as Cancelled
	# ex: /gestione_ordini/5/follow
	url(r'^(?P<order_id>\d+)/follow/$', views.OrderFollow, {'follow': True}, name='follow'),
	# ex: /gestione_ordini/5/unfollow
	url(r'^(?P<order_id>\d+)/unfollow/$', views.OrderFollow, {'follow': False}, name='unfollow'),
    # ex: /gestione_ordini/new
	url(r'^new/$', views.OrderChange, {'order_id': 'new'}, name='new'),
	# ex: /gestione_ordini/new
	url(r'^search/$', views.OrderSearch, name='search'),
	# ex: /gestione_ordini/last_det_n
	#url(r'^last_det_n/$', views.GetLastDetN, name='last_det_n'),
	url(r'^latest/(?P<field_name>\w+)/$', views.GetLatest, name='latest'),
	
	
	# ex: /polls/5/results/
    #url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
]