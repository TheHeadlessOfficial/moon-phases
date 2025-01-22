import os, sys
import re
import shutil
import requests
import datetime
from bleach.sanitizer import Cleaner
# Lock file to tell conky that the script is running
lock_file = "/tmp/script_moon.lock"
try:
    # Create lock file
    open(lock_file, 'w').close()
    # get your HOME name
    homepath = os.environ['HOME']
    homename = homepath
    homename = homename[6:]
    #                   set your emisphere (north or south plus "/")
    emi = 'north/'
    ###################################                  paths
    home = '/home/'
    conky = '/.conky/'
    filepath = home + homename + conky + 'moon/Moongiant_python/raw.txt'
    filepath2 = home + homename + conky + 'moon/Moongiant_python/rawstripped.txt'
    filepath3 = home + homename + conky + 'moon/Moongiant_python/rawstrippedclean.txt'
    filepath4 = home + homename + conky + 'moon/Moongiant_python/rawstrippedcleanrows.txt'
    filepath5 = home + homename + conky + 'moon/Moongiant_python/illumidays.txt'
    filepath6 = home + homename + conky + 'moon/Moongiant_python/picspath.txt'
    filepath7 = home + homename + conky + 'moon/Moongiant_python/moongiant_icons_' + emi
    filepath8 = home + homename + conky + 'moon/Moongiant_python/riseicons' + '/'
    filepath9 = home + homename + conky + 'moon/Moongiant_python/phases.txt'
    filepath10 = home + homename + conky + 'moon/Moongiant_python/rise.jpg'
    filepath11 = home + homename + conky + 'moon/Moongiant_python/todaymooninfo.txt'
    # write statements for conky
    filepath12 = home + homename + conky + 'moon/Moongiant_python/conkyrows.txt'
    #                                                    moon pics patterns PNG
    picspatterns = ['moon_day_first.png', 'moon_day_full.png', 'moon_day_last.png', 'moon_day_new.png', 'moon_day_WanC_0.png', 'moon_day_WanC_5.png', 'moon_day_WanC_10.png', 'moon_day_WanC_15.png', 'moon_day_WanC_20.png', 'moon_day_WanC_25.png', 'moon_day_WanC_30.png', 'moon_day_WanC_35.png', 'moon_day_WanC_40.png', 'moon_day_WanC_45.png', 'moon_day_WanG_50.png', 'moon_day_WanG_55.png', 'moon_day_WanG_60.png', 'moon_day_WanG_65.png', 'moon_day_WanG_70.png', 'moon_day_WanG_75.png', 'moon_day_WanG_80.png', 'moon_day_WanG_85.png', 'moon_day_WanG_90.png', 'moon_day_WanG_95.png', 'moon_day_WaxC_0.png', 'moon_day_WaxC_5.png', 'moon_day_WaxC_10.png', 'moon_day_WaxC_15.png', 'moon_day_WaxC_20.png', 'moon_day_WaxC_25.png', 'moon_day_WaxC_30.png', 'moon_day_WaxC_35.png', 'moon_day_WaxC_40.png', 'moon_day_WaxC_45.png', 'moon_day_WaxG_50.png', 'moon_day_WaxG_55.png', 'moon_day_WaxG_60.png', 'moon_day_WaxG_65.png', 'moon_day_WaxG_70.png', 'moon_day_WaxG_75.png', 'moon_day_WaxG_80.png', 'moon_day_WaxG_85.png', 'moon_day_WaxG_90.png', 'moon_day_WaxG_95.png', 'moon_day_first.jpg', 'moon_day_full.jpg', 'moon_day_last.jpg', 'moon_day_new.jpg', 'moon_day_WanC_0.jpg', 'moon_day_WanC_5.jpg', 'moon_day_WanC_10.jpg', 'moon_day_WanC_15.jpg', 'moon_day_WanC_20.jpg', 'moon_day_WanC_25.jpg', 'moon_day_WanC_30.jpg', 'moon_day_WanC_35.jpg', 'moon_day_WanC_40.jpg', 'moon_day_WanC_45.jpg', 'moon_day_WanG_50.jpg', 'moon_day_WanG_55.jpg', 'moon_day_WanG_60.jpg', 'moon_day_WanG_65.jpg', 'moon_day_WanG_70.jpg', 'moon_day_WanG_75.jpg', 'moon_day_WanG_80.jpg', 'moon_day_WanG_85.jpg', 'moon_day_WanG_90.jpg', 'moon_day_WanG_95.jpg', 'moon_day_WaxC_0.jpg', 'moon_day_WaxC_5.jpg', 'moon_day_WaxC_10.jpg', 'moon_day_WaxC_15.jpg', 'moon_day_WaxC_20.jpg', 'moon_day_WaxC_25.jpg', 'moon_day_WaxC_30.jpg', 'moon_day_WaxC_35.jpg', 'moon_day_WaxC_40.jpg', 'moon_day_WaxC_45.jpg', 'moon_day_WaxG_50.jpg', 'moon_day_WaxG_55.jpg', 'moon_day_WaxG_60.jpg', 'moon_day_WaxG_65.jpg', 'moon_day_WaxG_70.jpg', 'moon_day_WaxG_75.jpg', 'moon_day_WaxG_80.jpg', 'moon_day_WaxG_85.jpg', 'moon_day_WaxG_90.jpg', 'moon_day_WaxG_95.jpg', 'rise_FirstQuarter.jpg', 'rise_FullMoon.jpg', 'rise_LastQuarter.jpg', 'rise_NewMoon.jpg', 'rise_WaningCrescent.jpg', 'rise_WaningGibbous.jpg', 'rise_WaxingCrescent.jpg', 'rise_WaxingGibbous.jpg']
    ###################################                  phases patterns
    phasespatterns = ['Full Moon', 'New Moon', 'First Quarter', 'Last Quarter', 'Waxing Crescent', 'Waxing Gibbous', 'Waning Gibbous', 'Waning Crescent']
    ###################################                  chars patterns
    charspatterns = ['(', ')', ',', '<', ';', ' ', '%', "'"]
    ###################################                  chars patterns
    charspatterns2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December','(', ')', ',', '<', ';', ' ', '%', "'"]
    ###################################                  alphabet patterns
    alphabetpatterns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'z']
    ###################################                  website url
    url = 'https://www.moongiant.com/phase/today/'
    res = requests.get(url)
    data = res
    ###################################                  get the HTML page source code in a txt file named RAW.TXT
    with open(filepath, 'w') as f:
        f.write(data.text)
    ###################################                  strip HTML and save in file RAWSTRIPPED.TXT
    cleaner = Cleaner(tags=['<br>'], attributes={}, protocols=[], strip=True, strip_comments=True, filters=None)
    fo = open(filepath2, 'w')
    fo.write(cleaner.clean(data.text))
    fo.close()
    ###################################                  delete no usefull rows from the previous txt file and save in RAWSTRIPPEDCLEAN.TXT
    with open(filepath2) as old, open(filepath3, 'w') as new:
        lines = old.readlines()
        new.writelines(lines[1170:-364]) # time to time the website changes, check and change the row number
    ###################################                  delete empty rows and save in RAWSTRIPPEDCLEANROWS.TXT
    with open(filepath3) as infile, open(filepath4, 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output
    ###################################                  GET THE ILLUMINATION NUMBER (starts from zero)
    ##########   FIND THE RIGHT ROW INFO FOR MOONS AUTOMATICALLY
    month = datetime.date.today()
    month = month.strftime("%B")
    counter = 0
    lm2temp = 0
    with open(filepath4, 'r') as fo:
        lines = fo.read().splitlines()
        for counter in range(0, 5):
            if month in lines[counter]:
                lm2temp = counter
                lm2 = lm2temp + 0 #5
                lm1 = lm2temp + 1 #7
                lp1 = lm2temp + 3 #11
                lp2 = lm2temp + 4 #13
                lines[lm2] = lines[lm2].strip()
                illumim2 = lines[lm2]
                lines[lm1] = lines[lm1].strip()
                illumim1 = lines[lm1]
                lines[lp1] = lines[lp1].strip()
                illumip1 = lines[lp1]
                lines[lp2] = lines[lp2].strip()
                illumip2 = lines[lp2]
                illumim2 = illumim2[-3:]
                if illumim2 == '00%':
                   illumim2 = '100%'
                illumim1 = illumim1[-3:]
                if illumim1 == '00%':
                   illumim1 = '100%'
                illumip1 = illumip1[-3:]
                if illumip1 == '00%':
                   illumip1 = '100%'
                illumip2 = illumip2[-3:]
                if illumip2 == '00%':
                   illumip2 = '100%'
                for pattern in alphabetpatterns:
                   if re.findall(pattern, illumim2):
                      illumim2 = illumim2[1:]
                   if re.findall(pattern, illumim1):
                      illumim1 = illumim1[1:]
                   if re.findall(pattern, illumip1):
                      illumip1 = illumip1[1:]
                   if re.findall(pattern, illumip2):
                      illumip2 = illumip2[1:]
                ###################################                  write the illumination
                fo = open(filepath5, 'w')
                fo.write('{}\n'.format(illumim2))
                fo.write('{}\n'.format(illumim1))
                fo.write('{}\n'.format(illumip1))
                fo.write('{}\n'.format(illumip2))
                fo.close()
                ###################################                  find the match for the phases and write them
                for pattern in phasespatterns:
                   if re.findall(pattern, lines[lm2]):
                       lines[lm2] = re.findall(pattern, lines[lm2])
                       lines[lm2] = str(lines[lm2]).replace("[", "")
                       lines[lm2] = str(lines[lm2]).replace("]", "")
                       lines[lm2] = str(lines[lm2]).replace("'", "")
                   if re.findall(pattern, lines[lm1]):
                       lines[lm1] = re.findall(pattern, lines[lm1])
                       lines[lm1] = str(lines[lm1]).replace("[", "")
                       lines[lm1] = str(lines[lm1]).replace("]", "")
                       lines[lm1] = str(lines[lm1]).replace("'", "")
                   if re.findall(pattern, lines[lp1]):
                       lines[lp1] = re.findall(pattern, lines[lp1])
                       lines[lp1] = str(lines[lp1]).replace("[", "")
                       lines[lp1] = str(lines[lp1]).replace("]", "")
                       lines[lp1] = str(lines[lp1]).replace("'", "")
                   if re.findall(pattern, lines[lp2]):
                       lines[lp2] = re.findall(pattern, lines[lp2])
                       lines[lp2] = str(lines[lp2]).replace("[", "")
                       lines[lp2] = str(lines[lp2]).replace("]", "")
                       lines[lp2] = str(lines[lp2]).replace("'", "")
                fo = open(filepath9, 'w')
                fo.write('day-2: {}\n'.format(lines[lm2]))
                fo.write('day-1: {}\n'.format(lines[lm1]))
                fo.write('day+1: {}\n'.format(lines[lp1]))
                fo.write('day+2: {}\n'.format(lines[lp2]))
                fo.close()
                ##################################                 FIND THE RIGHT INFO ROW FOR TODAY MOON AUTOMATICALLY
                phrase = 'Phase Details for'
                counter = 0
                rtmi1temp = 0
                for counter in range(0, 38):
                    if phrase in lines[counter]:
                        rtmi1temp = counter
                        ###################################                 create text file for today moon info
                        ###                 set variables     r=row, t=today, m=moon, i=info, (starts from zero)
                        rtmi1 = rtmi1temp
                        rtmi2 = rtmi1 + 1
                        rtmi3 = rtmi1 + 2
                        rtmi4 = rtmi1 + 3
                        rtmi5 = rtmi1 + 4
                        rtmi6 = rtmi1 + 5
                        rtmi7 = rtmi1 + 6
                        rtmi8 = rtmi1 + 7
                        mi1 = lines[rtmi1].strip()
                        mi2 = lines[rtmi2].strip()
                        mi3 = lines[rtmi3].strip()
                        mi4 = lines[rtmi4].strip()
                        mi5 = lines[rtmi5].strip()
                        mi6 = lines[rtmi6].strip()
                        mi7 = lines[rtmi7].strip()
                        mi8 = lines[rtmi8].strip()
                        ###################################                  write the today moon info
                        fo = open(filepath11, 'w')
                        fo.write('{}\n'.format(mi1))
                        fo.write('{}\n'.format(mi2))
                        fo.write('{}\n'.format(mi3))
                        fo.write('{}\n'.format(mi4))
                        fo.write('{}\n'.format(mi5))
                        fo.write('{}\n'.format(mi6))
                        fo.write('{}\n'.format(mi7))
                        fo.write('{}\n'.format(mi8))
                        fo.close()
                ###################################                 FIND THE RIGHT INFO ROW FOR MOON AUTOMATICALLY
                phrase = 'divs for marking today'
                counter = 0
                rm2itemp = 0
                with open(filepath, 'r') as fo:
                    linespics = fo.read().splitlines()
                    for counter in range(1140, 1150):
                        if phrase in linespics[counter]:
                            rm2itemp = counter
                            ###################################                 r=row, m=minus, p=plus, i=image, p=phase, t=today, imm=image (starts from zero)
                            rm2i = rm2itemp + 9 #980
                            rm2p = rm2itemp + 10 #981
                            rm1i = rm2itemp + 15 #986
                            rm1p = rm2itemp + 16 #987
                            rti = rm2itemp + 18 #989
                            rp1i = rm2itemp + 24 #995
                            rp1p = rm2itemp + 25 #996
                            rp2i = rm2itemp + 30 #1001
                            rp2p = rm2itemp + 31 #1002
                            rimm = rm2itemp + 217 #1076
                            ###################################                 get the 5 moon pics (for the previous and next days), the phases description and the rise image  (rows count start from zero)
                            linespics[rm2i] = str(linespics[rm2i]).strip()
                            linespics[rm2p] = str(linespics[rm2p]).strip()
                            linespics[rm1i] = str(linespics[rm1i]).strip()
                            linespics[rm1p] = str(linespics[rm1p]).strip()
                            linespics[rti] = str(linespics[rti]).strip()
                            linespics[rp1i] = str(linespics[rp1i]).strip()
                            linespics[rp1p] = str(linespics[rp1p]).strip()
                            linespics[rp2i] = str(linespics[rp2i]).strip()
                            linespics[rp2p] = str(linespics[rp2p]).strip()
                            linespics[rimm] = str(linespics[rimm]).strip()
                            linespics[rm2i] = linespics[rm2i][:-40]
                            linespics[rm2i] = linespics[rm2i][80:]
                            linespics[rm1i] = linespics[rm1i][:-40]
                            linespics[rm1i] = linespics[rm1i][80:]
                            linespics[rti] = linespics[rti][:-40]
                            linespics[rti] = linespics[rti][70:]
                            linespics[rp1i] = linespics[rp1i][:-40]
                            linespics[rp1i] = linespics[rp1i][80:]
                            linespics[rp2i] = linespics[rp2i][:-40]
                            linespics[rp2i] = linespics[rp2i][80:]
                            linespics[rimm] = linespics[rimm][:-20]
                            linespics[rimm] = linespics[rimm][500:]
                            ##################################                  find the match for the moon images to show
                            linespics[rm2i] = re.findall(r'\b(moon_day_+)(\w+)(.png\b)', linespics[rm2i], re.IGNORECASE)
                            linespics[rm2i] = str(linespics[rm2i]).replace("(", "")
                            linespics[rm2i] = str(linespics[rm2i]).replace(")", "")
                            linespics[rm2i] = str(linespics[rm2i]).replace("[", "")
                            linespics[rm2i] = str(linespics[rm2i]).replace("]", "")
                            linespics[rm2i] = str(linespics[rm2i]).replace(" ", "")
                            linespics[rm2i] = str(linespics[rm2i]).replace(",", "")
                            linespics[rm2i] = str(linespics[rm2i]).replace("'", "")
                            linespics[rm1i] = re.findall(r'\b(moon_day_+)(\w+)(.png\b)', linespics[rm1i], re.IGNORECASE)
                            linespics[rm1i] = str(linespics[rm1i]).replace("(", "")
                            linespics[rm1i] = str(linespics[rm1i]).replace(")", "")
                            linespics[rm1i] = str(linespics[rm1i]).replace("[", "")
                            linespics[rm1i] = str(linespics[rm1i]).replace("]", "")
                            linespics[rm1i] = str(linespics[rm1i]).replace(" ", "")
                            linespics[rm1i] = str(linespics[rm1i]).replace(",", "")
                            linespics[rm1i] = str(linespics[rm1i]).replace("'", "")
                            linespics[rti] = re.findall(r'\b(moon_day_+)(\w+)(.jpg\b)', linespics[rti], re.IGNORECASE)
                            linespics[rti] = str(linespics[rti]).replace("(", "")
                            linespics[rti] = str(linespics[rti]).replace(")", "")
                            linespics[rti] = str(linespics[rti]).replace("[", "")
                            linespics[rti] = str(linespics[rti]).replace("]", "")
                            linespics[rti] = str(linespics[rti]).replace(" ", "")
                            linespics[rti] = str(linespics[rti]).replace(",", "")
                            linespics[rti] = str(linespics[rti]).replace("'", "")
                            linespics[rti] = linespics[rti][:-3]
                            linespics[rti] = linespics[rti] + 'png'
                            linespics[rp1i] = re.findall(r'\b(moon_day_+)(\w+)(.png\b)', linespics[rp1i], re.IGNORECASE)
                            linespics[rp1i] = str(linespics[rp1i]).replace("(", "")
                            linespics[rp1i] = str(linespics[rp1i]).replace(")", "")
                            linespics[rp1i] = str(linespics[rp1i]).replace("[", "")
                            linespics[rp1i] = str(linespics[rp1i]).replace("]", "")
                            linespics[rp1i] = str(linespics[rp1i]).replace(" ", "")
                            linespics[rp1i] = str(linespics[rp1i]).replace(",", "")
                            linespics[rp1i] = str(linespics[rp1i]).replace("'", "")
                            linespics[rp2i] = re.findall(r'\b(moon_day_+)(\w+)(.png\b)', linespics[rp2i], re.IGNORECASE)
                            linespics[rp2i] = str(linespics[rp2i]).replace("(", "")
                            linespics[rp2i] = str(linespics[rp2i]).replace(")", "")
                            linespics[rp2i] = str(linespics[rp2i]).replace("[", "")
                            linespics[rp2i] = str(linespics[rp2i]).replace("]", "")
                            linespics[rp2i] = str(linespics[rp2i]).replace(" ", "")
                            linespics[rp2i] = str(linespics[rp2i]).replace(",", "")
                            linespics[rp2i] = str(linespics[rp2i]).replace("'", "")
                            linespics[rimm] = re.findall(r'\b(rise_+)(\w+)(.jpg\b)', linespics[rimm], re.IGNORECASE)
                            linespics[rimm] = str(linespics[rimm]).replace("(", "")
                            linespics[rimm] = str(linespics[rimm]).replace(")", "")
                            linespics[rimm] = str(linespics[rimm]).replace("[", "")
                            linespics[rimm] = str(linespics[rimm]).replace("]", "")
                            linespics[rimm] = str(linespics[rimm]).replace(" ", "")
                            linespics[rimm] = str(linespics[rimm]).replace(",", "")
                            linespics[rimm] = str(linespics[rimm]).replace("'", "")
                            ###################################                 copy the moon images into main directory
                            original1 = filepath7 + linespics[rm2i]
                            target1 = home + homename + conky + 'moon/Moongiant_python/m2.png'
                            shutil.copyfile(original1, target1)
                            original2 = filepath7 + linespics[rm1i]
                            target2 = home + homename + conky + 'moon/Moongiant_python/m1.png'
                            shutil.copyfile(original2, target2)
                            original3 = filepath7 + linespics[rti]
                            target3 = home + homename + conky + 'moon/Moongiant_python/0.png'	
                            shutil.copyfile(original3, target3)
                            original4 = filepath7 + linespics[rp1i]
                            target4 = home + homename + conky + 'moon/Moongiant_python/p1.png'
                            shutil.copyfile(original4, target4)
                            original5 = filepath7 + linespics[rp2i]
                            target5 = home + homename + conky + 'moon/Moongiant_python/p2.png'
                            shutil.copyfile(original5, target5)
                            original6 = filepath8 + linespics[rimm]
                            target6 = home + homename + conky + 'moon/Moongiant_python/rise.jpg'
                            shutil.copyfile(original6, target6)
                            ###################################                 create path for moon images and write into file
                            linespics[rm2i] = filepath7 + linespics[rm2i]
                            linespics[rm1i] = filepath7 + linespics[rm1i]
                            linespics[rti] = filepath7 + linespics[rti]
                            linespics[rp1i] = filepath7 + linespics[rp1i]
                            linespics[rp2i] = filepath7 + linespics[rp2i]
                            linespics[rimm] = filepath8 + linespics[rimm]
                            fo = open(filepath6, 'w')
                            fo.write('{}\n'.format(linespics[rm2i]))
                            fo.write('{}\n'.format(linespics[rm1i]))
                            fo.write('{}\n'.format(linespics[rti]))
                            fo.write('{}\n'.format(linespics[rp1i]))
                            fo.write('{}\n'.format(linespics[rp2i]))
                            fo.write('{}\n'.format(linespics[rimm]))
                            fo.close()
            sys.exit()
    ###################################                  create CURRENT statement to use in conky file
    num1 = 28
    num2 = num1 + 1
    num3 = num2 + 1
    num4 = num3 + 1
    num5 = num4 + 1
    num6 = num5 + 1
    row1 = "${color5}Illumination: ${color}${execpi 600 sed -n '" + str(num1) + "p' $HOME/.conky/moon/Moongiant_python/rawstrippedcleanrows.txt | awk '{print $2}'}${color5}${goto 230}Moon Age: ${color}${execpi 600 sed -n '" + str(num2) + "p' $HOME/.conky/moon/Moongiant_python/rawstrippedcleanrows.txt | awk '{print $3}'}"
    row2 = "${color5}Sun Angle: ${color}${execpi 600 sed -n '" + str(num5) + "p' $HOME/.conky/moon/Moongiant_python/rawstrippedcleanrows.txt | awk '{print $3}'}${color5}${goto 230}Moon Angle: ${color}${execpi 600 sed -n '" + str(num3) + "p' $HOME/.conky/moon/Moongiant_python/rawstrippedcleanrows.txt | awk '{print $3}'}"
    row3 = "${color5}Sun Distance: ${color}${execpi 600 sed -n '" + str(num6) + "p' $HOME/.conky/moon//Moongiant_python/rawstrippedcleanrows.txt | awk '{print $3}'}${color5}${goto 230}Moon Distance: ${color}${execpi 600 sed -n '" + str(num4) + "p' $HOME/.conky/moon/Moongiant_python/rawstrippedcleanrows.txt | awk '{print $3}'}"
    fo = open(filepath12, 'w')
    fo.write('{}\n'.format(row1))
    fo.write('{}\n'.format(row2))
    fo.write('{}\n'.format(row3))
    fo.close()
except Exception as e:
    # Manage exceptions (optional)
    filelockerror = (f"Error during script execution: {e}")
finally:
    # remove lock file
    try:
        os.remove(lock_file)
    except FileNotFoundError:
        pass  # file already removed
