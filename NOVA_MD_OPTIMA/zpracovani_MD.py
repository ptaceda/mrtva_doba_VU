import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from potrebne_funkce import Graf_1, Graf_1_2, tew_correction
from lmfit import Model


# Define your decay function
def premenovy_zakon(aktivita, polocas, reference_time, nynejsi_time):
    # Time difference in days
    delta_days = (nynejsi_time - reference_time).total_seconds() / (24 * 3600)
    return aktivita * np.exp(-np.log(2) / polocas * delta_days)

def lin_fce(x, a):
    return a * x 

def linearni_fit(x,y):
    fit = Model(lin_fce)
    params = fit.make_params(a=1, b=0)
    results = fit.fit(y, params, x=x)
    return results.params["a"].value

def exp_md_fce(x, tau):
    return x * np.exp(-x * tau)

def lomenna_md_fce(x, tau):
    x = np.array(list(x))
    return x / (1 + x*tau)

def poly_x_stupen(x, a, b, c):
    return a*x**4 + b*x**2 + c*x + 1

def exp_md_fit(x_data, y_data):
    teor_cps = x_data
    mer_cps = y_data
    model = Model(exp_md_fce)
    params = model.make_params(tau=0.00001)
    for i in range(3):
        result = model.fit(mer_cps, params, x=teor_cps)
        params = result.params

    # Extracting the best-fit values and their errors
    tau = result.params['tau'].value
    
    # Return as a numpy array
    return tau

def lomenny_md_fit(x_data, y_data):
    teor_cps = x_data
    mer_cps = y_data
    model = Model(lomenna_md_fce)
    params = model.make_params(tau=0.00008)
    for i in range(3):
        result = model.fit(mer_cps, params, x=teor_cps)
        params = result.params
    # Extracting the best-fit values and their errors
    tau = result.params['tau'].value

    # Return as a numpy array
    return tau

def kvadr_fit(x_data, y_data):
    mer_cps = x_data
    pomer = y_data
    model = Model(poly_x_stupen)
    params = model.make_params(a=1, b=2, c=0.5)
    for i in range(3):
        result = model.fit(pomer, params, x=mer_cps)
        params = result.params
    print(result.fit_report())
    # Extracting the best-fit values and their errors
    a = result.params['a'].value
    b = result.params['b'].value
    c = result.params['c'].value
    # d = result.params['d'].value
    # print(a)
    # print(b)
    # print(c)
    # print('----')


    # Return as a numpy array
    return a, b, c





ref_aktivita = 700.589 # MBq
reference_time_akt = datetime.strptime("08.07.2024 14:45:00", "%d.%m.%Y %H:%M:%S")
polocas_I = 8.0233 # dne

pw_1 = {0: np.float64(8272.360476270616), 1: np.float64(8143.619490495638), 2: np.float64(7977.062094017094), 3: np.float64(7779.579902156993), 4: np.float64(7586.902944874677), 5: np.float64(6898.058292381557), 6: np.float64(6648.956188077245), 7: np.float64(6081.567944396428), 8: np.float64(5326.678076923078), 9: np.float64(4697.494319309322), 10: np.float64(4114.305322006825), 11: np.float64(3528.424783758914), 12: np.float64(3440.998034839013), 13: np.float64(2672.1901128136046), 14: np.float64(2244.498807498117), 15: np.float64(1528.008141963598), 16: np.float64(1203.8463478652698), 17: np.float64(857.37250502108), 18: np.float64(672.3375785642692), 19: np.float64(471.3267813964965), 20: np.float64(367.58049248698404), 21: np.float64(261.33128703985693), 22: np.float64(130.76118327735176), 23: np.float64(60.614521425821)}

lsc_1 = {0: np.float64(635.8811511275663), 1: np.float64(640.9611241365402), 2: np.float64(634.667834757835), 3: np.float64(596.1775094507449), 4: np.float64(601.7153176784079), 5: np.float64(522.8824189790299), 6: np.float64(506.3196515533164), 7: np.float64(461.1077398444252), 8: np.float64(398.9548990198991), 9: np.float64(345.1974780405043), 10: np.float64(315.9286930951862), 11: np.float64(260.96026685070166), 12: np.float64(260.2763882774207), 13: np.float64(199.8593152607061), 14: np.float64(166.6108772443676), 15: np.float64(116.31341507165801), 16: np.float64(90.44903130219278), 17: np.float64(62.9855602826475), 18: np.float64(49.50105696613013), 19: np.float64(34.981516160868495), 20: np.float64(27.61167068212619), 21: np.float64(19.19410254416488), 22: np.float64(9.562730036773361), 23: np.float64(4.425960907273961)}

