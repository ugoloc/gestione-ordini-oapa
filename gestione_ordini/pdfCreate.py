#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
from django.conf import settings
from gestione_ordini.models import Ordine
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE, call
from datetime import datetime

import os
formsPath = os.path.join(os.path.dirname(__file__), 'static/forms/')
#formsPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'statics\\forms\\')
#formsPath = os.path.join(settings.PROJECT_ROOT, 'statics\\forms\\')

def pdfCreate(request, order_id, type):
	order = get_object_or_404(Ordine, pk=order_id)
	# ----------------------------------------------------------
	# INSERIRE QUI NUOVI MODULI
	if type == 'modulo':
		if order.gara:
			[pdf_source, data, data_ck] = ordineGara01(order)
		else:
			[pdf_source, data, data_ck] = ordineDiretto01(order)
	if type == 'determina':
		[pdf_source, data, data_ck] = determina02(order)
	if type == 'determina_contrarre':
		[pdf_source, data, data_ck] = determina_contrarre_01(order)
	if type == 'determina_aggiudicazione':
		[pdf_source, data, data_ck] = determina_aggiudicazione_01(order)
	# ----------------------------------------------------------		
		
	#scrittura file .fdf che con il contenuto del modulo pdf
	#fdf = NamedTemporaryFile(delete=False)
	fdf_source = r'fdf_source.fdf'
	fdf_source = settings.MEDIA_ROOT + fdf_source
	with open(fdf_source,'w+b') as fdf:
		try:
			fdf.write(bytes('%FDF-1.2\n%âãÏÓ\n1 0 obj << /FDF << /Fields [\n','latin-1')) #intestazione .fdf file
			for index in data:  #scrittura dei dati
				try:
					fdf.write(bytes('<</T (' + index[0] + ") /V (" + str(index[1]) + ")>>\n",'latin-1'))
				except(AttributeError):
					pass
			if data_ck:
				for index in data_ck:  #scrittura dei checkbox
					stat = '/No' if (index[1] == '/No' or not index[1]) else '/Yes'
					fdf.write(bytes('<</T (' + index[0] + ") /V " + stat + ">>\n",'latin-1'))
			fdf.write(bytes('] >> >>\nendobj\ntrailer\n<</Root 1 0 R>>\n%%EOF','latin-1'))  #scrittura coda .fdf file
			
		# python 2.7 compatibility
		except TypeError:
			fdf.write('%FDF-1.2\n%âãÏÓ\n1 0 obj << /FDF << /Fields [\n') #intestazione .fdf file
			for index in data:  #scrittura dei dati
				try:
					fdf.write('<</T (' + index[0] + ") /V (" + index[1].encode('latin-1','ignore') + ")>>\n")
				except(AttributeError):
					pass
			if data_ck:
				for index in data_ck:  #scrittura dei checkbox
					stat = '/No' if (index[1] == '/No' or not index[1]) else '/Yes'
					fdf.write('<</T (' + index[0] + ") /V " + stat + ">>\n")
			fdf.write('] >> >>\nendobj\ntrailer\n<</Root 1 0 R>>\n%%EOF')  #scrittura coda .fdf file

	#pdf_source = os.path.join(settings.MEDIA_ROOT + 'Ordine_diretto.pdf')
	#pdf_source = settings.MEDIA_ROOT+"Ordine_diretto.pdf"	
	#pdf_output = settings.MEDIA_ROOT+"pdf_output_django.pdf"
	pdf_output = r'pdf_output_django.pdf'
	pdf_output = settings.MEDIA_ROOT + pdf_output
	try:
		os.remove(pdf_output)	# delete old output
	except OSError:
		pass
	#cmd = 'pdftk.exe %s fill_form %s output %s flatten' % (pdf_source, fdf_source, pdf_output)
	cmd = 'pdftk.exe %s fill_form %s output %s' % ('"'+pdf_source+'"', fdf_source, pdf_output)
	proc = call(cmd, shell=True)
	return

	
