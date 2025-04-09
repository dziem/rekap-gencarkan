import pandas as pd
import numpy as np
import os
import warnings
from difflib import get_close_matches as gcm
import editdistance

warnings.simplefilter(action='ignore', category=UserWarning)

def searchSektor(name):
    mins = 99999
    correctName = ''
    z = -1
    x = -1
    for j in pujk:
        x = x + 1
        newMins = editdistance.eval(name.lower().strip(), j.lower())
        if (newMins < mins):
            mins = newMins
            correctName = j 
            z = x
    if (mins < 2):
        return sektor[z]
    else:
        return 'N/A'

def clean(a):
    return a.lower().strip()

'''
def bulan(col, bulans):
    gcm1 = gcm(col, bulans, 1, 0.8)
    if (len(gcm1) > 0):
        return gcm1[0]
    else:
        return 'Invalid'
'''

def bulan(col, bulans):
    mins = 99999
    correctName = ''
    z = -1
    x = -1
    for j in bulans:
        x = x + 1
        newMins = editdistance.eval(col.lower().strip(), j.lower())
        if (newMins < mins):
            mins = newMins
            correctName = j 
            z = x
    if (mins < 3):
        return bulans[z]
    else:
        return 'Invalid'
        
def provinsiManual(col):
    p = clean(col)
    if 'yogyakarta' in p:
        return 'Daerah Istimewa Yogyakarta'
    elif 'jakarta' in p:
        return 'DKI Jakarta'
    elif 'bangka belitung' in p:
        return 'Kepulauan Bangka Belitung'
    elif p == 'kepri':
        return 'Kepulauan Riau'
    else:
        p = p.replace('sumatra', 'sumatera')
        return p.title().strip()
 
def provinsi(col, provs):
    p = provinsiManual(col)
    if p not in provs:
        mins = 99999
        correctName = ''
        z = -1
        x = -1
        for j in provs:
            x = x + 1
            newMins = editdistance.eval(p.lower().strip(), j.lower())
            if (newMins < mins):
                mins = newMins
                correctName = j 
                z = x
        if (mins < 3):
            return provs[z]
        else:
            return 'Blank'
    else:
        return p

def kabkotaManual(col):
    k = clean(col)
    if 'administrasi' in k:
        return k.replace("administrasi", "Adm.").title()
    elif 'jakarta' in k and 'adm' not in k:
        return 'Kota Adm. ' + k.title()
    else:
        return k.title()
        
def kabkota(col, kabs):
    kabb = kabkotaManual(col)
    if kabb not in kabs:   
        mins = 99999
        correctName = ''
        z = -1
        x = -1
        for j in kabs:
            x = x + 1
            for k in ['Kota ', 'Kabupaten ']:
                checking = k + kabb
                newMins = editdistance.eval(checking.lower().strip(), j.lower())
                if (newMins < mins):
                    mins = newMins
                    correctName = j 
                    z = x
        if (mins < 3):
            return kabs[z]
        else:
            return '-'
    else:
        return kabb
 
def namaKeg(col):
    n = clean(col)
    stat = 'Valid'
    if n == '':
        stat = 'Invalid'
    if n == '-':
        stat = 'Invalid'
    if 'nihil' in n:
        stat = 'Invalid'
    if n == 'nihil':
        stat = 'Invalid'
    if n == '0':
        stat = 'Invalid'
    if n == 'belum ada kegiatan' or ('belum' in n and 'kegiatan' in n):
        stat = 'Invalid'
    if n == 'null':
        stat = 'Invalid'
    if n == 'tidak ada' or (('tidak' in n or 'tdk' in n) and 'kegiatan' in n):
        stat = 'Invalid'
    return stat
    
def segmen(col):
    seg = clean(col)
    if 'perempuan' in seg or 'ibu' in seg or 'wanita' in seg or 'pkk' in seg or 'irt' in seg:
        return 'Perempuan / Ibu Rumah Tangga'
    elif 'pelajar' in seg or 'mahasiswa' in seg or 'siswa' in seg or 'mahasiswi' in seg or 'siswi' in seg or 'pemuda' in seg or 'santri' in seg or 'muda' in seg:
        return 'Pelajar / Mahasiswa / Pemuda'
    elif 'profesional' in seg or 'profesi' in seg or 'guru' in seg or 'dosen' in seg or 'jurnalis' in seg or 'direktur' in seg or 'tni' in seg or 'polri' in seg:
        return 'Profesional'
    elif 'petani' in seg or 'tani' in seg or 'nelayan' in seg:
        return 'Petani / Nelayan'
    elif 'pmi' in seg or 'tki' in seg or 'migran' in seg:
        return 'PMI / Calon PMI / Keluarga PMI'
    elif '3t' in seg or 'tertinggal' in seg or 'terpencil' in seg or 'terluar' in seg or 'desa' in seg:
        return 'Masyarakat Daerah Perdesaan / 3T'
    elif 'komunitas' in seg:
        return 'Komunitas'
    elif 'umkm' in seg or 'dagang' in seg or 'usaha' in seg:
        return 'UMKM'
    elif 'disabilitas' in seg or 'difabel' in seg:
        return 'Penyandang Disabilitas'
    elif 'karyawan' in seg or 'pekerja' in seg or 'asn' in seg or 'pns' in seg or 'pegawai negeri' in seg or 'aparat' in seg or 'pegawai' in seg or 'staf' in seg:
        return 'Karyawan'
    elif 'pensiun' in seg:
        return 'Pensiunan'
    elif 'pmks' in seg:
        return 'Penyandang Masalah Kesejahteraan Sosial (PMKS)'
    elif 'umum' in seg or 'nasabah' in seg or 'peserta' in seg:
        return 'Masyarakat Umum'
    else:
        return 'Lainnya'
        
