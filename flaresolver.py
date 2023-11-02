from requests import post, exceptions, Response
from requests import get as g
from json import loads



class FlareSolverrProxy():

    def __init__(self, domain : str,flareSolverrURL :str, timeout : int | None = 60000) -> None:
        self.__flaresolverrurl = flareSolverrURL
        self.__domain = domain
        self.__cookies = None
        self.__userAgent = None
        self.__timeout = timeout
        self.__data = {
            "cmd" : "request.get",
            "url" : self.__domain,
            "maxTimeout" : self.__timeout

        }

        self.get_cookies_and_userAgent()

    def get_cookies_and_userAgent(self):
        try:
            response = post(self.__flaresolverrurl, json=self.__data, headers={'Content-Type': 'application/json'})
        except (exceptions.RequestException) as e:
            self.__cookies = None
            self.__userAgent = None

        if response.status_code == 200:
            response_data = loads(response.content)
            cookies = response_data["solution"]["cookies"]
            self.__cookies = {cookie["name"] : cookie["value"] for cookie in cookies}

            self.__userAgent = response_data["solution"]["userAgent"]


        else:
            raise exceptions.ProxyError(response=response)

    def get(self, url : str) -> Response :
        args = {"url": url, 
                "cookies": self.__cookies, 
                "headers" : {"User-Agent": self.__userAgent}
            }
        
        response = g(**args)
        if response.status_code == 200:
            return response
        elif response.status_code == 403:
            self.get_cookies_and_userAgent()
            response = g(**args)
            return response
        else:
            raise exceptions.ProxyError(response=response)

        