def ordineDiretto01(order):
	pdf_source = r'Ordine_diretto_01.pdf'								# pdf form file name
	pdf_source = formsPath + pdf_source
	#raccolta dati (nella lista data) da inserire nel modulo pfd
	#suddivisione della stringa CUP in singole lettere, una per campo
	CodCupList = []
	idx = 1
	if order.CUP:
		for i in order.CUP:
			str_codiceCUP = 'CUP_' + str(idx)
			CodCupList.append([str_codiceCUP, i])
			idx += 1
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	#suddivisione della stringa codice fornitore in singole lettere, una per campo
	CodFornList = []
	idx = 1
	if order.cod_forn:
		for i in order.cod_forn:
			str_codForn = 'codForn_' + str(idx)
			CodFornList.append([str_codForn, i])
			idx += 1
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	#suddivisione del contenuto di "order.descriz" in tre campi distinti per tre distinti fields...
	#n_char = len(order.descriz)
	#len_descriz1=39   #numero max di caratteri per il campo Descrizione_1
	#len_descriz2=61   #numero max di caratteri per il campo Descrizione_2
	#len_descriz3=61   #numero max di caratteri per il campo Descrizione_3
	#order_descriz1 = order.descriz[0:len_descriz1]
	#order_descriz2 = order.descriz[len_descriz1:len_descriz1+len_descriz2]
	#order_descriz3 = order.descriz[len_descriz1+len_descriz2:len_descriz1+len_descriz2+len_descriz3]
	#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	data = [['RichAcqId', order.rich_acq_id if order.rich_acq_id else ''],   #solo i field di testo
			['Proponente', user2str(order.proponente)],
			['DataProp', date2str(order.data_prop)],
			['Tipologia', txt2str(order.get_tipologia_display())],
			['RespUfficio', user2str(order.resp_ufficio)],
			#['Descrizione_1', order_descriz1],
			#['Descrizione_2', order_descriz2],
			#['Descrizione_3', order_descriz3],
			['Descriz', txt2str(order.descriz)],
			['CostoPresunto', str(order.stima_costo)],
			['Cra', txt2str(order.CRA)],
			['FirmaRespFondi', user2str(order.Sez_Resp_fondi_closedby)],
			['DataRespFondi', date2str(order.data_firma_resp_fondi)], #order.data_firma_resp_fondi.strftime('%d/%m/%Y')],
			['FirmaRespUff', user2str(order.Sez_Resp_uff_closedby)],
			['DataRespUff', date2str(order.data_firma_resp_ufficio)], #order.data_firma_resp_ufficio.strftime('%d/%m/%Y')],
			#fine sez. 1 - Inizio sez.2
			['DetermN', txt2str(order.determ_n)],
			['DetermData', date2str(order.determ_data)], #order.determ_data.strftime('%d/%m/%Y')],
			['Rup', user2str(order.RUP)],  #<<<<<----- controllare come inserire la firma
			#['SceltaContr', order.modo_scelta_contr],
			['FunzCont', user2str(order.funz_contabile)],
			['FirmaDirettoreRup', user2str(order.Sez_Scelta_RUP_closedby)],  #<<<<<----- controllare come inserire la firma
			['DataDirettRup', date2str(order.data_firma_direttore)],  #<<<<<----- controllare come inserire la firma
			#fine sez. 2 - Inizio sez.3
			['DataCig', date2str(order.data_firma_direttore)], #order.data_firma_direttore.strftime('%d/%m/%Y')],
			['Cig', txt2str(order.CIG)],
			['DataCig', date2str(order.data_CIG)], #order.data_CIG.strftime('%d/%m/%Y')],
			['FirmaRupCig', user2str(order.Sez_CIG_closedby)],  #<<<<<----- controllare come inserire la firma
			#fine sez. 3 - Inizio sez.4
			['ImpegnoN', txt2str(order.impegno_n)],
			['Capitolo', txt2str(order.capitolo)],
			['FirmaImpegno', user2str(order.Sez_Impegno_closedby)],  #<<<<<----- controllare questo campo
			['DataFunzCont', date2str(order.data_firma_funz_contabile)], #order.data_firma_funz_contabile.strftime('%d/%m/%Y')],
			#fine sez. 4 - Inizio sez.5
			['contraente', txt2str(order.contraente)],
			['importo', txt2str(order.importo)],
			['dataCaricMepa', date2str(order.data_caric_mepa)],
			['idMepa', txt2str(order.id_mepa)],
			['dataTrasmDocAmm', date2str(order.data_trasm_doc) if order.mepa else ''],
			['dataStesuraOrd', date2str(order.data_stesura_ordine)],
			['dataTrasmDocAmm2', date2str(order.data_trasm_doc) if not order.mepa else ''],
			['firmaRupOrd', user2str(order.Sez_Ordine_Diretto_RUP_closedby)],
			['dataFirmaRupOrd', date2str(order.data_firma_RUP_ordine)],
			#Inizio sez.6
			['dataAutorizz', date2str(order.data_autorizz)],
			['firmaAutorizz', user2str(order.Sez_Autorizz_closedby)],
			['impConsN', txt2str(order.n_impegno_cons)],
			['dataImpCons', date2str(order.data_impegno_cons)],
			['dataTrasmPo', date2str(order.data_trasm_PO)],
			['firmaFunzCont', user2str(order.Sez_Ordine_Diretto_Amministr_closedby) if order.mepa else ''],
			['dataEmissOrd', date2str(order.data_ordine) if order.mepa else ''],
			['dataComunRup', date2str(order.data_comunic_RUP)],
			['dataProtOrd', date2str(order.data_ordine) if not order.mepa else ''],
			['firmaFunzCont2', user2str(order.Sez_Ordine_Diretto_Amministr_closedby) if not order.mepa else ''],
			['dataSpedOrd', date2str(order.data_spediz_ordine)],
			['firmaRupSped', user2str(order.Sez_Invio_Ordine_RUP_closedby)],
			['dataRichDurc', date2str(order.data_rich_durc)],
			#Inizio sez. 7
			['dataVerifica', date2str(order.data_verifica)],			
	]
	data.extend(CodCupList)
	data.extend(CodFornList)
	#"/No" o "/Yes" per lo stato dei checkbox
	data_ck = [['SceltaContr_ECO_ck', '/Yes' if order.modo_scelta_contr == 'ECO' else '/No'],   #solo lo stato dei checkbox
				['SceltaContr_ORD_ck', '/Yes' if order.modo_scelta_contr == 'ORD' else '/No'],
				['Mepa_SI_ck', '/Yes' if order.mepa else '/No'],
				['Mepa_NO_ck', '/Yes' if order.mepa is False else '/No'],
				['allegaRelScelta_ck', '/Yes' if order.allega_rel_scelta else '/No'],
				['caricMepa_ck', '/Yes' if order.data_caric_mepa else '/No'],
				['trasmDoc_ck', '/Yes' if order.data_trasm_doc and order.mepa else '/No'],
				['stesuraOrd_ck', '/Yes' if order.data_stesura_ordine else '/No'],
				['trasmDoc2_ck', '/Yes' if order.data_trasm_doc and not order.mepa else '/No'],
				#['compilInvent_ck', '/Yes' if order.compil_scheda_invent else '/No'],
				['impegnoCons_ck', '/Yes' if order.data_impegno_cons else '/No'],
				['trasmPo_ck', '/Yes' if order.data_trasm_PO else '/No'],
				['emissOrd_ck', '/Yes' if order.data_ordine and order.mepa else '/No'],
				['emailRup_ck', '/Yes' if order.Sez_Ordine_Diretto_Amministr_closed else '/No'],
				['protOrd_ck', '/Yes' if order.data_ordine and not order.mepa else '/No'],
				['spedOrd_ck', '/Yes' if order.data_spediz_ordine else '/No'],
				['richDurc_ck', '/Yes' if order.data_rich_durc else '/No'],
				#['ricezDurc_ck', '/Yes' if order.durc_ric else '/No'],
				#['ricezFatt_ck', '/Yes' if order.fatt_ric else '/No'],
				['verifica_ck', '/Yes' if order.data_verifica else '/No'],
				['liquidato_ck', '/Yes' if order.data_pagamento else '/No'],
	]

	return [pdf_source, data, data_ck]
	

