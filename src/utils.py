
class User :

    def __init__(self, name, api_key, api_secret, paper_trading) :
        self.name = name 
        self.api_key = api_key 
        self.api_secret= api_secret 
        self.paper_trading = paper_trading  



class Error :

    def __init__(self, error_message, error=None) :
        self.error_message = error_message
        self.error= error 


