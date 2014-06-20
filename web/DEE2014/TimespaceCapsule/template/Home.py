from template import TemplateBase

class HomeTemplate(TemplateBase):
    def html(self):
        return """
        <h3>Current menu</h3>
        <ol>
        <li><a href="{{add_url}}">Add a new TSC</a>
        </ol>
        <hr>
        <h3>listing all the added capsules</h3>
        <p>red are not yet open, black have been opened
        {{html}}
        <hr>
    """