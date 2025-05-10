#----*Author--Malick-Ould-Hamdi---UTF-8--
#--Github-repo-https://github.com/Ouldgeneral/Algo
from tkinter import *

from tkinter import messagebox as box
import random
import webbrowser
#En tete Partie declaration 
context={True:'mot',False:'vecteur'}
Mot_cacher=["MALIK","ITEEM",'GARWI','SALIF','TERRE','RAFIK','ISLAM','FRERE',
            "AIMER", "UTILE", "CHANT", "DONNE", "ENTRE", "FLORE", "GRAND", "HEROS", "IMAGE", "JOUER",
    "KOALA", "LIVRE", "MONDE", "NUAGE", "OEILS", "PARIS", "QUAND", "RIVES", "SABLE", "TABLE",
    "UNION", "VIVRE", "WAGON", "XENON", "YACHT", "ZEBRE", "ABIME", "BAINE", "CALME", "DELTA",
    "ECLAT", "FICHE", "GENRE", "HOTEL", "ILETS", "JUIFS", "KARMA", "LIGNE", "MAGIE", "NAIFS",
    "OCEAN", "PRISE", "QUETE", "RAINE", "SOMME", "TIGRE", "VOILE", "WHISK", "XYLOL", "YEUSE",
    "ZONES", "ACTIF", "BANAL", "CACHE", "DURCI", "ELANS", "FORCE", "GOUET", "HUMUS", "INUIT",
    "JANTE", "KAYAK", "LEGER", "METAL", "NEIGE", "OPALE", "PAIRE", "QUIET", "ROMAN", "SAUTE",
    "TIENS", "UNITE", "VASTE", "WEEDS", "YVRES", "ZORRO", "AVION", "BOITE", "COEUR", "DENSE",
    "EPOUX", "FABLE", "GALET", "HABIT", "ILEON", "JOLIE", "KIOSK", "LOUPE", "MOTIF", "NIDAS",
    "ONGLE", "PETIT", "QUOTA", "RANGE", "SOURD", "TOILE", "VITAL", "VITES", "WITHE", "ZINCS",
    "AILES", "BOUTE", "CRANE", "DOUCE", "ESPOI", "FUIES", "GEMME", "HURLE", "INDEX", "JURER"
            ]
deja=[]
Cache=[]
Score=10
Aider=0
mot=False #ca permet de jouer au mot
essaies=5 #nombre d'essais par defaut 5
res_essais=[] #Resultat graphique de l'essai serait stocke et manipuler dans ce tableau

def Ajouter():
    #cette fonction permet a l'utilisateur d'ajouter un mot a la liste des mot aleatoire
    global Mot_cacher
    mot=Ajout.get().upper()
    if(mot.isalpha() and len(mot)==5): #accepte que les mots de cinq caractere et contenant les lettres alphabetique seulement
        Le_mot="\n"+mot
        try:
            with open("Les_mots.mot","a") as file:
                if(mot in List.get("0",END)):
                    box.showwarning("Erreur","Le mot existe deja")
                else:
                    if(mot not in Mot_cacher and mot not in List.get("0",END)):
                        Mot_cacher+=[mot]
                        List.insert("0",mot)
                        file.write(Le_mot)
                    
        except FileNotFoundError:
            with open("Les_mots.mot","w") as file:
                if(mot not in List.get("0",END) and mot not in Mot_cacher):
                    Mot_cacher+=[mot]
                    List.insert("0",mot)
                    file.write(Le_mot)
                else:
                    box.showwarning("Erreur","Le mot existe deja")
        except PermissionError:
            return box.showerror("Erreur","Erreur de permission Motus ITEEM ne peut pas sauvegarder la liste de mot dans ce repertoire veuillez changer de repertoire")
    else:
        return box.showerror("Erreur","Le mot ne doit pas contenir des chiffres et ou doit contenir  5 caractere ")

