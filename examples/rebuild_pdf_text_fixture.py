"""Reproduce one reviewed CC BY 4.0 scientific article fixture.

Requires PyMuPDF 1.28.2 and python-bidi 0.6.11. Source/font are explicit local
inputs; this script never downloads or changes the source. See the attribution
and reader-specific limits in evals/PDF-TEXT-FIX.md before reuse.
"""
import argparse,re,json,html,unicodedata,hashlib
from pathlib import Path
import pymupdf as f
from bidi.algorithm import get_display
from bidi.algorithm import get_empty_storage,get_embedding_levels,explicit_embed_and_overrides,resolve_weak_types,resolve_neutral_types,resolve_implicit_levels,reorder_resolved_levels,apply_mirroring
parser=argparse.ArgumentParser(description="Rebuild the specific SysIdentPy partial translation fixture, not a general PDF converter.")
parser.add_argument('--source',type=Path,required=True)
parser.add_argument('--font',type=Path,required=True,help='Vazirmatn-Light.ttf v33.003')
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'evals/performance/pdf-rebuild-data.json').read_text(encoding='utf8'))
if hashlib.sha256(args.source.read_bytes()).hexdigest()!=data['source_sha256']:
 raise ValueError('Source does not match the reviewed article; inspect and map new regions separately.')
d=f.open(args.source);old=f.open(args.source)
pages=data['pages'];tr=data['translations']
tr['1-1']='بستهٔ پایتونی SysIdentPy برای شناسایی سیستم با استفاده از مدل‌های NARMAX'
jobs=[]
for p in pages:
 for v in p['blocks']:
  if v['id'] in tr:jobs.append(dict(id=v['id'],page=p['page']-1,rect=[v['bbox'][0],v['bbox'][1],552.75,v['bbox'][3]],source_rect=v['bbox'],font=v['size']))
for ident,rect in [('table-h1',[270.37,326.24,339,338.2]),('table-h2',[343.30,326.24,395,338.2])]:jobs.append(dict(id=ident,page=3,rect=rect,source_rect=rect,font=9))
fontfile=str(args.font);font=f.Font(fontfile=fontfile)
def clean(s):
 return ''.join(c for c in unicodedata.normalize('NFKC',s) if not c.isspace() and c!='\u200c' and not unicodedata.combining(c))
def visual_indices(s):
 storage=get_empty_storage();storage['base_level']=1;storage['base_dir']='R'
 get_embedding_levels(s,storage)
 for i,c in enumerate(storage['chars']):c['index']=i
 explicit_embed_and_overrides(storage);resolve_weak_types(storage);resolve_neutral_types(storage,False);resolve_implicit_levels(storage,False);reorder_resolved_levels(storage,False);apply_mirroring(storage,False)
 return storage['chars']
