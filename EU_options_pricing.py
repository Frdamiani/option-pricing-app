import math as m
import scipy.stats as st
import tkinter as tk
import tkinter.ttk as ttk

def pbs(S,K,T,r,sig,typ='call'):
 if T==0 or sig==0:
  return max(0,S-K) if typ=='call' else max(0,K-S)
 d1=(m.log(S/K)+(r+0.5*sig*sig)*T)/(sig*m.sqrt(T))
 d2=d1-sig*m.sqrt(T)
 if typ=='call':
  return S*st.norm.cdf(d1)-K*m.exp(-r*T)*st.norm.cdf(d2)
 return K*m.exp(-r*T)*st.norm.cdf(-d2)-S*st.norm.cdf(-d1)

def upd():
 S=float(eS.get()); K=float(eK.get()); T=float(eT.get())
 r=float(er.get()); sig=float(eSig.get()); typ=opt.get()
 print("S=",S,"K=",K,"T=",T,"r=",r,"sig=",sig,"typ=",typ)
 pr=pbs(S,K,T,r,sig,typ)
 labRes.config(text="Prix de l'option : %.4f" % pr)

root=tk.Tk()
root.title("CALL/PUT options EU")

params=[
 ("Spot (S)","100"),
 ("Strike (K)","100"),
 ("Mat (T, en années)","1"),
 ("risk free rate (r)","0.05"),
 ("Vol (σ)","0.2")
]

ents=[]
for txt,defv in params:
 l=tk.Label(root,text=txt); l.pack()
 e=tk.Entry(root); e.insert(0,defv); e.pack()
 ents.append(e)

eS,eK,eT,er,eSig=ents

opt=tk.StringVar(value="call")
f=tk.Frame(root); f.pack(pady=5)
ttk.Radiobutton(f,text="Call",variable=opt,value="call").pack(side=tk.LEFT,padx=5)
ttk.Radiobutton(f,text="Put",variable=opt,value="put").pack(side=tk.LEFT,padx=5)

btn=tk.Button(root,text="Calculer",command=upd)
btn.pack(pady=5)

labRes=tk.Label(root,text="Prix de l'option :")
labRes.pack(pady=5)

root.mainloop()