def ordineGara01(order):
	pdf_source = r'Ordine_gara_01.pdf'									# pdf form file name
	pdf_source = formsPath + pdf_source
	
	#raccolta dati (nella lista data) da inserire nel modulo pfd
	
	#suddivisione della stringa CUP in singole lettere, una per campo
	CodCupList = []
	idx = 1
	if order.CUP:
		for i in order.CUP:
			str_codiceCUP = 'CUP_' + str(idx)
			CodCupList.append([str_codiceCUP, i])
			idx += 1
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	#suddivisione della stringa codice fornitore in singole lettere, una per campo
	CodFornList = []
	idx = 1
	if order.cod_forn:
		for i in order.cod_forn:
			str_codForn = 'codForn_' + str(idx)
			CodFornList.append([str_codForn, i])
			idx += 1
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	#suddivisione del contenuto di "order.descriz" in tre campi distinti per tre distinti fields...
	#n_char = len(order.descriz)
	#len_descriz1=39   #numero max di caratteri per il campo Descrizione_1
	#len_descriz2=61   #numero max di caratteri per il campo Descrizione_2
	#len_descriz3=61   #numero max di caratteri per il campo Descrizione_3
	#order_descriz1 = order.descriz[0:len_descriz1]
	#order_descriz2 = order.descriz[len_descriz1:len_descriz1+len_descriz2]
	#order_descriz3 = order.descriz[len_descriz1+len_descriz2:len_descriz1+len_descriz2+len_descriz3]
	#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	data = [['RichAcqId', txt2str(order.rich_acq_id)],   #solo i field di testo
			['Proponente', user2str(order.proponente)],
			['DataProp', date2str(order.data_prop)],
			['Tipologia', txt2str(order.get_tipologia_display())],
			['RespUfficio', user2str(order.resp_ufficio)],
			['Descriz', txt2str(order.descriz)],
			['CostoPresunto', txt2str(order.stima_costo)],
			['Cra', txt2str(order.CRA)],
			['FirmaRespFondi', user2str(order.Sez_Resp_fondi_closedby)],
			['DataRespFondi', date2str(order.data_firma_resp_fondi)], #order.data_firma_resp_fondi.strftime('%d/%m/%Y')],
			['FirmaRespUff', user2str(order.Sez_Resp_uff_closedby)],
			['DataRespUff', date2str(order.data_firma_resp_ufficio)], #order.data_firma_resp_ufficio.strftime('%d/%m/%Y')],
			#fine sez. 1 - Inizio sez.2
			['DetermN', txt2str(order.determ_n)],
			['DetermData', date2str(order.determ_data)], #order.determ_data.strftime('%d/%m/%Y')],
			['Rup', user2str(order.RUP)],  #<<<<<----- controllare come inserire la firma
			#['SceltaContr', order.modo_scelta_contr],
			['FunzCont', user2str(order.funz_contabile)],
			['FirmaDirettoreRup', user2str(order.Sez_Scelta_RUP_closedby)],  #<<<<<----- controllare come inserire la firma
			['DataDirettRup', date2str(order.data_firma_direttore)],  #<<<<<----- controllare come inserire la firma
			#fine sez. 2 - Inizio sez.3
			['DataCig', date2str(order.data_firma_direttore)], #order.data_firma_direttore.strftime('%d/%m/%Y')],
			['Cig', txt2str(order.CIG)],
			['DataCig', date2str(order.data_CIG)], #order.data_CIG.strftime('%d/%m/%Y')],
			['FirmaRupCig', user2str(order.Sez_CIG_closedby)],  #<<<<<----- controllare come inserire la firma
			#Inizio sez.4
			['ImpegnoN', txt2str(order.impegno_n)],
			['Capitolo', txt2str(order.capitolo)],
			['FirmaImpegno', user2str(order.Sez_Impegno_closedby)],  #<<<<<----- controllare questo campo
			['DataFunzCont', date2str(order.data_firma_funz_contabile)], #order.data_firma_funz_contabile.strftime('%d/%m/%Y')],
			#Inizio sez.5
			['rdo1', date2str(order.data_rdo) if order.mepa else ''],
			['emissRdo1', date2str(order.data_emissione_rdo) if order.mepa else ''],
			['dataValutOfferte1', date2str(order.data_valut_offerte) if order.mepa else ''],
			['importo1', txt2str(order.importo) if order.mepa else ''],
			['dataCaricMepa', date2str(order.data_caric_mepa)],
			['idMepa', txt2str(order.id_mepa)],
			['dataTrasmDocAmm1', date2str(order.data_trasm_doc) if order.mepa else ''],
			['rdo2', date2str(order.data_rdo) if not order.mepa else ''],
			['emissRdo2', date2str(order.data_emissione_rdo) if not order.mepa else ''],
			['dataValutOfferte2', date2str(order.data_valut_offerte) if not order.mepa else ''],
			['dataStesuraOrd', date2str(order.data_stesura_ordine)],
			['importo2', txt2str(order.importo) if not order.mepa else ''],
			['dataTrasmDocAmm2', date2str(order.data_trasm_doc) if not order.mepa else ''],
			['firmaRupOrd', user2str(order.Sez_Gara_RUP_closedby)],
			#Inizio sez.6
			['dataAutorizz', date2str(order.data_autorizz)],
			['firmaAutorizz', user2str(order.Sez_Autorizz_closedby)],
			['impConsN', txt2str(order.n_impegno_cons)],
			['dataImpCons', date2str(order.data_impegno_cons)],
			['dataTrasmPo', date2str(order.data_trasm_PO)],
			['firmaFunzCont', user2str(order.Sez_Ordine_Diretto_Amministr_closedby) if order.mepa else ''],
			['dataEmissOrd', date2str(order.data_ordine) if order.mepa else ''],
			#['dataComunRup', date2str(order.data_comunic_RUP)],
			['dataProtOrd', date2str(order.data_ordine) if not order.mepa else ''],
			['firmaFunzCont2', user2str(order.Sez_Ordine_Diretto_Amministr_closedby) if not order.mepa else ''],
			['dataSpedOrd', date2str(order.data_spediz_ordine)],
			['firmaRupSped', user2str(order.Sez_Invio_Ordine_RUP_closedby)],
			['dataRichDurc', date2str(order.data_rich_durc)],
			#Inizio sez. 7
			['dataVerifica', date2str(order.data_verifica)],			
	]
	data.extend(CodCupList)
	data.extend(CodFornList)
	#"/No" o "/Yes" per lo stato dei checkbox
	data_ck = [['SceltaContr_ECO_ck', '/Yes' if order.modo_scelta_contr == 'ECO' else '/No'],   #solo lo stato dei checkbox
				['SceltaContr_ORD_ck', '/Yes' if order.modo_scelta_contr == 'ORD' else '/No'],
				['Mepa_SI_ck', '/Yes' if order.mepa else '/No'],
				['Mepa_NO_ck', '/Yes' if order.mepa is False else '/No'],
				['rdo1_ck', '/Yes' if order.data_rdo and order.mepa else '/No'],
				['emissRdo1_ck', '/Yes' if order.data_emissione_rdo and order.mepa else '/No'],
				['ValutOfferte1_ck', '/Yes' if order.data_valut_offerte and order.mepa else '/No'],
				['caricMepa_ck', '/Yes' if order.data_caric_mepa else '/No'],
				['trasmDoc1_ck', '/Yes' if order.data_trasm_doc and order.mepa else '/No'],
				['rdo2_ck', '/Yes' if order.data_rdo and not order.mepa else '/No'],
				['emissRdo2_ck', '/Yes' if order.data_emissione_rdo and not order.mepa else '/No'],
				['ValutOfferte2_ck', '/Yes' if order.data_valut_offerte and not order.mepa else '/No'],
				['stesuraOrd_ck', '/Yes' if order.data_stesura_ordine else '/No'],
				['trasmDoc2_ck', '/Yes' if order.data_trasm_doc and not order.mepa else '/No'],
				#['compilInvent_ck', '/Yes' if order.compil_scheda_invent else '/No'],
				
				['impegnoCons_ck', '/Yes' if order.data_impegno_cons else '/No'],
				['trasmPo_ck', '/Yes' if order.data_trasm_PO else '/No'],
				['emissOrd_ck', '/Yes' if order.data_ordine and order.mepa else '/No'],
				#['emailRup_ck', '/Yes' if order.Sez_Ordine_Diretto_Amministr_closed else '/No'],
				['protOrd_ck', '/Yes' if order.data_ordine and not order.mepa else '/No'],
				['spedOrd_ck', '/Yes' if order.data_spediz_ordine else '/No'],
				['richDurc_ck', '/Yes' if order.data_rich_durc else '/No'],
				#['ricezDurc_ck', '/Yes' if order.durc_ric else '/No'],
				#['ricezFatt_ck', '/Yes' if order.fatt_ric else '/No'],
				['verifica_ck', '/Yes' if order.data_verifica else '/No'],
				['liquidato_ck', '/Yes' if order.data_pagamento else '/No'],
	]

	return [pdf_source, data, data_ck]
		
	
