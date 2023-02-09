#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect #, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from django import forms as django_forms

import datetime
from collections import OrderedDict
import logging
import pdb		# debugger
import json

import gestione_ordini.forms as forms
from gestione_ordini.models import Ordine, File
from django.contrib.auth.models import User, Group
from django.db.models.base import ObjectDoesNotExist


logging.basicConfig(filename='debug.log', level=logging.DEBUG)


# Create your views here.

class OrdersIndex(generic.ListView):
	template_name = 'ordini/index.html'
	context_object_name = 'orders_list'
	def get_queryset(self):
		return Ordine.objects.filter(order_closed=False).order_by('-data_prop')
		#return Ordine.objects.order_by('-data_prop')

#class OrderDetail(generic.DetailView):
#	model = Ordine
#	template_name = 'ordini/detail.html'



def workinprogress(request):
	outStr = "WORK IN PROGRESS, contattare l'amministratore in caso di necessità"
	return HttpResponse(outStr, content_type="text/plain; charset=utf-8")

	
#@login_required	
def Trasparenza(request,anno=2016):
	dataStart = '{}-01-01'.format(anno)
	outStr=u''
	l = Ordine.objects.filter(determ_data__gte = dataStart).order_by('determ_data')
	head = ['id', 'data proposta', 'cig', 'cup', 'n.determina contrarre', 'data determina contrarre', 'n.determina aggiudicazione', 'data determina aggiudicazione', 'rup', 'oggetto', 'scelta del contraente', 'contraente', 'codice fornitore','Elenco operatori invitati/n. di offerte', 'data ordine', 'importo', 'importo liquidato', 'data pagamento']
	for col in head:
		outStr += col + '; '
	outStr = outStr[:-1] + '\r\n'
	for order in l:
		data = [order.rich_acq_id, dateConv(order.data_prop), order.CIG, order.CUP, order.determ_n, dateConv(order.determ_data),order.determ_sc_n, dateConv(order.determ_sc_data), order.RUP.profilo.full_name, order.descriz, order.modo_scelta_contr, order.contraente, order.cod_forn, order.operatori, dateConv(order.data_stesura_ordine)+dateConv(order.data_caric_mepa), order.importo, order.importo_liquidato, dateConv(order.data_pagamento)]
		chkstr(data)
		for col in data:
			outStr += col + '; '
		outStr = outStr[:-1] + '\r\n'
	return HttpResponse(outStr, content_type="text/plain; charset=utf-8")

'''
@login_required	
def Tempi(request,anno=2016):
	lista_campi = [
			#(tipo, nome campo, etichetta)
			('testo'	,'rich_acq_id'					,'id'),
			('testo'	,'stima_costo'					,'stima costo'),
			('data'		,'data_prop'					,'proposta'),
			('data'		,'data_sceltaFondi'				,'scelta fondi/RUP'),		# (Direzione) 
			('data'		,'data_firma_resp_fondi'		,'autorizzazione fondi'),	# (resp. fondi)
			#data_firma_resp_ufficio,
			('data'		,'data_firma_funz_contabile'	,'prenotazione importo'),	# (funz. contabile)
			#determ_data,
			('data'		,'data_firma_direttore'			,'determina a contrarre'),	# (Direzione)
			('data'		,'data_CIG'						,'acquisizione CIG'),		# (RUP)
			#dateConv(order.data_caric_mepa), 
			#dateConv(order.data_stesura_ordine),
			('data'		,'data_firma_RUP_ordine'		,'stesura ordine'),			# (RUP)
			#dateConv(order.data_trasm_doc),	# Solo GARA
			# NON C'E' DATA NELLA SEZIONE VERIFICHE!
			#dateConv(order.determ_sc_data), 
			('data'		,data_firma_direttore_sc'		,'determina di aggiudicazione'),	# (Direzione)
			# NON C'E' DATA NELLA SEZIONE CONTROLLO VERIFICHE!
			# NON C'E' DATA NELLA SEZIONE IMPEGNO CONSOLIDATO!
			#dateConv(order.data_rich_durc),
			#dateConv(order.data_trasm_PO),
			('data'		,'data_impegno_cons'			,'impegno consolidato'),	# (funz. contabile)
			('data'		,'data_autorizz'				,'autorizzazione acquisto'),	# (Direzione)
			('data'		,'data_ordine'					,'emissione ordine'),			# (Punto Ord.) - CASO MEPA SI
			('data'		,'data_spediz_ordine'			,'invio ordine'),				# (RUP) - CASO MEPA NO
			('data'		,'data_verifica'				,'verifica/collaudo'),			# (RUP)
			('data'		,'data_pagamento'				,'pagamento'),					# (funz. contabile)
			#dateConv(order.data_comunic_RUP),
			]
	dataStart = '{}-01-01'.format(anno)
	outStr=u''
	l = Ordine.objects.filter(determ_data__gte = dataStart).order_by('data_proposta')
	head = [campo[2] for campo in lista_campi]
	for col in head:
		outStr += col + '; '
	outStr = outStr[:-1] + '\r\n'
	# gara == False
	# order_status 'CANC'
	for order in l:
		data = []
		chkstr(data)
		for col in data:
			outStr += col + '; '
		outStr = outStr[:-1] + '\r\n'
	return HttpResponse(outStr, content_type="text/plain; charset=utf-8")
'''

