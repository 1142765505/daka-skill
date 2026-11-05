"""Prepare numbered identity boards for the current requested set only."""
import argparse
import json
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from plan import ROOT,ids


def prepare(room, selected, out):
    selected=ids(selected,room)
    if not selected:raise ValueError("至少选择一个编号")
    for ident in selected:
        if not (ROOT/"references/private/identities"/room/(str(ident)+".png")).is_file():
            raise FileNotFoundError("缺少本地裁图，请先运行 scripts/build_library.py")
    out=Path(out);out.mkdir(parents=True,exist_ok=True);result=[]
    # Five identities per board permits ten people in two image slots.
    for start in range(0,len(selected),5):
        group=selected[start:start+5];board=Image.new("RGB",(320*len(group),400),"white");draw=ImageDraw.Draw(board)
        for i,ident in enumerate(group):
            with Image.open(ROOT/"references/private/identities"/room/(str(ident)+".png")) as im:thumb=ImageOps.contain(im.convert("RGB"),(300,350))
            board.paste(thumb,(i*320+(320-thumb.width)//2,42));draw.text((i*320+12,12),f"ROOM {room} / PERSON {ident}",fill="black")
        dest=out/(room+"-identity-board-"+str(start//5+1)+".png");board.save(dest);result.append(str(dest.resolve()))
    roster=json.loads((ROOT/"references/private/roster.json").read_text(encoding="utf-8"))
    extra=[]
    for person in roster[room]["people"]:
        if person["id"] in selected:
            for index,ref in enumerate(person.get("identity_references",[]),1):
                path=ROOT/"references/private/identities"/room/(str(person["id"])+"-ref-"+str(index)+".png")
                if not path.is_file(): raise FileNotFoundError("缺少补充裁图，请重建参考库")
                extra.append((person["id"],index,path))
    for start in range(0,len(extra),5):
        group=extra[start:start+5]
        board=Image.new("RGB",(320*len(group),400),"white");draw=ImageDraw.Draw(board)
        for i,(ident,index,path) in enumerate(group):
            with Image.open(path) as im:thumb=ImageOps.contain(im.convert("RGB"),(300,350))
            board.paste(thumb,(i*320+(320-thumb.width)//2,42))
            draw.text((i*320+12,12),f"ROOM {room} / PERSON {ident} / VIEW {index+1}",fill="black")
        dest=out/(room+"-identity-details-"+str(start//5+1)+".png")
        board.save(dest);result.append(str(dest.resolve()))
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--room",choices=["401","403"],required=True);p.add_argument("--ids",required=True);p.add_argument("--out",required=True);a=p.parse_args()
    print(json.dumps(prepare(a.room,a.ids,a.out),ensure_ascii=False,indent=2))
