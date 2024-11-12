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

pw_1 = {0: np.float64(27748.003337821156), 1: np.float64(27462.74952175667), 2: np.float64(26770.13427350427), 3: np.float64(26019.63290638203), 4: np.float64(25317.603637688404), 5: np.float64(22996.6884371249), 6: np.float64(22144.978249370273), 7: np.float64(20085.524631230193), 8: np.float64(17626.400396495395), 9: np.float64(15624.19957262204), 10: np.float64(13599.640609888911), 11: np.float64(11686.223132045088), 12: np.float64(11352.29251518887), 13: np.float64(8791.265972947187), 14: np.float64(7353.039886282277), 15: np.float64(5050.235173901338), 16: np.float64(3974.9668859681346), 17: np.float64(2817.7127596902474), 18: np.float64(2196.291763521952), 19: np.float64(1555.795944979028), 20: np.float64(1213.223674510502), 21: np.float64(860.1907918575492), 22: np.float64(428.91372931180786), 23: np.float64(199.74028494416638)}

lsc_1 = {0: np.float64(4464.013716481544), 1: np.float64(4386.017149699995), 2: np.float64(4337.279843304844), 3: np.float64(4128.5815043362245), 4: np.float64(4053.400314763927), 5: np.float64(3646.0215752312365), 6: np.float64(3525.0572124265323), 7: np.float64(3150.3373998847596), 8: np.float64(2757.8690139590144), 9: np.float64(2432.4781981401543), 10: np.float64(2131.016096710956), 11: np.float64(1820.9331400966184), 12: np.float64(1774.1194715447155), 13: np.float64(1358.8826112701354), 14: np.float64(1150.7472653816471), 15: np.float64(795.2339523970523), 16: np.float64(613.9356170562911), 17: np.float64(436.5486965102185), 18: np.float64(343.750907877599), 19: np.float64(242.57269306686405), 20: np.float64(186.54397833933365), 21: np.float64(131.84075675891668), 22: np.float64(66.33211105521423), 23: np.float64(30.77914214203202)}

usc_1 = {0: np.float64(4337.195693369235), 1: np.float64(4158.370756819443), 2: np.float64(4106.985712250712), 3: np.float64(3944.2494440738274), 4: np.float64(3849.334230577067), 5: np.float64(3423.3507558426886), 6: np.float64(3266.4848572628043), 7: np.float64(2942.2172054163066), 8: np.float64(2589.0424274824277), 9: np.float64(2252.761448897193), 10: np.float64(1947.873639003848), 11: np.float64(1691.6186645962734), 12: np.float64(1623.1835628540402), 13: np.float64(1252.8682362350562), 14: np.float64(1044.9712192343814), 15: np.float64(721.5437604325151), 16: np.float64(560.0551866572628), 17: np.float64(400.3986199103715), 18: np.float64(308.0891555580569), 19: np.float64(217.03528559092032), 20: np.float64(169.33231557405102), 21: np.float64(120.4019779537389), 22: np.float64(60.78511231882216), 23: np.float64(28.301646130150182)}

pw_2 = {0: np.float64(16732.47267923258), 1: np.float64(15787.960670095297), 2: np.float64(14873.965641025643), 3: np.float64(13917.978082054704), 4: np.float64(13032.18485052877), 5: np.float64(11048.977540422227), 6: np.float64(10513.830100755666), 7: np.float64(9016.11926966292), 8: np.float64(7741.2441748341735), 9: np.float64(6716.51565792582), 10: np.float64(5672.026654323678), 11: np.float64(4790.962494824016), 12: np.float64(4585.224085732734), 13: np.float64(3502.91751164618), 14: np.float64(2897.608373687783), 15: np.float64(1945.8066218999854), 16: np.float64(1517.8031080075034), 17: np.float64(1078.0409827344713), 18: np.float64(822.835805742709), 19: np.float64(587.6021619787812), 20: np.float64(459.91859123534704), 21: np.float64(322.16889675818237), 22: np.float64(159.9769205231269), 23: np.float64(73.06256724792345)}

lsc_2 = {0: np.float64(3231.072412767867), 1: np.float64(3086.599598900822), 2: np.float64(2923.5690455840454), 3: np.float64(2647.18337891928), 4: np.float64(2518.4488675160296), 5: np.float64(2118.356695615336), 6: np.float64(2010.3554617968095), 7: np.float64(1736.221603284356), 8: np.float64(1489.835994950995), 9: np.float64(1282.4630497390633), 10: np.float64(1085.948307195237), 11: np.float64(915.512245226593), 12: np.float64(868.7267484077369), 13: np.float64(673.628838749509), 14: np.float64(555.7552717416571), 15: np.float64(372.6431262483017), 16: np.float64(289.5642504812143), 17: np.float64(201.73632596675435), 18: np.float64(154.6211407966039), 19: np.float64(111.58407044164817), 20: np.float64(85.73106281912635), 21: np.float64(61.48957738006527), 22: np.float64(30.783894546329183), 23: np.float64(14.339637493811543)}

usc_2 = {0: np.float64(2792.626447324133), 1: np.float64(2606.0713923763424), 2: np.float64(2396.150683760684), 3: np.float64(2230.519704247276), 4: np.float64(2069.416489299692), 5: np.float64(1755.5424101532162), 6: np.float64(1656.2643115029384), 7: np.float64(1447.221574474215), 8: np.float64(1211.2827987327987), 9: np.float64(1046.3849714365483), 10: np.float64(892.1555514412255), 11: np.float64(739.7573613986657), 12: np.float64(725.150210589651), 13: np.float64(546.3874013582533), 14: np.float64(450.7380866969791), 15: np.float64(305.9851090679139), 16: np.float64(234.79084590857664), 17: np.float64(166.73763628520433), 18: np.float64(123.83711267265915), 19: np.float64(91.69563039723661), 20: np.float64(70.66463096558114), 21: np.float64(50.12564269376065), 22: np.float64(24.845473039925604), 23: np.float64(11.522076938592148)}

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
graf_aktivita.Figure.savefig(r"NOVA_MD_OPTIMA/full_FOV/zavislost_rm_na_aktivite.png", bbox_inches='tight')	






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
paralyzabilni_MD.Figure.savefig(r"NOVA_MD_OPTIMA/full_FOV/paralyzabilni_model.png", bbox_inches='tight')








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
non_paralyzabilni_MD.Figure.savefig(r"NOVA_MD_OPTIMA/full_FOV/non_paralyzabilni_model.png", bbox_inches='tight')






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
pomery_graf.Figure.savefig(r"NOVA_MD_OPTIMA/full_FOV/pomery.png", bbox_inches='tight')