def genere():
    #cette fonction choisit un mot au hasard dans la liste si la variable mot est vrai 
    # sinon ell genere un vecteur rempli aleatoirement par des chiffres entre 0 et 9
    global Cache,mot
    ask=box.askyesno("Mot cache","Voulez vous jouer au mot cache ou non")
    if(ask):mot=True
    else:mot=False
    
    if(mot==True):
        Cache=list(random.choice(Mot_cacher).upper())
        List_de_mot.pack(side=LEFT,expand=YES,fill=Y)
        Context['text']='Deviner le Mot cacher'
    else:
        List_de_mot.pack_forget()
        Context['text']='Deviner le Vecteur cacher'
        for i in range(5):
             Cache+=[random.randint(0,9)]
    
    Les_Entrees[0].focus_force()
    


def reprendre():
    #cette fonction sert au joueur de reprendre le jeu elle reinitialise toutes les valeurs a leur etat originale et regenere le mot ou vecteur a chercher
    global Score,essaies,res_essais,Cache,Aider,deja,mot
    #Reinitialisation
    mot=False
    Aider=0
    deja=[]
    Aide['text']=f"Aidez(Score-{Aider+1})"
    Reprendre['bg']='gray'
    info_aide['text']=f"{Aider}"
    Cache=[]
    essaies=5
    Score=10
    score['text']=f'Score:{Score}'
    genere() #Regenere
    for x in Les_Entrees:
        #nettoies toutes les entrees
        x.delete("0")
        x['bg']='white'
    Les_Entrees[0].focus_set()
    for x in res_essais: #Enleve tout les resultats graphique du jeu precedent
        x.pack_forget()
        res_essais=[]
    #Retablissements des boutons disparu comme Verifier et aider
    ver.pack(fill=X,expand=YES,side=LEFT)
    Sort.pack_forget()
    Aide.pack(fill=X,expand=YES,side=LEFT)
    Sort.pack(fill=X,expand=YES,side=LEFT)
    window.bind('<Return>',lambda e:permettre())
def permettre():
    #Cette fonction empeche l'utilsateur de verifier s'il ne remplit pas toutes les cases
    Permis=True
    for x in Les_Entrees:
        if(len(x.get())<1):Permis=False
    if(Permis==True and essaies>0):app()
    else:
        if(essaies<1):
            return box.showwarning("Essaies ecouler","Vos essaies sont finis veuillez reprendre")
        return box.showwarning("Erreur","Veuillez remplir  toutes les cases ")


