from template import TemplateBase

class GeolocationTemplate(TemplateBase):

    def head(self):
        return """
            <!DOCTYPE HTML>
            <html>
            <head>
                <title>Timespace Capsule</title>

                    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

                    <script>
                        var id_watch = null;
                        var tscid=5383208929591296;
                        var distance = null;
                        var curr_lat;
                        var curr_lng;
                        var host = "http://127.0.0.1:8080/"

                        inCasoDiSuccesso = function(position){

                            curr_lat = position.coords.latitude
                            curr_lng = position.coords.longitude
                            $.get( host + "radar?tscid="+tscid+"&lat="+curr_lat+"&lng="+curr_lng,
                                function( data ) {
                                     d = data.split("|")
                                     rc = d[0]
                                     distance = d[1]
                                     $( ".result" ).html( distance );
                            });
                        }

                        sospendiLaRicezione = function(){
                            navigator.geolocation.clearWatch(id_watch);
                        }

                        window.onload = function(){
                            id_watch = navigator.geolocation.watchPosition(inCasoDiSuccesso);
                        }

                    </script>
                <title>TemplateBase head</title>
            </head>
        """

    def html(self):
        return """

            <h2>Distance from the opening location</h2>
            <b><p class="result"></p></b>

             <button type="button" onclick="sospendiLaRicezione()">
                 Stop Geolocation
             </button>
        """