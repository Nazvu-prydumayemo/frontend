from textual.widgets import Input

class CustomInput(Input):
    
    pass

class PasswordInput(Input):
   
    def __init__(self, **kwargs):
        super().__init__(password=True, **kwargs)