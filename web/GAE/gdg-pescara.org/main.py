#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="">

<title>GDG-PESCARA</title>

<!-- Bootstrap core CSS -->
<link href="css/bootstrap.css" rel="stylesheet">

<!-- Custom styles for this template -->
<link href="css/style.css" rel="stylesheet">

<!-- Google web Font -->
<link
  href='http://fonts.googleapis.com/css?family=Lato:300,400,700,900,100'
  rel='stylesheet' type='text/css'>

<!-- Just for debugging purposes. Don't actually copy this line! -->
<!--[if lt IE 9]><script src="../../docs-assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

<!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-48315347-1', 'gdg-pescara.appspot.com');
  ga('send', 'pageview');

</script>

</head>

<body data-spy="scroll" data-target="#my-navbar">

  <div class="container">
    <div class="navbar navbar-inverse navbar-fixed-top" id="my-navbar">

      <div class="navbar-header">
        <button type="button" class="navbar-toggle"
          data-toggle="collapse" data-target=".navbar-collapse">
          <span class="icon-bar"></span> <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="#">GDG-PESCARA</a>
      </div>
      <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
          <li class="active"><a href="#home">01. Benvenuti</a></li>
          <li><a href="#developer">02. Sviluppatori</a></li>
          <li><a href="#people">03. Gruppo</a></li>
          <li><a href="#work">04. Programma</a></li>
          <li><a href="#who">05. Contatti</a></li>
          <li><a href="#thanks">06. Grazie</a></li>
        </ul>
      </div>
      <!--/.nav-collapse -->
    </div>
  </div>

  <div class="full-panel" id="home">
    <div id="copertina"><img src="img/gdg-pescara.png">Ciao mondo!</div>
  </div>

  <div class="my-container">
    <div class="row">
      <div class="col-md-12 full-panel developer">
        <div class="in-panel" id="developer">
          <h2>02. Sviluppatori</h2>
          <p>
            <strong>Coloro che usano quotidianamente le
              tecnologie di Google e vogliono condividere con te le loro
              esperienze.</strong>
               
            <br> <br> Il GDG-PESCARA è un gruppo
            indipendente di sviluppatori appasionato delle tecnologie
            dell'azienda di Mountain View e non è assolutamente
            collegato con Google. <br>Oggi il giocoforza è gestire
            la complessità, sarete sorpresi di scoprire quanto è
            semplice con le loro tecnologie. <br>Lo sarete non meno
            di quanto lo siamo stati noi e, da qui, avrete anche voi la
            voglia di condividere queste incredibili esperienze con
            tutti gli altri. <br> <br>Trasferire una
            informazione tecnica da uno sviluppatore ad un altro è lo
            scopo principale degli incontri che questo GDG organizzerà,
            però non dimentichiamo che a volte serve un aiuto competente
            ed immediato per poter proseguire un discorso ed è per
            questo motivo che la voce "gruppo" è separata da
            "sviluppatori". <br> <br>E' imporante che, in
            qualche modo, ci sia sempre qualcuno a cui rivolgersi
            riguardo una certa tecnologia. Questo è vitale sia per la
            crescita del gruppo che per la propria esperienza
            professionale e non dimentichiamo che la presenza o assenza
            di un supporto spesso vincola la scelta. <br> <br>I
            <i>wildcard-man</i> sono un mito, chiunque è interessato a
            offrire le propria disponibilità a far parte di questa
            squadra speciale, il core del gruppo, può candidarsi a non
            più di tre tecnologie. Vedi <a href="#who">paragrafo 05</a>.
        </div>
      </div>


      <div class="col-md-12 full-panel people">
        <div class="in-panel" id="people">
          <h2>03. Gruppo</h2>
          <p id="paper">
            <strong>Partecipa, condividi.</strong>

            <br>Un gruppo è un insieme di persone collegate da interessi comuni, ma non confondete l'interesse con la competenza specifica. 
            <br>In questo GDG ci teniamo a tenere distinto il "gruppo" dal "gruppo di sviluppatori".
            <br>L'interesse per certe tecnologie non deve essere limitato
            dalla capacità di produrre con le stesse, una buona idea rimane tale anche se non avete idea di come implementarla. 
            <br>Le cose migliori nascono dove c'è diversità. 
            <br>Punti di vista differenti aiutano a modellare meglio la realtà ed a realizzare prodotti più usabili.
            <br>Le applicazioni del Web vanno oltre la messaggeria ed il social ed i nuovi campi di applicazione vanno scoperti di volta in volta. I soli sviluppatori possono solo vedere 
            una parte di essi.  
            <br>Conoscere le tecnologie, nel caso specifico quelle di Google, anche a solo titolo informativo, permette di capire le possibilità e le potenzialità che sono oggi disponibili
            per migliorare la vita odierna. 
            <br>Durante gli eventi, che terremo a Pescara e provincia, cercheremo sempre di costruire un ponte tra chi sa implementare e quelli che hanno idee da sviluppare.
            <br>Sentiti parte del gruppo se senti di avere interesse in questa tecnologia o sei curioso di conoscerla.
          </div>
      </div>


      <div class="col-md-12 full-panel work">
        <div class="in-panel" id="work">
          <h2>04. Programma</h2>
          <p>
            <strong>Condividere, inventare, sperimentare, crescere.</strong> 
            <br> <br> Lo scopo primario del gruppo è la condivisione di esperienze sull'uso delle tecnologie di Google, nel fare questo
            cerca anche di essere un punto di riferimento per coloro che vogliono avvicinarsi a questo mondo. Quando possibile, alcuni volontari
            offrono la propria disponibilità a coloro che intraprendono per la prima volta una soluzione basata su tecnologie Google. 
            Vedi <a href="#developer">paragrafo 02</a>.<br />

            <br>Per migliorare e rendere piacevole la condivisione delle esperienze e favorire la conoscenza di dette tecnologie, 
            questo gruppo organizza incontri dove chiunque può partecipare. Sono incontri non troppo formali tra sviluppatori e non, dove è possibile 
            esporre idee, esperienze, richieste di aiuto o cercare forme di collaborazione.
            <br>Cercheremo, per quanto possibile, di istituire anche dei laboratori permanenti, dove sarà possibile portare avanti dei progetti o idee. 
             Di certo la rete permette di realizzare laboratori "virtuali", ma è solo nella <i>interazione diretta</i> che sia ha il massimo profitto in 
             termini di creatività, produttività e crescita.
            <br>Il programma è ambizioso, difficile, impegnativo e soprattutto necessario se vogliamo che a Pescara il GDG sia qualcosa di più
            che un calendario di eventi usufruibile a pieno solo da programmatori.
            <br>Un sviluppatore essenzialmente sviluppa un'idea, non necessariemente sua, se l'idea è buona allora è innovazione.  
            <br>A noi serve l'innovazione, voi lo sapete.<br>
            </p> 
        </div>
      </div>


      <div class="col-md-12 full-panel who">
        <div class="in-panel" id="who">
          <h2>05. Contatti</h2>
          <p id="paper">
             <b>Gestori GDG-PESCARA</b>
             <br>Questo Google Developer Group è gestito da  <a href="https://sites.google.com/site/ozw1z5rd/">Alessio Palma</a> che può essere raggiunto al <a href="tel:+393498687665">349 8687665</a> ed 
             <a href="mailto:antonello.pinnella@gmail.com">Antonello Pinnella</a>.
             <br> 
             <br><b>Mailing list</b>
             <br>Questo gruppo possiede una mailing list, per essere un membro di questo gruppo è sufficiente iscriversi ad essa.<br>
             L'indirizzo è <a href="mailto:gdg-pescara@googlegroups.com">gdg-pescara@googlegroups.com</a><br>
             la pagina web corrispondente è <a href="https://groups.google.com/d/forum/gdg-pescara">https://groups.google.com/d/forum/gdg-pescara</a>.
             <br>L'iscrizione non vincola in alcun modo e permette di avere aggiornamenti sulle attività del gruppo.
             <br>La pagina su <a href="https://plus.google.com/109764437711338482169" rel="publisher">Google+</a>
             <br>
             <br>
             <b>Sito web</b> 
             <br>Ti consigliamo di usare solo <a href="http://www.gdg-pescara.org">www.gdg-pescara.org</a> per accedere a questo sito. La url dell'applicazione potrebbe variare nel futuro.
             <br>Il sito che stai visualizzando è ospitato sul Google App Engine ed il dominio ufficiale, per ora, fa un redirect verso l'indirizzo dell'applicazione (gdg-pescara.appspot.com)
             <br>
             <br><b>Sviluppatori</b>
             <br>Non appena sarà possibile le informazioni di contatto saranno disponibili in home page, dove saranno presentate le icone cliccabili delle varie tecnologie disponibili.
             
             </p>               
             
        </div>
      </div>

      <div class="col-md-12 full-panel thanks">
        <div class="in-panel" id="thanks">
          <h2>06. Grazie</h2>
          <p id="paper">
             <br><i>Tutto quello che avete visto fino ad ora è stato reso possibile grazie all'aiuto di</i>
             <br>
             <br><b>Alfredo Morresi</b> di Google Italia per l'opportunità.
             <br><br>
             <b>Marialena Di Giantomasso</b> (paragrafi 01 e 05) e <b>Nino D'Angelo</b> (paragrafo 03) per aver concesso l'uso dei loro magnifici scatti su questo sito.
             <br>
             <br><b>Andrea Marchetti</b>, freelance web designer, per l'aiuto nella realizzazione di questo sito.
             <br>
             <br><b>Antonello Pinnella</b> che non teme le sfide.
             <br>
             <br><b>Google</b>, a cui dedichiamo una frase di Arthur C. Clarke, autore di fantascienza ed inventore britannico.<i>"Ogni tecnologia sufficientemente avanzata è indistinguibile dalla magia"</i>. 
