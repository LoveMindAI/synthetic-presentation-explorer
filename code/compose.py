"""Reproduce the final alpha-compositing step from exported, face-locked layers.

This is the same Pillow alpha-composite operation used for the illustrated bank.
It does not generate images or approximate missing participant inputs.
"""
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

def main():
 p=argparse.ArgumentParser();p.add_argument('--layers',type=Path,default=Path('example_layers/S01'));p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 assert not a.output.exists(), 'Choose a new output directory; do not overwrite evidence.'
 a.output.mkdir(parents=True)
 base=Image.open(a.layers/'canonical_base.png').convert('RGB')
 mask=Image.open(a.layers/'face_core.png').convert('L')
 core=[i for i,v in enumerate(mask.getdata()) if v>0];source=list(base.getdata())
 checks=[]
 for fg in sorted(a.layers.glob('foreground__*.png')):
  foreground=Image.open(fg).convert('RGBA')
  for bg in sorted(a.layers.glob('background__*.png')):
   image=Image.open(bg).convert('RGBA');assert image.size==foreground.size==base.size
   image.alpha_composite(foreground);rgb=image.convert('RGB');pixels=list(rgb.getdata())
   assert all(pixels[i]==source[i] for i in core),'Face core changed'
   name=fg.stem.removeprefix('foreground__')+'__'+bg.stem.removeprefix('background__')+'.png'
   rgb.save(a.output/name)
   checks.append(dict(file=name,pixel_sha256=hashlib.sha256(rgb.tobytes()).hexdigest(),face_core_exact=True))
 assert len(checks)==16
 (a.output/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('16 cells reconstructed; face-core equality passed.')
if __name__=='__main__':main()