def determina01(order):
	pdf_source = r'DeterminaContrattare_01.pdf'								# pdf form file name
	pdf_source = formsPath + pdf_source
	
	#solo i field di testo
	data = [['determN', order.determ_n],  
			['determData', date2str(order.determ_data)],
			['propostaData', date2str(order.data_prop)],
			['descriz1', order.descriz],
			['descriz2', order.descriz],
			['cra', order.CRA],
			['cram', order.CRA],
			['capitolo', order.capitolo],
			['rup', user2str(order.RUP)],
			['costoPresunto1', str(order.stima_costo)],
			['costoPresunto2', str(order.stima_costo)],
	]

	#"/No" o "/Yes" per lo stato dei checkbox
	data_ck = [['sceltaContr_ECO_ck', '/Yes' if order.modo_scelta_contr == 'ECO' else '/No'],   #solo lo stato dei checkbox
			['sceltaContr_ORD_ck', '/Yes' if order.modo_scelta_contr == 'ORD' else '/No'],
	]

	return [pdf_source, data, data_ck]


def determina02(order):
	pdf_source = r'DeterminaContrattare_02.pdf'								# pdf form file name
	pdf_source = formsPath + pdf_source
	
	#solo i field di testo
	data = [['determN', order.determ_n],  
			['determData', date2str(order.determ_data)],
			#['propostaData', date2str(order.data_prop)],
			['descriz1', order.descriz],#.encode('latin-1','ignore')],
			['descriz2', order.descriz],#.encode('latin-1','ignore')],
			['obfu1', order.CRA],
			['obfu2', order.CRA],
			['capitolo', order.capitolo],
			['capitolo2', order.capitolo],
			['rup', user2str(order.RUP)],
			['costoPresunto1', order.stima_costo],#.encode('latin-1','ignore')],
			['costoPresunto2', order.stima_costo],#.encode('latin-1','ignore')],
	]

	#"/No" o "/Yes" per lo stato dei checkbox
	data_ck = [['sceltaContr_AFD_ck', '/Yes' if order.modo_scelta_contr == 'AFD' else '/No'],   #solo lo stato dei checkbox
			['sceltaContr_AMD_ck', '/Yes' if order.modo_scelta_contr == 'AMD' else '/No'],
			['sceltaContr_ORD_ck', '/Yes' if order.modo_scelta_contr == 'ORD' else '/No'],
			['sceltaContr_ALT_ck', '/Yes' if order.modo_scelta_contr == 'ALT' else '/No'],
	]

	return [pdf_source, data, data_ck]


