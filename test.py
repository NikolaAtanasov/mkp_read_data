import urllib.request
import zipfile
import os
import fnmatch
import shutil
import csv
import re

class Station:
  id = None
  recording_start = None
  recording_end = None
  height = None
  latitude = None
  longitude = None
  name = None
  state = None

  def __init__(self, id, recording_start, recording_end, height, latitude, longitude, name, state):
    self.id = id
    self.recording_start = recording_start
    self.recording_end = recording_end
    self.height = height
    self.latitude = latitude
    self.longitude = longitude
    self.name = name
    self.state = state


class StationData:
  stations_id = None
  mess_datum = None
  qn_3 = None
  fx = None
  fm = None
  qn_4 = None
  rsk = None
  rskf = None
  sdk = None
  shk_tag = None
  nm = None
  vpm = None
  pm = None
  tmk = None
  upm = None
  txk = None
  tnk = None
  tgk = None
  eor = None

  def __init__(self, stations_id,mess_datum,qn_3,fx,fm,qn_4,rsk,rskf,sdk,shk_tag,nm,vpm,pm,tmk,upm,txk,tnk,tgk,eor):
    self.station_id = stations_id
    self.mess_datum = mess_datum
    self.qn_3
    self.fx = fx
    self.fm = fm
    self.qn_4 = qn_4
    self.rsk = rsk
    self.rskf = rskf
    self.sdk = sdk
    self.shk_tag = shk_tag
    self.nm = nm
    self.vpm = vpm
    self.pm = pm
    self.tmk = tmk
    self.upm = upm
    self.txk = txk
    self.tnk = tnk
    self.tgk = tgk
    self.eor = eor


class DWD:

  file_prefix = "tageswerte_KL_"
  file_suffix = "_akt.zip"
  file_url = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/"
  station_list = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/KL_Tageswerte_Beschreibung_Stationen.txt"


  #parameter: -
  #return: list of all stations
  def get_stations(self):
    urllib.request.urlretrieve(self.station_list, "temp")
    with open("temp", 'r', encoding='cp1252') as f:
      lines = f.readlines()

    stations = []

    for x in range(2,len(lines)):
      lines[x] = re.sub(' +','',lines[x])
      line = lines[x].split('')
      new_station = Station(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
      stations.append(new_station)

    os.remove("temp")

    return stations

  #parameter: id of station
  #return: list of station data
  def get_station_data(self, station_id):
    local_file = "station_" + station_id

    urllib.request.urlretrieve(self.file_url + self.file_prefix + station_id + self.file_suffix, local_file + ".zip")
    zip_ref = zipfile.ZipFile(local_file + ".zip", 'r')
    zip_ref.extractall(local_file)
    zip_ref.close()
    os.remove(local_file + ".zip")

    for file in os.listdir(local_file):
      if fnmatch.fnmatch(file, "produkt_klima_tag*"):
        os.rename(local_file + "/"+ file, local_file + ".csv")

    shutil.rmtree(local_file)

    data = []

    with open(local_file + ".csv") as csvfile:
      readCSV = csv.reader(csvfile, delimiter='')
      first_row = True
      for row in readCSV:
          if(first_row == False):
            data.append(StationData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18]))
          else:
            first_row = False
    os.remove(local_file + ".csv")
    return data

dwd = DWD()

data_set = dwd.get_station_data("00078")
stations = dwd.get_stations()