def dateConv(dateString):
	if not dateString == None:
		return dateString.strftime('%d/%m/%Y')
	else:
		return ''
	
def chkstr(data):
	for index, item in enumerate(data):
		if (item and not item == None):
			data[index] = unicode(item)
			data[index] = data[index].replace('\n', ', ').replace('\r', '').replace(';', '.')
		else:
			data[index] = ''
	

@login_required
def OrderDetail(request, order_id):
	order = get_object_or_404(Ordine, pk=order_id)
	form = forms.OrderForm(instance=order)
	change = False
	for field in form:
		if isinstance(field.field.widget, django_forms.Textarea) or isinstance(field.field.widget, django_forms.TextInput):
			field.field.widget.attrs['readonly'] = 'True'
		else:	
			field.field.widget.attrs['disabled'] = 'True'
	list_form = [form]
	return render(request, 'ordini/detail.html', {'list_form': list_form, 'order': order, 'change': change})


@login_required
def OrderChange(request, order_id, **kwargs):
	#pdb.set_trace()
	if kwargs.get('change') == False:
		change = False
	else:
		change = True
	if kwargs.get('editAdmin') == True and ('super' in request.user.groups.values_list('name',flat=True)):
		editAdmin = True
	else:
		editAdmin = False
	message = ''
	#username = request.user.get_username()
	if order_id == 'new':
		order = Ordine(proponente=request.user, data_prop = datetime.datetime.today(),
			versione_procedura = '4',
			versione_PDF = '1')
		order.save()
		#NOTIFICA send_mail('Creato nuovo ordine', 'Hai creato un nuovo ordine.', settings.EMAIL_REPLYTO,[request.user.email], fail_silently=False)
		return redirect('../' + str(order.id) + '/edit')
	else:
		order = get_object_or_404(Ordine, pk=order_id)
	orderEdit_url = settings.SERVER_LINK + reverse('gestione_ordini:edit', kwargs={'order_id': order_id})
	text_link = "link: " + orderEdit_url
	html_message = "<a href='" + orderEdit_url + "'>Vai all'ordine</a>"
	
	editable_sections = CheckSection(order,request.user)

	sections_forms = OrderModelVersion(order).sections_forms

	# if this is a POST request we need to process the form data
	try:
		if request.method == 'POST':
			section = request.POST['section']
			sec_label = request.POST.get('sec_label','dummy')
			if section in editable_sections or editAdmin:
				if request.POST.get('reopen_section', False):			# if POST contain a request to reopen previous section (default False)
					prev_sect = OrderModelVersion(order).get_prev_sect(section)	# get previous section name
					if prev_sect:
						order.__dict__[prev_sect+'_closed'] = False			# set prev section to open
						notify_list = OrderModelVersion(order).notify_list_prev(section,user=request.user)
						message = 'Sezione precedente riaperta. Notificato a ' + notify_list.str
						message += '. Lista email: ' + str(notify_list.emails)
						print ('Notifica riapertura a: ' + str(notify_list.emails))
						if settings.ENABLE_EMAIL and not editAdmin:
							try:
								send_mail('[ORDINI] Riapertura sezione - '+str(order).replace('\n', ' ').replace('\r', ''), u'Una sezione è stata riaperta.\n'+"Richiesta di acquisto: " + str(order.rich_acq_id)+"\n"+text_link, settings.EMAIL_REPLYTO,notify_list.emails, fail_silently=False)
							except Exception as e:
								s = str(e)
								message = 'Sezione riaperta, INVIO EMAIL NON RIUSCITO!\n' + s	
								print ('Invio email non riuscito')
								print (s)
						else:
							message += '\n INVIO EMAIL DISABILITATO'
						order.attesa = notify_list.waitfor
						#order.save()											# save change
						OrderModelVersion(order).setOrderStatus()				# set order status and save
				else:												# else POST contains new DB data
					form = sections_forms[section](request.POST, instance=order)
					if form.is_valid():											# if form data is valid...
						form.save()												# ...save to DB
						if (request.POST[section + '_closed'] == 'True'):		# if 'section'_closed field is True: save and close section
							setattr(order, section+'_closedby', request.user)
							#order.save()
							notify_list = OrderModelVersion(order).notify_list_first_open(section,user=request.user)
							# if request.POST.get('order_closed') == 'True':									# if order is being closed
								# order.attesa = ''
								# #order.save()
								# OrderModelVersion(order).setOrderStatus()					# set order status and save
								# message = 'Ordine chiuso.'
								# message += ' Lista email: ' + str(notify_list.emails)
								# if settings.ENABLE_EMAIL and not editAdmin:
									# try:
										# send_mail('[ORDINI] Ordine chiuso - '+str(order), u"L'ordine è stato chiuso.\n"+"Richiesta di acquisto: " + str(order.rich_acq_id)+"\n"+text_link, settings.EMAIL_REPLYTO,notify_list.emails, fail_silently=False)
									# except Exception as e:
										# s = str(e)
										# message = 'Ordine chiuso, INVIO EMAIL NON RIUSCITO!\n' + s	
										# print 'Invio email non riuscito'
										# print s
								# else:
									# message += '\n INVIO EMAIL DISABILITATO'
							# else:
							order.attesa = notify_list.waitfor
							#order.save()
							OrderModelVersion(order).setOrderStatus()					# set order status and save
							message = 'Sezione "'+sec_label+'" salvata ed inviata. Notificato a: ' + notify_list.str	# if closing a section
							message += '. Lista email: ' + str(notify_list.emails)
							print ('Notifica chiusura sez. a: ' + str(notify_list.emails))
							emailText = "La sezione '"+sec_label+ u"' è stata chiusa.\n"+"Richiesta di acquisto: " + str(order.rich_acq_id)+"\n"+text_link
							if settings.ENABLE_EMAIL and not editAdmin:
								try:
									send_mail('[ORDINI] Chiusura sezione - '+str(order).replace('\n', ' ').replace('\r', ''), emailText, settings.EMAIL_REPLYTO,notify_list.emails, fail_silently=False)
								except Exception as e:
									s = str(e)
									message = 'Sezione salvata e chiusa, INVIO EMAIL NON RIUSCITO!\n' + s	
									print ('Invio email non riuscito')
									print (s)
							else:
								message += '\n INVIO EMAIL DISABILITATO'
						else:
							message = "Sezione '"+sec_label+"' salvata."
					else:
						message = 'Dati del form non corretti.'
			#change = form.save(commit=False)
			#change.save()
			#form.save_m2m()
			OrderModelVersion(order).setOrderStatus()					# set order status
			editable_sections = CheckSection(order,request.user)		# recheck open sections: POST action could have changed things
			sections_forms = OrderModelVersion(order).sections_forms	# load the dictionary with sections and corresponding forms
			return HttpResponse(message)
	except Exception as e:
		print(str(e))
		raise
	# if a GET (or any other method)
	if order.order_closed:
		change = False
	if order in request.user.profilo.ordini_seguiti.all():		# tracks if current order is already followed by the user
		followed = True
	else:
		followed = False
	list_form = list()
	from django.forms.fields import DateField,BooleanField,NullBooleanField	# load the form elements classes to later check if fields are instances of these classes
	
	enable_reopen = False
	for k,form in sections_forms.items():					# instantiate the form objects
		list_form.append(form(instance=order))
	for form in list_form:										# for each form (section):
		if enable_reopen:
			form.enable_reopen = True
		if (not change or not form.section in editable_sections) and not editAdmin:	# disable forms that are not included in editable sections
			form.is_editable = False
		else:
			form.is_editable = True
		for field in form:
			if isinstance(field.field, DateField):										# check if fields are datefields
					field.field.widget.attrs['class'] = field.field.widget.attrs.get('class','') + ' datepicker'	# if yes append the class datepicker to the old class
			if (isinstance(field.field, BooleanField) or isinstance(field.field, NullBooleanField)):		# check if fields are BooleanField or NullBoleanField
					field.field.widget.attrs['class'] = field.field.widget.attrs.get('class','') + ' checkbox'
			if not form.is_editable:
				if isinstance(field.field.widget, django_forms.Textarea) or isinstance(field.field.widget, django_forms.TextInput):
					field.field.widget.attrs['readonly'] = 'True'
				else:	
					field.field.widget.attrs['disabled'] = 'True'

		#from django import forms
		sec_clos_field = form.fields[form.section+'_closed']
		field_class = sec_clos_field.widget.attrs.get('class')
		if field_class:
			field_class += ' section_closed'
		else:
			field_class = 'section_closed'
		sec_clos_field.widget = django_forms.HiddenInput(attrs={'class':field_class})	# set widget HiddenInput and add class 'section_closed' for all the 'section'_closed fields
		try:
			ord_clos_field = form.fields['order_closed'] 
			field_class = ord_clos_field.widget.attrs.get('class')
			if field_class:
				field_class += ' section_closed order_closed'
			else:
				field_class = 'section_closed order_closed'
			ord_clos_field.widget = django_forms.HiddenInput(attrs={'class':field_class})	# set widget HiddenInput and add class 'section_closed' for the 'closed' fields
		except KeyError:
			pass
		#import pdb; pdb.set_trace()	#enable debug
		if getattr(order,form.section+'_closed'):				  						#	check if section is closed
			form.closed = True
			enable_reopen = True
			form.closedby = getattr(order,form.section+'_closedby').get_full_name()
		else:
			enable_reopen = False
	return render(request, 'ordini/detail.html', {'list_form': list_form, 'order': order, 'change': change, 'error_message':message, 'followed':followed, 'editAdmin':editAdmin})


