from asyncio import events
from codecs import EncodedFile
import numpy as np
import matplotlib.pyplot as plt


def variables(enddate):

    #Time

    date = np.array(0)

    H = np.zeros((1,1))
    H[:,0] = date + 1945


    #IO Table

    IO= np.matrix([ # what j column needs from i row per unit
    [0.2,  0.02, 0, 0, 0],
    [0, 0.02, 0.3, 0.1, 0],
    [0, 0.2, 0.5, 0.2, 0],
    [0.05, 0.1, 0.5, 0.2, 0],
    [0, 0.1, 0.3, 0.2, 0.3], 
    ],dtype=object)


    #Prices

    Prices = np.array([0.2, 0.06, 0.4, 0.8, 3.])


    #Production

    labpr = np.array(['Agriculture','Energy','Heavy Industry','Light Industry','Electronics'])

    PR = np.matrix([                   #AGR,  ENRG,  H.IND,  L.IND,  ETRN
         [100., 75., 50., 50., 10.],     # capital
         [0., 0., 0., 0., 0.],       # investment
         [100., 120., 50., 15., 0.],  # produced
         [90., 40., 45., 20., 0.],   # consumed
         [10., 10., 5., -5., 0. ],   # Surplus/Deficit
         [4.,30.,2.,1.,0.1]])          # Productivity
    

    HPR = np.zeros((6,5,1))
    HPR[:,:,0] = PR  #history


    #Economy

    ECO = np.array([140., 0., 100., 7., 0., 0., 0.]) #GDP GDPgrowth Reserves Income Expenses Com.Balance Budget
    
    HECO = np.zeros((7,1))
    HECO[:,0] = ECO 


    #Expenses

    EXP = np.array([10., 4., 4., 2., 8.]) #Administration Education Healthcare Science Army

    HEXP = np.zeros((5,1))
    HEXP[:,0] = EXP 


    #Politics/Geopolitics

    POL = np.array([0., 0., 0., 10., 0., 0.]) # Internal Popularity    External popularity   Education Score   Healthcare Score  Science pts   Military power

    HPOL = np.zeros((6,1))
    HPOL[:,0] = POL


    #Population

    POP = np.array(180.)

    HPOP = np.zeros((1,1))
    HPOP[:,0] = POP


    #Percentage of working population (1/2 of total)

    WP = 0.9*np.array([50., 2., 18., 8., 0., 10., 3., 3., 2., 4.])  #Agr Enrg H.Ind L.Ind Etrn Adm Edu Hlt Sc Arm


    #Science improvements

    SC = np.array([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])   #Agr Enrg H.Ind L.Ind Etrn Adm Edu Hlt Sc Arm


    #Electronics needed for projects

    Elecproj = np.array(0.)

    #Arsenal

    ARS = np.array(10.)


    #asked

    asked = np.zeros(11)

    #activated (Science projects)
    nbtotal = 10
    activated = np.zeros(nbtotal)

    return(date, H, POP, HPOP, IO, Prices, labpr, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, asked, activated)

def statistics(H, labpr, HPR, HECO, HEXP, HPOL, HPOP, asked):
     d = np.sum(asked)
     r = int(np.ceil(np.sqrt(d)))
     l = 1
     for i in range (0,np.size(asked)):
          if asked[i] == 1:
               plt.subplot(r,r,l)
               l = l+1
               plotstat(H, labpr, HPR, HECO, HEXP, HPOL, HPOP, i)
     
     plt.show()

