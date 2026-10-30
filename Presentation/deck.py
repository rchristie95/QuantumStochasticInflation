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
    Section("history", ("history", "motivation"),
            (1, CHAPTERS[0], "History, motivation, and the Langevin description"),
            ("assets/history_citations.json",)),
    Section("classical", ("starobinsky",)),
    Section("collective", ("collective_definitions",),
            (2, CHAPTERS[1], "Adding a mode, retaining a collective coordinate")),
    Section("joint_state", ("joint_wigner_example",), dependencies=("oscillator_states.py",)),
    Section("readout", ("collective_povms",)),
    Section("trajectories", ("oscillator_trajectories",), dependencies=("oscillator_states.py", "assets/oscillator_wigner/*.png", "assets/oscillator_wigner/manifest.json")),
    Section("canonical", ("canonical_derivation",),
            (3, CHAPTERS[2], "From the Lagrangian to a quantum boundary channel")),
    Section("continuum", ("continuum_connection",)),
    Section("boundary", ("formulation",)),
    Section("connection", ("measurement_connection",)),
    Section("massive", ("massive_spectator",)),
)
