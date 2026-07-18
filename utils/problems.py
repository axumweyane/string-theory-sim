"""Named problem presets for the debate panel."""

# Deep open-ended mode: the target space of variations beyond textbook cases,
# explored in order until a novel candidate survives or the list is exhausted.
DEEP_VARIATIONS = [
    {
        "name": "T^2 with complex/Kahler moduli",
        "slug": "deep-t2-moduli",
        "text": (
            "Open-ended string research, variation 1: closed bosonic string compactified on T^2 "
            "with non-trivial complex-structure modulus tau and Kahler modulus rho (alpha'=1). "
            "Derive the momentum/winding spectrum M^2(n1,n2,w1,w2; tau,rho) with level matching, "
            "verify the expected T-duality group action (SL(2,Z)_tau x SL(2,Z)_rho and "
            "tau <-> rho exchange) numerically, and scan moduli space for degeneracy patterns, "
            "enhanced-symmetry loci, or spectral crossings that standard treatments do not "
            "emphasize. Every claim needs a derivation or a computed number. Flag anything that "
            "looks genuinely novel as a candidate hypothesis with the argument for why."
        ),
    },
    {
        "name": "Wilson-line deformation",
        "slug": "deep-wilson-line",
        "text": (
            "Open-ended string research, variation 2: S^1 compactification deformed by a "
            "constant Wilson line coupling to a U(1) charge q — the momentum lattice shifts "
            "n -> n + a q. Compute the deformed spectrum across the Wilson-line parameter a, "
            "track how the self-dual enhanced symmetry breaks and where (if anywhere) it is "
            "restored, and look for degeneracy or monodromy patterns in the (R, a) plane that "
            "the standard treatments miss. Quantitative predictions with tolerances; flag "
            "candidate-novel patterns for the Analyst."
        ),
    },
    {
        "name": "Asymmetric shift orbifold of S^1",
        "slug": "deep-asym-orbifold",
        "text": (
            "Open-ended string research, variation 3: an asymmetric shift orbifold of the S^1 "
            "compactification — act with a half-shift on left-movers only (X_L -> X_L + pi R). "
            "Construct the untwisted and twisted sectors, impose level matching and the modular-"
            "consistency (spin-structure) constraints numerically, compute the resulting mode "
            "spectrum, and compare against the symmetric orbifold and the unorbifolded theory. "
            "Hunt for spectra, degeneracies, or duality relations in the asymmetric case that "
            "standard references do not catalogue. Every claim needs a derivation or number; "
            "flag candidate-novel results."
        ),
    },
]

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
