
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from matplotlib.patches import Rectangle, Polygon
from physics_models import NewtonSecondLaw, InclinedPlane

G, DT = 9.81, 0.04

def _font():
    plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Noto Sans CJK TC", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

def _arrow(ax, start, vec, color, label, offset=(0, 0)):
    end = (start[0] + vec[0], start[1] + vec[1])
    artist = ax.annotate("", xy=end, xytext=start,
        arrowprops=dict(arrowstyle="-|>", color=color, lw=2.5, mutation_scale=16))
    txt = ax.text(end[0]+offset[0], end[1]+offset[1], label, color=color,
        fontsize=9, fontweight="bold", ha="center", va="center",
        bbox=dict(boxstyle="round,pad=.2", fc="white", ec="none", alpha=.9))
    return artist, txt

def _show(fig, ani):
    fig._animation = ani
    plt.show()

def run_newton():
    _font()
    model = NewtonSecondLaw(5, 10, 0)
    fig = plt.figure(figsize=(12, 8))
    fig.suptitle("牛頓第二運動定律｜力如何改變物體的運動？", fontsize=17, fontweight="bold")
    ax = fig.add_axes([.07,.39,.86,.48])
    axx = fig.add_axes([.09,.22,.37,.11])
    axv = fig.add_axes([.55,.22,.37,.11])
    ax.set_ylim(-.5, 4.7); ax.set_xlim(-6, 10); ax.set_yticks([])
    ax.set_title("水平面上的方塊（本模型忽略摩擦力）")
    ax.plot([-100,100],[.45,.45],color="#444",lw=3)
    block = Rectangle((-.45,.48),.9,.85,fc="#78B7E5",ec="#174A70",lw=2,zorder=4)
    ax.add_patch(block)
    mass_label = ax.text(0,1.48,"m",ha="center",va="bottom",fontsize=12,fontweight="bold",zorder=5,
                         bbox=dict(boxstyle="round,pad=.15",fc="white",ec="none",alpha=.9))
    info = ax.text(.02,.95,"",transform=ax.transAxes,va="top",
        bbox=dict(boxstyle="round",fc="white",ec="#aaa",alpha=.95))
    ax.text(.98,.04,"紅：合力　綠：加速度　藍：速度",transform=ax.transAxes,ha="right",fontsize=9)
    axx.set_title("位置－時間圖"); axv.set_title("速度－時間圖")
    lx,=axx.plot([],[],lw=2,color="#2474B5"); lv,=axv.plot([],[],lw=2,color="#D97706")
    for a in (axx,axv):
        a.set_xlabel("時間（秒）",fontsize=8); a.grid(alpha=.25); a.tick_params(labelsize=8)
    sliders=[]
    slider_groups=[
        ("質量 m (kg)",1,20,5,.5),
        ("水平外力 F (N)",-40,40,10,1),
        ("初速度 $v_0$ (m/s)",-5,5,0,.5)
    ]
    slider_xs=(.06,.38,.70)
    for x,(label,lo,hi,val,step) in zip(slider_xs,slider_groups):
        fig.text(x+.105,.136,label,ha="center",va="center",fontsize=9)
        slider=Slider(fig.add_axes([x,.09,.21,.022]),label,lo,hi,valinit=val,valstep=step)
        slider.label.set_visible(False)
        sliders.append(slider)
    sm,sf,sv=sliders
    bp=Button(fig.add_axes([.27,.015,.12,.045]),"▶ 播放")
    bq=Button(fig.add_axes([.44,.015,.12,.045]),"Ⅱ 暫停")
    br=Button(fig.add_axes([.61,.015,.12,.045]),"↺ 重置")
    clock={"t":0.,"run":False}; arrows=[]
    ts_all=np.arange(0,10.001,DT)
    def draw(t):
        nonlocal arrows
        for a in arrows:
            a.remove()
        arrows=[]
        m,F,v0=sm.val,sf.val,sv.val; acc=F/m
        x=v0*t+.5*acc*t*t; v=v0+acc*t
        model.reset(m,F,v0)
        block.set_xy((x-.48,.48)); mass_label.set_position((x,1.38)); ax.set_xlim(x-6.5,x+9.5)
        if abs(F)>1e-8:
            arrows.extend(_arrow(ax,(x,2.0),(math.copysign(min(2.5,.6+abs(F)/17),F),0),
                                 "crimson",f"合力 F = {F:.1f} N",(0,.28)))
        if abs(acc)>1e-8:
            arrows.extend(_arrow(ax,(x,3.0),(math.copysign(min(1.8,.5+abs(acc)/3),acc),0),
                                 "seagreen",f"a = {acc:.2f} m/s²",(0,.28)))
        if abs(v)>1e-8:
            speed_arrow=min(1.2,.45+abs(v)/6)
            arrow_start=(x+.55+speed_arrow, .90) if v<0 else (x+.55, .90)
            arrow_vec=(-speed_arrow,0) if v<0 else (speed_arrow,0)
            arrow_end=(arrow_start[0]+arrow_vec[0],arrow_start[1])
            arrows.append(ax.annotate("",xy=arrow_end,xytext=arrow_start,
                arrowprops=dict(arrowstyle="-|>",color="#2474B5",lw=2.5,mutation_scale=16)))
            arrows.append(ax.text(x+.55+speed_arrow/2,1.10,f"v = {v:.2f} m/s",
                color="#2474B5",fontsize=9,fontweight="bold",ha="left",va="bottom",
                bbox=dict(boxstyle="round,pad=.2",fc="white",ec="none",alpha=.9)))
        info.set_text(f"m = {m:.1f} kg    ΣF = {F:.1f} N    a = ΣF/m = {acc:.2f} m/s²\\n"
                      f"t = {t:.2f} s    v = {v:.2f} m/s    x = {x:.2f} m")
        ts=ts_all[ts_all<=t+1e-9]; xs=v0*ts+.5*acc*ts**2; vs=v0+acc*ts
        lx.set_data(ts,xs); lv.set_data(ts,vs)
        axx.set_xlim(0,10); axv.set_xlim(0,10)
        xr=max(2,np.max(np.abs(xs))*1.2 if len(xs) else 2)
        vr=max(2,np.max(np.abs(vs))*1.2 if len(vs) else 2)
        axx.set_ylim(-xr,xr); axv.set_ylim(-vr,vr); fig.canvas.draw_idle()
    def tick(_):
        if clock["run"]:
            clock["t"]=min(10,clock["t"]+DT); draw(clock["t"])
            if clock["t"]>=10: clock["run"]=False
        return ()
    def changed(_):
        clock.update(t=0.,run=False); draw(0)
    for s in sliders: s.on_changed(changed)
    bp.on_clicked(lambda e: clock.update(run=True))
    bq.on_clicked(lambda e: clock.update(run=False))
    def reset(e):
        clock.update(t=0.,run=False)
        for s,val in zip(sliders,[5,10,0]): s.set_val(val)
        draw(0)
    br.on_clicked(reset)
    draw(0); _show(fig,FuncAnimation(fig,tick,interval=40,blit=False,cache_frame_data=False))