def plotstat(H, labpr, HPR, HECO, HEXP, HPOL, HPOP, i):
     if i <= 4:
          #plt.plot(np.transpose(H),HPR[0,i,:]) # capital (it grows too big)
          plt.plot(np.transpose(H),HPR[2,i,:])
          plt.plot(np.transpose(H),HPR[3,i,:])
          plt.legend(['Production','Consumption'])
          plt.title(labpr[i])
     elif i <= 6:
          if i == 5:
               plt.plot(np.transpose(H),HECO[0])
               plt.plot(np.transpose(H),HECO[1])
               plt.plot(np.transpose(H),HECO[2])
               plt.legend(['GDP (in million rubles)','Yearly GDP growth','Reserves'])
               plt.title(['GDP'])
          else:
               plt.plot(np.transpose(H),HECO[6])
               plt.plot(np.transpose(H),HECO[5])
               plt.plot(np.transpose(H),HECO[4])
               plt.plot(np.transpose(H),HECO[3])
               plt.legend(['Budget','Commercial Balance','Expenses','Income'])
               plt.title(['Finance'])
     elif i == 7:
          plt.plot(np.transpose(H),HEXP[0])
          plt.plot(np.transpose(H),HEXP[1])
          plt.plot(np.transpose(H),HEXP[2])
          plt.plot(np.transpose(H),HEXP[3])
          plt.plot(np.transpose(H),HEXP[4])
          plt.legend(['Administration','Education','Healthcare','Science','Army'])
          plt.title(['Expenses'])
     elif i == 8:
          plt.plot(np.transpose(H),HPOL[0])
          plt.plot(np.transpose(H),HPOL[1])
          plt.plot(np.transpose(H),HPOL[5])
          plt.legend(['Internal popularity','External popularity','Military power'])
          plt.title(['Indicators'])
     elif i == 9:
          plt.plot(np.transpose(H),HPOL[2])
          plt.plot(np.transpose(H),HPOL[3])
          plt.legend(['Education score','Healthcare score'])
     elif i == 10:
          plt.plot(np.transpose(H),np.transpose(HPOP))
          plt.legend(['Population (millions)'])
          plt.title(['Population'])

def turn(date, H, POP, HPOP, IO, Prices, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, activated):

     #New science projects effects

     (nbtotal, scPro, SC, Elecproj) = scienceProjects(SC, Elecproj, activated)



     #Investment

     PR[0] = PR[0] + PR[1]
     PR[1] = np.zeros(5)


     #Productivity

     PR[5] = np.multiply(HPR[5,:,0],np.log2(2*PR[0]/HPR[0,:,0]),SC)


     #Production
     WPP = np.zeros((1,5))
     WPP[0,:] = np.delete(WP,(5,6,7,8,9))
     PR[2] = np.multiply(WPP,PR[5])
     

     #Consumption

     PR[3] = np.matmul(PR[2],IO)   #Consumption to produce

     PR[3,0] = PR[3,0] + POP*0.1      #Food consumption

     PR[3,4] = PR[3,4] + Elecproj    #Projects


     #Surpluses

     PR[4] = PR[2] - PR[3]

     #GDP

     ECOtemp = np.dot(PR[2],Prices)
     ECO[1] = 100*ECOtemp/ECO[0] - 100
     ECO[0] = ECOtemp


     #Income

     ECO[3] = 0.05*ECO[0]

     #Expenses
     
     EXP[0] = 0.05*ECO[0]*SC[5]
     ECO[4] = np.sum(EXP)


     #Commercial Balance

     ECO[5] = np.dot(PR[4],Prices)


     #Budget

     ECO[6] = ECO[5] + ECO[3] - ECO[4]


     #Reserves

     ECO[2] = ECO[2] + ECO[6]
     

     #Edu/Health score

     POL[2] = EXP[1]*WP[6]*SC[6]
     POL[3] = EXP[2]*WP[7]*SC[7]


     #Science pts

     POL[4] = POL[4] + EXP[3]*WP[8]*SC[8]


     #Military Power

     POL[5] = EXP[4]*WP[9]*SC[9] + ARS


     #Internal popularity

     POL[0] = ECO[1]/ECO[0] + POL[2] + POL[3]   #maximizar en 100                    por hacer !!!!!!!!!!!!!!!!!!!!!!!!!!


     #External popularity

     POL[1] = POL[1] + POL[0]/2


     #Population growth
     rng = np.random.default_rng(date*328)
     R = 0.4*rng.random()+0.8
     if PR[4,0] <= 0:
          print()
          print('Careful comrade, if we depend on the imperialists for food they will slowly starve our people!')
          print()
          POP = POP + R*5*(1-0.5**np.log2(1+(POL[3]/HPOL[3,0]))) - 0.1*POP*(-PR[4,0]/PR[3,0])  #pop starts decreasing if there is imports on agriculture
     else:
          POP = POP + R*5*(1-0.5**np.log2(1+(POL[3]/HPOL[3,0])))  #Healthcare moves yearly growth within 0 and 5 million per year (with infinite Healthcare)
          
     



     
     #Working population

     WP = (POP/HPOP[0,date - 1])*WP

     
     #Histories
     H2 = H
     H = np.zeros([1,date + 1])
     H[:,0:date] = H2 
     H[:,date] = date + 1945
     HPOP2 = HPOP
     HPOP = np.zeros([1,date + 1])
     HPOP[:,0:date] = HPOP2 
     HPOP[:,date] = POP
     HPR2 = HPR
     HPR = np.zeros([6,5,date + 1])
     HPR[:,:,0:date] = HPR2 
     HPR[:,:,date] = PR
     HECO2 = HECO
     HECO = np.zeros([7,date + 1])
     HECO[:,0:date] = HECO2 
     HECO[:,date] = ECO
     HEXP2 = HEXP
     HEXP = np.zeros([5,date + 1])
     HEXP[:,0:date] = HEXP2 
     HEXP[:,date] = EXP
     HPOL2 = HPOL
     HPOL = np.zeros([6,date + 1])
     HPOL[:,0:date] = HPOL2 
     HPOL[:,date] = POL
     

     #date

     date = date + 1

     return(date, H, POP, HPOP, IO, Prices, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, activated)

