# This Python file uses the following encoding: utf-8

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from aula.apps.alumnes.models import Nivell
from django.db.models import get_model
    
TipusDAssignatura = get_model('assignatures','TipusDAssignatura')


def assignatura_clean( instance ):
        
    #
    # Pre-save
    #
    if instance.tipus_assignatura is None:
        #si és de cicle poso com unitat formativa
        cicles = Nivell.objects.filter( nom_nivell__contains = 'CF'  )
        if instance.curs and instance.curs.nivell.pk in [ nivell.pk for nivell in cicles]:
            uf = TipusDAssignatura.objects.get( tipus_assignatura__startswith = 'Unitat' )
            instance.tipus_assignatura = uf    
    
        #si és AO, Optativa, ...    
        if  instance.codi_assignatura.startswith( 'OP' ) or \
            instance.codi_assignatura.startswith( 'OE' ) or \
            instance.codi_assignatura.startswith( 'AO' ):
        
            op = TipusDAssignatura.objects.get( tipus_assignatura__startswith = 'Opcional' )    
            instance.tipus_assignatura = op
        
        #si el grup és aula d'acolloda poso nivell tot el centre, ...            
        if  instance.curs is not None and instance.curs.nom_curs == 'ACO/UEC':        
            ao = TipusDAssignatura.objects.get( tipus_assignatura__startswith = 'Aula Oberta' )    
            instance.tipus_assignatura = ao
    
    #rules
    
def assignatura_pre_save(sender, instance, **kwargs): 
    instance.clean()    
    
def assignatura_post_save(sender, instance, created, **kwargs):    
    pass