def CheckSection(order,curruser):
	''' Return a list of open sections editable by the current user '''
	groups_list = curruser.groups.values_list('name',flat=True)		# get a list of all the user groups
	section_list = list();
	if not order.Sez_Proposta_closed:								# if Sez_Proposta is open no other section can be modified
		if curruser == order.proponente or 'super' in groups_list:	# Proponente or 'super' group can modify Proposta
			section_list.append('Sez_Proposta')
	else:
		try:
			for section, person in OrderModelVersion(order).incharge:					# for each section-person in charge pair:
				if (not getattr(order,section+'_closed')):								# test if section is open
					if 'super' in curruser.groups.values_list('name',flat=True):		# test if user is in 'super' group
						section_list.append(section)
					elif person.startswith('group_'):									# test if current 'person' in charge is a group
						if person.replace('group_','') in curruser.groups.values_list('name',flat=True):	# if group: check if user is in that group
							section_list.append(section)								# 	if pass test add the section to the open sections
					#elif (curruser == getattr(order,person)):						# if not group: check user vs. pers. in ch. for the section
					#	section_list.append(section)
					else:
						try:
							print('Checking user')
							if curruser == User.objects.get(username=person):			# verifiy if given incharge is a username
								section_list.append(section)
						except(ObjectDoesNotExist):
							print('Checking with order getattr')
							if (curruser == getattr(order,person)): # if not username check if is a order field (es. RUP)
								section_list.append(section)

		except (AttributeError):				# if attribute doesn't exists exit (es. if field has not been set)
			pass
	return section_list

	
