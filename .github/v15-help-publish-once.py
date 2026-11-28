import hashlib,json,os,re,subprocess
from pathlib import Path
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()
old={"boot":"2869705a904eabafb1b9de541d0f265a8db4d6ace0851e0aad661e47b16e6175","tools":"3afcb90370d9aff975be06ff1cdde0ce5aea89e7abb959c7324617cc4f1b196e","bench":"15293d31bcc4a81e16f5298640fbf75c08d1f4c6ab04bf31e4824b57565b581a"}
expected={"boot":"990b08b28987ada7a137ef1df7696a44286de88325f6eb09e56c4285303dc7bf","tools":"4f0c097bb6d8b7119c374495c778ad83db793329119f85885d55c3bfa5d054f5","bench":"212e747ff88e376156f0998715dedc8de5cbcd2d6e71caec7e6ee7b510cee11d"}
gitblobs={"boot":"e180628bd1697082546512af71a79a8e77469e1d","tools":"603680787e89d3f97d8afbd0f85047341003dc1c","bench":"190c7ad3dfa16e14f79fe0bdeb66fc1aed6c968a"}
helpblob="afb82a867e4b36168a9c7b7b82634ae0cb29597f"
root=Path(os.environ["RUNNER_TEMP"])/"edb-help"
root.mkdir(exist_ok=True)
def asset_name(k):return "EDB_v15_512k_"+k.upper()+".dsk"
def repo_name(k):return "EDB_v15_512k_"+k+".dsk"
def release():
 return json.loads(subprocess.check_output(["gh","api","repos/"+os.environ["GITHUB_REPOSITORY"]+"/releases/tags/v15"]))
def check_release(digests):
 r=release()
 a={a["name"]:a for a in r["assets"]}
 for k,h in digests.items():assert a[asset_name(k)]["digest"]=="sha256:"+h and a[asset_name(k)]["size"]==184320
 return a
check_release(old)
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
  last=int.from_bytes(e[14:16],"big");assert 0<=last<=256
  size=(len(chain)-1)*2304+(g-193)*256+last
  b=b"".join(d[loc(g):loc(g)+2304] for g in chain)[:size]
  assert len(b)==size
  files[n]=(b,e[11],e[12],chain)
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
source=Path("extracted/bench/HELP.BAS").read_bytes()
assert blob(source)=="6c390a3cfac4c0935d35e800bb6905413014efd0"
base,prior,tail=basic(source);new=dict(prior)
def topic(start,end,messages):
 for ln in list(new):
  if start<ln<=end:del new[ln]
 for i,s in enumerate(messages,1):
  assert len(s)<=31
  new[start+i]=b'\x87"'+s.encode("ascii")+b'"'
 new[start+len(messages)+1]=b"\x8a"
topic(19000,19005,["EDIT: first line; empty exits.","EDIT n: edit line n.","EDIT file: load, edit first.","SHIFT UP/DOWN: browse lines.","ENTER commits; SAVE to disk.","BREAK cancel not verified."])
topic(12400,12406,["XMM: mouse or keys.","B: RUN BENCHMARK TESTS.","S: SHOW SYSTEM INFO.","Q/exit: return to EDB.","HELP XMM3: viewers."])
topic(12650,12656,["PREV/NEXT or N/P.","Q/exit: main menu.","S: score page or info page 1.","PASS/FAIL/--: status.","Exit restores width/colors."])
topic(12750,12755,["XMM6809/6309 engines.","XMMHW/XMATH: service drivers.","XT*.DRV: diagnostics.","XMM BENCH: service timings."])
topic(13600,13605,["XMMHW: service driver.","Used by XBENCH.","Use XMM or XMM STATUS."])
topic(13700,13705,["XMMTST: status help.","Use XMM for System Info.","Save BASIC before XMM."])
topic(39500,39507,["XMM: 512K menu; B/S/Q.","HW ALLOC ARENA API OBJ GC","MATH MUL SIGNED PAGE","ALL BENCH STATUS CLASSIC","XMM CLASSIC: Sockmaster.","HELP XMM2/XMM3: details."])
topic(39700,39705,["XMM BENCH: service timings.","XMMHW/XMATH: object/math.","XMM menu: full benchmark."])
topic(34000,34005,['FIND ""text"" [filename]',"No file: search Last load.","Searches saved disk files.","Case-insensitive."])
assert {k:v for k,v in new.items() if v.startswith(b"\x82")}=={k:v for k,v in prior.items() if v.startswith(b"\x82")}
compact={};active=False;previous=None
for n in sorted(new):
 b=new[n]
 if b.startswith(b"\x82") and n>=10000:active=True;previous=None
 if n>=10000 and active and b.startswith(b'\x87"') and b.endswith(b'"') and b.count(b'"')==2:
  if previous is not None and len(compact[previous])+1+len(b)<=175:
   compact[previous]+=b":"+b;continue
  previous=n
 else:previous=None
 compact[n]=b
