class ngrok:

  def __init__(self, TOKEN=None,
               service=[['Service1', 80, 'tcp'], ['Service2', 8080, 'tcp']],
               region='us',
               dBug=[f"{HOME}/.ngrok2/ngrok.yml", 4040]):
    self.region = region
    self.configPath, self.dport = dBug
    self.TOKEN = TOKEN
    self.service = service

  def nameport(self, TOKEN, AUTO):
    if AUTO:
        try:
            return tokens.popitem()[1]
        except KeyError:
            return "Invalid Token"
    elif not TOKEN:
        if not 'your' in tokens.keys():
            from IPython import get_ipython
            from IPython.display import clear_output
            ipython = get_ipython()

            print(r"Copy authtoken from https://dashboard.ngrok.com/auth")
            __temp = ipython.magic('%sx read -p "Token :"')
            tokens['your'] = __temp[0].split(':')[1]
            USR_Api = "your"
            clear_output()
        else:
            USR_Api = "your"
    else:
        USR_Api = "mind"
        tokens["mind"] = TOKEN
    return tokens[USR_Api]


  def ngrok_config(self, token, Gport, configPath, region, service):
    import os
    data = """
    region: {}
    update: false
    update_channel: stable
    web_addr: localhost:{}
    tunnels:\n""".format(region, Gport)
    if not self.USE_FREE_TOKEN:
      auth ="""
    authtoken: {}""".format(token)
      data = auth+data
    tunnels = ""
    for S in service:
        Sn, Sp, SpC = S
        tunnels += """      {}:
        addr: {}
        proto: {}
        inspect: false\n""".format(Sn, Sp, SpC)
    data = data + tunnels
    os.makedirs(f'{HOME}/.ngrok2/', exist_ok=True)
    with open(configPath, "w+") as configFile:
        configFile.write(data)
    return True


  def startWebUi(self, token, dport, nServer, region, btc, configPath,
               displayB, service, v):
    import os, time, urllib
    from IPython.display import clear_output
    from json import loads

    if token == "Invalid Token":
        print(tokens)
        os.exit()

    installNgrok()
    if v:
      clear_output()
      loadingAn(name="lds")
      textAn("Starting ngrok ...", ty='twg')
    if self.USE_FREE_TOKEN:
      for sn in service:
        self.ngrok_config(
          token,
          self.sdict[nServer][0],
          self.sdict[nServer][2],
          region,
          service)
        if sn[0] == nServer:
          runSh(f"ngrok {sn[2]} -config={self.sdict[nServer][2]} {sn[1]} &", shell=True)
    else:
      self.ngrok_config(token, dport, configPath, region, service)
      runSh(f"ngrok start --config {configPath} --all &", shell=True)
    time.sleep(3)
    try:
        if self.USE_FREE_TOKEN:
          dport = self.sdict[nServer][0]
          nServer = 'command_line'
          host = urllib.request.urlopen(f"http://localhost:{dport}/api/tunnels")
        else:
          host = urllib.request.urlopen(f"http://localhost:{dport}/api/tunnels")
        host = loads(host.read())['tunnels']
        for h in host:
          if h['name'] == nServer:
            host = h['public_url'][8:]
            break
    except urllib.error.URLError:
        if v:
          clear_output()
          loadingAn(name="lds")
          textAn("Ngrok Token is in used!. Again trying token ...", ty='twg')
        time.sleep(2)
        return True

    data = {"url": f"http://{host}"}
    if displayB:
      displayUrl(data, btc)
    return data


  def start(self, nServer, btc='b', displayB=True, v=True):
    import urllib
    from IPython.display import clear_output
    from json import loads

    try:
      nServerbk = nServer
      dport = self.dport
      host = urllib.request.urlopen(f"http://localhost:{dport}/api/tunnels")
      host = loads(host.read())['tunnels']
      for h in host:
        if h['name'] == nServer:
          host = h['public_url'][8:]
          data = {"url": f"http://{host}"}
          if displayB:
            displayUrl(data, btc)
          return data

      raise Exception('Not found tunnels')
    except urllib.error.URLError:
      for run in range(10):
        if v:
          clear_output()
          loadingAn(name='lds')
        dati = self.startWebUi(
            self.nameport(self.TOKEN, self.USE_FREE_TOKEN) if not self.USE_FREE_TOKEN else {},
            self.dport,
            nServerbk,
            self.region,
            btc,
            self.configPath,
            displayB,
            self.service,
            v
            )
        if dati == True:
            continue
        return dati
