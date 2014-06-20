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
            Content: <a href="{{content}}">{{content}}</a>
        """

class OpenCapsuleErrorTemplate(TemplateBase):
    def head(self):
        return """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Timespace Capsule</title>
                    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

                    <script>
                        var id_watch = null;
                        var tscid={{tscid}};
                        var distance = null;
                        var curr_lat;
                        var curr_lng;
                        var host = "{{host}}"

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
            Can't open the capsule, {{message}}
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
    def head(self):
        return """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Timespace Capsule</title>
            </head>
        """


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