def run_incline():
    _font()
    fig=plt.figure(figsize=(12,8))
    fig.suptitle("摩擦力與斜面｜物體為什麼會滑下來？",fontsize=17,fontweight="bold",x=.5,y=.98)
    ax=fig.add_axes([.06,.25,.60,.55]); info_ax=fig.add_axes([.06,.81,.42,.14]); info_ax.axis("off")
    ax.set_aspect("equal"); ax.set_xlim(-1.2,8.5); ax.set_ylim(-1,7.5); ax.axis("off")
    ax.set_title("斜面上的方塊與受力分析（箭頭長度為示意）")
    plane,=ax.plot([],[],color="#555",lw=7,solid_capstyle="round",zorder=1)
    block=Polygon([[0,0],[1,0],[1,1],[0,1]],closed=True,fc="#78B7E5",ec="#174A70",lw=2.2,zorder=5)
    ax.add_patch(block); block_text=ax.text(0,0,"m",ha="center",va="center",fontweight="bold",fontsize=14,zorder=6)
    info=info_ax.text(0,1,"",va="top",fontsize=10,linespacing=1.5,
                      bbox=dict(boxstyle="round,pad=.6",fc="#f7f7f7",ec="#aaa"))
    specs=[("質量 m (kg)",1,20,5,.5),("斜面角度 θ (°)",0,60,30,1),
           ("靜摩擦係數 μs",0,1,.5,.01),("動摩擦係數 μk",0,1,.3,.01)]
    sliders=[Slider(fig.add_axes([.15,.215-i*.037,.70,.018]),s[0],s[1],s[2],valinit=s[3],valstep=s[4])
             for i,s in enumerate(specs)]
    angle_slider=sliders[1]
    critical_region=angle_slider.ax.axvspan(0,60,facecolor="#d8f0dc",alpha=.55,zorder=-2)
    sliding_region=angle_slider.ax.axvspan(0,60,facecolor="#f6d8d8",alpha=.55,zorder=-2)
    critical_line=angle_slider.ax.axvline(0,color="red",lw=2.2,zorder=6)
    critical_label=angle_slider.ax.text(0,.84,"",transform=angle_slider.ax.get_xaxis_transform(),
        ha="center",va="bottom",fontsize=8,color="red",fontweight="bold",
        bbox=dict(boxstyle="round,pad=.15",fc="white",ec="red",alpha=.95),zorder=7)
    bp=Button(fig.add_axes([.27,.025,.12,.05]),"▶ 播放")
    bq=Button(fig.add_axes([.44,.025,.12,.05]),"Ⅱ 暫停")
    br=Button(fig.add_axes([.61,.025,.12,.05]),"↺ 重置")
    clock={"t":0.,"run":False}; vector_artists=[]
    colors={"mg":"#222222","parallel":"#D62728","perp":"#E28E2C","normal":"#2A8C55","friction":"#7B4AB5"}
    def draw(t):
        nonlocal vector_artists
        for artist in vector_artists: artist.remove()
        vector_artists=[]
        m,angle,mus,muk=[s.val for s in sliders]
        model=InclinedPlane(m,angle,mus,muk); theta=math.radians(angle)
        up=np.array([math.cos(theta),math.sin(theta)])
        normal=np.array([-math.sin(theta),math.cos(theta)])
        end=7*up; plane.set_data([0,end[0]],[0,end[1]])
        if model.is_sliding:
            disp=.5*model.acceleration*t*t; speed=model.acceleration*t
        else: disp=speed=0.
        center=end-disp*up+.43*normal
        half_l,half_h=.48,.34
        corners=np.array([center-half_l*up-half_h*normal,center+half_l*up-half_h*normal,
                          center+half_l*up+half_h*normal,center-half_l*up+half_h*normal])
        block.set_xy(corners); block_text.set_position(center)
        forces={"mg":m*9.81,"parallel":model.gravity_parallel,
                "perp":model.gravity_perpendicular,"normal":model.normal_force,
                "friction":model.kinetic_friction if model.is_sliding else model.static_friction}
        dirs={"mg":np.array([0.,-1.]),"parallel":-up,"perp":-normal,"normal":normal,"friction":up}
        labels={"mg":"重力 mg","parallel":"平行分力 mg sinθ","perp":"垂直分力 mg cosθ",
                "normal":"正向力 N","friction":"摩擦力 f"}
        scale=2.1/max(m*9.81,1)
        offsets={"mg":(.25,-.15),"parallel":(-.3,-.25),"perp":(-.5,-.1),
                 "normal":(.4,.2),"friction":(0,.35)}
        for key,val in forces.items():
            vec=dirs[key]*val*scale; endp=center+vec
            art=ax.annotate("",xy=endp,xytext=center,
                arrowprops=dict(arrowstyle="-|>",color=colors[key],lw=2.4,mutation_scale=15),zorder=8)
            txt=ax.text(endp[0]+offsets[key][0],endp[1]+offsets[key][1],
                f"{labels[key]}\\n{val:.1f} N",color=colors[key],fontsize=8.5,
                fontweight="bold",ha="center",va="center",
                bbox=dict(boxstyle="round,pad=.2",fc="white",ec="none",alpha=.9),zorder=9)
            vector_artists.extend([art,txt])
        sliding=model.is_sliding
        critical_angle=math.degrees(math.atan(mus))
        state_text="物體正在斜面上滑動" if sliding else "物體保持靜止"
        info.set_text("\n".join([
            state_text,
            rf"$m={m:.1f}\,\mathrm{{kg}}$",
            rf"$\theta={angle:.1f}^\circ$",
            rf"$\mu_s={mus:.2f}$",
            rf"$\mu_k={muk:.2f}$"
        ]))
        fig.canvas.draw_idle()
    def tick(_):
        if clock["run"]:
            clock["t"]=min(8.,clock["t"]+.04); draw(clock["t"])
            if clock["t"]>=8: clock["run"]=False
        return ()
    def update_critical_marker(_=None):
        critical_angle=math.degrees(math.atan(sliders[2].val))
        critical_region.set_x(0); critical_region.set_width(critical_angle)
        sliding_region.set_x(critical_angle); sliding_region.set_width(60-critical_angle)
        critical_line.set_xdata([critical_angle,critical_angle])
        critical_label.set_position((critical_angle,.84))
        critical_label.set_text(f"θc = {critical_angle:.1f}°")
        fig.canvas.draw_idle()
    def changed(_):
        clock.update(t=0.,run=False); update_critical_marker(); draw(0)
    for s in sliders: s.on_changed(changed)
    bp.on_clicked(lambda e: clock.update(run=True)); bq.on_clicked(lambda e: clock.update(run=False))
    def reset(e):
        clock.update(t=0.,run=False)
        for s,val in zip(sliders,[5,30,.5,.3]): s.set_val(val)
        draw(0)
    br.on_clicked(reset)
    update_critical_marker(); draw(0); _show(fig,FuncAnimation(fig,tick,interval=40,blit=False,cache_frame_data=False))
