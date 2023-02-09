import os
from django.db import models
import datetime
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.models import User
from gdoapa import settings

# Create your models here.

class Ordine(models.Model):
	attesa = models.CharField(max_length=200, blank=True, null=True)
	versione_procedura = models.CharField(max_length=10)
	versione_PDF = models.CharField(max_length=10)
	rich_acq_id = models.CharField(max_length=40, blank=True, null=True)
	cod_forn = models.CharField(max_length=40, blank=True, null=True)									# V0, V1
	numero_ordine = models.CharField(max_length=40, blank=True, null=True)								# V0, V1
	tipo_struttura = models.CharField(max_length=4,choices=(('IST.', 'Istituto'),('OSS.', 'Osservatorio')), blank=True, null=True)	# V0
	fondi0 = models.CharField(max_length=10, blank=True, null=True)										# V0
	numero_ordine_0 = models.CharField(max_length=10, blank=True, null=True)							# V0
	resp_acquisto = models.ForeignKey(User, related_name='Ordine_resp_acquisto', blank=True, null=True)	# V0
	
	
	# Sez_Proposta
	proponente = models.ForeignKey(User, related_name='Ordine_proponente')																# V0, V1
	data_prop = models.DateField()																		# V0, V1
	richiesto_da = models.CharField(max_length=40, blank=True, null=True)		
	TIPOLOGIA_SCELTE = (
		('SERV', 'Servizio'),
		('CONS', 'Consumo'),
		('INV', 'Bene inventariabile'),
		('LAV', 'Lavori'),
		('OPE', 'Opere'),
		('ALT', 'Altro'),
	)
	tipologia = models.CharField(max_length=4,choices=TIPOLOGIA_SCELTE, blank=True, null=True)			# V1
	TIPOLOGIA_SCELTE0 = (
		('SERV', 'Servizi'),
		('CONS', 'Consumo'),
		('INV', 'Beni inventariabili'),
		('INVC', 'Beni inventariabili CED'),
		('SW', 'Software'),
		('MAN', 'Manutenzione'),
	)
	tipologia0 = models.CharField(max_length=4,choices=TIPOLOGIA_SCELTE0, blank=True, null=True)		# V0
	n_invent_manutenzione = models.CharField(max_length=40, blank=True, null=True)						# V0
	FONDI0_R1 = (			# V0
		('CD', 'C.D.'),
		('CI', 'C.I.'),
		('CA', 'C.A.'),
	)
	FONDI0_R2 = (			# V0
		('AMF', 'Antimafia'),
		('AUT', 'Autocertificazione'),
		('PREF', 'N.O. Prefettura'),
	)
	FONDI0_R3 = (			# V0
		('UTE', 'U.T.E.'),
		('OSS', 'U.T. Oss.'),
		('UNIV', 'U.T. Univ.'),
	)
	fondi0_r1 = models.CharField(max_length=4,choices=FONDI0_R1, blank=True, null=True)					# V0
	fondi0_r2 = models.CharField(max_length=4,choices=FONDI0_R2, blank=True, null=True)					# V0
	fondi0_r3 = models.CharField(max_length=4,choices=FONDI0_R3, blank=True, null=True)					# V0
	riduz_iva = models.BooleanField(default=False)														# V0
	resp_ufficio = models.ForeignKey(User, limit_choices_to={'groups__name': 'resp_ufficio'}, related_name='Ordine_resp_ufficio', blank=True, null=True)
	#resp_ufficio = models.CharField(max_length=40, blank=True, null=True)
	descriz = models.TextField(blank=True, null=True)													# V0, V1
	#stima_costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)			# V0, V1
	stima_costo = models.CharField(max_length=10, blank=True, null=True)								# V0, V1
	dest_ricerca = models.BooleanField(default=False)
	fondi0_prop = models.CharField(max_length=40, blank=True, null=True)										# V0
	fondi_amministrazione0 = models.CharField(max_length=40, blank=True, null=True)						# V0
	autorizza = models.BooleanField(default=False)														# V0
	note_direzione = models.TextField(blank=True, null=True)											# V0
	note_proposta = models.TextField(blank=True, null=True)
	Sez_Amministr_closed = models.BooleanField(default=False)
	Sez_Amministr_closedby = models.ForeignKey(User, related_name='Sez_Amministr_closedby', blank=True, null=True)
	#resp_fondi = models.CharField(max_length=40, blank=True, null=True)
	#firma_proponente = models.BooleanField(default=False)
	Sez_Proposta_closed = models.BooleanField(default=False)
	Sez_Proposta_closedby = models.ForeignKey(User, related_name='Sez_Proposta_closedby', blank=True, null=True)


	# Sez_Resp_fondi
	#firma_resp_fondi = models.BooleanField(default=False)
	data_firma_resp_fondi = models.DateField(blank=True, null=True)
	resp_fondi_autorizza = models.BooleanField(default=False)
	note_resp_fondi = models.TextField(blank=True, null=True)
	Sez_Resp_fondi_closed = models.BooleanField(default=False)
	Sez_Resp_fondi_closedby = models.ForeignKey(User, related_name='Sez_Resp_fondi_closedby', blank=True, null=True)

	
	# Sez_Resp_uff
	#firma_resp_ufficio = models.BooleanField(default=False)
	data_firma_resp_ufficio = models.DateField(blank=True, null=True)
	Sez_Resp_uff_closed =  models.BooleanField(default=False)
	Sez_Resp_uff_closedby = models.ForeignKey(User, related_name='Sez_Resp_uff_closedby', blank=True, null=True)

	
	# sezione Scelta_RUP		V1
	determ_n = models.CharField(max_length=40, blank=True, null=True)
	determ_data = models.DateField(blank=True, null=True)
	note_determina = models.TextField(blank=True, null=True)
	determ_sc_n = models.CharField(max_length=40, blank=True, null=True)
	determ_sc_data = models.DateField(blank=True, null=True)
	note_determina_sc = models.TextField(blank=True, null=True)
	MODO_SCELTA_CONTR_SCELTE = (
		('AFD', 'Affidamento diretto'),
		('AMD', 'Amministrazione diretta'),
		('ORD', 'Procedura Ordinaria'),
		('ALT', 'Altro'),
		#('ECO', 'Procedura in Economia'),
	)
	modo_scelta_contr = models.CharField(max_length=3,choices=MODO_SCELTA_CONTR_SCELTE, blank=True, null=True)
	data_firma_direttore = models.DateField(blank=True, null=True)
	data_firma_direttore_sc = models.DateField(blank=True, null=True)
	Sez_Scelta_RUP_closed = models.BooleanField(default=False)	#V1
	Sez_Scelta_RUP_closedby = models.ForeignKey(User, related_name='Sez_Scelta_RUP_closedby', blank=True, null=True) #V1
	Sez_Determina_closed = models.BooleanField(default=False)
	Sez_Determina_closedby = models.ForeignKey(User, related_name='Sez_Determina_closedby', blank=True, null=True)
	Sez_Determina_sc_closed = models.BooleanField(default=False)
	Sez_Determina_sc_closedby = models.ForeignKey(User, related_name='Sez_Determina_sc_closedby', blank=True, null=True)
	
	# sezione sceltaFondi		V2
	RUP = models.ForeignKey(User, related_name='RUP', limit_choices_to={'groups__name': 'RUP'}, blank=True, null=True)
	CRA = models.CharField(max_length=40, blank=True, null=True)
	CUP = models.CharField(max_length=40, blank=True, null=True)
	resp_fondi = models.ForeignKey(User, related_name='Ordine_resp_fondi', limit_choices_to={'groups__name': 'resp_fondi'},blank=True, null=True)
	funz_contabile = models.ForeignKey(User, related_name='funz_contabile', limit_choices_to={'groups__name': 'amministrazione'}, blank=True, null=True)
	data_sceltaFondi = models.DateField(blank=True, null=True)
	note_sceltaFondi = models.TextField(blank=True, null=True)
	Sez_sceltaFondi_closed = models.BooleanField(default=False)
	Sez_sceltaFondi_closedby = models.ForeignKey(User, related_name='Sez_sceltaFondi_closedby', blank=True, null=True)
	
	# sezione CIG
	CIG = models.CharField(max_length=40, blank=True, null=True)
	data_CIG = models.DateField(blank=True, null=True)
	Sez_CIG_closed = models.BooleanField(default=False)
	Sez_CIG_closedby = models.ForeignKey(User, related_name='Sez_CIG_closedby', blank=True, null=True)

	# sezione impegno
	impegno_n = models.CharField(max_length=40, blank=True, null=True)
	capitolo = models.CharField(max_length=40, blank=True, null=True)							# V0, V1
	data_firma_funz_contabile = models.DateField(blank=True, null=True)
	note_prenotazione = models.TextField(blank=True, null=True)
	Sez_Impegno_closed = models.BooleanField(default=False)
	Sez_Impegno_closedby = models.ForeignKey(User, related_name='Sez_Impegno_closedby', blank=True, null=True)

		
	# sezione scelta gara
	gara = models.BooleanField(default=False)
	Sez_scelta_gara_closed = models.BooleanField(default=False)
	Sez_scelta_gara_closedby = models.ForeignKey(User, related_name='Sez_scelta_gara_closedby', blank=True, null=True)

	
	# sezione Ordine Diretto - RUP
	contraente = models.CharField(max_length=40, blank=True, null=True)						# V0, V1
	#importo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	importo = models.CharField(max_length=10, blank=True, null=True)
	allega_rel_scelta = models.BooleanField(default=False)
	operatori = models.TextField(blank=True, null=True)
	verifica_CIG = models.BooleanField(default=False)
	mepa = models.NullBooleanField(default=None, blank=True, null=True)
	#si mepa
	data_caric_mepa = models.DateField(blank=True, null=True)
	id_mepa = models.CharField(max_length=40, blank=True, null=True)
	bollo_no_mepa = models.BooleanField(default=True)
	#no mepa
	data_stesura_ordine = models.DateField(blank=True, null=True)								# V0, V1
	data_trasm_doc = models.DateField(blank=True, null=True)									# not used
	#compil_scheda_invent = models.BooleanField(default=False)
	data_firma_RUP_ordine = models.DateField(blank=True, null=True)
	Sez_Ordine_Diretto_RUP_closed = models.BooleanField(default=False)
	Sez_Ordine_Diretto_RUP_closedby = models.ForeignKey(User, related_name='Sez_Ordine_Diretto_RUP_closedby', blank=True, null=True)

	# sezione Verifiche Amministrative
	note_verifiche_ammin = models.TextField(blank=True, null=True)
	Sez_Verifiche_Ammin_closed = models.BooleanField(default=False)
	Sez_Verifiche_Ammin_closedby = models.ForeignKey(User, related_name='Sez_Verifiche_Ammin_closedby', blank=True, null=True)

	# sezione controllo verifiche amministrative
	controllo_verifiche = models.BooleanField(default=False)
	note_controllo_verifiche = models.TextField(blank=True, null=True)
	Sez_Controllo_Verifiche_closed = models.BooleanField(default=False)
	Sez_Controllo_Verifiche_closedby = models.ForeignKey(User, related_name='Sez_Controllo_Verifiche_closedby', blank=True, null=True)
	
	
	# sezione gara - RUP
	data_rdo = models.DateField(blank=True, null=True)
	data_emissione_rdo = models.DateField(blank=True, null=True)
	data_valut_offerte = models.DateField(blank=True, null=True)
	Sez_Gara_RUP_closed = models.BooleanField(default=False)
	Sez_Gara_RUP_closedby = models.ForeignKey(User, related_name='Sez_Gara_RUP_closedby', blank=True, null=True)

	
	
	# sezione di controlli Uff. Amm.
	#data_controllo = models.DateField(blank=True, null=True)
	#Sez_Ordine_Diretto_Controllo_Ammin_closed = models.BooleanField(default=False)
	#Sez_Ordine_Diretto_Controllo_Ammin_closedby = models.ForeignKey(User, related_name='Sez_Ordine_Diretto_Controllo_Ammin_closedby', blank=True, null=True)

	
	# sezione Ordine Diretto - Direzione
	data_autorizz = models.DateField(blank=True, null=True)
	note_autorizz = models.TextField(blank=True, null=True)
	Sez_Autorizz_closed = models.BooleanField(default=False)
	Sez_Autorizz_closedby = models.ForeignKey(User, related_name='Sez_Autorizz_closedby', blank=True, null=True)

	# Impegno_Bollo (caso MEPA)
	var_bilancio_bollo = models.CharField(max_length=20, blank=True, null=True)	# V3
	accert_bollo = models.CharField(max_length=20, blank=True, null=True)		# V3
	impegno_bollo = models.CharField(max_length=20, blank=True, null=True)		# V3
	note_bollo = models.TextField(blank=True, null=True)
	Sez_Impegno_Bollo_closed = models.BooleanField(default=False)				# V3
	Sez_Impegno_Bollo_closedby = models.ForeignKey(User, related_name='Sez_AImpegno_Bollo_closedby', blank=True, null=True) # V3

	
	# sezione Ordine Diretto - uff. amministrativo
	n_impegno_cons = models.CharField(max_length=20, blank=True, null=True)
	data_impegno_cons = models.DateField(blank=True, null=True)
	#si mepa
	data_trasm_PO = models.DateField(blank=True, null=True)
	#data_emiss_ordine = models.DateField(blank=True, null=True)
	data_comunic_RUP = models.DateField(blank=True, null=True)
	#no mepa
	data_ordine = models.DateField(blank=True, null=True)		# emissione/protocollo		# V0, V1
	#
	data_rich_durc = models.DateField(blank=True, null=True)
	note_consolidato = models.TextField(blank=True, null=True)
	Sez_Ordine_Diretto_Amministr_closed = models.BooleanField(default=False)
	Sez_Ordine_Diretto_Amministr_closedby = models.ForeignKey(User, related_name='Sez_Ordine_Diretto_Amministr_closedby', blank=True, null=True)
	
	imposta_bollo = models.BooleanField(default=False)
	Sez_Ordine_Diretto_PuntoOrd_closed = models.BooleanField(default=False)
	Sez_Ordine_Diretto_PuntoOrd_closedby = models.ForeignKey(User, related_name='Sez_Ordine_Diretto_PuntoOrd_closedby', blank=True, null=True)
	
	# sezione invio_ordine_RUP
	data_spediz_ordine = models.DateField(blank=True, null=True)
	rich_autocert = models.BooleanField(default=False)
	Sez_Invio_Ordine_RUP_closed	= models.BooleanField(default=False)
	Sez_Invio_Ordine_RUP_closedby = models.ForeignKey(User, related_name='Sez_Invio_Ordine_RUP_closedby', blank=True, null=True)
	
	
	# sezione fattura - funz. contabile
	reg_team = models.CharField(max_length=20, blank=True, null=True)
	note_fattura = models.TextField(blank=True, null=True)
	Sez_fattura_closed = models.BooleanField(default=False)
	Sez_fattura_closedby = models.ForeignKey(User, related_name='Sez_fattura_closedby', blank=True, null=True)


	# sezione collaudo
	data_verifica = models.DateField(blank=True, null=True)
	note_collaudo = models.TextField(blank=True, null=True)
	descriz_breve = models.CharField(max_length=40, blank=True, null=True)
	utilizzatore_finale = models.CharField(max_length=40, blank=True, null=True)
	dislocazione = models.CharField(max_length=40, blank=True, null=True)
	bene_portatile = models.BooleanField(default=False)
	Sez_collaudo_closed =  models.BooleanField(default=False)
	Sez_collaudo_closedby = models.ForeignKey(User, related_name='Sez_collaudo_closedby', blank=True, null=True)
	
	
	# sezione buono_carico - Anna Incardona
	Sez_buono_carico_closed = models.BooleanField(default=False)
	Sez_buono_carico_closedby = models.ForeignKey(User, related_name='Sez_buono_carico_closedby', blank=True, null=True)
	
	
	# sezione dopo ricezione bene e fattura
	#durc_ric = models.BooleanField(default=False)
	#fatt_ric = models.BooleanField(default=False)
	#liquidato = models.BooleanField(default=False)
	firma_RUP_fattura = models.BooleanField(default=False)
	equitalia = models.BooleanField(default=False)
	durc_finale = models.BooleanField(default=False)
	mandato_pagamento = models.CharField(max_length=20, blank=True, null=True)
	data_pagamento= models.DateField(blank=True, null=True)
	n_inventario = models.CharField(max_length=20, blank=True, null=True)
	importo_liquidato = models.CharField(max_length=40, blank=True, null=True)
	note_pagamento = models.TextField(blank=True, null=True)
	Sez_dopo_consegna_closed = models.BooleanField(default=False)
	Sez_dopo_consegna_closedby = models.ForeignKey(User, related_name='Sez_dopo_consegna_closedby', blank=True, null=True)

	# sezione cancellato (ordine segnato come cancellato)
	note_cancellato = models.TextField(blank=True, null=True)
	data_cancellato= models.DateField(blank=True, null=True)
	Sez_cancellato_closed = models.BooleanField(default=False)
	Sez_cancellato_closedby = models.ForeignKey(User, related_name='Sez_cancellato_closedby', blank=True, null=True)
	
	
	order_closed = models.BooleanField(default=False)
	STATI_ORDINE = (
		('OPEN', 'Aperto'),
		('SENT', 'Inviato'),
		('RCVD', 'Ricevuto'),
		('CLSD', 'Chiuso'),
		('CANC', 'Annullato'),
	)
	order_status = models.CharField(max_length=4,choices=STATI_ORDINE, blank=True, null=True)
	
	
	def __unicode__(self):
		if self.descriz:
			if len(self.descriz) > 30:		
				return self.descriz[0:30] + ' ...'
			else:
				return self.descriz[0:30]
		else:
			return 'Senza nome'
		

