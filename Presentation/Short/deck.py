"""Section order and build dependencies. This module requires no rendering runtime."""
from dataclasses import dataclass

CHAPTERS = ["Classical theory", "Toy model", "Quantum stochastic inflation"]


@dataclass(frozen=True)
class Section:
    id: str
    methods: tuple[str, ...]
    chapter: tuple[int, str, str] | None = None
    dependencies: tuple[str, ...] = ()

    @property
    def source(self):
        return f"sections/{self.id}.py"


SECTIONS = (
    Section("intro", ("introduction",)),
    Section("history", ("motivation",),
            (1, CHAPTERS[0], "Moving cutoff and the classical Langevin description"),
            ("sections/condensed.py",)),
    Section("classical", ("short_classical",)),
    Section("collective", ("short_collective",),
            (2, CHAPTERS[1], "Adding a mode, retaining a collective coordinate")),
    Section("joint_state", ("joint_wigner_example",), dependencies=("oscillator_states.py",)),
    Section("readout", ("short_readout",), dependencies=("assets/paper_povm.png", "assets/paper_povm.tex")),
    Section("trajectories", ("oscillator_trajectories",), dependencies=("oscillator_states.py", "assets/oscillator_wigner/*.png", "assets/oscillator_wigner/manifest.json")),
    Section("canonical", ("short_canonical",),
            (3, CHAPTERS[2], "The retained field mode and its quantum boundary channel")),
    Section("boundary", ("formulation",)),
    Section("connection", ("measurement_connection",)),
    Section("massive", ("short_massive",)),
)
