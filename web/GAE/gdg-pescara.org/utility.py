# 
# General utlity class
#
import string

#
# simple template service
#

class Template( object ):
    templateFile = ""
    templateText = ""

    def __init__(this, templateFile ):
        this.templateFile = templateFile
        ftemplate = file ( templateFile, "r" )
        this.templateText = ftemplate.read()
        ftemplate.close()
 
    def render(this, data ):
        text = this.templateText
        for key in data.keys():
            value = data[key]
            if type(value) is dict:
                for key1 in value.keys():
                    text = string.replace( text, '{{'+key+"."+key1+"}}", value[key1])
            else:
                text = string.replace(text, '{{'+key+'}}', data[key] )
        return text

#t = Template("/home/apalma/Desktop/TheNextUniverse/google_appengine/gdg-pescara.org/templates/index.template")
#testo = t.render( { 'pageNavbar' : 'testo che finisce al posto del tag', 'pageParagraph06' : {'title' : 'secondo livello sostituito' } })
#print testo