layers=[]
for pi in sorted({j['page'] for j in jobs}):
 p=d[pi];links=p.get_links()
 for j in jobs:
  if j['page']==pi:p.add_redact_annot(f.Rect(j['source_rect']),fill=False,cross_out=False)
 p.apply_redactions(images=0,graphics=0,text=0)
 present={(l['kind'],tuple(l['from']),l.get('uri'),l.get('page')) for l in p.get_links()}
 for l in links:
  if (l['kind'],tuple(l['from']),l.get('uri'),l.get('page')) not in present:l.pop('xref',None);l.pop('id',None);p.insert_link(l)
 for j in [x for x in jobs if x['page']==pi]:
  rect=f.Rect(j['rect']);tmp=f.open();tp=tmp.new_page(width=rect.width,height=rect.height)
  text=re.sub(r'(SysIdentPy|NARMAX|model\.results|model\.residuals|fit|ERR|SI)',r'<span dir="ltr">\1</span>',html.escape(tr[j['id']]))
  css='@font-face{font-family:fa;src:url('+args.font.name+')} body{font-family:fa;font-size:'+str(j['font'])+'pt;margin:0;line-height:1.05;direction:rtl;text-align:left}'
  spare,scale=tp.insert_htmlbox(tp.rect,'<div dir="rtl" style="text-align:left">'+text+'</div>',css=css,archive=f.Archive(str(args.font.parent)),scale_low=.85)
  assert spare>=0,j['id']
  # Preserve shaped appearance as vector outlines; only the replacement regions.
  svg=tp.get_svg_image(text_as_path=True);vector=f.open(stream=svg.encode(),filetype='svg');vpdf=f.open(stream=vector.convert_to_pdf(),filetype='pdf');p.show_pdf_page(rect,vpdf,0)
  grouped={}
  for block in tp.get_text('dict')['blocks']:
   if block['type']!=0:continue
   for line in block['lines']:
    for span in line['spans']:
     y=round(span['origin'][1],2);grouped.setdefault(y,[]).append(span)
  source=tr[j['id']];offset=0;logical_lines=[]
  for y,spans in sorted(grouped.items()):
   count=sum(len(clean(s['text'])) for s in spans)
   start=offset;n=0
   while offset<len(source) and n<count:
    n+=len(clean(source[offset]));offset+=1
   # Include trailing combining marks/joiners, but leave inter-line spaces out.
   while offset<len(source) and (unicodedata.combining(source[offset]) or source[offset]=='\u200c'):offset+=1
   line=source[start:offset].strip()
   while offset<len(source) and source[offset].isspace():offset+=1
   assert n==count,(j['id'],n,count)
   bbox=f.Rect(min(s['bbox'][0] for s in spans),min(s['bbox'][1] for s in spans),max(s['bbox'][2] for s in spans),max(s['bbox'][3] for s in spans))
   display_source=line.replace('\u200c','|').replace('\u0654','^')
   chars=visual_indices(display_source)
   widths=[font.text_length(c['ch'],fontsize=j['font']*scale) for c in chars]
   ratio=bbox.width/sum(widths);px=rect.x0+bbox.x0;positions={}
   for c,width in zip(chars,widths):positions[c['index']]=px;px+=width*ratio
   p.insert_font(fontname='LogicalFa',fontfile=fontfile)
   stream=f'BT /LogicalFa {j["font"]*scale} Tf 3 Tr\n'.encode()
   for i,ch in enumerate(display_source):
    gid=font.has_glyph(ord(ch))
    stream+=f'{ratio} 0 0 1 {positions[i]} {p.rect.height-rect.y0-y} Tm <{gid:04x}> Tj\n'.encode()
   stream+=b'ET';xref=d.get_new_xref();d.update_object(xref,'<<>>');d.update_stream(xref,stream)
   contents=p.get_contents();d.xref_set_key(p.xref,'Contents','['+' '.join(f'{x} 0 R' for x in contents+[xref])+']')
   logical_lines.append(line)
  assert clean(source[offset:])=='',(j['id'],source[offset:])
  layers.append({'id':j['id'],'page':pi+1,'logical_lines':logical_lines,'scale':scale})
  tmp.close();vector.close();vpdf.close()
# Give joiners and hamza a real searchable glyph cell, mapped to their exact Unicode.
for p in d:
 for fx,*rest in p.get_fonts():
  if rest[3]!='LogicalFa':continue
  tx=int(d.xref_get_key(fx,'ToUnicode')[1].split()[0]);s=d.xref_stream(tx)
  for placeholder,code in [('|','200c'),('^','0654')]:
   gid=font.has_glyph(ord(placeholder));s=s.replace(f'<{gid:04x}> <{ord(placeholder):04x}>'.encode(),f'<{gid:04x}> <{code}>'.encode())
  d.update_stream(tx,s)
d.set_metadata({**old.metadata,'subject':'Partial Persian translation; vector appearance and exact logical Unicode text layer. Source CC BY 4.0.'})
args.output.parent.mkdir(parents=True,exist_ok=True)
d.save(args.output,garbage=4,deflate=True)
args.output.with_suffix('.lines.json').write_text(json.dumps(layers,ensure_ascii=False,indent=2),encoding='utf8')
print('Created',len(layers),'Unicode text regions; validate copy/search and render before delivery.')