def bentuk(col):
    ben = clean(col)
    if 'edukasi' in ben and 'digital' in ben:
        return 'Edukasi Digital'
    elif 'publikasi' in ben and 'digital' in ben:
        return 'Publikasi Digital'
    elif 'edukasi' in ben and 'langsung' in ben:
        return 'Edukasi Langsung'
    elif 'training of trainers' in ben:
        return 'Training of Trainers (ToT)'
    else:
        return 'Blank'
        
def jenis(col):
    ben = clean(col)
    if 'dan' in ben:
        return 'Konvensional dan Syariah'
    elif 'konven' in ben:
        return 'Konvensional'
    elif 'syar' in ben:
        return 'Syariah'
    else:
        return 'Blank'
        
def sektor(col, pujk, pujks):
    gcm1 = gcm(col, pujks, 1, 0.9)
    if (len(gcm1) > 0):
        pujkIndex = pujk.index[pujk["Nama PUJK"] == gcm1[0]]
        return pujk.loc[pujkIndex,'Nama Sektor'].values[0]
    else:
        return '-'

def peserta(col):
    pes = str(col)
    pes = pes.replace(',', '')
    if pes.isdigit():
        return int(pes)
    else:
        return 0

master = pd.read_excel('master.xlsx', na_filter=False, sheet_name=None)
bulans = master["Bulan"]["Bulan"].values.tolist()
provs = master["Provinsi"]["Provinsi"].values.tolist()
kabs = master["KabKota"]["Kab/Kota"].values.tolist()
pujk = pd.read_excel('pujk.xlsx', na_filter=False)
pujks = pujk["Nama PUJK"].values.tolist()
deleting = []
#data = pd.read_excel('testing.xlsx', na_filter=False)
data = pd.read_excel('Gencarkan - Result 2.xlsx', na_filter=False)
count = 0
rows = len(data.index)
for i in range(0, rows):
    rowIndex = data.index[i]
    
    #periode bulan
    month = data.loc[rowIndex,'Periode (Bulan)']
    if month.strip():
        newMonth = bulan(month, bulans)
        if (newMonth == 'Invalid'):
            deleting.append(i)
        else:
            data.loc[rowIndex,'Periode (Bulan)'] = newMonth
    else:
        deleting.append(i)
        
    #provinsi
    data.loc[rowIndex,'Provinsi'] = provinsi(data.loc[rowIndex,'Provinsi'], provs)
    
    #kab/kota
    data.loc[rowIndex,'Kabupaten/ Kota'] = kabkota(data.loc[rowIndex,'Kabupaten/ Kota'], kabs)
        
    #clean nama kegiatan
    nama = data.loc[rowIndex,'Nama Kegiatan']
    checkNama = namaKeg(nama)
    if checkNama == 'Invalid':
        deleting.append(i)
        
    #segmen
    data.loc[rowIndex,'Segmen Sasaran'] = segmen(data.loc[rowIndex,'Segmen Sasaran'])
    
    #Jenis
    jeniss = jenis(data.loc[rowIndex,'Jenis Kegiatan'])
    data.loc[rowIndex,'Jenis Kegiatan'] = jeniss
    
    #Jumlah Peserta
    data.loc[rowIndex,'Jumlah Peserta / Viewers'] = peserta(data.loc[rowIndex,'Jumlah Peserta / Viewers'])
    
    #bentuk
    data.loc[rowIndex,'Klasifikasi Kegiatan'] = bentuk(data.loc[rowIndex,'Klasifikasi Kegiatan'])
    
    #sektor
    data.loc[rowIndex,'Sektor PUJK'] = sektor(data.loc[rowIndex,'Nama PUJK'], pujk, pujks)
    
    #geraks
    if ' - GERAKS' in newMonth and 'Syariah' not in jeniss:
        data.loc[rowIndex,'Periode (Bulan)'] = newMonth.replace(" - GERAKS", "") 

print(deleting)
data.reset_index()
data.drop(deleting, axis=0, inplace=True)

data.to_excel("Gencarkan - Result 2 Clean.xlsx", index=False)
#data.to_excel("testing res.xlsx", index=False)