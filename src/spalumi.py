from requests_html import HTMLSession
from bs4 import BeautifulSoup

enlaces = {
    "AcompanantesMadrid": "/f4/",
    "CallejerasMadrid": "/f45/",
    "AgenciasMadrid": "/f40/",
    "ClubesMadrid": "/f5/",
    "Masde40Madrid": "/f6/",
    "ChicasVIPMadrid": "/f7/",
    "MasajesEroticosMadrid": "/f8/",
    "TravestisMadridyTransexuales": "/f13/",
    "SeXtremeMadrid": "/f87/",
    "FotosFalsasMadrid": "/f10/",
    "NuevosubforodeMasajistasyAcompanantes": "/f303/",
    "SUBFORODEINFORMACIONYOPINIONESDELACOMUNIDADVALENCIANAyMURCIA": "/f21/",
    "AcompanantesValencia": "/f29/",
    "AcompanantesAlicante": "/f48/",
    "AcompanantesMurcia": "/f47/",
    "AcompanantesCastellon": "/f49/",
    "TravestisValenciayTransexuales": "/f150/",
    "SUBFORODEINFORMACIONYOPINIONESDEEUSKADIYNAVARRA": "/f59/",
    "Acompanantesalava": "/f139/",
    "AcompanantesGuipuzcoa": "/f140/",
    "Vizcaya": "/f141/",
    "NuevosubforodeMasajistasyAcompanantesEuskadi": "/f304/",
    "AcompanantesNavarra": "/f219/",
    "FotosfalsasEuskadiyNavarra": "/f220/",
    "SUBFORODEINFORMACIONYOPINIONESDEGALICIA": "/f57/",
    "ACoruna": "/f144/",
    "AcompanantesLugo": "/f145/",
    "AcompanantesOurense": "/f146/",
    "AcompanantesPontevedra": "/f147/",
    "SUBFORODEINFORMACIONYOPINIONESDEARAGON": "/f19/",
    "Zaragoza": "/f28/",
    "AcompanantesTeruel": "/f123/",
    "AcompanantesHuesca": "/f122/",
    "SUBFORODEINFORMACIONYOPINIONESDEANDALUCiA": "/f18/",
    "Sevilla": "/f26/",
    "AcompanantesCordoba": "/f66/",
    "AcompanantesCadiz": "/f67/",
    "AcompanantesGranada": "/f64/",
    "AcompanantesHuelva": "/f68/",
    "AcompanantesJaen": "/f65/",
    "AcompanantesMalaga": "/f63/",
    "TravestisAndaluciayTransexuales": "/f149/",
    "AcompanantesAlmeria": "/f69/",
    "SUBFORODEINFORMACIONYOPINIONESDECASTILLA-LEON": "/f54/",
    "AcompanantesAvila": "/f131/",
    "AcompanantesBurgos": "/f132/",
    "AcompanantesLeon": "/f133/",
    "AcompanantesPalencia": "/f134/",
    "AcompanantesSalamanca": "/f135/",
    "AcompanantesSegovia": "/f136/",
    "AcompanantesSoria": "/f137/",
    "AcompanantesValladolid": "/f27/",
    "AcompanantesZamora": "/f138/",
    "SUBFORODEINFORMACIONDECASTILLALAMANCHA": "/f23/",
    "AcompanantesAlbacete": "/f126/",
    "AcompanantesCiudadReal": "/f127/",
    "AcompanantesCuenca": "/f128/",
    "AcompanantesGuadalajara": "/f129/",
    "AcompanantesToledo": "/f130/",
    "SUBFORODEINFORMACIONYOPINIONESDEEXTREMADURA": "/f55/",
    "AcompanantesBadajoz": "/f142/",
    "AcompanantesCaceres": "/f143/",
    "SUBFORODEINFORMACIONYOPINIONES:MASAUTONOMIAS": "/f24/",
    "AcompanantesAsturias": "/f20/",
    "AcompanantesBaleares": "/f53/",
    "AcompanantesCanarias": "/f60/",
    "AcompanantesCantabria": "/f56/",
    "AcompanantesCeuta": "/f61/",
    "AcompanantesLaRioja": "/f22/",
    "AcompanantesMelilla": "/f62/",
    "SUBFORODEINFORMACIONYOPINIONESDECATALUnA": "/f70/",
    "AcompanantesBarcelona": "/f72/",
    "PisosyAgenciasBarcelona": "/f73/",
    "ClubesBarcelona": "/f74/",
    "AcompanantesdelujoBarcelonayChicasVip": "/f75/",
    "AcompanantesGirona": "/f50/",
    "AcompanantesLleida": "/f51/",
    "AcompanantesTarragona": "/f52/",
    "FotosfalsasdeCataluna": "/f236/",
    "SUBFORODEINFORMACIONYOPINIONESDEELMUNDO": "/f71/",
    "TVMundo": "/f151/",
    "AcompanantesAmerica": "/f81/",
    "AcompanantesAfrica": "/f82/",
    "AcompanantesAsia": "/f83/",
    "AcompanantesEuropa": "/f84/",
    "AcompanantesOceania": "/f85/",
    "SUBFOROGENERALWWW.SPALUMI.COM": "/f3/",
    "TODOSOBRESPALUMI": "/f16/",
    "TemasGeneralesTodaslascomunidades": "/f15/",
    "ConsultaMedicaTodaslascomunidades": "/f9/",
}

session = HTMLSession()
r = session.get("https://spalumi.com/")
r.html.render()
soup = BeautifulSoup(r.html.find("a", first=True).html, "html.parser")
