from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vireo_sla_report import run
def test_invariants():
    b=Path(__file__).resolve().parents[1]
    t=run(b/'data',b/'test_outputs')
    assert len(t)==11200
    assert t.ticket_id.is_unique
    assert (t.response_minutes>=0).all()
    assert t.target_minutes.notna().all()
    assert t['shift_name'].notna().all()
    assert abs(t.breach.mean()-0.21785714285714286)<1e-12
    assert int(t.breach.sum())==2440
