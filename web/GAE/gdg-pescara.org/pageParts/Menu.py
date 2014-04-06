# -*- coding: latin-1 -*-
import string

class Menu( object ):
    def getContent( self, user, login_url, logout_url ):
     
        if user is None:
             url=login_url
             text="Login"
        else:
            url=logout_url
            text=str(user).split("@")[0]
         
        return """
  <div class="container">
    <div class="navbar navbar-inverse navbar-fixed-top" id="my-navbar">

      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
          <span class="icon-bar"></span> <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="%s">%s</a>
      </div> <!-- navbar-header -->

      <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav">
          <li class="active"><a href="#home"><span class="G1">01</span>.Benvenuto</a></li>
          <li><a href="#developer"><span class="O1">02.</span> Sviluppatori</a></li>
          <li><a href="#people"><span class="O2">03.</span> Gruppo</a></li>
          <li><a href="#work"><span class="G2">04.</span> Programma</a></li>
          <li><a href="#indice"><span class="L">05.</span> Indice</a></li>
          <li><a href="#thanks"><span class="E">06.</span> Grazie</a></li>
        </ul>
      </div>
      <!--/.nav-collapse -->
    </div> <!-- navbar .. -->
  </div> <!-- container -->
        """ % ( url, text )
