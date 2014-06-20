#     This file is part of Timespace Capsule.
#
#     Timespace Capsule is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Timespace Capsule is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Timespace Capsule.  If not, see <http://www.gnu.org/licenses/>.
#
#     Alessio Palma / 2014
#     fb.com/alessio.palma
#     https://sites.google.com/site/ozw1z5rd/

from template import TemplateBase

class OpenCapsuleTemplate(TemplateBase):
    def html(self):
        return """
            <p>Content: <a href="{{content}}">{{content}}</a></p>
        """

class OpenCapsuleErrorTemplate(TemplateBase):
    def head(self):
        # make me better
        return """
            <!DOCTYPE HTML>
            <html>
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="description" content="">

                <!-- Bootstrap core CSS -->
                <link href="css/bootstrap.css" rel="stylesheet">

                <!-- Custom styles for this template -->
                <link href="css/style.css" rel="stylesheet">

                <!-- Google web Font -->
                <link href='http://fonts.googleapis.com/css?family=Lato:300,400,700,900,100'  rel='stylesheet' type='text/css'>

                <!-- Just for debugging purposes. Don't actually copy this line! -->
                <!--[if lt IE 9]><script src="../../docs-assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

                <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
                <!--[if lt IE 9]>
                      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
                      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
                <![endif]-->

                <title>Timespace Capsule</title>
                    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

                    <script>
                        var id_watch = null;
                        var tscid={{tscid}};
                        var distance = null;
                        var curr_lat;
                        var curr_lng;
                        var host = "{{host}}";

                        inCasoDiSuccesso = function(position){

                            curr_lat = position.coords.latitude
                            curr_lng = position.coords.longitude
                            $.get( host + "/radar?tscid="+tscid+"&lat="+curr_lat+"&lng="+curr_lng,
                                function( data ) {
                                     d = data.split("|")
                                     rc = d[0]
                                     distance = d[1]
                                     $( ".result" ).html( distance );
                                     $('#lat').val(curr_lat )
                                     $('#lng').val( curr_lng )
                            });
                        }

                        sospendiLaRicezione = function(){
                            navigator.geolocation.clearWatch(id_watch);
                        }

                        window.onload = function(){
                            id_watch = navigator.geolocation.watchPosition(inCasoDiSuccesso);
                        }

                    </script>
            </head>
        """


    def html(self):
        return """
        <form id="formActivate" action="{{host}}/activate" method="GET">
        <p class="bg-danger">Can't open the capsule, {{message}}</p>
        <hr>
            <ul>
              <li>Open not before: {{openingDate}}
              <li>and not after: {{closingDate}}
              <li>{{space}}
            </ul>

            <h2>Distance from the opening location</h2>
            <b><p class="result"></p></b>

             <button id="bntStop" type="button" onclick="sospendiLaRicezione()">
                 Stop Geolocation
             </button>

            <input type="hidden" id="tscid"name="tscid" value="{{tscid}}">
            <input type="hidden" id="lat" name="lat" value="0">
            <input type="hidden" id="lng" name="lng" value="0">
            <button id="bntOpen" type="submit" >
                Try to open
            </button>
            </form>
        """


class OpenCapsuleErrorTemplateNoGeo(TemplateBase):


    def html(self):
        return """
        <form id="formActivate" action="{{host}}/activate" method="GET">
            Can't open the capsule, {{message}}
            <hr>
            <ul>
              <li>Open not before: {{openingDate}}
              <li>and not after: {{closingDate}}
              <li>{{space}}
            </ul>

            <input type="hidden" id="tscid"name="tscid" value="{{tscid}}">
            <button id="bntOpen" type="submit" >
                Try to open
            </button>
            </form>
        """
