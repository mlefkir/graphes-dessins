import xspec
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


plt.style.use("https://github.com/mlefkir/beauxgraphs/raw/main/beautifulgraphs_latex.mplstyle")

xspec.Xset.chatter = 0

xspec.Plot.device = "/null"
xspec.Plot.xAxis = 'keV'
xspec.Plot.area = True
xspec.Plot.add = True

xspec.Xset.restore("Typical_AGN_nonjetted_model.xcm")
xspec.AllModels.setEnergies(".1 100. 1100 log")
xspec.Plot("eemodel")


colors = ["#FF7C43","#46AB21","#005982","#665191"]

flux_unit=r"$\mathrm{keV}^2\left(\mathrm{counts}~ \mathrm{s}^{-1}\,\mathrm{keV}^{-1} \mathrm{cm}^{-2}\right)$"

linewidth=1.4


fig,ax = plt.subplots(1,1,figsize=(9,5.5))

x = xspec.Plot.x(1)
y = np.array(xspec.Plot.model(1))
xErrs = xspec.Plot.xErr(1)

ax.loglog()
ax.set_ylabel(flux_unit)
ax.set_xlabel("Energy (keV)")
ax.set_xlim(0.1,100)
ax.set_ylim(0.5e-2,6)
xticks = np.unique(np.ravel([np.linspace(1,10,10)*k for k in [0.1,1,10] ]))
ax.set_xticks(xticks, minor=True)
xticks_labels = [str(xticks[k]) if not (k%9) else "" for  k in range(len(xticks))]
ax.set_xticklabels(xticks_labels, minor=True)
formatter = FuncFormatter(lambda y, _: '{:.16g}'.format(y))
ax.get_xaxis().set_major_formatter(formatter)

# plot the components
for k,name in enumerate(xspec.AllModels(1).componentNames[1:]): 
    print(k+1)
    y_comp = xspec.Plot.addComp(k+1)
    if name=="xillverEc_5":
        ax.step(x, y_comp,linewidth=1.5,color=colors[k],linestyle='--',label=name,alpha=0.8)
    else :
        ax.step(x, y_comp,linewidth=1.5,color=colors[k],linestyle='--',label=name,alpha=0.8)
        
# plot the total spectrum 
ax.step(x, y,linewidth=linewidth,color="k")

# annotations and text
ax.text(35, 0.05, 'Compton\nhump',alpha=0.8, ha='center', va='bottom', transform=ax.transData,color=colors[3])
ax.text(13,1.3e-2, 'Neutral reflection',alpha=0.8,  ha='center', va='bottom', transform=ax.transData,color=colors[3])
ax.text(6,1.7, 'Fluorescent\niron lines',alpha=0.8, ha='center', va='bottom', transform=ax.transData)
ax.text(2.95,14.5e-3, 'Ionised\nreflection',alpha=0.8, ha='center', va='bottom', transform=ax.transData,color=colors[1])

ax.annotate("Ionised\nabsorptions",
            xy=(0.8, 2e-2), xycoords='data',
            xytext=(.12,2e-2), textcoords='data',color=colors[0],alpha=0.8,
            arrowprops=dict(arrowstyle="->",alpha=0.8, linewidth=1.5,connectionstyle="arc3,rad=-0.1",color=colors[0])) 
ax.annotate("Power law \& cutoff",
            xy=(25,0.42), xycoords='data',
            xytext=(12,1.2), textcoords='data',color=colors[0],alpha=0.8,
            arrowprops=dict(arrowstyle="->",alpha=0.8, linewidth=1.5,connectionstyle="arc3,rad=-0.1",color=colors[0])) 
ax.annotate("Multi-temperature\nblack body",
            xy=(0.18, 0.35), xycoords='data',
            xytext=(0.12,2.35), textcoords='data',color=colors[2],alpha=0.8,
            arrowprops=dict(arrowstyle="->",linewidth=1.5,alpha=0.8,connectionstyle="arc3,rad=-0.1",color=colors[2])) 

fig.tight_layout()
fig.subplots_adjust(top=0.98,bottom=0.12,left=0.12,right=0.97)
fig.savefig("nonjetted_AGN_X-ray.pdf")