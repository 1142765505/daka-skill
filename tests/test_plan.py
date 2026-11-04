import importlib.util
from pathlib import Path
import tempfile
import unittest
import json
spec=importlib.util.spec_from_file_location("plan",Path(__file__).resolve().parents[1]/"scripts/plan.py");m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class PlanTests(unittest.TestCase):
    def test_add_one(self):
        p=m.plan("使用打卡skill，401增加3",True,[]);self.assertEqual(p["to_add"],[3]);self.assertEqual(p["candidate_count"],3)
    def test_present_is_noop(self):
        p=m.plan("401增加3",True,[3]);self.assertEqual(p["state"],"noop");self.assertEqual(p["candidate_count"],0);self.assertEqual(p["skipped"],[3])
    def test_mixed_existing_preserved(self):
        p=m.plan("401增加3、4、5",True,[1,3,9]);self.assertEqual(p["to_add"],[4,5]);self.assertEqual(p["skipped"],[3]);self.assertEqual(p["final_numbered_people"],[1,3,4,5,9]);self.assertTrue(p["preserve_unrequested_existing_people"])
    def test_without_input(self):
        p=m.plan("使用打卡skill，401增加3、4、5");self.assertEqual(p["final_numbered_people"],[3,4,5]);self.assertTrue(p["forbid_other_people"])
    def test_all_default(self):
        self.assertEqual(m.plan("使用打卡skill，增加全部")["requested"],list(range(1,11)))
    def test_403(self):
        self.assertEqual(m.plan("403增加全部")["requested"],[1,2,3,4]);self.assertEqual(m.plan("403增加1、3",True,[1])["to_add"],[3])
    def test_403_four_missing(self):
        p=m.plan("使用打卡skill，403增加4",True,[1]);self.assertEqual(p["to_add"],[4]);self.assertEqual(p["final_numbered_people"],[1,4]);self.assertEqual(p["candidate_count"],3)
    def test_403_four_present(self):
        p=m.plan("403增加4",True,[4]);self.assertEqual(p["state"],"noop");self.assertEqual(p["skipped"],[4]);self.assertEqual(p["candidate_count"],0)
    def test_403_four_subset_without_input(self):
        p=m.plan("403增加3、4");self.assertEqual(p["final_numbered_people"],[3,4]);self.assertTrue(p["forbid_other_people"])
    def test_403_all_present(self):
        p=m.plan("403增加全部",True,[1,2,3,4]);self.assertEqual(p["state"],"noop");self.assertEqual(p["skipped"],[1,2,3,4])
    def test_403_four_uncertain(self):
        p=m.plan("403增加4",True,[],[4]);self.assertEqual(p["state"],"needs_clarification");self.assertEqual(p["candidate_count"],0)
    def test_duplicates_and_fullwidth(self):
        self.assertEqual(m.plan("使用打卡skill，４０１增加３、３、４")["requested"],[3,4])
    def test_invalid(self):
        for text in ["401增加0","401增加11","403增加5","402增加1","401增加-1","401增加3.5","401增加3，403增加1","401增加全部3"]:
            with self.subTest(text=text),self.assertRaises(ValueError):m.plan(text)
    def test_unverified_presence(self):
        p=m.plan("401增加3",True);self.assertEqual(p["state"],"requires_visual_check");self.assertEqual(p["candidate_count"],0)
    def test_uncertain_requested_blocks(self):
        p=m.plan("401增加3、4",True,[],[3]);self.assertEqual(p["state"],"needs_clarification");self.assertEqual(p["candidate_count"],0)
    def test_extra_uncertain_does_not_block(self):
        self.assertEqual(m.plan("401增加3",True,[],[8])["to_add"],[3])
    def test_presence_conflict(self):
        with self.assertRaises(ValueError):m.plan("401增加3",True,[3],[3])
    def test_roster_integrity(self):
        root=Path(__file__).resolve().parents[1]
        if not (root/"references/private/roster.json").is_file():self.skipTest("个人编号参考库未随开源代码发布")
        r=json.loads((root/"references/private/roster.json").read_text(encoding="utf-8"))
        for room,count in [("401",10),("403",4)]:
            self.assertEqual([p["id"] for p in r[room]["people"]],list(range(1,count+1)))
            for p in r[room]["people"]:self.assertTrue(p["identity_source"].startswith(room+"照片/"))

if __name__=="__main__":unittest.main()