def determina_contrarre_01(order):
	pdf_source = r'determina_contrarre_2021-01_1.pdf'								# pdf form file name
	pdf_source = formsPath + pdf_source
	
	modo_scelta = dict(order.MODO_SCELTA_CONTR_SCELTE)
	#solo i field di testo
	data = [['detnome', order.determ_n],  
			['detdata', date2str(order.determ_data)],
			['descrizione1', order.descriz],#.encode('latin-1','ignore')],
			['descrizione2', order.descriz],#.encode('latin-1','ignore')],
			['obfu1', order.CRA],
			['obfu2', order.CRA],
			['cap1', order.capitolo],
			['cap2', order.capitolo],
			['rup1', user2str(order.RUP)],
			['costo1', order.stima_costo],#.encode('latin-1','ignore')],
			['costo2', order.stima_costo],#.encode('latin-1','ignore')],
			['procedura', modo_scelta[order.modo_scelta_contr]],#.encode('latin-1','ignore')],
	]
	data_ck = None		# Nessun checkbox
	return [pdf_source, data, data_ck]


def determina_aggiudicazione_01(order):
	pdf_source = r'determina_aggiudicazione_2021-01_1.pdf'								# pdf form file name
	pdf_source = r'determina_aggiudicazione_2021-11_1.pdf'								# pdf form file name
	pdf_source = formsPath + pdf_source
	
	modo_scelta = dict(order.MODO_SCELTA_CONTR_SCELTE)
	#solo i field di testo
	data = [['aggnum', order.determ_sc_n],
			['aggdata', date2str(order.determ_sc_data)],
			['detnum', order.determ_n],  
			['detdata', date2str(order.determ_data)],
			['cap1', order.capitolo],
			['cig', order.CIG],
			['cup', order.CUP],
			['costo1', order.stima_costo],#.encode('latin-1','ignore')],
			['descrizione1', order.descriz],#.encode('latin-1','ignore')],
			['obfu1', order.CRA],
			['costofinale', order.importo],#.encode('latin-1','ignore')],
			['costofinale_2', order.importo],#.encode('latin-1','ignore')],
			['fornitore1', order.contraente],#.encode('latin-1','ignore')],
			['fornitore2', order.contraente],#.encode('latin-1','ignore')],
	]
	data_ck = None		# Nessun checkbox
	return [pdf_source, data, data_ck]


def txt2str(obj):
	if obj:
		try:
			return unicode(obj)
		except NameError:
			return str(obj)
	else:
		return ''
	
def date2str(obj):
	if obj:
		return obj.strftime('%d/%m/%Y')
	else:
		return ''
		
def user2str(obj):
	if obj and not obj is None:
		try:
			return unicode(obj.profilo)
		except NameError:
			return str(obj.profilo.full_name)
	else:
		return ''
		

def dbg():
	import pdb
	pdb.set_trace()					# debugger