helpdata=rebuild(base,compact,tail)
assert len(helpdata)==10812 and blob(helpdata)==helpblob
assert b"XMEM" not in helpdata.upper()
disks=[]
for k in ("boot","tools","bench"):
 path=Path(repo_name(k));orig=path.read_bytes();assert sha(orig)==old[k]
 files,free=parse(orig)
 assert all((Path("extracted")/k/n).read_bytes()==v[0] for n,v in files.items())
 d=bytearray(orig)
 if k=="boot":
  d[85283:85504]=b"LACK\r\r"+bytes(215)
 else:
  priorhelp,ft,fa,chain=files["HELP.BAS"];assert ft==0 and fa==0
  off=next(o for o in range(DIR,DIR+9*256,32) if d[o:o+11]==b"HELP    BAS")
  oldchain=chain[:];chain=chain[:(len(helpdata)+2303)//2304]
  for g in oldchain[len(chain):]:d[FAT+g]=255
  for i,g in enumerate(chain[:-1]):d[FAT+g]=chain[i+1]
  for i,g in enumerate(chain):
   b=helpdata[i*2304:(i+1)*2304];o=loc(g);d[o:o+len(b)]=b
   if i==len(chain)-1 and len(helpdata)<len(priorhelp):
    end=min(2304,len(priorhelp)-i*2304)
    d[o+len(b):o+end]=bytes(end-len(b))
  last=len(helpdata)-(len(chain)-1)*2304
  d[FAT+chain[-1]]=0xc0+(last+255)//256
  d[off+14:off+16]=((last-1)%256+1).to_bytes(2,"big")
 assert sha(d)==expected[k] and blob(d)==gitblobs[k],(k,sha(d),blob(d))
 newfiles,newfree=parse(d)
 assert files.keys()==newfiles.keys()
 changed=[n for n in files if files[n]!=newfiles[n]]
 assert changed==([] if k=="boot" else ["HELP.BAS"])
 assert len(newfree)=={"boot":6,"tools":46,"bench":6}[k]
 path.write_bytes(d);(root/asset_name(k)).write_bytes(d)
 for n,v in newfiles.items():
  p=Path("extracted")/k/n
  if p.read_bytes()!=v[0]:p.write_bytes(v[0])
 disks.append(dict(filename=repo_name(k),sha256=sha(d),git_blob_sha=blob(d),size_bytes=len(d),active_files=len(newfiles),allocated_granules=78-len(newfree),free_granules=newfree))
 print(k,sha(d),len(newfiles),len(newfree),changed)
# All three local-authorized byte hashes must match before any release mutation.
assert sum(x["active_files"] for x in disks)==116
assert (Path("extracted/tools/HELP.BAS").read_bytes()==Path("extracted/bench/HELP.BAS").read_bytes()==helpdata)
check_release(old)
# Draft the documentation before publication.
helpnote="The owner-approved compact HELP.BAS on TOOLS and BENCH is byte-for-byte identical (10,812 bytes). It corrects EDIT, XMM, XBENCH and FIND wording, removes obsolete XMEM terminology, and recovers one granule per disk. The BOOT dispatcher is distinct. Targeted VCC-EDB tests passed on the 6809 and 6309, including WIDTH 32/40/80 on the 6309; not every HELP topic was exercised."
oldnote="The exact TOOLS and BENCH HELP.BAS payloads differ: TOOLS retains legacy XMEM names; BENCH uses XMM naming. Both omit bare EDIT's first-line behavior and retain older XMM menu wording. See the current manual; on-disk HELP correction is a separate disk revision, not part of the exact extraction."
for p in [Path("README.md"),*Path("docs").glob("*.md")]:
 s=p.read_text()
 for k,h in old.items():s=s.replace(h,expected[k])
 s=s.replace("bb3d55a03ea151b8568fd949bab9fe2deed9a762",gitblobs["bench"]).replace("1496f1e70803cfeb02a5d3e256ccab2a99c733d8",gitblobs["tools"]).replace("179f457154a4956f0dc07abf806b87705aed45c2",gitblobs["boot"])
 s=s.replace(oldnote,helpnote)
 s=s.replace("The owner confirmed testing of that earlier revision; "+helpnote,"The owner confirmed testing of that earlier keyboard revision. "+helpnote)
 s=s.replace("The exact release copy differs from TOOLS (BENCH blob 6c390a3cfac4c0935d35e800bb6905413014efd0).","The full HELP payload is identical on TOOLS and BENCH (Git blob "+helpblob+").")
 s=s.replace("the verified release copies differ.","the verified release copies are identical.")
 s=s.replace("known FIND wording discrepancy, and dispatcher implementation","corrected FIND wording, and dispatcher implementation")
 s=s.replace("The HELP file may describe older XMM menu keys; its keyboard correction is confined to the COLOR handoff.","The compact HELP topics describe the current B/S/Q menu, viewer navigation, inherited display restoration, and XMM service names.")
 s=s.replace("Current EDIT help contract (manual correction; on-disk wording is older)","Current EDIT help contract")
 s=re.sub(r"^\*\*Known discrepancy:\*\* The current HELP description of .*", "**FIND help correction:** FIND without a filename searches the saved Last load file, not the live listing in BASIC RAM. The compact HELP now states this explicitly.",s,flags=re.M)
 s=s.replace("The full 480-line HELP engine","The compact 10,812-byte HELP engine").replace("this 480-line HELP engine","this compact 10,812-byte HELP engine")
 s=s.replace("The manual records code-verified behavior where HELP wording and implementation differ; see FIND in Chapter 5.","The compact HELP now documents bare EDIT, filename loading, XMM and FIND consistently with the manual; see Chapter 5.")
 s=s.replace("This is a key difference from the brief text in the existing \u0060HELP FIND\u0060 screen, which describes the omitted-filename search as a loaded-program search. The underlying \u0060FIND.BAS\u0060 and \u0060TYPE.BAS\u0060 code is authoritative: the search is file-based.","The corrected \u0060HELP FIND\u0060 screen and underlying \u0060FIND.BAS\u0060 / \u0060TYPE.BAS\u0060 implementation agree: the search is file-based.")
 s=s.replace("the on-disk HELP can retain older XMM menu wording, so use this manual for the current interface.","the compact on-disk HELP describes the current interface.")
 s=s.replace("45 files; 73 allocated and 5 free granules","45 files; 72 allocated and 6 free granules")
 s=s.replace("The source inventory is verified; earlier candidate emulator results are not new tests of these uploaded bytes.","The source inventory is verified; the approved compact HELP passed targeted 6809/6309 VCC tests. Earlier candidate tests are not a full new system regression.")
 if p.name=="RELEASE_SYNC.md":
  s+="\n## Approved compact HELP and final BOOT upload\n\n"+helpnote+"\n\nThe final BOOT upload has 54 active files and 6 free granules, with 114 byte differences outside its active file payloads compared with the prior BOOT. TOOLS has 17 active files and 46 free granules; BENCH has 45 active files and 6 free granules. Only the two full HELP payloads changed; all 114 other extracted payloads are identical. No new executable code was generated during synchronization. The exact approved images are the distribution authority.\n"
 elif p.name=="EDB_AI_PROGRAMMING_PROMPT.md":
  s+="\n**Current HELP template:** Keep the full HELP payload within the tested memory budget (10,812 bytes for this revision). Preserve REM dispatch markers, control-flow targets and unrelated messages; combine adjacent constant PRINT statements where safe. Keep HELP copies on TOOLS and BENCH identical, and verify loading and topic dispatch on both processors.\n"
 elif p.name=="README.md":
  s=s.replace("## Official v15 disk images","## Official v15 disk images\n\n**Approved final disk allocation:** BOOT: 6 free granules; TOOLS: 46; BENCH: 6. The final BOOT upload preserves all 54 active file payloads. The two full HELP copies are the approved compact version.")
 p.write_text(s)
# Verify documents do not refer to prior release SHA-256 values.
for p in [Path("README.md"),*Path("docs").glob("*.md")]:
 assert all(h not in p.read_text() for h in old.values())
# Release replacement is explicitly authorized. Preserve asset names and tag.
subprocess.run(["gh","release","upload","v15",*[str(root/asset_name(k)) for k in ("boot","tools","bench")],"--clobber","--repo",os.environ["GITHUB_REPOSITORY"]],check=True)
assets=check_release(expected)
m_path=Path("extracted/MANIFEST.json")
m=json.loads(m_path.read_text());m["disks"]=disks;m["extracted_files"]=116
m["verification"]=[
 "Owner explicitly promoted the compact HELP TOOLS and BENCH candidates and the final BOOT upload as official baselines.",
 "All three images reproduced exactly against independently computed SHA-256 and Git blob hashes of the approved local images. All FAT chains and directory entries validated.",
 "116 extracted payloads, 54 BOOT, 17 TOOLS, 45 BENCH; free granules 6, 46, 6 respectively.",
 "BOOT active file payloads unchanged; 114 disk bytes outside active payloads differ from its predecessor. TOOLS and BENCH changed only HELP.BAS. All 114 other file payloads unchanged.",
 "Both full HELP copies identical, 10812 bytes, Git blob "+helpblob+".",
 "Targeted prior 6809/6309 HELP tests passed; not every topic exercised. No new runtime tests performed by synchronization."
]
m["release_sync"]={"status":"verified_exact_binary_extraction","authority":"Owner-approved final BOOT upload and compact HELP TOOLS/BENCH images; exact release assets, root images and extracted payloads verified.","tag":"v15","assets":[{"name":asset_name(k),"id":assets[asset_name(k)]["id"],"sha256":expected[k],"size_bytes":184320,"download_url":assets[asset_name(k)]["browser_download_url"]} for k in ("boot","tools","bench")],"verification":"Approved image byte hashes verified before replacement and GitHub release asset digests verified after upload. No unapproved disk changes."}
m_path.write_text(json.dumps(m,indent=2)+"\n")
print("All approved release assets and documentation verified.")
