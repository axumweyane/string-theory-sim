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

# Frontier mode: seed collisions between fields that rarely talk. The
# Orchestrator starts here and then invents its own, steering by the death log.
SEED_COLLISIONS = [
    {
        "field_a": "holographic entanglement geometry (Ryu-Takayanagi)",
        "field_b": "optimization-landscape geometry of over-parameterized networks",
        "bridge_question": "Is the RT minimal surface the same variational object as the "
        "loss-landscape geodesic, and does either side predict a scaling law the other has not reported?",
    },
    {
        "field_a": "Narain lattices / string spectra",
        "field_b": "error-correcting codes beyond known lattice constructions",
        "bridge_question": "What 'spacetime' do codes that do NOT come from known lattices imply?",
    },
    {
        "field_a": "spectral dimension flow (quantum-gravity diffusion)",
        "field_b": "non-equilibrium thermodynamics / complete monotonicity",
        "bridge_question": "Does positivity of the spectral measure impose a fluctuation-theorem-like "
        "constraint on how fast dimension can RUN that the dimension-flow literature has not stated?",
    },
    {
        "field_a": "renormalization group flows",
        "field_b": "biological self-organization / morphogenesis",
        "bridge_question": "Is there a shared fixed-point structure under coarse-graining that predicts "
        "something in one field from the other?",
    },
    {
        "field_a": "amplituhedron / positive-Grassmannian combinatorics",
        "field_b": "integer sequences and their generating functions",
        "bridge_question": "Do positroid cell counts match an integer sequence whose generating "
        "function implies an unnoticed recursion?",
    },
]

# Deep-innovation mode: attack the foundational assumptions themselves.
# Each entry names the orthodox assumption, the heresy, and a computation that
# can genuinely falsify one side. Memos must state why the alternative fails
# or survives, which assumption rescues the orthodoxy, and where the frontier is.
INNOVATION_CHALLENGES = [
    {
        "name": "Is D=26 actually forced?",
        "slug": "innov-critical-dimension",
        "text": (
            "Heresy 1: maybe the critical dimension of the bosonic string is a convention, "
            "not a necessity. Interrogate it computationally, not by citation. In light-cone "
            "quantization the level-1 state has D-2 polarizations and M^2 = (4/alpha')(1 - a) "
            "with normal-ordering constant a = (D-2)/24 (zeta-regularized sum of half-integer "
            "mode zero-point energies — derive it with SymPy, both via zeta(-1) and via a "
            "cutoff-regularized partial sum extrapolation, and show they agree). A massive "
            "vector needs D-1 states, so Lorentz invariance forces M^2=0 at level 1, i.e. "
            "a=1, i.e. D=26. Compute the Lorentz-anomaly obstruction ((26-D)/12) m^3-type "
            "coefficient numerically for D in {4, 10, 26} and show exactly where the theory "
            "breaks and by how much. THEN steelman the heresy: what modification rescues "
            "D != 26 (linear-dilaton / Liouville sector shifting the central charge)? State "
            "precisely which assumption (flat background, no dilaton gradient) the textbook "
            "conclusion depends on. If your computation contradicts a textbook claim, re-derive "
            "the textbook claim independently before deciding which is wrong."
        ),
    },
    {
        "name": "Is dimension emergent?",
        "slug": "innov-emergent-dimension",
        "text": (
            "Heresy 2: maybe spacetime dimension is not fundamental input (as in string "
            "theory's D=26/10) but an emergent, scale-dependent observable. Build a concrete "
            "toy: define spectral dimension d_s(sigma) = -2 dlog P(sigma)/dlog sigma from the "
            "return probability P(sigma) of random walks on (a) a regular 4D lattice (control: "
            "d_s = 4 at all scales) and (b) a hierarchical/graph geometry engineered so d_s "
            "runs with scale (e.g. ~2 in the UV flowing toward ~4 in the IR). Run the actual "
            "random-walk ensembles, plot d_s(sigma) for both, and quantify the running. Debate: "
            "does a running d_s genuinely dissolve the 'how many dimensions' question that "
            "string theory answers by fiat, or does the graph model smuggle the answer in "
            "through its construction? Identify what experiment or computation could "
            "distinguish emergent from fundamental dimensionality, and check the literature "
            "for whether this running-dimension phenomenon is already charted."
        ),
    },
    {
        "name": "What if an extra dimension is timelike?",
        "slug": "innov-timelike-dimension",
        "text": (
            "Heresy 3: compactification always assumes the extra dimensions are spacelike — "
            "why? Compute what actually goes wrong if one is timelike: Kaluza-Klein reduce a "
            "massless scalar on a timelike circle of radius R so the tower becomes "
            "M^2 = m^2 - (n/R)^2, and compute (a) the number of tachyonic modes below any "
            "cutoff as a function of R (show it diverges as the cutoff is lifted), (b) the "
            "classical instability growth rates, and (c) the norm structure showing which "
            "modes become ghostlike in the reduced theory. Contrast with the spacelike case "
            "computed in earlier debates. Then steelman: are there frameworks that claim to "
            "tame extra times (constrained two-time systems)? State exactly which assumption "
            "(unitarity/boundedness of the Hamiltonian) rules the naive version out, and "
            "whether the panel's computation constitutes proof or only strong evidence."
        ),
    },
    {
        "name": "Do we even need compactification?",
        "slug": "innov-no-compactification",
        "text": (
            "Heresy 4: maybe hiding extra dimensions by curling them up is unnecessary. Test "
            "the alternative: an INFINITE warped extra dimension with gravity localized on a "
            "brane. Numerically solve the graviton-fluctuation Schrodinger problem in the "
            "warped metric (the 'volcano potential' V(z) = 15k^2/(8(k|z|+1)^2) - (3k/2) "
            "delta(z)): show (a) a single normalizable zero mode bound to the brane (the 4D "
            "graviton), (b) a gapless continuum of KK modes, and (c) that the zero mode "
            "dominates the propagator at long distance — i.e. 4D gravity emerges without "
            "compactification. Verify normalizability and the delta-function matching "
            "condition numerically. Debate honestly: does this kill the compactification "
            "assumption, does it merely relocate it, and what does string theory need from "
            "it? Literature-check whether this localization mechanism is already charted."
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