def userInteraction(date, H, POP, HPOP, IO, Prices, labpr, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, asked, activated):
     print()
     print()
     print()
     print('Year ' + str(date + 1945))
     print()
     print('We have a budget of ' + str(ECO[6]) + ' million rubles from last year getting our reserves to ' + str(ECO[2]))
     print()
     k = int(input('Do you wish to invest in Gosplan?'))
     if k != 0:
          (PR, ECO) = Gosplan(PR, ECO)
     print()
     k = int(input('Do you wish to alter expenses?'))
     if k != 0:
          EXP = alterExp(ECO,EXP,SC)
     
     print()
     k = int(input('Do you wish to change the working population distribution?'))
     if k != 0:
          WP = alterDist(POP,WP,SC)
     

     print()
     k = 0
     if k != -1:
          (POL, activated, k) = science(POL, activated) 


     (date, H, POP, HPOP, IO, Prices, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, activated) = turn(date, H, POP, HPOP, IO, Prices, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, activated)
     
     print()
     k = int(input('Do you wish to check the Statistics Bureau?'))
     if k != 0:
          print('For the following data, indicate if you want to see it.')
          print()
          asked[0] = int(input('Agriculture Data'))
          print()
          asked[1] = int(input('Energy Data'))
          print()
          asked[2] = int(input('Heavy Industry Data'))
          print()
          asked[3] = int(input('Light Industry Data'))
          print()
          asked[4] = int(input('Electronics Data'))
          print()
          asked[5] = int(input('GDP Data'))
          print()
          asked[6] = int(input('Budget Data'))
          print()
          asked[7] = int(input('Expenses Data'))
          print()
          asked[8] = int(input('Indicators Data'))
          print()
          asked[9] = int(input('Scores Data'))
          print()
          asked[10] = int(input('Population Data'))
          
          statistics(H, labpr, HPR, HECO, HEXP, HPOL, HPOP, asked)

     print()

     return(date, H, POP, HPOP, IO, Prices, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, asked, activated)
     
     
def Gosplan(PR, ECO):
      print()
      print('Write how much you want to invest in capital per sector:')
      PR[1,0] = float(input('Agriculture (Current capital :' + str(PR[0,0]) +'): '))
      PR[1,1] = float(input('Energy (Current capital :' + str(PR[0,1]) +'):'))
      PR[1,2] = float(input('Heavy Industry (Current capital :' + str(PR[0,2]) +'): '))
      PR[1,3] = float(input('Light Industry (Current capital :' + str(PR[0,3]) +'): '))
      PR[1,4] = float(input('Electronics (Current capital :' + str(PR[0,4]) +'): '))

      ECO[2] = ECO[2] - np.sum(PR[1])

      return(PR, ECO)

def alterExp(ECO,EXP,SC):
     print()
     print('Write how much you want to spend in each branch (Administration is automatically calculated): ')
     EXP[0] = ECO[0]*0.1/SC[5]
     EXP[1] = float(input('Education (Currently spending ' + str(EXP[1]) + '): '))
     EXP[2] = float(input('Healthcare (Currently spending ' + str(EXP[2]) + '): '))
     EXP[3] = float(input('Science (Currently spending ' + str(EXP[3]) + '): '))
     EXP[4] = float(input('Army (Currently spending ' + str(EXP[4]) + '): '))

     return EXP

