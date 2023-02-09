#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm
from gestione_ordini.models import Ordine, File
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.forms.fields import Field
setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput ))

import datetime

# Create the form class.
class OrderForm(ModelForm):
	class Meta:
		model = Ordine
		#fields = ['cod_forn', 'proponente', 'tipologia', 'resp_ufficio', 'descriz']
		fields = '__all__'


class AddfileForm(ModelForm):
	class Meta:
		model = File
		fields = ['file', 'description'] 
		labels = {
			'file': '',
			'description': 'Descrizione (obbligatoria) ',
		}
	

class PropostaForm(ModelForm):		#V1,V2
	section = 'Sez_Proposta'
	sec_label = 'PROPOSTA: a cura del Proponente / Responsabile ufficio'
	sec_short_label = 'Proposta'
	first_section = True
	incharge = ['proponente']
	notes = ['(1) opzionale']
	stateChange = 'OPEN'
	class Meta:
		model = Ordine
		fields = ['id','data_prop','richiesto_da','tipologia','resp_ufficio','descriz','stima_costo','dest_ricerca','note_proposta','Sez_Proposta_closed'] 
		initial = {
			'data_prop': datetime.date.today()
		}
		labels = {
			'id': 'ID procedura',
			'data_prop': 'Data proposta', 
			'richiesto_da': 'Acquisto richiesto da (1)',
			'tipologia': 'Tipologia acquisto', 
			'resp_ufficio': "Responsabile dell'Ufficio", 
			'descriz': 'Descrizione del bene/servizio (con motivazione o scopo)', 
			'stima_costo': 'Costo presunto (IVA esclusa)', 
			'dest_ricerca': 'Bene o servizio funzionalmente destinato alla ricerca',
			'note_proposta': 'Note (con eventuale suggerimento su funzione obiettivo e su modalità di scelta del contraente)',
		}		
	def __init__(self, *args, **kwargs):
		super(PropostaForm, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs) #assign a unique id to each element
		self.fields['resp_ufficio'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)

		
class Resp_fondiForm(ModelForm):		#V1
	section = 'Sez_Resp_fondi'
	sec_label = 'AUTORIZZAZIONE DEI FONDI: a cura del responsabile dei Fondi'
	sec_short_label = 'Autorizzazione fondi'
	incharge = ['resp_fondi']
	class Meta:
		model = Ordine
		fields = ['resp_fondi_autorizza','data_firma_resp_fondi','note_resp_fondi', 'Sez_Resp_fondi_closed'] 
		labels = {
			'resp_fondi_autorizza': "Autorizza",
			'data_firma_resp_fondi': 'Data di autorizzazione',
			'note_resp_fondi': "Note",
		}
			
			
