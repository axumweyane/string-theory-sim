import json

from utils.transcript import Transcript


def test_transcript_persists_each_event():
    t = Transcript("pytest-scratch")
    t.log("physicist", "propose", {"model_name": "m"})
    t.log("engineer", "build", {"code": "pass"})
    on_disk = json.loads(t.path.read_text())
    assert len(on_disk) == 2
    assert on_disk[0]["role"] == "physicist"
    assert t.tail(1)[0]["phase"] == "build"
    t.path.unlink()