usc_1 = {0: np.float64(400.13361887131146), 1: np.float64(375.04902183229973), 2: np.float64(379.41551282051284), 3: np.float64(348.7008438959306), 4: np.float64(331.4313739695229), 5: np.float64(289.058658123279), 6: np.float64(276.51097397145253), 7: np.float64(240.10848026505332), 8: np.float64(202.78453618453614), 9: np.float64(175.56634667010286), 10: np.float64(151.5376250635301), 11: np.float64(128.01833678398896), 12: np.float64(125.5486868597928), 13: np.float64(91.4992364034349), 14: np.float64(75.87126023970916), 15: np.float64(51.179415090441225), 16: np.float64(41.328441208594754), 17: np.float64(29.302485775062614), 18: np.float64(20.998151870373647), 19: np.float64(15.462475943745373), 20: np.float64(12.031216068226309), 21: np.float64(8.28572792404008), 22: np.float64(4.228814020966405), 23: np.float64(2.042021104937932)}

pw_2 = {0: np.float64(4095.365710198586), 1: np.float64(3897.3732508949734), 2: np.float64(3672.2721225071223), 3: np.float64(3497.5885323549037), 4: np.float64(3253.186590473811), 5: np.float64(2748.459461272329), 6: np.float64(2603.220692695214), 7: np.float64(2211.9716897147796), 8: np.float64(1942.6191094941096), 9: np.float64(1671.8172128084532), 10: np.float64(1432.7533405939155), 11: np.float64(1195.7095640671728), 12: np.float64(1152.8300381556162), 13: np.float64(887.8266209238369), 14: np.float64(727.2987803007059), 15: np.float64(484.60164778952765), 16: np.float64(382.78945631358033), 17: np.float64(270.071425567513), 18: np.float64(206.4577952156598), 19: np.float64(146.0542709104367), 20: np.float64(116.17944374478105), 21: np.float64(81.9011740222601), 22: np.float64(40.12548952103162), 23: np.float64(18.14716724425619)}

lsc_2 = {0: np.float64(414.6068602041961), 1: np.float64(367.9446586497252), 2: np.float64(360.47797720797723), 3: np.float64(310.27022681787855), 4: np.float64(309.944153551503), 5: np.float64(250.50917037350845), 6: np.float64(252.31628043660788), 7: np.float64(209.77973494670127), 8: np.float64(175.74917582417578), 9: np.float64(156.3648861757189), 10: np.float64(134.21113628112974), 11: np.float64(109.22242811134116), 12: np.float64(106.47555399019693), 13: np.float64(77.27808974574843), 14: np.float64(66.8841407942574), 15: np.float64(45.240133454798176), 16: np.float64(34.3193039413041), 17: np.float64(24.13334658898401), 18: np.float64(18.648803137746764), 19: np.float64(13.439497285961016), 20: np.float64(10.40915830492852), 21: np.float64(7.326912205900458), 22: np.float64(3.749619122148201), 23: np.float64(1.6674021306635864)}

usc_2 = {0: np.float64(166.90382250645126), 1: np.float64(158.16781324055867), 2: np.float64(147.67413105413104), 3: np.float64(127.36661218590173), 4: np.float64(116.72074277625114), 5: np.float64(98.23092847560544), 6: np.float64(92.5461251049538), 7: np.float64(76.19663353500432), 8: np.float64(72.33715572715573), 9: np.float64(58.71576724008332), 10: np.float64(48.016539606476435), 11: np.float64(36.903352887048534), 12: np.float64(38.47083047166212), 13: np.float64(28.00686058258966), 14: np.float64(22.861615107813332), 15: np.float64(17.191781776517214), 16: np.float64(13.327505008056972), 17: np.float64(9.239673638545128), 18: np.float64(6.799006013925292), 19: np.float64(4.937182950900568), 20: np.float64(3.928955341701916), 21: np.float64(2.750917607849998), 22: np.float64(1.2439340552498166), 23: np.float64(0.5255344995140915)}