class Resp_uffForm(ModelForm):		#V1
	section = 'Sez_Resp_uff'
	sec_label = 'A cura del Responsabile Ufficio'
	sec_short_label = 'Resp. ufficio'
	incharge = ['resp_ufficio']
	links = [('Elenco CRA e CUP dei progetti attivi','LINK')]
	class Meta:
		model = Ordine
		fields = [ 'CRA', 'CUP', 'resp_fondi', 'data_firma_resp_ufficio', 'Sez_Resp_uff_closed'] 
		labels = {
			'CRA': 'Fondi (CRA)', 
			'CUP': 'CUP', 
			'resp_fondi': 'Responsabile fondi',
			'data_firma_resp_ufficio': 'Data di autorizzazione',
		}	
	def __init__(self, *args, **kwargs):
		super(Resp_uffForm, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['resp_fondi'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)


class sceltaFondi(ModelForm):		#V2
	section = 'Sez_sceltaFondi'
	sec_label = "Scelta dei fondi e indicazione del responsabile dell'istruttoria/RUP: a cura della Direzione"
	sec_short_label = 'Scelta fondi e RUP'
	incharge = ['group_direzione']
	notifyto = ['resp_fondi','RUP']
	attach = "attachReq"
	links = [('Elenco Ob.Fu. e CUP dei progetti attivi (prima salvare la sezione)','funds')]
	#notes = ['']
	class Meta:
		model = Ordine
		fields = ['RUP', 'resp_fondi', 'CRA', 'CUP', 'funz_contabile', 'data_sceltaFondi', 'note_sceltaFondi', 'Sez_sceltaFondi_closed'] 
		labels = {
			'RUP': 'Responsabile Unico del Procedimento (RUP)', 
			'resp_fondi': 'Responsabile fondi',
			'CRA': 'Fondi (Ob.Fu.)', 
			'CUP': 'CUP', 
			'funz_contabile': 'Funzionario Contabile addetto', 
			'data_sceltaFondi': 'Data', 
			'note_sceltaFondi': 'Note',
		}	
	def __init__(self, *args, **kwargs):
		super(sceltaFondi, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['RUP'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
		self.fields['resp_fondi'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)		
		self.fields['funz_contabile'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)		
		

class Impegno(ModelForm):		#V1, V2
	section = 'Sez_Impegno'
	sec_label = "PRENOTAZIONE IMPORTO: a cura del Funzionario Contabile"
	sec_short_label = 'Prenotaz. importo'
	incharge = ['funz_contabile']
	#links = [('Ultimo id di richiesta acquisto', '/gestione_ordini/latest/rich_acq_id', 'infolink')]
	class Meta:
		model = Ordine
		fields = ['rich_acq_id', 'capitolo', 'tipologia', 'data_firma_funz_contabile', 'note_prenotazione', 'Sez_Impegno_closed'] 
		labels = {
			'rich_acq_id': "ID richiesta motivata d'acquisto",
			'capitolo': 'Capitolo',
			'tipologia': 'Tipologia acquisto', 
			'data_firma_funz_contabile': 'Data',
			'note_prenotazione': 'Note',
        }	

		
class Determina(ModelForm):		#V2
	section = 'Sez_Determina'
	sec_label = 'DETERMINA A CONTRARRE: a cura della Direzione'
	sec_short_label = 'Determina a Contrarre'
	incharge = ['group_direzione']
	notifyto = ['resp_fondi']
	attach = "attachReq"
	links = [('Ultimo numero di determina', '/gestione_ordini/latest/determ_n', 'infolink'), 
				('Genera PDF (prima salvare la sezione)','pdfDetermina')]
	notes = ['Allegato richiesto: determina a contrarre o nulla (se si sceglie la determina unica semplificata)']
	class Meta:
		model = Ordine
		fields = ['determ_n', 'determ_data', 'modo_scelta_contr', 'data_firma_direttore', 'note_determina','Sez_Determina_closed'] 
		labels = {
			'determ_n': 'Determina a contrattare n.', 
			'determ_data': 'Data determina', 
			'modo_scelta_contr': 'Modalità di scelta del contraente',
			'data_firma_direttore': 'Data', 
			'note_determina': 'Note',
		}	
	def __init__(self, *args, **kwargs):
		super(Determina, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)	

class Determina_sc(ModelForm):		#V2
	section = 'Sez_Determina_sc'
	sec_label = 'DETERMINA DI AGGIUDICAZIONE o Determina a contrarre semplificata, a cura della Direzione'
	sec_short_label = 'Determina di Aggiudicazione'
	incharge = ['group_direzione']
	notifyto = ['resp_fondi']
	attach = "attachReq"
	links = [('Genera PDF (prima salvare la sezione)','pdfDeterminaSC')]
	notes = ['Allegato richiesto: determina']
	class Meta:
		model = Ordine
		fields = ['determ_sc_n', 'determ_sc_data', 'data_firma_direttore_sc', 'note_determina_sc','Sez_Determina_sc_closed'] 
		labels = {
			'determ_sc_n': 'Determina n.', 
			'determ_sc_data': 'Data determina', 
			'data_firma_direttore_sc': 'Data', 
			'note_determina_sc': 'Note',
		}	
	def __init__(self, *args, **kwargs):
		super(Determina_sc, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)	


class Scelta_RUP(ModelForm):		#V1
	section = 'Sez_Scelta_RUP'
	sec_label = 'DETERMINA: a cura della Direzione'
	sec_short_label = 'Determina'
	incharge = ['group_direzione']
	notifyto = ['resp_fondi']
	attach = "attachReq"
	links = [('Ultimo numero di determina', '/gestione_ordini/latest/determ_n', 'infolink'), ('Genera PDF (prima salvare la sezione)','pdfDetermina')]
	notes = ['Allegato richiesto: scansione della determina']
	class Meta:
		model = Ordine
		fields = ['determ_n', 'determ_data', 'RUP', 'modo_scelta_contr','capitolo','funz_contabile', 'data_firma_direttore', 'Sez_Scelta_RUP_closed'] 
		labels = {
            'determ_n': 'Determina a contrattare n.', 
			'determ_data': 'Data determina', 
			'RUP': 'Responsabile Unico del Procedimento (RUP)', 
			'modo_scelta_contr': 'Modalità di scelta del contraente',
			'capitolo': 'Capitolo', 
			'funz_contabile': 'Funzionario Contabile addetto', 
			'data_firma_direttore': 'Data', 
        }	
	def __init__(self, *args, **kwargs):
		super(Scelta_RUP, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['RUP'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)		
		self.fields['funz_contabile'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)
		
		
class CIG(ModelForm):		#V1
	section = 'Sez_CIG'
	sec_label = 'CIG: a cura del RUP'
	sec_short_label = 'CIG'
	incharge = ['RUP']
	attach = "attachReq"
	links = [('Per ordini sotto 40.000 euro, si consiglia di usare lo SmartCIG (click qui)','https://smartcig.anticorruzione.it/AVCP-SmartCig/')]
	notes = ['Allegato richiesto: schermata AVCP di avvenuta assegnazione']
	class Meta:
		model = Ordine
		fields = ['CIG', 'data_CIG', 'gara', 'Sez_CIG_closed'] 
		labels = {
            'CIG': 'CIG',
			'data_CIG': 'Data acquisizione CIG',
			'gara': 'Ordine con svolgimento di gara'
        }	

		
class scelta_gara(ModelForm):		# V1 (si può eliminare riordinando le sezioni)
	section = 'Sez_scelta_gara'
	sec_label = "SCELTA DEL CONTRAENTE (affidamento diretto o gara): a cura del RUP"
	sec_short_label = 'Scelta contraente'
	incharge = ['RUP']
	class Meta:
		model = Ordine
		fields = ['gara', 'Sez_scelta_gara_closed'] 
		labels = {
            'gara': 'Ordine con svolgimento di gara', 
        }	
		

class Ordine_Diretto_RUP(ModelForm):
	section = 'Sez_Ordine_Diretto_RUP'
	sec_label = "AFFIDAMENTO DIRETTO: a cura del RUP"
	sec_short_label = "Affid. diretto (RUP)"
	incharge = ['RUP']
	attach = "attachReq"
	links = [('Relazione di scelta del contraente','LINK'),
			('Dichiarazione assolvimento imposta di bollo', 'LINK'),
			("Dichiarazione requisiti generali art 80", "LINK"),
			('Dichiarazione sostitutiva "Conto Dedicato"', "LINK"),]
	notes = ["1: Verificare che l'importo non sia superiore all'importo indicato in determina\n\n","Allegati richiesti:\n- ordine o bozza ordine MEPA\n- relazione su scelta fornitore contenente informazioni riguardo la procedura comparativa effettuata nonche' la dichiarazione se si e' rispettato o no il principio di rotazione (in caso negativo, relazionare sulle motivazioni, solo sommariamente in caso di importi inferiori a 1000 euro, dettagliatamente negli altri casi).\n- Dichiarazione del fornitore dalla quale risulti il possesso dei requisiti di carattere generale di cui all'Art. 80 del Codice dei contratti pubblici, da sollecitare anche tramite email  (v. link in alto).\n- Dichiarazione sostitutiva 'Conto Dedicato' debitamente compilata dal fornitore (vedasi Circolare del Direttore 'Disposizioni riguardanti il ricorso al MEPA e richiesta di conto dedicato', prot. n. 624 del 6.9.2019)\n- (SOLO PER ORDINI MEPA) Dichiarazione del fornitore sull'assolvimento dell'imposta di bollo, da sollecitare anche tramite email (v. link in alto).",
	"Questa sezione non verra' accettata in caso di allegati mancanti, incompleti o lacunosi sui punti sopracitati"] 
	class Meta:
		model = Ordine
		fields = ['contraente', 'importo', 'verifica_CIG', 'allega_rel_scelta', 'operatori', 'mepa', 'data_caric_mepa', 'id_mepa','bollo_no_mepa', 'data_stesura_ordine', 'data_firma_RUP_ordine', 'Sez_Ordine_Diretto_RUP_closed'] 
		labels = {
            'contraente': 'Contraente', 
			#'importo': 'Importo (IVA esclusa)', 
			'importo': mark_safe('Importo (IVA esclusa)<sup>1</sup>'),
			'verifica_CIG': 'Verifica importo CIG',
			'allega_rel_scelta': 'Si allega relazione su scelta fornitore', 
			'operatori':"Elenco degli operatori invitati/numero di offerte",
			'mepa': 'MEPA', 
			'data_caric_mepa': 'Data di caricamento ordine su carrello MEPA', 
			'id_mepa': 'Codice identificativo su MEPA',
			'bollo_no_mepa': 'Imposta di bollo su ordini non MEPA (ad es. contratti con privati)',
			'data_stesura_ordine': 'Data di stesura ordine cartaceo',
			'data_firma_RUP_ordine': 'Data',
        }	
	def __init__(self, *args, **kwargs):
		super(Ordine_Diretto_RUP, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['data_caric_mepa'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[true]'})
		self.fields['id_mepa'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[true]'})
		self.fields['bollo_no_mepa'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[false]'})
		self.fields['data_stesura_ordine'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[false]'})
		self.fields['mepa'].widget.attrs.update({'class':'trigger'})
		
	#def clean(self):
	#	if self.cleaned_data['importo'] > self.cleaned_data['stima_costo']:
	#		msg = "L'importo non può essere maggiore dell'importo indicato nella determina."
	#		self._errors['importo'] = ErrorList([msg])
	#		del self.cleaned_data['importo']
	#	return self.cleaned_data
		
class Ordine_Gara_RUP(ModelForm):
	section = 'Sez_Gara_RUP'
	sec_label = "ORDINE CON SVOLGIMENTO GARA: a cura del RUP in collaborazione con P.I. e P.O."
	sec_short_label = "Gara (RUP)"
	incharge = ['RUP', 'group_punto_ordinante']
	attach = "attachReq"
	notes = ['Allegato richiesto: ordine (se fuori MEPA), schermata CIG se modificato']
	class Meta:
		model = Ordine
		fields = ['mepa', 'data_rdo', 'data_emissione_rdo', 'data_valut_offerte', 'contraente', 'importo','operatori','verifica_CIG', 'data_caric_mepa', 'data_stesura_ordine', 'data_trasm_doc', 'data_firma_RUP_ordine', 'Sez_Gara_RUP_closed'] 
		labels = {
			'mepa': 'MEPA',
			'data_rdo': "Data di predesposizione RdO",
			'data_emissione_rdo': "Data emissione/protocollo e spedizione RdO",
			'data_valut_offerte': "Data apertura buste, valutazione offerte e verbale delle operazioni",
            'contraente': 'Contraente', 
			'importo': 'Importo (IVA esclusa)',
			'operatori':"Elenco degli operatori invitati/numero di offerte",			
			'verifica_CIG': 'Verifica importo CIG',
			'data_caric_mepa': 'Data di caricamento ordine su carrello MEPA', 
			'data_stesura_ordine': 'Data di stesura ordine cartaceo', 
			'data_trasm_doc': "Data di trasmissione documentazione all'Ufficio Amministrativo", 
			'data_firma_RUP_ordine': 'Data',
        }	
	def __init__(self, *args, **kwargs):
		super(Ordine_Gara_RUP, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['data_caric_mepa'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[true]'})
		self.fields['data_stesura_ordine'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[false]'})
		self.fields['mepa'].widget.attrs.update({'class':'trigger'})


class Verifiche_Ammin(ModelForm):
#solo in caso MEPA
	section = 'Sez_Verifiche_Ammin'
	sec_label = "SERVIZIO VERIFICHE AMMINISTRATIVE: a cura dell'Addetto alle Verifiche"
	sec_short_label = "Verifiche"
	incharge = ['group_servizio_verifiche']
	attach = "attachReq"
	# notes = ['Allegare obbligatoriamente in questa sezione le risultanze delle verifiche effettuate a norma di legge, e cioè:\n' +
				# '\n  - Per importi fino a euro 5.000 + IVA: ANAC+CCIAA+DURC' +
				# '\n  - Per importi compresi fra 5.000 e 20.000 + IVA: aggiungere Sammin + Casellario + RegFiscale < 20000,' +
				# '\n  - Per importi compresi fra Euro 20.000 e 150.000: aggiungere Legge 68/99' +
				# '\n  - Per importi compresi fra Euro 150.000 e 221.000: aggiungere: Com. Antimafia' +
				# '\n  - Per importi superiori a 221.000: aggiungere: Informativa Antimafia']
	notes = ["Documenti da allegare in funzione dell'importo (al netto dell'IVA):\n" +
				
			'\n<b>         <   5.000</b>: ANAC + CCIAA + DURC' +
			'\n<b>   5.000 -  20.000</b>: ANAC + CCIAA + DURC + Sammin + Casell. + RegFiscale,' +
			'\n<b>  20.000 - 150.000</b>: ANAC + CCIAA + DURC + Sammin + Casell. + RegFiscale + Legge 68/99' +
			'\n<b> 150.000 - 221.000</b>: ANAC + CCIAA + DURC + Sammin + Casell. + RegFiscale + Legge 68/99 + Com. Antimafia' +
			'\n<b>         > 221.000</b>: ANAC + CCIAA + DURC + Sammin + Casell. + RegFiscale + Legge 68/99 + Com. Antimafia + Antimafia']
	class Meta:
		model = Ordine
		fields = ['note_verifiche_ammin','Sez_Verifiche_Ammin_closed'] 
		labels = {
			'note_verifiche_ammin': 'Note dell’amministrazione su eventuali problematiche dei documenti caricati',
		}

class Controllo_Verifiche(ModelForm):
#solo in caso MEPA
	section = 'Sez_Controllo_Verifiche'
	sec_label = "CONTROLLO VERIFICHE AMMINISTRATIVE: a cura del RUP"
	sec_short_label = "Controllo Verifiche"
	incharge = ['RUP']
	notes = ["Il RUP, viste le risultanze delle verifiche allegate nella sezione 'Servizio Verifiche Amministrative', dichiara qui l'esito delle stesse."]
	class Meta:
		model = Ordine
		fields = ['controllo_verifiche','note_controllo_verifiche','Sez_Controllo_Verifiche_closed'] 
		labels = {
			'controllo_verifiche': 'Esito positivo',
			'note_controllo_verifiche': 'Note',
		}


class Impegno_Bollo(ModelForm):
#solo in caso MEPA
	section = 'Sez_Impegno_Bollo'
	sec_label = "IMPEGNO IMPOSTA DI BOLLO: a cura di XXXX"
	sec_short_label = "Bollo"
	incharge = ['XXXX']		# consente di specificare un utente
	attach = "attachReq"
	class Meta:
		model = Ordine
		fields = ['var_bilancio_bollo', 'accert_bollo', 'impegno_bollo','note_bollo', 'Sez_Impegno_Bollo_closed'] 
		labels = {
			'var_bilancio_bollo': 'N. variazione di bilancio',
			'accert_bollo': 'N. accertamento',
			'impegno_bollo': 'N. impegno',
			'note_bollo': 'Note',
		}	


class Ordine_Diretto_Amministr(ModelForm):
	section = 'Sez_Ordine_Diretto_Amministr'
	sec_label = "IMPEGNO CONSOLIDATO: a cura del funzionario contabile"
	sec_short_label = "Impegno consolid."
	incharge = ['funz_contabile']
	notifyto = ['XXXX']
	class Meta:
		model = Ordine
		fields = ['n_impegno_cons', 'data_impegno_cons', 'cod_forn', 'data_trasm_PO', 'data_rich_durc', 'note_consolidato','Sez_Ordine_Diretto_Amministr_closed'] 
		labels = {
			'n_impegno_cons': "N. assegnazione impegno consolidato",
            'data_impegno_cons': 'Data impegno consolidato',
			'cod_forn': "Codice anagrafico fornitore",
			'data_trasm_PO': 'Data trasmissione documentazione al P.O.', 
			#'data_ordine': 'Data protocollo ordine', 
			#'data_spediz_ordine': "Data spedizione dell'ordine",  
			'data_rich_durc': "Data richiesta telematica DURC", 
			'note_consolidato': 'Note',
        }			
	def __init__(self, *args, **kwargs):
		super(Ordine_Diretto_Amministr, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['data_trasm_PO'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[true]'})
		#self.fields['data_ordine'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["mepa"]', 'data-condition':'[false]'})


class Ordine_Diretto_Direzione(ModelForm):
	section = 'Sez_Autorizz'
	sec_label = "AUTORIZZAZIONE ALL'ACQUISTO: a cura della Direzione"
	sec_short_label = "Autorizz. Direzione"
	incharge = ['group_direzione']
	attach = "attachReq"
	notes = ['Allegato richiesto: ordine firmato (se fuori MEPA)']
	class Meta:
		model = Ordine
		fields = ['data_autorizz', 'note_autorizz','Sez_Autorizz_closed'] 
		labels = {
			'data_autorizz': 'Data',
			'note_autorizz': 'Note',
		}			


class Ordine_Diretto_PuntoOrd(ModelForm):	# MEPA SI
	section = 'Sez_Ordine_Diretto_PuntoOrd'
	sec_label = "EMISSIONE ORDINE: a cura del Punto Ordinante"
	sec_short_label = "Emissione ordine (PO)"
	incharge = ['group_punto_ordinante']
	notifyto = ['funz_contabile']
	stateChange = 'SENT'
	notes = ['Allegato richiesto: ordine MEPA']
	class Meta:
		model = Ordine
		fields = ['imposta_bollo', 'data_ordine', 'Sez_Ordine_Diretto_PuntoOrd_closed'] 
		labels = {
			'imposta_bollo': 'Verifica evasione imposta di bollo',
			'data_ordine': 'Data emissione ordine',
        }			
	def __init__(self, *args, **kwargs):
		super(Ordine_Diretto_PuntoOrd, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		
class invio_ordine_RUP(ModelForm):			# MEPA NO
	section = 'Sez_Invio_Ordine_RUP'
	sec_label = "EMISSIONE e invio ordine: a cura del RUP"
	sec_short_label = "Invio ordine (RUP)"
	incharge = ['RUP']
	notifyto = ['funz_contabile']
	stateChange = 'SENT'
	links = [('Modulo conto dedicato','LINK'),
	("Modulo per acquisti all'estero", 'LINK')]
	notes = ["Prima di chiudere la sezione, inviare l’ordine firmato a invio.ordini.oapa@inaf.it insieme all’indirizzo del fornitore, in modo tale che gli uffici lo inviino via PEC al fornitore."]
	class Meta:
		model = Ordine
		fields = ['rich_autocert', 'data_spediz_ordine', 'Sez_Invio_Ordine_RUP_closed'] 
		labels = {
			'rich_autocert': "Richiesta conto dedicato", 
			'data_spediz_ordine': "Data spedizione dell'ordine",  
        }			


class fattura(ModelForm):
	section = 'Sez_fattura'
	sec_label = "FATTURA: a cura del Funzionario Contabile "
	sec_short_label = "Fattura"
	incharge = ['funz_contabile']
	attach = "attachReq"
	notes = ["Allegato obbligatorio: fattura elettronica/n/n","Nel caso di contratti di forniture o servizi cadenzato o continuativi, inserire qui le fatture che arrivano senza chiudere la sezione prima della termine di durata del contratto"]
	class Meta:
		model = Ordine
		fields = ['reg_team','note_fattura','Sez_fattura_closed'] 
		labels = {
			'reg_team': "Codice registrazioni TEAM della fattura", 
			'note_fattura': "Note",  
        }			

class collaudo(ModelForm):
	section = 'Sez_collaudo'
	sec_label = "VERIFICA/COLLAUDO DEL BENE/SERVIZIO: a cura del RUP"
	sec_short_label = "Verifica/collaudo"
	incharge = ['RUP']
	stateChange = 'RCVD'
	links = [('Schema di verbale di verifica/collaudo','LINK')]
	attach = "attachReq"
	notes = ["<b>Nel caso di forniture e servizi avente carattere cadenzato</b>, il RUP dovrà certificare in corso d'opera le regolari prestazioni intermedie subito dopo che esse siano state effettuate (ad es- ritiro semestrale dei rifiuti pericolosi, consegna bombole di gas), mediante il caricamento dei certificati intermedi SENZA chiudere la sezione.\n", "<b>Nel caso invece di forniture e servizi continuativi</b> aventi caratteristiche standard ( ad es. pulizie, luce, ecc)  la certificazione in corso d'opera del RUP può avvenire con cadenza semestrale (SENZA chiudere la sezione) o a sorpresa o essere omessa, assumendo implicitamente la regolare esecuzione, e dunque il pagamento delle fatture intermedie.\n", "<b>Alla scadenza della durata dei contratti</b>, il RUP emanerà un certificato di regolare prestazione FINALE, che deve contenere eventuali saldi ancora non pagati, desumibili dalle fattura che via via vengono caricate in Procedura dal Funzionario Contabile. A quel punto il RUP potrà chiudere la Sezione.\n","<b>Per tutti gli altri tipi di forniture e servizi</b>, il RUP caricherà l'unico certificato di verifica/collaudo non appena gli/le sarà possibile effettuare la completa verifica, senza aspettare la fattura, e chiudendo la sezione."]
	class Meta:
		model = Ordine
		fields = ['data_verifica', 'note_collaudo', 'descriz_breve', 'utilizzatore_finale', 'dislocazione', 'bene_portatile', 'Sez_collaudo_closed'] 
		labels = {
			'data_verifica': "Data di verifica/collaudo",
			'note_collaudo': "Note",
			'descriz_breve': "Descrizione breve del bene",
			'utilizzatore_finale': "Utilizzatore finale",
			'dislocazione': "Dislocazione",
			'bene_portatile': "Bene portatile",
        }
	def __init__(self, *args, **kwargs):
		super(collaudo, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['descriz_breve'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["tipologia"]', 'data-condition':'INV'})
		self.fields['utilizzatore_finale'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["tipologia"]', 'data-condition':'INV'})
		self.fields['dislocazione'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["tipologia"]', 'data-condition':'INV'})
		self.fields['bene_portatile'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["tipologia"]', 'data-condition':'INV'})


class buono_carico(ModelForm):
	section = 'Sez_buono_carico'
	sec_label = 'BUONO DI CARICO: a cura del Responsabile della Posizione Organizzativa "Inventario"'
	sec_short_label = "Buono di carico"
	incharge = ['XXXX']
	attach = "attachReq"
	notes = ["Allegato obbligatorio: buono di carico elettronico firmato"]
	class Meta:
		model = Ordine
		fields = ['Sez_buono_carico_closed'] 


class dopo_consegna(ModelForm):
	section = 'Sez_dopo_consegna'
	#last_section = True
	sec_label = "PAGAMENTO: a cura del funzionario contabile"
	sec_short_label = "Pagamento fattura"
	incharge = ['funz_contabile','XXXX','group_direzione']
	stateChange = 'CLSD'
	attach = "attachReq"
	notes = ['Allegato obbligatorio: quietanza di mandato']
	class Meta:
		model = Ordine
		fields = ['importo_liquidato','firma_RUP_fattura', 'mandato_pagamento', 'data_pagamento', 'equitalia','durc_finale', 'n_inventario','note_pagamento','Sez_dopo_consegna_closed'] 
		labels = {
			'importo_liquidato': "Importo liquidato",
			'firma_RUP_fattura': "Firma del RUP sulla fattura",
			'mandato_pagamento': "Mandato n.", 
			'data_pagamento': "del", 
			'equitalia': 'Verifica Equitalia',
			'durc_finale': 'Verifica DURC',
			'note_pagamento': 'Note',
			'n_inventario': "Numero di inventario",
		}			
	def __init__(self, *args, **kwargs):
		super(dopo_consegna, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		self.fields['n_inventario'].widget.attrs.update({'class':'conditional', 'data-cond_elem':'["tipologia"]', 'data-condition':'INV'})

		
class cancellato(ModelForm):
	section = 'Sez_cancellato'
	sec_label = "ORDINE CANCELLATO: a cura della Direzione"
	sec_short_label = "ORDINE CANCELLATO"
	incharge = ['group_direzione']
	stateChange = 'CANC'
	class Meta:
		model = Ordine
		fields = ['note_cancellato', 'data_cancellato', 'Sez_cancellato_closed'] 
		labels = {
			'note_cancellato': "Note",
			'data_cancellato': "Data", 
        }			
	def __init__(self, *args, **kwargs):
		super(cancellato, self).__init__(auto_id='id_%s_'+datetime.datetime.now().strftime('%S%f'),*args, **kwargs)
		
#---------- VERSION 0 ------------		
class PropostaForm0(ModelForm):			# V0
	section = 'Sez_Proposta'
	incharge = ['proponente']
	first_section = True
	class Meta:
		model = Ordine
		fields = [ 'resp_acquisto', 'data_prop', 'descriz', 'stima_costo', 'fondi0_prop', 'contraente', 'tipologia0', 'n_invent_manutenzione', 'Sez_Proposta_closed'] 
		initial = {
        'data_prop': datetime.date.today()
		}
		
		
class AutorizzForm0(ModelForm):			# V0
	section = 'Sez_Autorizz'
	incharge = ['group_direzione']
	class Meta:
		model = Ordine
		fields = ['autorizza', 'note_direzione', 'data_autorizz','Sez_Autorizz_closed'] 


class AmministrForm0(ModelForm):			# V0
	section = 'Sez_Amministr'
	incharge = ['group_direzione', 'funz_contabile']
	class Meta:
		model = Ordine
		fields = ['tipo_struttura', 'fondi0', 'capitolo', 'cod_forn', 'numero_ordine_0', 'fondi0_r1', 'fondi0_r2', 'fondi0_r3', 'riduz_iva','numero_ordine','data_ordine','Sez_Amministr_closed'] 
		