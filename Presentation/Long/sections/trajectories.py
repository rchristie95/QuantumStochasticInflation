"""Presentation content: trajectories."""
from presentation_common import *
from hashlib import sha256


def wigner_image(path):
    """Manim excludes pixel_array from hashes, so include the file contents."""
    image=ImageMobject(str(path))
    image.asset_content_digest=sha256(Path(path).read_bytes()).hexdigest()
    return image


class TrajectoriesSection:
    def oscillator_trajectories(self):
        assets=ASSET_DIR/'oscillator_wigner'
        data=make_assets(assets)
        images=[];purities=[];records=[]
        for n,row in enumerate(data['rows'],1):
            self.step(f"Oscillator trajectories: n={n}", "Compare the unconditioned reduced-map state (Master), one recorded Fock history and one recorded position history. Same initial pure state VarQ=1, VarP=1/4; every fresh oscillator is a pure squeezed vacuum with Varq=1/4, Varp=1. No free evolution: this is an addition-only discrete toy channel, not a GKLS time simulation. Each addition requires Right. Fock record m2,...,m7=(1,0,1,0,0,0); position record r2,...,r7=(0.8,-0.6,0.5,-0.4,0.3,-0.2). These are selected possible records, not typical or ensemble averages. Wigner grids are computed from the actual conditional wavefunctions; Fock negativity is retained. All columns use fixed Q in [-3,3], P in [-8,8] and common signed colour limits +/-1/pi. Each conditional Wigner function integrates to one. The Master column is unconditioned; Fock and Q are conditioned on recorded outcomes. Purities use the full numerical domain, not only the displayed window. The master state is mixed; each recorded conditional state is pure. Averaging all full histories, not these two selected histories, gives the master state.")
            if n==1:
                self.section(2,"One process, three conditional states")
                stage=equation(r"n=1:\quad\text{same initial pure oscillator}",size=33).move_to([0,2.33,0])
                self.play(Write(stage))
                for x,kind,title,color in [(-4.4,'master','Master (unconditioned)',BULK),(0,'fock','Fock',SHELL),(4.4,'position','Q',GREEN)]:
                    image=wigner_image(assets/f'{kind}-1.png').stretch_to_fit_width(3.45).stretch_to_fit_height(2.65).move_to([x,0,0])
                    ax=Axes(x_range=[-3,3,1.5],y_range=[-8,8,4],x_length=3.45,y_length=2.65,tips=False,axis_config={'stroke_opacity':.45,'stroke_width':1.2}).move_to([x,0,0])
                    heading=text_line(title,25,color,width=3.9).move_to([x,1.77,0])
                    labels=VGroup(equation("Q_n",size=20).move_to([x+1.95,.18,0]),equation("P_n",size=20).move_to([x-1.95,.75,0]),equation("-3",size=16).move_to([x-1.65,-1.49,0]),equation("3",size=16).move_to([x+1.65,-1.49,0]),equation("8",size=16).move_to([x-1.85,1.3,0]),equation("-8",size=16).move_to([x-1.9,-1.28,0]))
                    purity=equation(r"\mu=1",size=29,color=color).move_to([x,-1.95,0])
                    record=text_line("No outcomes yet",20,MUTED,width=3.8).move_to([x,-2.58,0])
                    self.play(FadeIn(image),Create(ax),FadeIn(heading),FadeIn(labels),Write(purity),FadeIn(record),run_time=.65)
                    images.append(image);purities.append(purity);records.append(record)
                legend=text_line("Wigner colour: blue positive, orange negative | fixed axes and colour scale",18,MUTED).move_to([0,-3.12,0])
                self.play(FadeIn(legend))
            else:
                new_stage=equation(fr"n={n-1}\ \longrightarrow\ {n}:\quad\text{{add one fresh oscillator}}",size=33).move_to(stage)
                self.play(Transform(stage,new_stage),run_time=.45)
                for j,(x,kind,color) in enumerate([(-4.4,'master',BULK),(0,'fock',SHELL),(4.4,'position',GREEN)]):
                    target=wigner_image(assets/f'{kind}-{n}.png').stretch_to_fit_width(3.45).stretch_to_fit_height(2.65).move_to(images[j])
                    mu=row['master_purity'] if kind=='master' else 1.
                    ptext=equation(fr"\mu={mu:.3f}" if kind=='master' else r"\mu=1",size=29,color=color).move_to(purities[j])
                    if kind=='master': label="Trace over the output"
                    elif kind=='fock': label=f"m = {row['fock_outcome']} | p = {row['fock_probability']:.3f}"
                    else: label=f"r = {row['position_outcome']:+.2f}"
                    rtext=text_line(label,19,color,width=3.9).move_to(records[j])
                    self.play(Transform(images[j],target),Transform(purities[j],ptext),Transform(records[j],rtext),run_time=.75)
                    # Transform copies pixels but does not copy custom metadata.
                    images[j].asset_content_digest=target.asset_content_digest
            self.hold()