datum_akvizice = {0: b'20240708', 1: b'20240709', 2: b'20240710', 3: b'20240711', 4: b'20240712', 5: b'20240714', 6: b'20240715', 7: b'20240717', 8: b'20240719', 9: b'20240721', 10: b'20240723', 11: b'20240725', 12: b'20240726', 13: b'20240729', 14: b'20240731', 15: b'20240805', 16: b'20240808', 17: b'20240812', 18: b'20240815', 19: b'20240819', 20: b'20240822', 21: b'20240826', 22: b'20240903', 23: b'20240912'}

cas_akvizice = {0: b'170722.00 ', 1: b'145934.00 ', 2: b'150647.00 ', 3: b'151735.00 ', 4: b'135342.00 ', 5: b'220251.00 ', 6: b'160508.00 ', 7: b'150010.00 ', 8: b'183949.00 ', 9: b'154324.00 ', 10: b'151721.00 ', 11: b'191441.00 ', 12: b'062830.00 ', 13: b'151809.00 ', 14: b'224354.00 ', 15: b'143725.00 ', 16: b'143200.00 ', 17: b'164433.00 ', 18: b'152614.00 ', 19: b'163902.00 ', 20: b'151934.00 ', 21: b'145907.00 ', 22: b'151825.00 ', 23: b'133219.00 '}

trvani_akvizice = {0: 5.942, 1: 6.611, 2: 7.02, 3: 7.495, 4: 8.006, 5: 9.442, 6: 9.925, 7: 11.57, 8: 13.468, 9: 15.521, 10: 18.364, 11: 21.735, 12: 22.714, 13: 29.695, 14: 35.849, 15: 53.239, 16: 68.057, 17: 95.431, 18: 124.378, 19: 172.928, 20: 219.153, 21: 308.654, 22: 590.373, 23: 1163.456}


### Zjištění aktivity
datum_akvizice = {key: val.decode('utf-8') for key, val in datum_akvizice.items()}
cas_akvizice = {key: val.decode('utf-8') for key, val in cas_akvizice.items()}

decayed_activities = {}

for key in datum_akvizice:
    date_str = datum_akvizice[key]
    time_str = cas_akvizice[key].strip()  # Remove any extra whitespace
    nynejsi_time = datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S.%f")
    
    acquisition_duration = trvani_akvizice[key]  # in seconds
    nynejsi_time += timedelta(seconds=(acquisition_duration/2))
    
    activity = premenovy_zakon(ref_aktivita, polocas_I, reference_time_akt, nynejsi_time)
    decayed_activities[key] = activity

# print(decayed_activities.values())

pw_1_array = np.array(list(pw_1.values()))
pw_2_array = np.array(list(pw_2.values()))
pw_gm = np.sqrt(pw_1_array * pw_2_array)

lsc_1_array = np.array(list(lsc_1.values()))
lsc_2_array = np.array(list(lsc_2.values()))
usc_1_array = np.array(list(usc_1.values()))
usc_2_array = np.array(list(usc_2.values()))


hlava_1_array_tew = tew_correction(pw_1_array, lsc_1_array, usc_1_array)
hlava_2_array_tew = tew_correction(pw_2_array, lsc_2_array, usc_2_array)
gm_array_tew = np.sqrt(hlava_1_array_tew * hlava_2_array_tew)


aktivity_array = np.array(list(decayed_activities.values()))



### Provedeni fitu
a_ant = linearni_fit(aktivity_array[-2:], pw_1_array[-2:])
a_pos = linearni_fit(aktivity_array[-2:], pw_2_array[-2:])
a_gm = linearni_fit(aktivity_array[-2:], pw_gm[-2:])

a_ant_tew = linearni_fit(aktivity_array[-2:], hlava_1_array_tew[-2:])
a_pos_tew = linearni_fit(aktivity_array[-2:], hlava_2_array_tew[-2:])
a_gm_tew = linearni_fit(aktivity_array[-2:], gm_array_tew[-2:])



