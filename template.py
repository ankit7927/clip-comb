import json

class Template:
    MEDIA_HEIGHT:int=None
    VERTICAL:bool = None
    MEDIA_POSITION:list = None
    MEDIA_POSITION_RELATIVE:bool = None
    FONT_SIZE:int = None
    FONT_WEIGH:str =None
    TEXT_SIZE:int = None
    TEXT_POSITION:list = None
    TEXT_POSITION_RELATIVE:bool = None
    CLIP_DURATION:str = None

    def __init__(self, template_name:str) -> None:
        temps = self.template_reader()
        template:object = temps[template_name]
        
        self.MEDIA_HEIGHT = template[""]


    def template_reader(self) ->object:
        f = open("template.json", "r")
        return json.loads(f.read())

Template("v3")



