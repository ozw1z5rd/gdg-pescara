from template import TemplateBase

class AddCapsuleFormTemplate(TemplateBase):
    def html(self):
        return """
          <form action="/add" method="POST">
          <ul>
              <li>Opening Date:<input type="text" name="txtOpenDate"></input>
              <li>Closing Date:<input type="text" name="txtCloseDate"></input>
              <li>Content:<input type="text" name="txtContent"></input>
              <li>latitude:<input type="text" name="txtLatitude"></input>
              <li>longitude:<input type=text" name="txtLongitude"></input>
              <li>Tollerance:<input type="text" name="txtTollerance"></input>
              <input type="submit">
          </form>
        """

class AddCapsuleOkTemplate(TemplateBase):
    def html(self):
        return """
            <h3>Capsule created</h3>
            <br>Capsule id:<b>{{tscid}}</b>
            <ul>
            <li>opening date:{{openingDate}}
            <li>closing date:{{closingDate}}
            <li>Content: {{content}}
            <li>latitude: {{latitude}}
            <li>longitude: {{longitude}}
            <li>tollerance(m): {{tollerance}}
            </ul>
        """

class AddCapsuleKoTemplate(TemplateBase):
    def html(self):
        return """
            <h3>Capsule Not created</h3>
        """