@login_required
def openSection(request, order_id, section):
	order = get_object_or_404(Ordine, pk=order_id)
	groups = request.user.groups.values_list('name',flat=True)
	if ('direzione' in groups or 'super' in groups):
		setattr(order,section+'_closed',False)						# open section
		notify_list = OrderModelVersion(order).notify_list_first_open(section,user=request.user)
		order.attesa = notify_list.waitfor							# update waitfor
		OrderModelVersion(order).setOrderStatus()					# set order status and save
	return redirect(reverse('gestione_ordini:editAdmin', kwargs={'order_id': order_id})+'#'+section)

@login_required
#def GetLastDetN(request):
def GetLatest(request, field_name):
	#return HttpResponse(Ordine.objects.latest('determ_n').determ_n)
	#return HttpResponse(getattr(Ordine.objects.latest(field_name),field_name))
	filter = {field_name + "__isnull":True}			# filter out null values
	return HttpResponse(getattr(Ordine.objects.exclude(**filter).latest(field_name),field_name))
	
@login_required
def OrderDelete(request, order_id):
	order = get_object_or_404(Ordine, pk=order_id)
	groups = request.user.groups.values_list('name',flat=True)
	if ( ((request.user == order.proponente) and order.Sez_Proposta_closed == False)
		or 'direzione' in groups
		or 'super' in groups):
		order.delete()
		#message = 'Ordine eliminato'
		return redirect('../../')
	#message = "Non è stato possibile eliminare l'ordine"
	#return redirect('gestione_ordini:OrderChange', order_id)
	return redirect('../../' + order_id)

	
@login_required
def OrderCancel(request, order_id):
	order = get_object_or_404(Ordine, pk=order_id)
	groups = request.user.groups.values_list('name',flat=True)
	if (('direzione' in groups) or ('super' in groups)):
		order.order_status = 'CANC'
		order.order_closed = True
		order.save()
		#message = 'Ordine impostato come "cancellato"'
		return redirect(reverse('gestione_ordini:editAdmin', kwargs={'order_id': order_id})+'#'+'Sez_cancellato')
	#message = "Non è stato possibile cancellare l'ordine"
	return redirect(reverse('gestione_ordini:edit', kwargs={'order_id': order_id}))
	
	
@login_required
def OrderFollow(request, order_id, **kwargs):
	order = get_object_or_404(Ordine, pk=order_id)
	if kwargs.get('follow'):
		request.user.profilo.ordini_seguiti.add(order)
	else:
		request.user.profilo.ordini_seguiti.remove(order)
	return HttpResponse('')
	
	
@login_required
def OrderAddfile(request, order_id, section, **kwargs):
	order = get_object_or_404(Ordine, pk=order_id)
	message = ''
	# if POST request
	if request.method == 'POST':
		if hasattr(request,'FILES'):
			form = forms.AddfileForm(request.POST, request.FILES, instance=order)
			if form.is_valid():
				editable_sections = CheckSection(order,request.user)
				if section in editable_sections:
					file = File(order = order, file = request.FILES['file'], description = form.cleaned_data['description'], 
					section =	section)
					file.save()
					return redirect(reverse('gestione_ordini:edit', kwargs={'order_id': order_id})+'#'+file.section)
				else:
					message='Non puoi allegare file a questa sezione.'
			else:
				message='Dati non validi.\n'
				print(str(form.errors))
		else:
			message='Seleziona un file.'
	# if a GET (or any other method)
	form = forms.AddfileForm()
	return render(request, 'ordini/addfile.html', {'order': order, 'form': form, 'section':	section, 'sec_label': kwargs['sec_label'], 'error_message': message})


