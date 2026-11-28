import hashlib,json,os,re,subprocess,zlib,base64
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
old="212e747ff88e376156f0998715dedc8de5cbcd2d6e71caec7e6ee7b510cee11d"
new="0cf48fc3ce74c4d96bd13730eb57a126240ab34b6c1297c49f856918caeaaa5d"
oldblob="190c7ad3dfa16e14f79fe0bdeb66fc1aed6c968a"
newblob="9d25179e5b0ac7a5564c1725ea461f8fb013040c"
repo=os.environ["GITHUB_REPOSITORY"]
other={"EDB_v15_512k_BOOT.dsk":"990b08b28987ada7a137ef1df7696a44286de88325f6eb09e56c4285303dc7bf","EDB_v15_512k_TOOLS.dsk":"4f0c097bb6d8b7119c374495c778ad83db793329119f85885d55c3bfa5d054f5"}
asset="EDB_v15_512k_BENCH.dsk"
def release():
 return {a["name"]:a for a in json.loads(subprocess.check_output(["gh","api","repos/"+repo+"/releases/tags/v15"]))["assets"]}
def check_release(h):
 a=release()
 for k,v in {**other,asset:h}.items():assert a[k]["digest"]=="sha256:"+v and a[k]["size"]==184320
 return a
a0=check_release(old)
FAT=17*4608+256;DIR=FAT+256
def loc(g):return (g//2+int(g//2>=17))*4608+g%2*2304
def parse(d):
 assert len(d)==184320
 fat=d[FAT:FAT+78];files={};used=set()
 for off in range(DIR,DIR+9*256,32):
  e=d[off:off+32]
  if e[0] in (0,255):continue
  n=e[:8].decode("ascii").rstrip()+"."+e[8:11].decode("ascii").rstrip()
  assert n not in files and "/" not in n and "\\" not in n and n not in (".","..")
  g=e[13];chain=[]
  while g<78:
   assert g not in used
   used.add(g);chain.append(g);g=fat[g]
  assert 193<=g<=201 and chain
  last=int.from_bytes(e[14:16],"big");assert 0<last<=256
  size=(len(chain)-1)*2304+(g-193)*256+last
  b=b"".join(d[loc(g):loc(g)+2304] for g in chain)[:size]
  assert len(b)==size
  files[n]=(off,chain,b,e[11],e[12])
 assert used=={i for i,v in enumerate(fat) if v!=255}
 return files,[i for i,v in enumerate(fat) if v==255]
def basic(b):
 assert b[0]==255 and int.from_bytes(b[1:3],"big")==len(b)-3
 i=3;base=None;items={}
 while b[i:i+2]!=b"\0\0":
  ptr=int.from_bytes(b[i:i+2],"big");ln=int.from_bytes(b[i+2:i+4],"big");j=b.index(0,i+4)
  if base is None:base=ptr-(j+1-3)
  assert ptr==base+(j+1-3) and (not items or ln>max(items))
  items[ln]=b[i+4:j];i=j+1
 return base,items,b[i:]
def rebuild(base,items,tail):
 result=bytearray()
 for ln,b in sorted(items.items()):
  result+=(base+len(result)+5+len(b)).to_bytes(2,"big")+ln.to_bytes(2,"big")+b+b"\0"
 result+=tail
 return b"\xff"+len(result).to_bytes(2,"big")+result
patches={
"SMBENCH.BAS":("1427a9fe59c91b75b2f940cc5e32ab5448fad756","eNp9VNGSmjAU/Rde2xnDrqLuTB8gxDZAYDFBx+30wW13MIZWFFvATv+9NwGtWzt9ciTnnpx7zr35aX15KayHj2P06a1VvRyth5/WEFkP1hZ766zNm5A3a8HhV+y9UroN89062WV5amPEMG4osekxYjUNP+eJr2rrrTW0oT5fr3ImSM38/YySaVSd3Lxs3RHUv9OYO8AsC7ZLbbes7NhPijIOSZyGz3HM3XcaM9I6JPZ/UPq+oMANXE9UTWSEWRPhQIgsECma8jkfkXSRymT3ect4LTNk4wzFj5nKWrrdf6AnUsE9htNow15o9HC36Woa6HUTQo8Gu1Rox6VyZOuFSbnbstTocbSerzwIqKz/vuf7nMwyuCvQ9QuZOpKDxtnK2XBvGUS8pUUcp0XsCzuYMUnzCr4fo8DPMP5meut6dm71Ka1vqT1fHHirPQNt11462svr+4AXMoN++Gvue4079yT2lCaTPF9n+mwy1c1t2kAsF3Eg1NMjhTAWfOoLMvV56wWiePIEKQg06YGw8+U2QroSxuF08IkjMnlifinEmMGY5Pm4xRoNY2NGA9C6wVTx02C42gUqv0/I6g6MhyEJSLVl0JiH5zBQHfrub8vtQvBs9F60I1C5cuj+x0C2OUrCI55j5WTozQlaMzFkSKmu1U5Px6hN2HB/8E1uBOdpRberIaiT4TM1Q6w76Q0D9PAWfbpBp2f0CNBZ9PgHrWz6Immpw8v6JWECvLvwO1DBD3EK3vVfxuZGLzz6RId85dyk16Jwx85l3YTPMFrSlZoZeEKdAUSqb6nj+nzLFCp1MoOh2g1G7k47E5H9AQYrPZB9xbgqDXJ6vXJGtfZTj1FwWQNA6QxV34Nt8hfo+79zF6pOSiU5p5XO5HoNIjX3Fpi+ygxWp2O1UecDLA+7XrQm5hR8wR16C3MzW7fMLBFpkn4m7bs/1berZ1wVnav2PbpZHkg2cs2ymc41r+h5zdP4j/U8Px/B1fPRVYx6JR3iOQVukneIr+ii+8zvvEYzo+SMrraufjb6M3p9drphGqN+2c2/iXm6JGuSIn4E7c4lY6WfZuJc0vz/BIh92qHsc+b6y69fvwF9J+ne"),
"XMSHOW.BAS":("441a50283ac567cad4079f3f446fe4330d5e3139","eNplU8ty2jAU/RdvYSYyiU2SmSyMJTKyLQlHUintdEGTjLFliqlp/cjk3yvJhEK7QVj33Mc55+rNeXktnfuvnncDxvrHHbu+d+t9Gzv168G5f3Nc4Nw7JQ9aAoMmCb9gCl8en4qfQvAgX6LDfMk9JMtVznZNJrusTWBaJQioGKIqmdNQnzURz/p/9Gjv0PGcR2exSgx3FTUnU3dJ3Qd+qn71BFYLmZCGqTaJEpLjouLplDTO2PG8azNdFs4ijc4qPSUr4576h4gp1jNYfa77lf8p5D3OwQEX+zk2HZCq6kLju5mMksWVCourPNysBd9EMVc1ydXDUN011derjEHc6Dlg3SOPla89LSppZkk40LxltizJjvNtR8LwB56nqr4apfFihGPDS3eLedPF6cOx6uSi6j7BSPkqsFEtPjCUJLDEhSHKSrowYuQh/I3xY4khmlChmgFu/dnyKMJ5UxDe5BK4oQR0IZX89YTmUuslxJS0bKd0vF1Gp04Tk7rhs6WhcpbWUo61OGGEe1RLQPxsLTMiVi7tg2Pq9d9U3uGS0rSkULjRXPujU4OWFtIjp043Bp5z0iaohUYwgRgwFtThjKRT3hGuhbvg5R2djU/ODvOvZbeJY7G3wy0V2PHBLZPiDkMNkO9pgxOUDZAtsNZcdphcwImGBye4He4Uw+ex/v9SvuXXzWLtFaxdY3oLj4br8PSolrYzbXH8bMVk4kPMW2thri36x2n9rZ8BOluOO9voI6yFlGDUW/GiXUFODe88u0Mju0N82CFoKptFJeHW3K/NYzW0WWkeXVDZuKZIuInvU+f9/Q+ofERD")}
path=Path("EDB_v15_512k_bench.dsk")
orig=path.read_bytes();assert sha(orig)==old and blob(orig)==oldblob
files,free=parse(orig);assert len(files)==45 and len(free)==6
assert all((Path("extracted/bench")/n).read_bytes()==v[2] for n,v in files.items())
d=bytearray(orig)
for n,(expected,packed) in patches.items():
 off,ch,b,ft,fa=files[n]
 base,items,tail=basic(b);patch=json.loads(zlib.decompress(base64.b64decode(packed)))
 before=items.copy()
 for ln in patch["del"]:del items[ln]
 for ln,val in patch["set"].items():items[int(ln)]=base64.b64decode(val)
 if n=="SMBENCH.BAS":assert all(before[i]==items[i] for i in (5,8,10,20,25,30))
 nb=rebuild(base,items,tail);assert blob(nb)==expected
 assert (len(ch)-1)*2304<len(nb)<=len(ch)*2304
 for i,g in enumerate(ch):
  chunk=nb[i*2304:(i+1)*2304];o=loc(g);d[o:o+len(chunk)]=chunk
 last=len(nb)-(len(ch)-1)*2304;d[FAT+ch[-1]]=0xc0+(last+255)//256;d[off+14:off+16]=((last-1)%256+1).to_bytes(2,"big")
 (Path("extracted/bench")/n).write_bytes(nb)
 print(n,len(b),len(nb),blob(nb))
assert sha(d)==new and blob(d)==newblob,(sha(d),blob(d))
nf,nfree=parse(d);assert nf.keys()==files.keys() and nfree==free
assert set(n for n in files if files[n]!=nf[n])==set(patches)
assert all((Path("extracted/bench")/n).read_bytes()==v[2] for n,v in nf.items())
path.write_bytes(d)
for k,v in other.items():
 assert sha(Path(k.lower()).read_bytes())==v
assert Path("extracted/bench/HELP.BAS").read_bytes()==Path("extracted/tools/HELP.BAS").read_bytes()
# Verify the unchanged compact HELP and the old untagged score payload as distributed.
assert nf["SMBSCORE.DAT"]==files["SMBSCORE.DAT"]
behavior="Page 5 displays independent measured 6809 and 6309 scores and their cached clock speeds, with no fixed-clock gate. SMBENCH reads the CPU name and MHz from the BOOT disk's cached SYSINFO.INF (not live CPU detection); after changing processor or clock, refresh the cache through the normal EDB startup path before benchmarking. The latest run updates only that CPU's pair; the other pair survives. Unmeasured CPU rows show --. The multiplier columns compare the most recently measured score to the historical 6809 bases 100 and 200. The historical 13,544-point result remains a documentation reference, not a substitute for a measured row."
record="SMBSCORE.DAT uses the SMBSCORE2 marker after the first successful new save, followed by last CPU index (0=6809, 1=6309), 6809 score, 6809 MHz, 6309 score, 6309 MHz, each on its own BASIC sequential-file record. A zero score/clock pair indicates unmeasured. The distributed legacy SMBSCORE15 record is preserved byte-for-byte; it has no CPU tag and must not be assigned to either CPU row. The viewer can still use its untagged score for the multiplier columns. The first successful benchmark migrates it without assigning its old value to a processor. SMBENCH reopens the new record and checks the CPU index and both score/clock pairs before continuing. A valid cache and a writable BENCH working disk are required. Back up score records; the overwrite is not transactional."
tests="Approved dual-CPU candidate tests: direct 6809 at cached 125.28 MHz (13,194 points), then 6309 at 125.28 MHz (13,237), preserving the 6809 row, and 6309 at 101.12 MHz (10,596), preserving the earlier 6809 result. Full 6309 XMM suite and WIDTH 80 cyan-on-red restoration passed. Full 6809 suite regression and disk-error recovery remain untested. These are candidate test results, not scores seeded in the distributed image."
for p in [Path("README.md"),*Path("docs").glob("*.md")]:
 s=p.read_text();origtext=s
 s=s.replace(old,new).replace(oldblob,newblob)
 s=s.replace("and preserves the "+chr(96)+"SMBSCORE.DAT"+chr(96)+" record format ("+chr(96)+"SMBSCORE15"+chr(96)+" is a compatibility marker, not the current number of trials).","and saves independent CPU score/clock pairs in "+chr(96)+"SMBSCORE.DAT"+chr(96)+" using the "+chr(96)+"SMBSCORE2"+chr(96)+" format after a successful run.")
 s=re.sub(r"^The current page 5 layout compares the saved score to the historical 6809 bases[^\n]*",behavior+"\n\n"+record,s,flags=re.M)
 s=s.replace("A new run replaces the single Sockmaster score record; retain copies for comparisons.","A new run replaces only the measured CPU's score/clock pair, retaining the other pair; retain copies for comparisons.")
 s=s.replace("Page 5 retains the reference in the 6309 field when no applicable fresh measurement is available.","This is a historical reference only; page 5 displays independently measured scores or --.")
 if p.name=="SOCKMASTER_BENCH.md":
  s=s.replace("The latest approved behavior uses four trials, a simplified score display, clean transitions and inherited display restoration.","The latest approved behavior uses four trials, independently persisted CPU-tagged scores with dynamic cached clocks, clean transitions and inherited display restoration.")
  s+="\n**Dual-CPU verification:** "+tests+"\n"
 if p.name=="BASIC_PROGRAMS_BENCH.md":
  s=s.replace("| 40–70 | Save and read back score record |","| 40–63 | Read cached identity and existing record; update one CPU pair, save and read back both pairs |")
  s=s.replace("| 900–901 | Save/verification error and cleanup |","| 890, 900–901 | Invalid-cache or save/verification error and cleanup |\n| 1000–1091 | Read cached CPU/MHz from BOOT SYSINFO.INF |\n| 1100–1191 | Load and validate old/new score record; legacy migration |")
  s=s.replace("16500–16595 read the Sockmaster score.","16500–16595 read and validate legacy or CPU-tagged Sockmaster scores; 5530–5532 draw the per-CPU clock/score fields.")
 if p.name in ("README.md","USER_MANUAL.md","BASIC_PROGRAMS_BENCH.md"):s+="\n**Sockmaster dual-CPU verification:** "+tests+"\n"
 if p.name=="BASIC_PROGRAM_REFERENCE.md":
  s=s.replace("Sockmaster Classic BASIC loop","Sockmaster Classic BASIC loop and CPU-tagged score persistence")
 if p.name=="EDB_AI_PROGRAMMING_PROMPT.md":
  s+="\n**Benchmark score provenance rule:** For Sockmaster, continue to use cached BOOT SYSINFO.INF as the CPU and clock authority. Do not replace it with live CPU detection. Preserve independent CPU score/clock pairs, do not require a fixed MHz value, and do not assign an untagged historical score to a processor. Keep the four original timed samples separate from disk I/O and display code; preserve inherited video settings and all unrelated behavior. See the current Sockmaster notes for the exact record format.\n"
 if p.name=="RELEASE_SYNC.md":
  s=s.replace("Only the two full HELP payloads changed; all 114 other extracted payloads are identical.","At that earlier HELP synchronization, only the two full HELP payloads changed; all 114 other extracted payloads were identical.")
  s+="\n## Approved Sockmaster dual-CPU score baseline\n\n"+behavior+"\n\n"+record+"\n\n"+tests+"\n\nOnly SMBENCH.BAS and XMSHOW.BAS changed relative to the immediately preceding BENCH baseline. Six free granules, original timing loop, the legacy distributed score file, all 43 other BENCH payloads, BOOT and TOOLS remain unchanged. No new runtime tests were performed by publication.\n"
 if s!=origtext:p.write_text(s)
# Require exact approved image hash before publishing; only BENCH release attachment is replaced.
a1=check_release(old)
out=Path(os.environ["RUNNER_TEMP"])/asset;out.write_bytes(d)
subprocess.run(["gh","release","upload","v15",str(out),"--clobber","--repo",repo],check=True)
assets=check_release(new)
for k in other:assert assets[k]["id"]==a0[k]["id"]
mp=Path("extracted/MANIFEST.json");m=json.loads(mp.read_text())
entry=next(x for x in m["disks"] if x["filename"]==path.name)
assert entry["sha256"]==old
entry.update(sha256=new,git_blob_sha=newblob,active_files=len(nf),allocated_granules=78-len(nfree),free_granules=nfree)
m["verification"].append("Owner-approved Sockmaster dual-CPU BENCH baseline. Exact candidate SHA-256 and Git blob verified. Only SMBENCH.BAS and XMSHOW.BAS changed; 43 other BENCH payloads, all BOOT and TOOLS bytes and distributed legacy score record preserved. "+tests)
m["release_sync"]["authority"]="Owner-approved final BOOT, compact HELP TOOLS, and Sockmaster dual-CPU BENCH; exact release assets, root images and extracted payloads verified."
for a in m["release_sync"]["assets"]:
 if a["name"]==asset:a.update(id=assets[asset]["id"],sha256=new,download_url=assets[asset]["browser_download_url"])
m["release_sync"]["verification"]="Exact approved image SHA-256 verified before publication; GitHub release asset digests verified after upload. BOOT and TOOLS attachments preserved. All 116 extracted payloads synchronized."
mp.write_text(json.dumps(m,indent=2)+"\n")
print("Verified exact approved BENCH, 43 unchanged BENCH payloads, and unchanged BOOT/TOOLS release assets.")