### Spocteni R_real

r_real_ant = lin_fce(aktivity_array, a_ant)
r_real_pos = lin_fce(aktivity_array, a_pos)
r_real_gm = lin_fce(aktivity_array, a_gm)

r_real_ant_tew = lin_fce(aktivity_array, a_ant_tew)
r_real_pos_tew = lin_fce(aktivity_array, a_pos_tew)
r_real_gm_tew = lin_fce(aktivity_array, a_gm_tew)





### Závislost r_M na aktivite
graf_aktivita = Graf_1_2(10, None, 
                         "Pouze PW okno", "Aktivita [MBq]", "Četnost impulsů [cps]",
                         "Po TEW korekci", "Aktivita [MBq]", "Četnost impulsů [cps]",
                         (15,5))

## PW okno
graf_aktivita.fig[0].plot(aktivity_array, r_real_ant, "--", color = "red")
graf_aktivita.fig[0].plot(aktivity_array, r_real_pos, "--", color = "blue")
graf_aktivita.fig[0].plot(aktivity_array, r_real_gm, "--", color = "green")

graf_aktivita.fig[0].plot(aktivity_array, pw_1_array, "o", label = "ANT", color = "red")
graf_aktivita.fig[0].plot(aktivity_array, pw_2_array, "o", label = "POS", color = "blue")
graf_aktivita.fig[0].plot(aktivity_array, pw_gm, "o", label = "GM", color = "green")

graf_aktivita.fig[0].legend(loc='best', edgecolor='black', fontsize=9)


## po TEW korekce
graf_aktivita.fig[1].plot(aktivity_array, r_real_ant_tew, "--", color = "red")
graf_aktivita.fig[1].plot(aktivity_array, r_real_pos_tew, "--", color = "blue")
graf_aktivita.fig[1].plot(aktivity_array, r_real_gm_tew, "--", color = "green")

graf_aktivita.fig[1].plot(aktivity_array, hlava_1_array_tew, "o", label = "ANT", color = "red")
graf_aktivita.fig[1].plot(aktivity_array, hlava_2_array_tew, "o", label = "POS", color = "blue")
graf_aktivita.fig[1].plot(aktivity_array, gm_array_tew, "o", label = "GM", color = "green")

graf_aktivita.fig[1].legend(loc='best', edgecolor='black', fontsize=9)

## ulozeni grafu
graf_aktivita.Figure.savefig(r"NOVA_MD_OPTIMA/ROI_zdroj/zavislost_rm_na_aktivite.png", bbox_inches='tight')	






### Paralyzabilní MODEL
paralyzabilni_MD = Graf_1_2(10, "Paralyzabilní model", 
                         "Pouze PW okno", "Teoretická četnost impulsů [cps]", "Měřená četnost impulsů [cps]",
                         "Po TEW korekci", "Teoretická četnost impulsů [cps]", "Měřená četnost impulsů [cps]",
                         (15,5))


tau_ant = exp_md_fit(r_real_ant, pw_1_array)
tau_pos = exp_md_fit(r_real_pos, pw_2_array)
tau_gm = exp_md_fit(r_real_gm, pw_gm)

tau_ant_tew = exp_md_fit(r_real_ant_tew, hlava_1_array_tew)
tau_pos_tew = exp_md_fit(r_real_pos_tew, hlava_2_array_tew)
tau_gm_tew = exp_md_fit(r_real_gm_tew, gm_array_tew)

# print(round(tau_ant, 8), round(tau_pos, 8), round(tau_gm, 8))
# print(round(tau_ant_tew, 8), round(tau_pos_tew, 8), round(tau_gm_tew, 8))


## PW okno
paralyzabilni_MD.fig[0].plot(r_real_ant, exp_md_fce(r_real_ant, tau_ant), "--", label = "ANT", color = "red")
paralyzabilni_MD.fig[0].plot(r_real_pos, exp_md_fce(r_real_pos, tau_pos), "--", label = "POS", color = "blue")
paralyzabilni_MD.fig[0].plot(r_real_gm, exp_md_fce(r_real_gm, tau_gm), "--", label = "GM", color = "green")