def get_file_path(instance, filename):
    #return os.path.join('photos', str(instance.id), filename)
	#print filename
	uploadto = os.path.join(str(instance.order.id), filename.lower())
	if len(uploadto)>90:
		strippedname, extension = os.path.splitext(uploadto)
		strippedname = strippedname[0:90-len(extension)]
		uploadto = strippedname+extension
	#print uploadto
	return	uploadto
		
class File(models.Model):
	file = models.FileField(upload_to=get_file_path)
	description = models.CharField(max_length=200)
	order = models.ForeignKey(Ordine)
	section = models.CharField(max_length=40)
	def __unicode__(self):
		return self.description
		

# This auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	"""Deletes file from filesystem
	when corresponding `File` object is deleted.
	"""
	#raise Exception("auto delete")
	if instance.file:
		if os.path.isfile(instance.file.path):
			os.remove(instance.file.path)
	else:
		raise Exception("Nessun file!")
			

# User profile
class Profilo(models.Model):
	#user = models.ForeignKey(User)
	user = models.OneToOneField(User)
	full_name = models.CharField(max_length=40)
	ordini_seguiti = models.ManyToManyField(Ordine)
	def __unicode__(self):
		return self.user.get_full_name()
	def save( self, *args, **kw ):
		#self.full_name = user.first_name + user.last_name	
		#'{0} {1}'.format( first_name, last_name )
		self.full_name = self.user.get_full_name()
		super( Profilo, self ).save( *args, **kw )		

	def natural_key(self):
		return 'profilo' + self.user.natural_key()
	#natural_key.dependencies = ['django.contrib.admin']#,'django.contrib.auth']
		
		
# This automatically update profiles or add a profile for new users:
@receiver(models.signals.post_save, sender=User)
def auto_add_profile(sender, instance, **kwargs):
	"""automatically add a profile for new users"""
	if settings.ENABLE_AUTOCREATE:
		try:
			profilo = getattr(instance,'profilo')
			profilo.save()
		except (AttributeError):
			profilo = Profilo(user = instance)
			profilo.save()