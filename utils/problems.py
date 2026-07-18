"""Named problem presets for the debate panel."""

PROBLEMS = {
    "two-body": {
        "slug": "two-body-gravity",
        "text": (
            "Model the gravitational two-body problem (a small mass orbiting a large one). "
            "Provide the governing equations, an analytic ground truth (Kepler's third law and "
            "energy conservation), and quantitative predictions a numerical simulation must "
            "reproduce. This validates the panel's pipeline before scaling to harder problems."
        ),
    },
    "string-modes": {
        "slug": "string-modes-torus",
        "text": (
            "Study vibration modes of the closed bosonic string with one spatial dimension "
            "compactified on a circle of radius R (the flat torus — the simplest Calabi-Yau "
            "compactification), in alpha'=1 units. Derive the mass-spectrum formula including "
            "Kaluza-Klein momentum modes n and winding modes w with the level-matching "
            "constraint, state every assumption (bosonic 26D starting point, flat background, "
            "free spectrum, no interactions), and give quantitative predictions a numerical "
            "simulation must reproduce — at minimum: T-duality invariance of the spectrum under "
            "R -> 1/R with n <-> w, the massless sector at generic R, and any spectrum change at "
            "the self-dual radius R=1. The simulation must render higher-dimensional mode "
            "structure as a 3D Matplotlib projection and report which invariants the projection "
            "preserves. Flag anything in the resulting spectrum that looks like a candidate "
            "novel pattern for the Analyst to write up."
        ),
    },
}
