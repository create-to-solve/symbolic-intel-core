# Symbolic drift scoring utilities

import re

#: Baseline narrative archetype expressed symbolically.  The phrases chosen
#: capture the expected themes within a typical climate project description.
BASELINE_ARCHETYPE = (
    "The project emphasises sustainability, renewable energy, carbon reduction, "
    "community engagement and measurable impact."
)


def _tokenize(text):
    """Return a set of lowercase word tokens extracted from ``text``."""

    return set(re.findall(r"[A-Za-z0-9']+", text.lower()))


def _symbolic_similarity(a, b):
    """Return Jaccard similarity between the token sets of ``a`` and ``b``."""

    tokens_a = _tokenize(a)
    tokens_b = _tokenize(b)
    if not tokens_a and not tokens_b:
        return 1.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def score_drift(document):
    """Compare ``document`` against a baseline narrative archetype.

    Parameters
    ----------
    document : str
        The project narrative to evaluate.

    Returns
    -------
    tuple[float, list[str]]
        ``(drift_score, reasons)`` where ``drift_score`` is ``1 - similarity``
        with the baseline archetype and ``reasons`` lists symbolic terms missing
        from the document.
    """

    similarity = _symbolic_similarity(document, BASELINE_ARCHETYPE)
    drift_score = 1.0 - similarity

    baseline_tokens = _tokenize(BASELINE_ARCHETYPE)
    doc_tokens = _tokenize(document)
    missing = sorted(baseline_tokens - doc_tokens)

    reasons = []
    if missing:
        reasons.append("missing: " + ", ".join(missing))

    return drift_score, reasons

