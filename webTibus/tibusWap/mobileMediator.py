'''
Created on 15/02/2013

@author: diego
'''
import re

class RequestMobileMiddleware(object):
    def process_request(self, request):
        is_mobile = False;
        is_http_mobile = False;
        
        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront|android|ipad|iphone)"
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)

            if match:
                is_mobile = True;
            else:
                # Test for WAP browsers.
                if request.META.has_key('HTTP_ACCEPT'):
                    http_accept = request.META['HTTP_ACCEPT']
                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog = re.compile(pattern, re.IGNORECASE)
                    match = prog.search(http_accept)
                    if match:
                        is_mobile = True

            if not is_mobile:
                # Verifica el user_agent de una lista. Actualizar la lista, por lo menos, una vez cada 3 meses.
                user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
                                    "avan", "benq", "bird", "blac", "blaz", "brew",
                                    "cell", "cldc", "cmd-", "dang", "doco", "eric",
                                    "hipt", "inno", "ipaq", "java", "jigs", "kddi",
                                    "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
                                    "maui", "maxo", "midp", "mits", "mmef", "mobi",
                                    "mot-", "moto", "mwbp", "nec-", "newt", "noki",
                                    "xda",  "palm", "pana", "pant", "phil", "play",
                                    "port", "prox", "qwap", "sage", "sams", "sany",
                                    "sch-", "sec-", "send", "seri", "sgh-", "shar",
                                    "sie-", "siem", "smal", "smar", "sony", "sph-",
                                    "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
                                    "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
                                    "wapi", "wapp", "wapr", "webc", "winw", "winw",
                                    "xda-",)

                test = user_agent[0:4].lower()
                if test in user_agents_test:
                    is_mobile = True

        request.is_mobile = is_mobile
        if is_mobile:
            if request.META.has_key('HTTP_ACCEPT'):
                http_accept = request.META['HTTP_ACCEPT']
                pattern = "text/html"
                prog = re.compile(pattern, re.IGNORECASE)
                match = prog.search(http_accept)
                if match:
                    is_http_mobile = True
        request.is_http_mobile = is_http_mobile

class ResponseMobileMiddleware(object):
    def process_response(self, request, response):
        if request.META.has_key('is_mobile') and request.META.has_key('is_http_mobile') and request.is_mobile and not request.is_http_mobile:
                response['Content-Type'] = "text/vnd.wap.wml"
        return response