def alterDist(POP,WP,SC):
     print()
     Dist = np.zeros(10)
     print('Write the ratio at which you want the next distribution of working people to be (the necessary administration personnel will be substracted proportionately from all sectors): ')
     Dist[0] = float(input('Agriculture (Currently: ' + str(WP[0]) + '): '))
     Dist[1] = float(input('Energy (Currently: ' + str(WP[1]) + '): '))
     Dist[2] = float(input('Heavy Industry (Currently: ' + str(WP[2]) + '): '))
     Dist[3] = float(input('Light Industry (Currently: ' + str(WP[3]) + '): '))
     Dist[4] = float(input('Electronics (Currently: ' + str(WP[4]) + '): '))
     Dist[6] = float(input('Education (Currently: ' + str(WP[6]) + '): '))
     Dist[7] = float(input('Healthcare (Currently: ' + str(WP[7]) + '): '))
     Dist[8] = float(input('Science (Currently: ' + str(WP[8]) + '): '))
     Dist[9] = float(input('Army (Currently: ' + str(WP[9]) + '): '))
     print()

     POPADM = POP*0.1/SC[5] # administration
     WP  = ((POP-POPADM)/np.sum(Dist))*Dist
     WP[5] = POPADM
     print('People working in Administration: ' + str(WP[5]))

     return(WP)

def science(POL, activated):   #Only to get the new vector 'activated' (Science projects activated)
     
     (nbtotal, scPro, SC, Elecproj) = scienceProjects(activated)
     if nbtotal != np.size(activated):
          print('Error change activated vector size or nbtotal value')
     available = 0
     nb = 0
     for i in range (0, nbtotal - 1):
          if scPro[0,i] <= POL[4] and scPro(3) == 0:
               nb = nb+1
               available = np.append(available,i)
     available = np.delete(available,0)

     print('You have ' + str(POL[4]) + ' research points, that makes ' + str(nb) + ' research projects available.')
     k = int(input('Do you wish to make any research?'))
     if k != 0:
          print()
          print('The available technologies are: ')
          for i in range (0,nb - 1):
               print()
               print(str(available[i]) + ' - ' + str(scPro[1,available[i]]) + ': ' + str(scPro[2,available[i]]))
     print()
     k = int(input('Choose which sience project you want to conduct  (its number, -1 if you do not want any): '))
     if k != -1:
          activated[k] = 1
          POL[4] = POL[4] - scPro[0,k]

     return (POL, activated, k)
     

   


def scienceProjects(SC, Elecproj, activated):
     scPro = np.matrix([20.,20.,40.,30.,40.,40.,50.,60.,100.,50.,70.,80.,100.,80.,120.,120.,360.,240.],
     ['Widespread Vaccines','New Tractors','Atomic Bomb','New Machinery','First Transistors','SRBM','AK-47','H Bomb','First Computers','MRBM','ICBM','Sputnik','1st Man in Space','Nuclear Reactors','Advanced Computers','1st Man on the Moon','Advanced Computers','OGAS','1st Space Station'])



     nbtotal = int(np.size(scPro[0]))
     return (nbtotal, scPro, SC, Elecproj)

def main():
     enddate = 100
     (date, H, POP, HPOP, IO, Prices, labpr, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, asked, activated) = variables(enddate)
     print()
     print('IO Table: ')
     print(IO)
     print()
     print('Prices (Agriculture, Energy, Heavy Industry, Light Industry, Electronics)')
     print(Prices)

     for i in range (0,51):
          try:
               (date, H, POP, HPOP, IO, Prices, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, asked, activated) = userInteraction(date, H, POP, HPOP, IO, Prices, labpr, PR, HPR, ECO, HECO, EXP, HEXP, POL, HPOL, WP, SC, Elecproj, ARS, asked, activated)
          except:
               print()
               print('!')
               print('!')
               print('!')
               print('!')
               print('Value mistake: remake the plan')
          
          
          
     



     




          








if __name__ == '__main__':
	main()