paralyzabilni_MD.fig[0].plot(r_real_ant, pw_1_array, "o", label = "ANT", color = "red")
paralyzabilni_MD.fig[0].plot(r_real_pos, pw_2_array, "o", label = "POS", color = "blue")
paralyzabilni_MD.fig[0].plot(r_real_gm, pw_gm, "o", label = "GM", color = "green")

paralyzabilni_MD.fig[0].legend(loc='best', edgecolor='black', fontsize=9)


## po TEW korekce
paralyzabilni_MD.fig[1].plot(r_real_ant_tew, exp_md_fce(r_real_ant_tew, tau_ant_tew), "--", color = "red")
paralyzabilni_MD.fig[1].plot(r_real_pos_tew, exp_md_fce(r_real_pos_tew, tau_pos_tew), "--", color = "blue")
paralyzabilni_MD.fig[1].plot(r_real_gm_tew, exp_md_fce(r_real_gm_tew, tau_gm_tew), "--", color = "green")

paralyzabilni_MD.fig[1].plot(r_real_ant_tew, hlava_1_array_tew, "o", label = "ANT", color = "red")
paralyzabilni_MD.fig[1].plot(r_real_pos_tew, hlava_2_array_tew, "o", label = "POS", color = "blue")
paralyzabilni_MD.fig[1].plot(r_real_gm_tew, gm_array_tew, "o", label = "GM", color = "green")

paralyzabilni_MD.fig[1].legend(loc='best', edgecolor='black', fontsize=9)

## ulozeni grafu
paralyzabilni_MD.Figure.savefig(r"NOVA_MD_OPTIMA/ROI_zdroj/paralyzabilni_model.png", bbox_inches='tight')








### NON-paralyzabilní MODEL
non_paralyzabilni_MD = Graf_1_2(10, "Non-paralyzabilní model", 
                         "Pouze PW okno", "Teoretická četnost impulsů [cps]", "Měřená četnost impulsů [cps]",
                         "Po TEW korekci", "Teoretická četnost impulsů [cps]", "Měřená četnost impulsů [cps]",
                         (15,5))

tau_ant_non = lomenny_md_fit(r_real_ant, pw_1_array)
tau_pos_non = lomenny_md_fit(r_real_pos, pw_2_array)
tau_gm_non = lomenny_md_fit(r_real_gm, pw_gm)

tau_ant_tew_non = lomenny_md_fit(r_real_ant_tew, hlava_1_array_tew)
tau_pos_tew_non = lomenny_md_fit(r_real_pos_tew, hlava_2_array_tew)
tau_gm_tew_non = lomenny_md_fit(r_real_gm_tew, gm_array_tew)


## PW okno
non_paralyzabilni_MD.fig[0].plot(r_real_ant, lomenna_md_fce(r_real_ant, tau_ant_non), "--", color = "red")
non_paralyzabilni_MD.fig[0].plot(r_real_pos, lomenna_md_fce(r_real_pos, tau_pos_non), "--", color = "blue")
non_paralyzabilni_MD.fig[0].plot(r_real_gm, lomenna_md_fce(r_real_gm, tau_gm_non), "--", color = "green")

non_paralyzabilni_MD.fig[0].plot(r_real_ant, pw_1_array, "o", label = "ANT", color = "red")
non_paralyzabilni_MD.fig[0].plot(r_real_pos, pw_2_array, "o", label = "POS", color = "blue")
non_paralyzabilni_MD.fig[0].plot(r_real_gm, pw_gm, "o", label = "GM", color = "green")

non_paralyzabilni_MD.fig[0].legend(loc='best', edgecolor='black', fontsize=9)

## po TEW korekce
non_paralyzabilni_MD.fig[1].plot(r_real_ant_tew, lomenna_md_fce(r_real_ant_tew, tau_ant_tew_non), "--", color = "red")
non_paralyzabilni_MD.fig[1].plot(r_real_pos_tew, lomenna_md_fce(r_real_pos_tew, tau_pos_tew_non), "--", color = "blue")
non_paralyzabilni_MD.fig[1].plot(r_real_gm_tew, lomenna_md_fce(r_real_gm_tew, tau_gm_tew_non), "--", color = "green")

