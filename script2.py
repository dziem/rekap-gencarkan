import pandas as pd
import numpy as np
import os
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

template = pd.read_excel('col_template2.xlsx')
replacement = pd.read_excel('col_replace2.xlsx')
file = pd.read_excel('Laporan Gencarkan Monthly Gabungan.xlsx', sheet_name=None)
'''
popSheet = [
    "BPR Wilayah II - Jawa Barat, Banten, dan DKI",
    "BPR Wilayah II - Jawa Barat, Banten, dan DKI 2",
    "BPR Wilayah II - Jawa Barat, Banten, dan DKI 3",
    "BPR Wilayah II - Jawa Barat, Banten, dan DKI 4",
    "BPRS Wilayah II - Jawa Barat, Banten, dan DKI",
    "BPR Wilayah IV - Jawa Timur",
    "BPR Wilayah IV - Jawa Timur 2",
    "BPR Wilayah IV - Jawa Timur 3",
    "BPR Wilayah IV - Jawa Timur 4",
    "BPRS Wilayah IV - Jawa Timur",
    "BPR Wilayah III - Jawa Tengah dan DI Yogyakarta",
    "BPR Wilayah III - Jawa Tengah dan DI Yogyakarta 2",
    "BPR Wilayah III - Jawa Tengah dan DI Yogyakarta 3",
    "BPRS Wilayah III - Jawa Tengah dan DI Yogyakarta",
    "BPR Wilayah I - Sumatera",
    "BPR Wilayah I - Sumatera 2",
    "BPR Wilayah I - Sumatera 3",
    "BPR Wilayah I - Sumatera 4",
    "BPRS Wilayah I - Sumatera",
    "BPR Wilayah VII - Bali dan Nusa Tenggara",
    "Copy of BPR Wilayah VII - Bali dan Nusa Tenggara",
    "BPR Wilayah VII - Bali dan Nusa Tenggara 2",
    "BPRS Wilayah VII - Bali dan Nusa Tenggara",
    "BPR Wilayah V - Kalimantan",
    "BPRS Wilayah V - Kalimantan",
    "BPR VI Wilayah Sulawesi, Maluku, dan Papua",
    "BPRS VI Wilayah Sulawesi, Maluku, dan Papua",
    "BUK",
    "BUS",
    "SRO",
    "PPE1",
    "PPE2",
    "MI",
    "PEE",
    "AW",
    "AJK",
    "AJS",
    "AUK",
    "AUS",
    "ReasK",
    "ReasS",
    "PialangReas",
    "PenjaminanK",
    "PenjaminanS",
    "DPLKK",
    "PLKDS",
    "DPPKK1",
    "DPPKK2",
    "DPPKS",
    "PPK1",
    "PPK2",
    "PPS",
    "MVK",
    "MVS",
    "P2PLK",
    "P2PLS",
    "GadaiP",
    "GadaiK1",
    "GadaiK2",
    "GadaiS",
    "SCFK",
    "SCFK",
    "LKK",
    "Asosiasi"
]
'''
pops = [
    "KOJT1",
    "KOJT2",
    "KOBD",
    "KOCB",
    "KOSG",
    "KOPW",
    "KOTG",
    "KOSL",
    "KOYK",
    "KOPD",
    "KOAC",
    "KOMN",
    "KOKR",
    "KOPB",
    "KOPG",
    "KOJM",
    "KOBK",
    "KOLP",
    "KODS",
    "KOMT",
    "KOKP",
    "KOPT",
    "KOBM",
    "KOSR",
    "KOPR",
    "KOMS",
    "KOMD",
    "KOPL",
    "KOKN",
    "KOAB",
    "KOJP",
    "Database Query & Cek",
    "Query Gabungan",
    "GABUNGAN",
    "Sheet8"
]
sheets = (list(file.keys()))

finalSheet = [x for x in sheets if x not in pops]

count = 0
curNum = ''
for i in finalSheet:
    try:
        data = file[i].iloc[2:]
        data.columns = replacement.columns
        allData = data
        allData = allData[allData['Nama Kegiatan'].notnull()]
        allData = allData[allData['Provinsi'].notnull()]
        allData.insert(0, 'Sektor PUJK', None)
        rows = len(allData.index)
        if (rows > 0):
            for i in range(0, rows):
                count += 1
                curNum = count
                rowIndex = allData.index[i]
                allData.loc[rowIndex,'No'] = curNum
                allData.loc[rowIndex,'Sektor PUJK'] = ''
            template = pd.concat([template, allData])
    except Exception as e:
        print(i)
        print(str(e))
        
template.to_excel("Gencarkan - Result 2.xlsx", index=False)