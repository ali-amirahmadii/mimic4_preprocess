
#read prescription file from MIMIC4
pat_meds = pd.read_csv(root_adr+"prescriptions.csv.gz",usecols=[0,1,6,12],dtype={"ndc":str})

#put nan if len ndc is less than 11
pat_meds["ndc"] = pat_meds["ndc"].apply(lambda x: np.nan if len(str(x))<11 else x)
#delete rows with ndc = nan
pat_meds = pat_meds[pat_meds['ndc'].notna()]

#you can download the following file from here: 
#https://github.com/fabkury/ndc_map/blob/master/FDA%20NDC%20Directory%20with%20drug%20classes/FDA%20NDC%20directory%20with%20atc5%20atc4%20ingredients%20(2020_06_17).zip
ndc2atc_map = pd.read_csv("ndc_map 2020_06_17 (atc5 atc4 ingredients).csv")[["ndc", "atc5"]]

#convert 10digit format to 111digit format ndc codes
#based on https://kb.daisybill.com/articles/how-do-i-convert-a-10-digit-ndc-number-to-11-digits#:~:text=Summary,0%20in%20the%206th%20position.

def add_zero_ndc(ndc_10dig):
    ndc_arr = ndc_10dig.split("-")
    if len(ndc_arr[0])==4:
        return ("0"+str(ndc_10dig).replace("-",""))[:]
    else:
        if len(ndc_arr[1])==3:
            return ("".join(ndc_arr[0])+"0"+"".join(ndc_arr[1:]))[:]
        else:
            return ("".join(ndc_arr[:2])+"0"+"".join(ndc_arr[2]))[:]
    
ndc2atc_map["ndc"] = ndc2atc_map["ndc"].apply(lambda x: add_zero_ndc(x))


#map ndc to atc
atc_list = []
used_digits = 9
ndc_list = ndc2atc_map.ndc.apply(lambda x : x[:used_digits])
coresp_atc = ndc2atc_map.atc5
dict_ndc_atc = dict(zip(ndc_list, coresp_atc))
for x in tqdm(pat_meds.ndc):
    try:
        atc_list.append(dict_ndc_atc[x[:used_digits]])
    except:
        atc_list.append(np.nan)



pat_meds["atc5"] = atc_list
pat_meds