def app():
    #Cette fonction est la foction principale du logique du programme
    Resultat=[0,0,0,0,0] #On assume que rien n'est correcte
    Proposition=[]
    global essaies,res_essais,Les_Entrees,Score
    #Prise du contenu des entrees et son placement dans la case correspondante dans le vecteur de proposition
    for x in Les_Entrees:
        if(mot==False):
            Proposition+=[int(x.get())]
        else:
            Proposition+=[x.get()]
    #recherche des elements existants et mal placee
    for i in range(5):
        for j in range(5):
            if(Proposition[i]==Cache[j] and i!=j):Resultat[i]=2
    #recherche des elements existants et bien placee
    for i in range(5):
        for j in range(5):
            if(Proposition[i]==Cache[j] and i==j):Resultat[i]=1
    egal=True #on assume que tout est correcte
    #on cherche une condition pour que egal soit faux
    for i in range(5):
        if(Resultat[i]==2 or Resultat[i]==0):
            egal=False
    
    colors={0:'red',1:'green',2:'yellow'}
    #Affichage graphique du resultat
    a=Frame(graph)
    a.pack(side=TOP,fill=X,expand=YES)
    b=Frame(a,bg="cyan")
    b.pack(side=TOP,fill=X,expand=YES)
    Label(b,text=f"Essaies:{6-essaies}/5",bg="cyan",font=("Arial",16)).pack(side=LEFT)
    #Affichage du resultat de test
    for x in range(5):
        Label(a,text=Resultat[x],bg=colors[Resultat[x]],width=1,justify="center",font=("Arial",35)).pack(side=LEFT,fill=X,expand=YES)
        if(x<4):
            Label(a,text="-",width=1,justify="center",font=("Arial",35)).pack(side=LEFT,fill=X,expand=YES)
    Mal=[]#vecteur pour contenir les mal placee ou proppsitions inexistante pour manipuler l'affichage
    for i in range(5):
        if(Resultat[i]!=1):
            Les_Entrees[i].delete("0",END)#si la proposition n'est strictement vrai(1 dans resultats) nettoyer sa case correpondante
            Mal+=[Les_Entrees[i]]
            Mal[0].focus_set()#positionner le curseur sur la premiere mauvaise reponse
    #Mettres l'ensemble graphique dans la liste manipulatrice
    res_essais+=[a]
    ess={1:"Premier",2:"Deuxieme",3:"Troisieme",4:"Quatrieme,",5:"Cinquieme"}
    statut={1:"Excellent",2:"Bien",3:"Passable",4:"Faible,",5:"Tres Faible"}

    context2=Cache
    if(mot==True):context2="".join(Cache).upper()
    if(egal==False):
        Score-=2
        if(Score<0):Score=0
    else:
        window.bind('<Return>',lambda e:reprendre())
        ver.pack_forget()
        Aide.pack_forget()
        Reprendre['bg']='green'
        ask=box.askyesno("Felicitations",
                     f"Vous avez gagnez au {ess[6-essaies]} essaie le {context[mot]} cachee etait {context2} votre score est {Score} vous etes {statut[6-essaies]} on vous a aidez {Aider} fois\nVoulez vous rejouer")
        
        if(ask):reprendre()
        else:return    
    score['text']=f"  Score:{Score}"
    essaies-=1
    if(essaies<1):
        window.bind('<Return>',lambda e:reprendre())
        Reprendre['bg']='green'
        ver.pack_forget()
        Aide.pack_forget()
        ask=box.askyesno("Vous avez Perdu",
                        f"Vous avez perdu le {context[mot]} cachee etait {context2} votre score est {Score} vous etes vraiement Nulle on vous a aidez {Aider} fois\nVoulez vous rejouer"
                        )
        if(ask):reprendre()
        else:return
def verify(e,x):
    #Cette fonction verifie les entrees et supprime les caracteres invalide
    e['bg']='white'
    if(len(e.get())>1):
        e.delete(0)
    if(e.get().isdigit()==False and mot==False):
        e.delete(0,END)
    up=e.get().upper()
    e.delete(0,END)
    e.insert("0",up)
    if(mot==True and e.get().isdigit()==True):e.delete("0",END)
    if(len(e.get())==1 and (e.get().isdigit()==True or mot==True)):
        idx=x.index(e)
        if(idx<4):
            x[idx+1].focus_set()
    
def aider():
    #Cette fonction aide le joueur 3 fois en lui montrant une partie aleatoire  de ce que l'on cache 
    global Aider,deja,Score
    if(Score<3):
        return box.showwarning("Score insuffisant","Vous n'avez pas assez de score pour obtenir de l'aide")
    if(Aider>2):
        box.showwarning("Ahhh","Faites un peu d'effort ")
        Aide.pack_forget()
        return
    x=random.randint(0,4)
    if(x in deja):return aider()
    Les_Entrees[x].delete("0")
    Les_Entrees[x]['bg']='green'
    Les_Entrees[x].insert("0",Cache[x])
    Aider+=1
    
    Score-=Aider
    score['text']=f"  Score:{Score}"
    info_aide['text']=f"{Aider}"
    deja+=[x]
    Aide['text']=f"Aidez(Score-{Aider+1})"
