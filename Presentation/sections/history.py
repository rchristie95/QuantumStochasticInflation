"""Presentation content: history."""
from presentation_common import *

ROOT=Path(__file__).resolve().parents[1]
START=0.
END=6.
MODE_COUNT=96
CROSSINGS=np.linspace(.35,5.65,MODE_COUNT)
RNG=np.random.default_rng(1986)
PHASES=RNG.uniform(0,2*np.pi,MODE_COUNT)
AMPLITUDES=RNG.uniform(.55,1.15,MODE_COUNT)
FREQUENCIES=RNG.uniform(.7,1.7,MODE_COUNT)
WEIGHT=.18


def displacement(j,time):
    return AMPLITUDES[j]*np.sin(2*np.pi*FREQUENCIES[j]*(np.minimum(time,CROSSINGS[j])-START)+PHASES[j])


FROZEN=AMPLITUDES*np.sin(2*np.pi*FREQUENCIES*(CROSSINGS-START)+PHASES)
KICKS=WEIGHT*FROZEN


def coarse_field(time):
    return float(KICKS[CROSSINGS<=time+1e-10].sum())


def validate_model():
    assert coarse_field(START)==0
    for j,t in enumerate(CROSSINGS):
        assert np.isclose(coarse_field(t)-coarse_field(t-1e-6),WEIGHT*displacement(j,t))
        assert np.isclose(displacement(j,t+.4),displacement(j,t))
    assert np.any(KICKS<0) and np.any(KICKS>0)
    return {'seed':1986,'start_N':START,'mode_count':MODE_COUNT,'crossing_times':CROSSINGS.tolist(),
            'initial_displacements':(AMPLITUDES*np.sin(PHASES)).tolist(),
            'frozen_displacements':FROZEN.tolist(),'weight':WEIGHT,'kicks':KICKS.tolist(),
            'field_after_crossings':np.cumsum(KICKS).tolist()}




