from template import TemplateBase

class HomeTemplate(TemplateBase):
    def html(self):
        return """
        <h3>Current menu</h3>
        <ol>
        <li>Register a new TSC <a href="{{register_url}}">Here</a> DEBUG
        <li><a href="{{add_url}}">Add a new TSC</a>
        <li><a href="{{open_url}}">Open (request)</a>
        </ol>
        <hr>
        <h3>listing all the added capsules</h3>
        <p>red are not yet open, black have been opened
        {{html}}
        <hr>
    """