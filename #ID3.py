import math 
import pandas as pd

#LOAD DATASET
dataset = pd.read_csv('tennis.csv')
target = 'play'
Pri = dataset 

def ID3(dataset):#Calculating entropy and info Gain
  P=0
  N=0
  Es=0
  for i in dataset[target]:#For Full Data
    if i=='yes':
      P+=1
    else:
      N+=1
  T=int(dataset.shape[0])
  try:
      M1=math.log2(P/T)
  except:
      M1=0
  try:
      M2=math.log2(N/T)
  except:
      M2=0

  Es = (-1*((P/T)*M1))-(N/T)*M2
#   print(P,N,Es)

  if Es == 0 :
      if P == 0:
          return "no"
      else:
          return "yes"
    #   print("LEAF")

  Others = list(dataset.columns)
  Others.remove(target)
  FE = []
  for C in dataset[Others]:#For Diffrent Features
    Name = C
    # print(Name)
    C= dataset[C]
    s = set(C)
    AE=0
    for i in s: # Unique values
      ind=0
      P=0
      N=0
      E=0
      for j in C: # Full Iterate
        if j==i: # Unique Equates
          if dataset[target].iloc[ind]=='yes': # Yes
            P+=1
          else:
            N+=1
        ind+=1
      T1=P+N
      try:
        M1 = math.log2(P/T1)
      except:
        M1 = 0

      try:
        M2 = math.log2(N/T1)
      except:
        M2 = 0
      E = (-1*((P/T1)*M1))-(N/T1)*M2
      if E == -0.0:
        E = 0
      
      AE += ((P+N)/T)*E
    #   print(i,P,N,E,((P+N)/T)*E)
    # print(AE)
    FE.append([Name,Es-AE])
  return FE    

# Main Driving Function 

ANSr=[] # For leaf nodes
Tree = [] # For Parent Nodes
Serial=[] # Halper List
NDS =[] # Dataset Stack
NDS.append(dataset)
Serial.append(target)

while(not len(NDS)==0):# Making Decision Tree  
    dataset = NDS.pop()
    Name = Serial.pop()
    FE = ID3(dataset)
    
    if (type(FE) == str):
        ANSr.append([FE,Name])
    else:
        DF = sorted(FE,key=lambda x: float(x[1]),reverse=True)
        newDataset = set(dataset[DF[0][0]])
        NPar = DF[0][0]
        print("\n\n")
        print(NPar)
        print("\n\n")
        Tree.append(Name)
        Tree.append(NPar)
        for Npar, df_region in dataset.groupby(NPar):# Dataset Divide
            NDS.append(df_region)
            Serial.append(Npar)           
        # print(NPar,Serial)


print("\nLeaf Nodes -> ",ANSr)
print("Parent Nodes -> ",Tree)
XO=[]

def TREE(ANSr, Tree):# Tree Form STORE and Display
    Tree = Tree[1:]
    RN = Tree.pop(0)
    while(not len(Tree)==0):
      XOO=[]
      print(RN,end=" -> ")
      XOO.append(RN)
      CL = set(Pri[RN])
      NN = Tree.pop(0)
      if NN in CL:
        print(NN,end=" -> ")
        XOO.append(NN)
        NN = Tree.pop(0)
        while not NN in CL:
          XOO.append(NN)
          print(NN,end=" -> ")
          if len(Tree)==0:
            break
          NN = Tree.pop(0)
        if NN in CL:
          Tree.insert(0,NN)
        CCl = set(Pri[XOO[-1]])
        C=0
        for W in ANSr:
          if W[1] in CCl:
            print(W,end=" | ")
            XOO.append(W)
            CCl.remove(W[1])
            C+=1
          if len(CCl)==0:
            ANSr=ANSr[C:]
            break

      XO.append(XOO)
      print(" ")
      # print(Tree)
    XOO=[]
    if not len(ANSr)==0:
      XOO.append(RN)
      print(RN,end=" -> ")
      while not len(ANSr)==0:
        NN = ANSr.pop(0)
        XOO.append(NN)
        print(NN,end=" | ")
    XO.append(XOO)
    print(" ")
    

def TREE2(ANSr, Tree): # Simple Tree Formation
    Tree = Tree[1:]
    for i in Tree:
        nodes = set(Pri[i])
        child=[]
        for j in Tree:
            if j in nodes:
                child.append(j)
                Tree.remove(j)
        for j in nodes:
            for Y in ANSr:
                if j == Y[1]:
                    child.append(Y)
                    ANSr.remove(Y)
        XO.append([i,child])
        # print(child)


print("\n--------____---------\n")
print("STored Final TREE\n")

TREE(ANSr, Tree)

print("\n--------____---------\n")
print("Final TREE\n")

FXO=XO
XO=[]
TREE2(ANSr, Tree)

# Printing Simple Tree

YO=[]
for i in XO: 
    YO.append(i)
    for j in i[1]:
        # print(j)
        if not len(j)==2:
            # print(j)
            ind = Tree.index(j)
            YO.append([j,[Tree[ind+1]]])
for i in YO:
    if not len(i)==2:
        print(i,":",end=" ")
    else:    
        print(i[0],":",end=" ")
        for j in i[1]:
            print(j,end=" | ")
    
    print(" ")

#Prediction Making

print("\n--------____---------\n")
print(" Prediction \n")


Others = list(Pri.columns)
Others.remove(target)
PR={}
# PR={'outlook': 'rainy', 'temperature': 'mild', 'humidity': 'high', 'windy': 'weak'}
# yes

for i in Others:
  Pos = set(Pri[i])
  opt = ' / '.join([str(elem) for elem in Pos])
  Temp = input("Enter "+i+" ("+ opt +") : ")
  PR[i]=Temp

# print(PR)

S = FXO[0][0]
while True:
  # print(S)
  V = PR[S]
  for i in FXO:
    for j in i:
      if len(j)==2:
        if j[1]==V:
          print("\nPredicted ans = ",j[0])
          exit()
      elif j== V:
        a=FXO.index(i)
        b=i.index(j)
        S=FXO[a][b+1]
      
#rainy mild high weak