class HistorySection:
    def history(self):
        self.step("Origins", "History: about two minutes. Starobinsky's 1986 formulation turns crossing quantum modes into an effective stochastic source.")
        self.section(1, "Stochastic inflation")
        self.timeline = Line([-4.8, 0.5, 0], [4.8, 0.5, 0], color=MUTED)
        self.play(Create(self.timeline))
        entries = [(-4.5, "1986", "Starobinsky", "Quantum noise drives\nlarge-scale Langevin evolution", "Lect. Notes Phys. 246, 107"),
                   (0, "1988", "Nambu & Sasaki", "Phase-space analysis of\nrelaxation toward slow roll", "Phys. Lett. B 205, 441"),
                   (4.5, "1994", "Starobinsky & Yokoyama", "Equilibrium distribution\nfor a self-interacting field", "Phys. Rev. D 50, 6357")]
        for x, year, author, message, citation in entries[:1]:
            self.history_entry(x, year, author, message, citation)
        self.hold()

        self.step("Developments", "Nambu and Sasaki (1988) analysed the scalar field in phase space for a new-inflation model with a Higgs-type potential. Under their stated initial conditions, velocity dispersion becomes negligible on a Hubble timescale, supporting relaxation toward slow roll. This is a model-specific result, not a universal slow-roll theorem. The timeline is selective, not an exhaustive priority history.")
        for args in entries[1:]:
            if args[1]=="1994":
                self.hold()
                self.step("Equilibrium with interactions", "Starobinsky and Yokoyama's 1994 result adds interacting-field equilibrium to the timeline. This historical example is broader than the free spectator considered in our formulation.")
            self.history_entry(*args)
        self.hold()

        self.step("Quantum question", "The effective stochastic method works. The question for this talk is what quantum state and what conditional information lie behind it.")
        question = text_line("How does stochastic evolution emerge", 30, BULK).move_to([0, -2.15, 0])
        question2 = text_line("from a quantum reduced state?", 30, BULK).next_to(question, DOWN, buff=0.16)
        self.play(FadeIn(question, shift=UP * .15), FadeIn(question2))
        self.hold()


    def history_entry(self, x, year, author, message, citation):
        dot = Dot([x, .5, 0], color=SHELL)
        year_obj = text_line(year, 38, SHELL).move_to([x, 1.3, 0])
        author_obj = text_line(author, 22, width=3.8).move_to([x, -.05, 0])
        lines=VGroup(*[text_line(line,20,INK,width=3.3) for line in message.split("\n")]).arrange(DOWN,aligned_edge=LEFT,buff=.13)
        bullet=Dot(radius=.04,color=BULK)
        contribution=VGroup(bullet,lines).arrange(RIGHT,buff=.13,aligned_edge=UP).move_to([x,-.85,0])
        bullet.shift(DOWN*.1)
        cite = text_line(citation, 16, MUTED, width=3.8).move_to([x, -1.5, 0])
        self.play(FadeIn(dot), Write(year_obj), FadeIn(author_obj), FadeIn(contribution), FadeIn(cite), run_time=.9)


    def motivation(self):
        self.step('What stochastic inflation does', 'Define Q_N at the representative patch centre, chosen to be x=0 in the homogeneous background. The sharp Fourier window retains k<k_sigma(N). No momentum variable is introduced. Pause here to explain the field definition before the explicit step function appears.')
        if hasattr(self,'slide_counter'):self.slide_counter.move_to([6,3.55,0])
        self.clear_content()
        self.remove(self.chrome)
        self.chrome=VGroup()
        self.chrome_state=None
        (ROOT/'previews'/'stochastic'/'model.json').write_text(json.dumps(validate_model(),indent=2))
        title=text_line('What stochastic inflation does',34).move_to([0,3.5,0])
        definition=equation(r'Q_N=\int\!\frac{d^3k}{(2\pi)^3}\,'
                            r'\Theta\!\bigl(k_\sigma(N)-k\bigr)\,'
                            r'\Phi_{\mathbf k}(N)',size=31).move_to([0,2.83,0])
        window=equation(r'k_\sigma(N)=\sigma a(N)H,\quad k_\sigma/a=\sigma H,\qquad'
                        r'\Theta(k_\sigma-k)=\begin{cases}1&k<k_\sigma\\0&k>k_\sigma\end{cases}',size=21).move_to([0,2.12,0])
        x0,x1=-4.6,5.9
        def xpos(t): return x0+(x1-x0)*(t-START)/(END-START)
        mode_y=.65
        amp_scale=.48
        baseline=-1.95
        def qpoint(t,q): return np.array([xpos(t),baseline+q,0])
        mode_axis=Line([x0,mode_y,0],[x1,mode_y,0],color=MUTED,stroke_width=1.2,stroke_opacity=.6)
        mode_title=text_line('Modes ordered by crossing time',21,MUTED).move_to([-.8,1.52,0])
        mode_order=equation(r'N_j=\ln\!\frac{k_j}{k_\sigma(0)}',size=21,color=MUTED).move_to([4.5,1.52,0])
        legend=VGroup(text_line('Frozen after crossing',19,BULK),text_line('Oscillating modes',19,SHELL)).arrange(RIGHT,buff=1.4).move_to([.5,-.18,0])
        qlabel=equation(r'Q_N',size=30,color=BULK).move_to([-5.65,-1.95,0])
        qcaption=text_line('Long field',18,BULK).move_to([-5.65,-1.37,0])
        zero_line=Line(qpoint(START,0),qpoint(END,0),color=MUTED,stroke_width=.9,stroke_opacity=.4)
        y_ticks=VGroup()
        for q in [-.5,0,.5]:
            y_ticks.add(Line([x0-.06,baseline+q,0],[x0+.06,baseline+q,0],color=MUTED,stroke_width=1))
            y_ticks.add(text_line(f'{q:g}',14,MUTED).move_to([x0-.28,baseline+q,0]))
        time_axis=Line([x0,-3.05,0],[x1+.15,-3.05,0],color=MUTED,stroke_width=1.2)
        ticks=VGroup()
        for k in range(7):
            ticks.add(Line([xpos(k),-3,0],[xpos(k),-3.1,0],color=MUTED,stroke_width=1))
            ticks.add(text_line(str(k),16,MUTED).move_to([xpos(k),-3.24,0]))
        time_label=equation(r'N\ \text{(e-folds)}',size=21,color=MUTED).move_to([5.15,-3.52,0])
        formula=equation(r'\Delta Q_j=c\,\varphi_j(N_j),\qquad k_j=k_\sigma(N_j)',size=25,width=8).move_to([-.9,-3.52,0])
        scope=text_line('Finite-mode illustration: boundary kicks only; blue dots retain their crossing amplitudes.',16,MUTED,width=12.6).move_to([0,-3.82,0])
        intro_footer=text_line('Quantum Stochastic Inflation',16,MUTED).move_to([4.7,-3.8,0])
        self.play(FadeIn(title),Write(definition),FadeIn(intro_footer),run_time=.8)
        self.hold()
        self.step('The sharp Fourier window', 'Theta is one for k<k_sigma and zero above. Explain the retained infrared band and the growing comoving cutoff. The physical cutoff is sigma H in de Sitter. The modes and Q are stationary at N=0 until the NEXT Right-arrow press. Ninety-six modes span the same six e-fold interval as before: only the time origin changes. The upper axis orders fixed modes by crossing time; the lower axis is actual N. Their scales coincide in de Sitter.')
        if hasattr(self,'slide_counter'):self.slide_counter.move_to([6,3.55,0])
        self.play(Write(window),FadeOut(intro_footer),run_time=.6)
        self.add(mode_axis,mode_title,mode_order,legend,qlabel,qcaption,
                 zero_line,y_ticks,time_axis,ticks,time_label,formula,scope)
        time=ValueTracker(START)
        dots=VGroup(*[Dot([xpos(t),mode_y+amp_scale*displacement(j,START),0],radius=.034,color=SHELL)
                      for j,t in enumerate(CROSSINGS)])
        # A dot has FIXED x. It oscillates only vertically, then freezes in place.
        frozen_flags=np.zeros(MODE_COUNT,dtype=bool)
        def update_dots(group):
            now=time.get_value()
            values=AMPLITUDES*np.sin(2*np.pi*FREQUENCIES*(np.minimum(now,CROSSINGS)-START)+PHASES)
            for j,dot in enumerate(group):
                if frozen_flags[j]: continue
                dot.set_y(mode_y+amp_scale*values[j])
                if now>=CROSSINGS[j]:
                    dot.set_color(BULK)
                    frozen_flags[j]=True
        dots.add_updater(update_dots)
        def field_path():
            now=time.get_value();points=[qpoint(START,0)];value=0.
            for cross,kick in zip(CROSSINGS,KICKS):
                if cross>now+1e-10: break
                points.append(qpoint(cross,value));value+=kick;points.append(qpoint(cross,value))
            points.append(qpoint(max(now,START+.00001),value))
            return VMobject(color=BULK,stroke_width=2.7).set_points_as_corners(points)
        history=always_redraw(field_path)
        qdot=always_redraw(lambda:Dot(qpoint(time.get_value(),coarse_field(time.get_value())),radius=.06,color=BULK))
        cursor=always_redraw(lambda:Line([xpos(time.get_value()),1.26,0],[xpos(time.get_value()),-2.92,0],color=INK,stroke_width=1.3,stroke_opacity=.65))
        cutoff_label=equation(r'k_\sigma(N)',size=22,color=INK).move_to([xpos(START),-.65,0])
        cutoff_label.add_updater(lambda m:m.set_x(xpos(time.get_value())))
        # Crossing flashes link each displacement to its kick without stopping time.
        def crossing_flash():
            now=time.get_value();j=int(np.searchsorted(CROSSINGS,now,side='right'))-1
            if j<0: return VGroup()
            opacity=max(0,1-(now-CROSSINGS[j])/.085)
            color=GREEN if KICKS[j]>=0 else MIX
            start=[xpos(CROSSINGS[j]),mode_y+amp_scale*FROZEN[j],0]
            end=qpoint(CROSSINGS[j],float(KICKS[:j+1].sum()))
            return VGroup(Line(start,end,color=color,stroke_width=1,stroke_opacity=.45*opacity),
                          Circle(radius=.068,color=color,stroke_width=2).move_to(start).set_opacity(opacity))
        flash=always_redraw(crossing_flash)
        clock_label=text_line('N =',18,MUTED).move_to([-5.8,.68,0])
        clock=DecimalNumber(START,num_decimal_places=2,font_size=19,color=INK).next_to(clock_label,RIGHT,buff=.08)
        clock.add_updater(lambda m:m.set_value(time.get_value()))
        self.add(flash,history,cursor,dots,qdot,cutoff_label,clock_label,clock)
        self.hold()
        self.step("Cutoff sweep: boundary kicks", 'One uninterrupted animation, without intermediate pauses, from N=0 to N=6. Q is the sharp-window long field; no momentum is introduced. Ninety-six real mode contributions have fixed horizontal positions ordered by crossing time N_j=ln[k_j/k_sigma(0)] in de Sitter. Seeded phases and amplitudes give random initial displacements. Mode spacing and signed kicks are unchanged by shifting the time origin. Orange dots oscillate vertically. Each dot freezes exactly when the cutoff passes and becomes blue. Its stored signed displacement supplies the matching kick Delta Q_j=c varphi_j(N_j) below, on the same horizontal scale. c is an illustrative quadrature weight. Only boundary accumulation is shown; bulk drift is omitted. The visual freeze records a crossing amplitude, rather than asserting arbitrary massive modes cease evolving at this cutoff. The continuum noise normalization follows from actual shell weights and mode functions.')
        if hasattr(self,'slide_counter'):self.slide_counter.move_to([6,3.55,0])
        # Exactly one play and one video: the sweep never pauses at a crossing.
        self.play(time.animate.set_value(END),run_time=16,rate_func=linear)
        self.hold()
        if not getattr(self,"cutoff_only",False):
            self.separate_regions()

    def separate_regions(self):
        self.step('Gradients and separate regions', 'For each retained Fourier mode, k/(aH)<sigma, hence k^2/(a^2 H^2)<sigma^2. This suppresses the Laplacian relative to the Hubble scale in a controlled long-wavelength expansion; it is not a bound relative to an arbitrarily small mass or a vanishing drift. The paper neglects these O(sigma^2) terms in the super-Hubble Hamiltonian. This is the local homogeneous or separate-universe approximation.')
        self.section(1,'From one patch to a patchwork')
        gradient_title=text_line('Controlled gradient expansion',23,BULK,width=5.9).move_to([-3.2,2.18,0])
        bound=equation(r'k<k_\sigma\quad\Longrightarrow\quad\frac{k^2}{a^2H^2}<\sigma^2\ll1',size=29,width=6).move_to([-3.2,1.55,0])
        patch=Circle(radius=.58,color=BULK,fill_color=BULK,fill_opacity=.25).move_to([3.25,.1,0])
        patch_label=text_line('One coarse-grained region',22,BULK,width=5.8).move_to([3.25,2.08,0])
        local=text_line('Evolve local homogeneous variables',21,MUTED,width=5.8).move_to([3.25,-.88,0])
        self.play(FadeIn(gradient_title),Write(bound),Create(patch),FadeIn(patch_label),FadeIn(local),run_time=.9)
        self.hold()

        self.step('Conditions for local evolution', 'Small sigma controls spatial gradients only while gradient corrections stay small through the evolution; sudden transitions can invalidate this on finite super-Hubble scales (Jackson et al., arXiv:2311.03281). The local homogeneous evolution must be consistent with the gravitational constraints and chosen time slicing. Local fields and the local expansion can evolve together in the classical separate-universe description. Slow roll is an additional approximation, not a requirement for the separate-universe construction (Pattison et al., arXiv:1905.06300). A classical white-noise interpretation and independent noise between spatial regions are separate questions. Sources: https://arxiv.org/abs/1905.06300 ; https://arxiv.org/abs/2311.03281 ; paper_v2.tex, super-Hubble Hamiltonian discussion.')
        conditions=VGroup()
        for y,lines in [(.64,['Smooth evolution: gradient corrections','remain small, including at transitions']),
                        (-.27,['Local homogeneous dynamics consistent','with constraints and time slicing'])]:
            bullet=Dot([-6.1,y+.12,0],radius=.04,color=BULK)
            words=VGroup(*[text_line(line,20,width=5.7) for line in lines]).arrange(DOWN,aligned_edge=LEFT,buff=.12).move_to([-3.08,y,0])
            conditions.add(bullet,words)
        slow_roll=text_line('Slow roll is an additional approximation.',20,MIX,width=6).move_to([-3.2,-2.32,0])
        refs=text_line('Pattison et al. (2019); Jackson et al. (2024)',14,MUTED,width=6).move_to([-3.2,-2.95,0])
        self.play(FadeIn(conditions),FadeIn(slow_roll),FadeIn(refs),run_time=.8)
        self.hold()

        self.step("Today's Hubble volume contains many regions", 'The circle is today\'s Hubble volume, drawn as a 2D schematic of many regions defined at a sufficiently late inflationary time. Compare COMOVING sizes: R_0=(a_0 H_0)^(-1), ell_sigma=1/k_sigma(N_late). Many regions requires k_sigma(N_late)>>a_0 H_0, after sufficient expansion beyond the exit of the present Hubble scale. In 3D their schematic number scales as (R_0/ell_sigma)^3. Do not directly compare a physical inflationary patch radius with a present physical Hubble radius. The regions evolve approximately locally once gradients are negligible, but can retain shared long-wavelength initial conditions and correlated stochastic forcing. Locally evolved does not mean statistically independent; the patchwork is not an exact tiling by disjoint top-hat windows, since the Fourier cutoff is sharp. Colour is schematic local field history, not observational data.')
        outer=Circle(radius=1.75,color=INK,stroke_width=2).move_to([3.25,.1,0])
        cells=VGroup()
        rng=np.random.default_rng(2026)
        for i in range(-4,5):
            for j in range(-4,5):
                centre=np.array([3.25+i*.4,.1+j*.4,0])
                if np.linalg.norm(centre-outer.get_center())>1.75+.4/np.sqrt(2): continue
                amount=float(np.clip(.5+.23*np.sin(.65*i)+.2*np.cos(.8*j)+rng.normal(0,.045),0,1))
                colour=interpolate_color(ManimColor(BULK),ManimColor(SHELL),amount)
                square=Square(side_length=.4).move_to(centre)
                cell=Intersection(square,outer,fill_color=colour,fill_opacity=.78,stroke_color=BG,stroke_width=.8)
                if cell.has_points(): cells.add(cell)
        today=text_line("Today's Hubble volume",24,INK,width=5.8).move_to([3.25,2.08,0])
        caption=text_line('Many locally evolved regions',22,BULK,width=5.8).move_to([3.25,-1.98,0])
        correlation=text_line('Shared initial conditions can correlate them',17,MUTED,width=6).move_to([3.25,-2.35,0])
        scale=equation(r'\underbrace{(a_0H_0)^{-1}}_{R_0}\gg'
                       r'\underbrace{k_\sigma^{-1}(N_{\rm late})}_{\ell_\sigma}',size=25,width=5.8).move_to([3.25,-2.97,0])
        self.play(FadeOut(local),Transform(patch,outer),Transform(patch_label,today),run_time=.7)
        self.play(LaggedStart(*[FadeIn(cell) for cell in cells],lag_ratio=.015),FadeIn(caption),FadeIn(correlation),run_time=1.5)
        self.add(outer)
        self.play(Write(scale),run_time=.65)
        self.hold()

