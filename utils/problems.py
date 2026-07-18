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
    "string-viz": {
        "slug": "string-viz-s1",
        "text": (
            "Project the already-computed closed-string vibration results (closed bosonic "
            "string on S^1, alpha'=1) into 3D space so a human can see them, and debate what "
            "the projection reveals. Physicist: define the projection mathematics explicitly — "
            "which worldsheet/embedding coordinates map to the 3 visible axes, which coordinate "
            "is compressed and encoded as colour, and which invariants (mode energy, closure/"
            "periodicity of the string, node count, symmetry) MUST be preserved for the picture "
            "to be faithful. Engineer: render (a) static Matplotlib 3D PNGs of the vibrating "
            "string's mode shape from several camera angles plus the mode-lattice at the "
            "self-dual radius R=1, and (b) an animation of the string oscillating over time "
            "with the camera rotating (matplotlib.animation; MP4 via ffmpeg, GIF via pillow as "
            "fallback), all saved to outputs/ with labelled axes and a colourbar for the "
            "compressed dimension. Emit quantitative invariant metrics (energy drift across "
            "frames, closure error, node count) in RESULT_JSON. Validator: verify the claimed "
            "invariants hold in the rendered data and that the animation is physically "
            "consistent frame to frame. Analyst: describe the visible patterns — nodes, "
            "symmetries, radius dependence — and flag anything worth a Phase-2 novelty check. "
            "The memo must state clearly that a 3D projection is a compression of the "
            "mathematics, not the full higher-dimensional object and not evidence that extra "
            "dimensions physically exist."
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
