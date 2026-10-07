import json,glob,os
d=os.path.dirname(os.path.abspath(__file__))
S={os.path.basename(f)[:-5]:json.load(open(f)) for f in glob.glob(d+"/*.json")}
ids={n:{r["id"] for r in rows} for n,rows in S.items()}
bad=[]
for n,rows in S.items():
    for r in rows:
        for k,v in r.items():
            if v is None: bad.append(f"UNFILLED  {n}.{r['id']}.{k}")
            if k=="verified_readable" and v is False: bad.append(f"UNVERIFIED {n}.{r['id']}.{k}")
            if k=="audio_ref" and v not in ids["audio"]: bad.append(f"UNRESOLVED {n}.{r['id']}.{k}={v}")
            if k=="role_ref" and v not in ids["roles"]: bad.append(f"UNRESOLVED {n}.{r['id']}.{k}={v}")
            if k=="spawn" and v not in ids["map"]: bad.append(f"UNRESOLVED {n}.{r['id']}.{k}={v}")
print("\n".join(bad)); print(f"\n{len(bad)} findings -> build blocked" if bad else "CLEAN")
