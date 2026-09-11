"""Portable extraction of the image-request pattern; dry-run unless --go.

Input: one trial object from data/generation_prompts.json plus a local synthetic
reference image. One call only. An existing output directory blocks re-execution.
The historical endpoint/model identifiers are documented, not availability claims.
"""
import argparse,base64,hashlib,json,mimetypes,os,urllib.request
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--trial',required=True);p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--go',action='store_true');a=p.parse_args()
 root=Path(__file__).resolve().parent.parent
 trials=json.loads((root/'data/generation_prompts.json').read_text())
 choices=trials['initial_layer_prompts']+trials['selected_repair_prompts']
 matching=[r for r in choices if r['trial_id']==a.trial];assert len(matching)==1
 t=matching[0];raw=a.reference.read_bytes();mime=mimetypes.guess_type(a.reference.name)[0];assert mime in ['image/png','image/jpeg','image/webp']
 payload=dict(model=t['model'],prompt=t['prompt'],aspect_ratio=t.get('aspect_ratio','16:9'),n=1)
 for k in ['quality','resolution']:
  if t.get(k) is not None:payload[k]=t[k]
 if not a.go:print(json.dumps(payload,indent=2));return
 key=os.environ['OPENROUTER_API_KEY']
 a.output.mkdir(parents=True,exist_ok=False)
 (a.output/'intent.json').write_text(json.dumps(payload|{'reference_sha256':hashlib.sha256(raw).hexdigest()},indent=2))
 payload['input_references']=[{'type':'image_url','image_url':{'url':'data:'+mime+';base64,'+base64.b64encode(raw).decode()}}]
 req=urllib.request.Request('https://openrouter.ai/api/v1/images',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=420) as response:result=json.load(response)
 assert len(result.get('data',[]))==1
 b=base64.b64decode(result['data'][0]['b64_json'],validate=True)
 (a.output/'returned_image').write_bytes(b)
 (a.output/'result.json').write_text(json.dumps({'requested_model':t['model'],'returned_model':result.get('model'),'returned_provider':result.get('provider'),'image_sha256':hashlib.sha256(b).hexdigest(),'usage':result.get('usage')},indent=2))
 print('One response saved. Inspect image format and verify quality before reuse.')
if __name__=='__main__':main()