@login_required
def OrderDeletefile(request, order_id, file_id):
	file = get_object_or_404(File, pk=file_id)
	order = get_object_or_404(Ordine, pk=order_id)
	#username = request.user.get_username()
	editable_sections = CheckSection(order,request.user)
	if file.section in editable_sections:
		file.delete()
	return redirect(reverse('gestione_ordini:edit', kwargs={'order_id': order_id}))

	
@login_required
def VerifyAttachment(request, order_id, section):
	if File.objects.filter(order_id=order_id,section=section):	# check if there is any attachment to the section
		return HttpResponse('True')
	else:
		return HttpResponse('False')

@login_required
def OrderSearch(request):
	post_field = request.POST.getlist('field')
	post_value = request.POST.getlist('value')
	search = generic()						# save search data from request
	search.field_names = json.dumps(post_field)
	search.field_values = json.dumps(post_value)
	search.followed = request.POST.get('filter_followed', 'false')
	search.open = request.POST.get('filter_includeClosed', 'false')
	search.mine = request.POST.get('filter_mine', 'false')
	search.fields_number = request.POST.get('fields_number', 1)
	search.range = range(int(search.fields_number)) 
	pairs = dict(zip(post_field, post_value))	# assemble a field-velue dictionary
	#orders_list = Ordine.objects.all()
	filters = dict()
	for field,value in pairs.items():
		field_parts = field.split('__')
		field_type = Ordine._meta.get_field(field_parts[0]).get_internal_type()
		if field_type == 'CharField' or field_type == 'TextField':
			filter = field + '__icontains'
		if field_type == 'DateField':
			filter = field + '__gte'
			try:
				date_range = value.split('-',1)				# try to get the value as a date range
				if len(date_range) == 2:
					date_first = datetime.datetime.strptime(date_range[0].strip(), '%d/%m/%Y').strftime('%Y-%m-%d')		# convert date format and eliminate leading and ending spaces
					date_last = datetime.datetime.strptime(date_range[1].strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
					value = date_first
					filters[field + '__lte'] = date_last	# set an additional filter to get dates in given range
				else:										# try to get the value as a single date
					value = datetime.datetime.strptime(value.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
			except ValueError:
				value = '1970-01-01'						# if invalid get all dates after 01/01/1970
		#elif field_type == 'ForeignKey':
		else:
			filter = field + '__icontains'
		#elif field_type == django.db.models.fields.related.ReverseSingleRelatedObjectDescriptor:
		#	filter = field_str + '__username__icontains'
		filters[filter]=value

		#orders_list = orders_list.filter(**{ filter: value})
	#import pdb; pdb.set_trace()
	if request.POST.getlist('filter_followed'):									# if followed filter is active
		orders_list = request.user.profilo.ordini_seguiti.filter(**filters)		# the query is made on the ordini_seguiti subset
	else:
		orders_list = Ordine.objects.filter(**filters)							# else the query is made on all the Ordine objects
	if not request.POST.getlist('filter_includeClosed'):
		orders_list = orders_list.filter(order_closed=False)
	if request.POST.getlist('filter_mine'):
		from django.db.models.deletion import Collector
		from django.contrib.admin.util import NestedObjects
		collector = NestedObjects(using="default") 								# use default database
		user_filt = User.objects.filter(id=request.user.id)						# a filter selection is needed
		collector.collect(user_filt) 											# set of related objects
		#orders_list = collector.data[Ordine].intersection(orders_list)			# get related objects of type Ordine (type set)
		rel_data = collector.data.get(Ordine,None)								# get related objects of type Ordine (type set)
		if rel_data:
			orders_list = rel_data.intersection(orders_list)			# get related objects of type Ordine (type set)
		else:
			orders_list = None
	for o in orders_list:
		if o in request.user.profilo.ordini_seguiti.all():
			o.followed = True
		else:
			o.followed = False
	return render(request, 'ordini/index.html', {'orders_list': orders_list, 'last_search': search})


def mergeRotateAroundPointPage(page, page2, rotation, tx, ty):
	import math
	from PyPDF2 import utils
	translation = [[1, 0, 0],
				   [0, 1, 0],
				   [-tx,-ty,1]]
	rotation = math.radians(rotation)
	rotating = [[math.cos(rotation), math.sin(rotation),0],
				[-math.sin(rotation),math.cos(rotation), 0],
				[0,				  0,				  1]]
	rtranslation = [[1, 0, 0],
				   [0, 1, 0],
				   [tx,ty,1]]
	ctm = utils.matrixMultiply(translation, rotating)
	ctm = utils.matrixMultiply(ctm, rtranslation)

	return page.mergeTransformedPage(page2, [ctm[0][0], ctm[0][1],
											 ctm[1][0], ctm[1][1],
											 ctm[2][0], ctm[2][1]])


@login_required
def loadFunds(request, order_id):
	""" Carica la tabella fondi da un file csv. Permette quindi di selezionarne uno e carica i dati nel DB"""
	import os,csv#,urllib2
	try:
		import urllib.request as urllib2
	except ImportError:
		import urllib2
	key = request.GET.get('key','')
	funds_list = list()
	#with open(os.path.join(os.path.dirname(__file__), 'static','data','fondi.csv')) as f:
	if settings.DEVELOPMENT:
		f = open(os.path.join(os.path.dirname(__file__), 'static','data','fondi_out.csv'),'br')
	else:
		f = urllib2.urlopen("YOUR_LINK_TO_fondi.csv")
	reader = UnicodeReader(f, delimiter=';', quoting=csv.QUOTE_NONE)
	for row in reader:
		if row:
			funds_list.append(row)
	for fund in funds_list:
		for element in fund:
			loc = fund.index(element)
			fund[loc] = element.strip()			# remove white spaces
	head = funds_list[0]
	funds_list.pop(0)
	if key:										# if a fund has been selected
		for fund in funds_list:
			if fund[0] == key:
				user_groups = request.user.groups.values_list('name',flat=True)
				order = get_object_or_404(Ordine, pk=order_id)
				if ('direzione' in user_groups or 'super' in user_groups) \
					and not order.Sez_sceltaFondi_closed :
					order.CRA = fund[0]
					order.CUP = fund[2]
					order.save()
					return HttpResponse("<script>alert('Dati salvati nel database.');window.close();window.onunload=refreshParent();function refreshParent(){window.opener.location.reload();}</script>")
				else:	
					return HttpResponse("<script>alert('Accesso al database negato.');window.close();</script>")
		return HttpResponse('Codice '+key+' non trovato.')
	else:
		return render(request, 'ordini/funds.html', {'head': head, 'funds_list': funds_list})


import csv, codecs #,cStringIO

class UTF8Recoder:
	"""
	Iterator that reads an encoded stream and reencodes the input to UTF-8
	"""
	def __init__(self, f, encoding):
		self.reader = codecs.getreader(encoding)(f)
	def __iter__(self):
		return self
	def __next__(self):
		return next(self.reader)
	def next(self):			# for python 2.7 compatibility
		return self.__next__().encode("utf-8")

		
class UnicodeReader:
	"""
	A CSV reader which will iterate over lines in the CSV file "f",
	which is encoded in the given encoding.
	"""
	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		f = UTF8Recoder(f, encoding)
		self.reader = csv.reader(f, dialect=dialect, **kwds)
	def __next__(self):
		row = next(self.reader)
		return [s for s in row]
	def next(self):			# for python 2.7 compatibility
		return self.__next__()
	def __iter__(self):
		return self

		
@login_required
def OrderPdf(request, order_id, type):
	from gestione_ordini.pdfCreate import pdfCreate
	pdfCreate(request, order_id, type)
	return redirect(reverse('servefile', kwargs={'path':'pdf_output_django.pdf'}))
	
	
def date2str(obj):
	if obj:
		return obj.strftime('%d/%m/%Y')
	else:
		return ''
def user2str(obj):
	if obj:
		return obj.get_full_name()
	else:
		return ''

class OrderModelVersion():
	''' Here are defined all the differerent Order versions '''
	def __init__(self, order, *args, **kwargs):
		self.order = order
		vers = order.versione_procedura
		################## CHANGE THIS LIST TO ADD VERSIONS ##################
		if vers == '4':
			if order.gara:
				forms_list = [forms.PropostaForm, forms.sceltaFondi, forms.Impegno, forms.Determina, forms.CIG, forms.Ordine_Gara_RUP, forms.Verifiche_Ammin, forms.Determina_sc, forms.Controllo_Verifiche, forms.Ordine_Diretto_Amministr, forms.Ordine_Diretto_Direzione, forms.collaudo, forms.fattura, forms.dopo_consegna]
			else:
				forms_list = [forms.PropostaForm, forms.sceltaFondi, forms.Impegno, forms.Determina, forms.CIG, forms.Ordine_Diretto_RUP, forms.Verifiche_Ammin, forms.Determina_sc, forms.Controllo_Verifiche, forms.Ordine_Diretto_Amministr, forms.Ordine_Diretto_Direzione, forms.collaudo, forms.fattura, forms.dopo_consegna]
				
			if order.resp_fondi:			# se è indicato un responsabile fondi e non è il direttore:
				if not 'direzione' in order.resp_fondi.groups.values_list('name',flat=True):
					forms_list.insert(forms_list.index(forms.Impegno),forms.Resp_fondiForm)	# add form 'Resp_fondiForm' before 'impegno'
			
			if not order.mepa:
				forms_list.insert(forms_list.index(forms.collaudo),forms.invio_ordine_RUP)	# add form 'invio_ordine_RUP' before 'collaudo'
				if True:	# Sezione bollo SEMPRE #order.bollo_no_mepa:		# se il bollo è richiesto anche fuori MEPA aggiunge la sezione
					forms_list.insert(forms_list.index(forms.Ordine_Diretto_Amministr),forms.Impegno_Bollo)	# add form 'Impegno_Bollo' before 'Ordine_Diretto_Amministr'
			else:
				forms_list.insert(forms_list.index(forms.Ordine_Diretto_Amministr),forms.Impegno_Bollo)	# add form 'Impegno_Bollo' before 'Ordine_Diretto_Amministr'
				forms_list.insert(forms_list.index(forms.collaudo),forms.Ordine_Diretto_PuntoOrd)	# add form 'PuntoOrdinante' before 'collaudo'
			if order.tipologia == 'INV':	# se inventariabile aggiunge la sezione "buono di carico"
				forms_list.insert(forms_list.index(forms.dopo_consegna),forms.buono_carico)	# add form 'buono_carico' before 'dopo_consegna'
			if (order.order_status == 'CANC'):
				forms_list.append(forms.cancellato)
		
		if vers == '3':
			if order.gara:
				forms_list = [forms.PropostaForm, forms.sceltaFondi, forms.Impegno, forms.Determina, forms.CIG, forms.Ordine_Gara_RUP, forms.Ordine_Diretto_Amministr, forms.Ordine_Diretto_Direzione, forms.collaudo, forms.dopo_consegna]
			else:
				forms_list = [forms.PropostaForm, forms.sceltaFondi, forms.Impegno, forms.Determina, forms.CIG, forms.Ordine_Diretto_RUP, forms.Ordine_Diretto_Amministr, forms.Ordine_Diretto_Direzione, forms.collaudo, forms.dopo_consegna]
			if not order.mepa:
				forms_list.insert(forms_list.index(forms.collaudo),forms.invio_ordine_RUP)	# add form 'invio_ordine_RUP' before 'collaudo'
			else:
				forms_list.insert(forms_list.index(forms.Ordine_Diretto_Amministr),forms.Impegno_Bollo)	# add form 'Impegno_Bollo' before 'Ordine_Diretto_Amministr'
				forms_list.insert(forms_list.index(forms.collaudo),forms.Ordine_Diretto_PuntoOrd)	# add form 'PuntoOrdinante' before 'collaudo'
			if (order.order_status == 'CANC'):
				forms_list.append(forms.cancellato)

		if vers == '2':
			if order.gara:
				forms_list = [forms.PropostaForm, forms.sceltaFondi, forms.Impegno, forms.Determina, forms.CIG, forms.Ordine_Gara_RUP, forms.Ordine_Diretto_Amministr, forms.Ordine_Diretto_Direzione, forms.collaudo, forms.dopo_consegna]
			else:
				forms_list = [forms.PropostaForm, forms.sceltaFondi, forms.Impegno, forms.Determina, forms.CIG, forms.Ordine_Diretto_RUP, forms.Ordine_Diretto_Amministr, forms.Ordine_Diretto_Direzione, forms.collaudo, forms.dopo_consegna]
				if not order.mepa:
					forms_list.insert(forms_list.index(forms.collaudo),forms.invio_ordine_RUP)	# add form 'invio_ordine_RUP' before 'collaudo'
				else:
					forms_list.insert(forms_list.index(forms.collaudo),forms.Ordine_Diretto_PuntoOrd)	# add form 'PuntoOrdinante' before 'collaudo'
			if (order.order_status == 'CANC'):
				forms_list.append(forms.cancellato)

		if vers == '1':
			if order.gara:
				forms_list = [forms.PropostaForm, forms.Resp_uffForm, forms.Resp_fondiForm, forms.Scelta_RUP, forms.CIG, forms.Impegno, forms.scelta_gara, forms.Ordine_Gara_RUP, forms.Ordine_Diretto_Direzione, forms.Ordine_Diretto_Amministr, forms.collaudo, forms.dopo_consegna]
			else:
				forms_list = [forms.PropostaForm, forms.Resp_uffForm, forms.Resp_fondiForm, forms.Scelta_RUP, forms.CIG, forms.Impegno, forms.scelta_gara, forms.Ordine_Diretto_RUP, forms.Ordine_Diretto_Direzione, forms.Ordine_Diretto_Amministr, forms.collaudo, forms.dopo_consegna]
				if not order.mepa:
					forms_list.insert(forms_list.index(forms.collaudo),forms.invio_ordine_RUP)	# add form 'invio_ordine' before 'collaudo'
				else:
					forms_list.insert(forms_list.index(forms.collaudo),forms.Ordine_Diretto_PuntoOrd)	# add form 'PuntoOrdinante' before 'collaudo'
		if vers == '0':
			forms_list = [forms.PropostaForm0, forms.AutorizzForm0, forms.AmministrForm0]
		######################################################################
		self.forms_list = forms_list
		self.sections_forms = OrderedDict()
		self.incharge = list()
		self.notifyto = list()
		for form in forms_list:
			self.sections_forms[form.section] = form				# create dictionary sections - forms
			for incharge in form.incharge:							# create list sections - persons in charge
				self.incharge.append((form.section, incharge))
			try:
				for notifyto in form.notifyto:							# create list sections - persons to be notified when the section is closed
					self.notifyto.append((form.section, notifyto))
			except AttributeError:
				pass
			#dbg()


	def setOrderStatus(self):
		order = self.order
		if (not order.order_status == 'CANC'):
			for form in self.forms_list:
				if getattr(order,form.section+'_closed'):
					if getattr(form,'stateChange',False):
						order.order_status = form.stateChange
						if (form.stateChange == 'CLSD'):
							order.order_closed = True
						else:
							order.order_closed = False
				else: 
					break
		order.save()
	
	
	def get_prev_sect(self,section):								# get previous section name
		sect_list = list()
		for k,v in self.sections_forms.items():
			sect_list.append(k)
		try:
			idx = sect_list.index(section)
		except ValueError:
			return ''
		if idx == 0:
			return ''
		else:
			return sect_list[idx-1]
	def get_next_sect(self,section):								# get next section name
		sect_list = list()
		for k,v in self.sections_forms.items():
			sect_list.append(k)
		try:
			idx = sect_list.index(section)
		except ValueError:
			return ''
		if len(sect_list)>idx-1:
			return sect_list[idx+1]
		else:
			return ''
	def get_incharge_curr(self,section):							# get current section persons in charge
		incharge = list()
		for sect, inch in self.incharge:
			if sect == section:
				incharge.append(inch)
		return incharge
	def get_incharge_prev(self,section):							# get previous section persons in charge
		return self.get_incharge_curr(self.get_prev_sect(section))
	def get_incharge_next(self,section):							# get next section persons in charge
		return self.get_incharge_curr(self.get_next_sect(section))
	def get_incharge_first_open(self):
		for k,v in self.sections_forms.items():
			if not getattr(self.order, k+'_closed'):
				return self.get_incharge_curr(k)
		return ''
	def generate_list(self,incharge_list,**kwargs):								# generate the list of people for the notification
		curruser = kwargs.get('user',None)
		notify_list = generic()
		notify_list.str = ''
		notify_list.strfoll = ''
		emails_set = set()
		for incharge in incharge_list:
			print('incharge: ' + incharge)
			if incharge.startswith('group_'):
				print('isGroup')
				group_name = incharge.replace('group_','')
				notify_list.str += group_name + ', '			# if group append group name
				for usr in Group.objects.get(name=group_name).user_set.all():
					if (curruser != usr):										# skip current user for email notification
						emails_set.add(usr.email)
			else:
				try:
					inchusr = User.objects.get(username=incharge)				# verifiy if given incharge is a username
					print('isUsername')
				except(ObjectDoesNotExist):
					inchusr = getattr(self.order,incharge)						# if not username check if is a order field (es. RUP)
					print('isRole')
				if inchusr:				# it may be None if no one is assigned to a role
				#print(inchusr)
					notify_list.str += inchusr.get_full_name() + ', '			# if user append full name
					if (curruser != inchusr):									# skip current user for email notification
						emails_set.add(inchusr.email)
			print(notify_list.str)
		for usr_profile in self.order.profilo_set.all():						# add users that follow the order
			notify_list.strfoll += usr_profile.full_name
			emails_set.add(usr_profile.user.email)
		if self.order.RUP:														# RUP is always notyfied...
			notify_list.strfoll += self.order.RUP.get_full_name()
			if (curruser != self.order.RUP):									# ... unless he is closing the section
				emails_set.add(self.order.RUP.email)
				print ('RUP: ' + str(self.order.RUP))
		notify_list.emails = list(emails_set)
		notify_list.str = notify_list.str[0:-2]									# delete trailing comma and space
		return notify_list
	def notify_list_prev(self,section,**kwargs):
		incharge_list = self.get_incharge_prev(section)
		notify_list = self.generate_list(incharge_list,**kwargs)
		notify_list.waitfor = notify_list.str
		return notify_list
	def notify_list_first_open(self,section,**kwargs):
		incharge_list = self.get_incharge_first_open()
		notifyto = list()										# add people of the notifyto form property
		for sect, notiTo in self.notifyto:
			if sect == section:
				notifyto.append(notiTo)
		#notifyto += incharge_list
		notify_list = self.generate_list(incharge_list,**kwargs)
		#print notify_list.emails
		notify_list.waitfor = notify_list.str
		#for element in notifyto:
		#	print('notifyto: ' + element)
		notifyOnly = self.generate_list(notifyto,**kwargs)
		#print notifyOnly.emails
		if notifyOnly:
			notify_list.emails  += notifyOnly.emails
			notify_list.emails = list(set(notify_list.emails))	# converting back and forth to 'set' eliminates duplicates
			notify_list.str  += ', ' + notifyOnly.str
		return notify_list
	
	
def dbg():
	pdb.set_trace()					# debugger
	
class generic(object):				# class definition for a generic extendible object
	pass