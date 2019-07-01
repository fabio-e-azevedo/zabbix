[14/06 17:05] Fabio Eduardo
    

#!/usr/bin/env python
# Discovery de valores de uma macro
# O delimitador em um valor e outro de ser o | (pipe), exemplo: fabio|azevedo
# Exemplo do retorno JSON:
# {
#     "data": [
#         {
#             "{#NAME}": "fabio"
#         },
#         {
#             "{#NAME}": "azevedo"
#         }
#     ]
# }
# Obrigatorio 2 argumentos: Hostname e Nome da Macro (sem as chaves e sem o cifrao) 
# Exemplo: discovery_macro.py[{HOST.HOST},DISCOVERY]
# Modulos dependentes: ZabbixAPI e ConfigParser
# 

import sys
import json
from zabbix_api import ZabbixAPI
import ConfigParser
from os import path

fileconf = '/etc/zabbix/api_script.conf'

if path.exists(fileconf):
  config = ConfigParser.RawConfigParser()
  config.read(fileconf)
else:
  sys.exit(1)

zapi = ZabbixAPI(server=config.get('DEFAULT', 'URL'))
zapi.validate_certs = False
zapi.login(config.get('DEFAULT', 'User'), config.get('DEFAULT', 'Password'))

hostname = sys.argv[1]
macro = '{$' + sys.argv[2] + '}'

host = zapi.host.get({ "output": "extend", "filter": {"name": hostname}, "selectMacros": ["macro", "value"] })
values = next((str(item["value"]) for item in host[0]["macros"] if macro in item["macro"])).split('|')

result_json =[]
for v in values:
 element = {'{#NAME}': v}
 result_json.append(element)
print json.dumps({'data': result_json}, indent=4)
sys.exit(0)

