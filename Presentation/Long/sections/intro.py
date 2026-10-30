"""Presentation content: intro."""
from presentation_common import *


class IntroSection:
    def introduction(self):
        self.step("Title page", "Quantum Stochastic Inflation, arXiv:2606.12636. Presenter Robson Christie, Pusan National University, South Korea. Collaborators Jaewoo Joo, Greg Kaplanek, Vincent Vennin and David Wands. The QR code links to the arXiv abstract page, verified against the published author list.")
        title=text_line("Quantum Stochastic Inflation",51,width=12.3).move_to([0,2.45,0])
        rule=Line([-6,1.8,0],[6,1.8,0],color=BULK,stroke_opacity=.6)
        presenter=text_line("Robson Christie",34,BULK).move_to([-2,1.12,0])
        affiliation=text_line("Pusan National University, South Korea",23,MUTED,width=7.5).move_to([-2,.55,0])
        collaborators=VGroup(text_line("With Jaewoo Joo, Greg Kaplanek,",24,width=7.7),
                             text_line("Vincent Vennin and David Wands",24,width=7.7)).arrange(DOWN,buff=.22).move_to([-2,-.5,0])
        identifier=text_line("arXiv:2606.12636",29,SHELL).move_to([-2,-1.65,0])
        link=text_line(PAPER_URL,20,MUTED,width=7.5).move_to([-2,-2.2,0])
        qr=self.paper_qr().move_to([4.55,-.25,0])
        scan=text_line("Read the paper",21,MUTED,width=3).move_to([4.55,-2.02,0])
        self.play(Write(title),Create(rule),FadeIn(presenter),FadeIn(affiliation),run_time=1.4)
        self.play(FadeIn(collaborators),Write(identifier),FadeIn(link),FadeIn(qr),FadeIn(scan))
        self.hold()

        self.step("Talk outline", "Classical theory comes first: history, motivations, moving cutoffs and Langevin dynamics. The toy model follows with collective oscillators and reduced versus conditional Wigner trajectories. Quantum stochastic inflation then derives the boundary channel from the Lagrangian and ends with massive spectator results.")
        self.clear_content()
        heading=text_line("Talk outline",43).move_to([0,3,0])
        rows=VGroup()
        for i,label in enumerate(CHAPTERS,1):
            number=text_line(f"0{i}",31,MIX)
            name=text_line(label,29,width=10)
            rows.add(VGroup(number,name).arrange(RIGHT,buff=.55))
        rows.arrange(DOWN,aligned_edge=LEFT,buff=.48).move_to([0,-.15,0])
        self.play(Write(heading))
        self.play(LaggedStart(*[FadeIn(row,shift=RIGHT*.15) for row in rows],lag_ratio=.18),run_time=1.7)
        self.hold()


    def paper_qr(self):
        """Native vector QR avoids raster resampling and image-backend dependencies."""
        encoder=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4)
        encoder.add_data(PAPER_URL);encoder.make(fit=True)
        matrix=encoder.get_matrix();count=len(matrix);side=2.8;cell=side/count
        result=VGroup(Square(side_length=side,fill_color=WHITE,fill_opacity=1,stroke_width=0))
        for row,values in enumerate(matrix):
            col=0
            while col<count:
                if not values[col]:
                    col+=1
                    continue
                start=col
                while col<count and values[col]:col+=1
                run=col-start
                block=Rectangle(width=run*cell,height=cell,fill_color=BLACK,fill_opacity=1,stroke_width=0)
                block.move_to([-side/2+(start+run/2)*cell,side/2-(row+.5)*cell,0])
                result.add(block)
        return result