#Interface graphique du programme
window=Tk()
window.title("Motus ITEEM")
window.iconbitmap('C:\\Users\\Malick\\Desktop\\Projet algo\\iteem_1.ico')
window.resizable(False,False) #Empeche l'aggrendissement de l'interface
#Containeur graphique
graph=Frame(window)
graph.pack(side=LEFT,expand=YES ,fill=Y)
List_de_mot=Frame(window)
Ajout_de_mot=Frame(List_de_mot)
Ajout_de_mot.pack(side=TOP,expand=YES,fill=X)

f0=Frame(graph)#Pour les phrases en haut et le score
f0.pack(side=TOP,expand=YES,fill=X)

f1=Frame(graph)#Pour les entrees 
f1.pack(expand=YES ,fill=X)

f2=Frame(graph)#Pour les bouttons
f2.pack(side=TOP,fill=BOTH,expand=YES)
f=Frame(f0)
f.pack(side=LEFT)
#Parties Visibles
Button(f,text='A propos de Motus ITEEM',command=lambda:box.showinfo("Motus Iteem","Motus iteem est un jeu de devinette de mot et de vecteur cache  cette version a ete code par\n Malick Ould Hamdi")).pack(side=TOP)
Button(f,text='Code_Source',command=lambda:webbrowser.open_new("https://github.com/Ouldgeneral/Algo")).pack(side=TOP)

Label(f,text="1:Bien Placee ,2:Mal Placee ,0:Ca n'existe pas Nombre d'aide:").pack(side=LEFT)
info_aide=Label(f,text=f"{Aider}")
info_aide.pack(side=LEFT,fill=X,expand=YES)
Context=Label(f0,font=('Arial',16))
Context.pack(side=LEFT)
score=Label(f0,text=f"  Score:{Score}",font=("Arial",35),justify="left")
score.pack(side=TOP)

#Les bouttons
Reprendre=Button(f2,text="Reprende",command=reprendre)
Reprendre.pack(side=LEFT ,fill=X,expand=YES)
ver=Button(f2,text="Verifiez",bg="green",command=permettre)
ver.pack(side=LEFT ,fill=X,expand=YES)
Aide=Button(f2,text=f"Aidez(Score-{Aider+1})",command=aider)
Aide.pack(side=LEFT ,fill=X,expand=YES)
Sort=Button(f2,text="Sortir",bg="red",command=window.destroy)
Sort.pack(side=LEFT ,fill=X,expand=YES)

#Les Entres
Les_Entrees=[]
for x in range(5):
    Entree1=Entry(f1,width=1,font=("Arial",35),justify="center")
    Entree1.pack(side=LEFT,fill=BOTH,expand=YES)
    if(x<4):
        Label(f1,text="-" ,font=("Arial",35),justify="center").pack(side=LEFT,expand=YES,fill=X)
    Les_Entrees+=[Entree1]
    Les_Entrees[x].bind("<KeyRelease>",lambda e, s=Les_Entrees[x]:verify(s,Les_Entrees))#fonction de verification d'entres
Les_Entrees[0].focus_set()

#Liste des mots cacher et option d'en ajouter
Label(Ajout_de_mot,text="Ajouter un mot",font=("Arial",20)).pack(side=TOP)
Ajout=Entry(Ajout_de_mot)
Ajout.pack(side=LEFT,expand=YES,fill=X)
Button(Ajout_de_mot,text='Ajouter',command=Ajouter).pack(side=LEFT)

List=Listbox(List_de_mot)
try:
    with open("Les_mots.mot","r") as file:
        Le_mot=file.read().splitlines()
        for x in Le_mot:
            if(len(x)==5 and x not in Mot_cacher and x.isalpha()):
                Mot_cacher+=[x.upper()]
except FileNotFoundError:
    ()
except PermissionError:
    ()
for x in sorted(Mot_cacher):
    List.insert(END,x)
List.pack(side=TOP,expand=YES,fill=Y)

#Si l'utilisteur click entree on verifie
window.bind('<Return>',lambda e:permettre())
#Appele automatique a la fonction generatrice

genere()

#Demarrage du programme
window.mainloop()
