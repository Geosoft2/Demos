library("openeo")
library("ncdf4")

# Verbindung zum Backend aufbauen
con = connect(host = "http://localhost/api/v1")

# Prozesse abrufen
p = processes()

# Parameter Uebersicht
p

# Mit processes Objekt einen Prozessgraphen bauen 
# Hier kann es zu Komplikationen kommen, da der Parameter im Prozess JSON und der Parameter der internene Funktion anders benannt sind
# Konkret 'Collection' im JSON und 'DataType' in der internen Funktion 
load = p$load_collection(timeframe=c('01-12-1981 00:00:00','31-12-1981 00:00:00','%d-%m-%Y %H:%M:%S'), DataType='SST') 
sst  = p$mean_sst(data=load, timeframe=c('1981-12-01', '1981-12-15'), bbox=c(-999,-999,-999,-999))
save = p$save_result(SaveData=sst, Format='netcdf' ) 

#Aus den einzelnen Prozessen einen Graph erzeugen
graph = as(save, "Graph")

graph

# Job erzeugen
job = create_job(graph=graph,title = "Cooler Title", description = "Dolle Beschreibung")

# Job starten
start_job(job=job)

# Nachdem Durchlaufen des Jobs Ergebnis herunterladen 
result = download_results(job = job, folder = (getwd()))

# Bearbeitung fuer Darstellung des Ergebnis mit interner image Funktion
ncin <- nc_open(result[[1]])
tmp_array <- ncvar_get(ncin,'sst')
lat <- ncvar_get(ncin,'lat')
lon <- ncvar_get(ncin,'lon')

image(lon,lat,tmp_array)