non_paralyzabilni_MD.fig[1].plot(r_real_ant_tew, hlava_1_array_tew, "o", label = "ANT", color = "red")
non_paralyzabilni_MD.fig[1].plot(r_real_pos_tew, hlava_2_array_tew, "o", label = "POS", color = "blue") 
non_paralyzabilni_MD.fig[1].plot(r_real_gm_tew, gm_array_tew, "o", label = "GM", color = "green")

non_paralyzabilni_MD.fig[1].legend(loc='best', edgecolor='black', fontsize=9)

## ulozeni grafu
non_paralyzabilni_MD.Figure.savefig(r"NOVA_MD_OPTIMA/ROI_zdroj/non_paralyzabilni_model.png", bbox_inches='tight')






### Pomery
pomer_ant = r_real_ant/pw_1_array
pomer_pos = r_real_pos/pw_2_array
pomer_gm = r_real_gm/pw_gm

pomer_ant_tew = r_real_ant_tew/hlava_1_array_tew
pomer_pos_tew = r_real_pos_tew/hlava_2_array_tew
pomer_gm_tew = r_real_gm_tew/gm_array_tew

## fitovani
n = 2
par_ant_pomer = kvadr_fit(pw_1_array[n:], pomer_ant[n:])
par_pos_pomer = kvadr_fit(pw_2_array[n:], pomer_pos[n:])
par_gm_pomer = kvadr_fit(pw_gm[n:], pomer_gm[n:])

par_ant_pomer_tew = kvadr_fit(hlava_1_array_tew[n:], pomer_ant_tew[n:])
par_pos_pomer_tew = kvadr_fit(hlava_2_array_tew[n:], pomer_pos_tew[n:])
par_gm_pomer_tew = kvadr_fit(gm_array_tew[n:], pomer_gm_tew[n:])



pomery_graf = Graf_1_2(10, None,
                        "Pouze PW okno", "Měřená četnost impulsů [cps]", "Faktor mrtvé doby [-]",
                        "Po TEW korekci", "Měřená četnost impulsů [cps]", "Faktor mrtvé doby [-]",
                        (15,5))

## PW okno
pomery_graf.fig[0].plot(pw_1_array[n:], poly_x_stupen(pw_1_array[n:], *par_ant_pomer), "--", color = "red")
pomery_graf.fig[0].plot(pw_2_array[n:], poly_x_stupen(pw_2_array[n:], *par_pos_pomer), "--", color = "blue")
pomery_graf.fig[0].plot(pw_gm[n:], poly_x_stupen(pw_gm[n:], *par_gm_pomer), "--", color = "green")

pomery_graf.fig[0].plot(pw_1_array, pomer_ant, "o", label = "ANT", color = "red")
pomery_graf.fig[0].plot(pw_2_array, pomer_pos, "o", label = "POS", color = "blue")
pomery_graf.fig[0].plot(pw_gm, pomer_gm, "o", label = "GM", color = "green")

pomery_graf.fig[0].legend(loc='best', edgecolor='black', fontsize=9)

## TEW korekce    
pomery_graf.fig[1].plot(hlava_1_array_tew[n:], poly_x_stupen(hlava_1_array_tew[n:], *par_ant_pomer_tew), "--", color = "red")
pomery_graf.fig[1].plot(hlava_2_array_tew[n:], poly_x_stupen(hlava_2_array_tew[n:], *par_pos_pomer_tew), "--", color = "blue")
pomery_graf.fig[1].plot(gm_array_tew[n:], poly_x_stupen(gm_array_tew[n:], *par_gm_pomer_tew), "--", color = "green")

pomery_graf.fig[1].plot(hlava_1_array_tew, pomer_ant_tew, "o", label = "ANT", color = "red")
pomery_graf.fig[1].plot(hlava_2_array_tew, pomer_pos_tew, "o", label = "POS", color = "blue")
pomery_graf.fig[1].plot(gm_array_tew, pomer_gm_tew, "o", label = "GM", color = "green")

pomery_graf.fig[1].legend(loc='best', edgecolor='black', fontsize=9)

## ulozeni grafu
pomery_graf.Figure.savefig(r"NOVA_MD_OPTIMA/ROI_zdroj/pomery.png", bbox_inches='tight')

