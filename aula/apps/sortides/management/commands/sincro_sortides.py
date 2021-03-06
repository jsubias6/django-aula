# This Python file uses the following encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from aula.apps.sortides.sincronitza import sincronitza

class Command(BaseCommand):
    help = "Notifica a les families"

    def handle(self, *args, **options):

        try:
            self.stdout.write(u"Iniciant procés sincronitzacio sortides" )
            sincronitza()
            self.stdout.write(u"Fi procés sincronitzacio sortides" )
        except Exception, e:
            self.stdout.write(u"Error al procés sincronitzacio sortides: {0}".format( unicode(e) ) )
            errors = [unicode(e)]            
         
            #Deixar missatge a la base de dades (utilitzar self.user )
            from aula.apps.missatgeria.models import Missatge
            from django.contrib.auth.models import User, Group
     
            usuari_notificacions, new = User.objects.get_or_create( username = 'TP')
            if new:
                usuari_notificacions.is_active = False
                usuari_notificacions.first_name = u"Usuari Tasques Programades"
                usuari_notificacions.save()
            msg = Missatge( 
                        remitent= usuari_notificacions, 
                        text_missatge = u"Error sincronitzant sortides.")    
            importancia = 'VI' 
             
            administradors, _ = Group.objects.get_or_create( name = 'administradors' )
             
            msg.envia_a_grup( administradors , importancia=importancia)
            msg.afegeix_errors( errors )
            
            