<br/><cite><a href="http://it.wikipedia.org/wiki/Arthur_C._Clarke">Wikipedia</a></cite>
           </p>
            
        </div>
      </div>

    </div>

    <div class="col-md-12 full-panel footer">
      <p>GDG-PESCARA.ORG</p>
    </div>

  </div>
  <!-- /.container -->


  <!-- Bootstrap core JavaScript
    ================================================== -->
  <!-- Placed at the end of the document so the pages load faster -->
  <script src="http://code.jquery.com/jquery-1.9.1.min.js"
    type="text/javascript"></script>
  <script src="js/bootstrap.min.js"></script>

  <script>

//    $('body').scrollspy({ target: '#my-navbar' })
 
    $(".navbar-collapse ul li a[href^='#']").on('click', function(e) {
	    
	    target = this.hash;
       // prevent default anchor click behavior
       e.preventDefault();

       // animate
       $('html, body').animate({
           scrollTop: $(this.hash).offset().top 
         }, 300, function(){
   
           // when done, add hash to url
           // (default click behaviour)
           window.location.hash = target;
         });

    });

    
    $(document).ready(function(){
		   // cache the window object
		   $window = $(window);
		 
		        $('.full-panel').each(function() {
		            // declare the variable to affect the defined data-type
		            var $scroll = $(this);
		 
		            $(window).scroll(function() {
		                // HTML5 proves useful for helping with creating JS functions!
		                // also, negative value because we're scrolling upwards
		                var yPos = -($window.scrollTop() /10);
		 
		                // background position
		                var coords = '20% ' + yPos + 'px';
		 
		                // move the background
		                $scroll.css({ backgroundPosition: coords });
		            }); // end window scroll
		        });  // end section function
		 
		}); // close out script

//$('body').on('activate.bs.scrollspy', function (e) {
//   window.console.log( e );
//})
    </script>

</body>
</html>
        """);

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
