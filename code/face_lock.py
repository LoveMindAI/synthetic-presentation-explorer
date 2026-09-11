"""Alignment and head-weight functions extracted unchanged from the source compositor.
Use explicit synthetic inputs; no participant data are included.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
SIZE=(1280,720)

def merge_locked_head(base_rgb, base_alpha, edited_rgb, edited_alpha, weights, core):
    """The source pipeline's premultiplied head/clothing merge, with explicit arrays."""
    base=np.asarray(base_rgb,dtype=float);source=np.asarray(edited_rgb,dtype=float)
    ba=np.asarray(base_alpha,dtype=float)/255.;a=np.asarray(edited_alpha,dtype=float)/255.
    core=np.asarray(core)>0;ba[core]=1
    upper=ba*weights;lower=a*(1-weights);alpha=upper+lower
    premul=base*upper[:,:,None]+source*lower[:,:,None]
    pix=np.divide(premul,alpha[:,:,None],out=np.zeros_like(premul),where=alpha[:,:,None]>0)
    pix=np.clip(np.rint(pix),0,255).astype('uint8');pix[core]=base.astype('uint8')[core];alpha[core]=1
    rgba=Image.fromarray(pix).convert('RGBA');rgba.putalpha(Image.fromarray(np.rint(alpha*255).astype('uint8')))
    return rgba

def eye_centers(f):
    return np.array([np.mean(f[k],axis=0)*SIZE for k in ['left_eye_norm_top_left','right_eye_norm_top_left']])

def align(rgb,alpha,face,baseface):
    src=eye_centers(face);dst=eye_centers(baseface)
    assert np.isfinite(src).all() and np.isfinite(dst).all()
    zsrc=complex(*(src[1]-src[0]));zdst=complex(*(dst[1]-dst[0]));z=zdst/zsrc
    a,b=z.real,z.imag
    matrix=np.array([[a,-b],[b,a]])
    translation=dst.mean(axis=0)-matrix@src.mean(axis=0)
    inv=np.linalg.inv(matrix);offset=-inv@translation
    coeff=tuple([inv[0,0],inv[0,1],offset[0],inv[1,0],inv[1,1],offset[1]])
    record=dict(scale=abs(z),rotation_degrees=float(np.degrees(np.angle(z))),translation=translation.tolist(),pil_inverse_affine=coeff)
    assert .80<abs(z)<1.25 and abs(record['rotation_degrees'])<8,record
    return rgb.transform(SIZE,Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC),alpha.transform(SIZE,Image.Transform.AFFINE,coeff,Image.Resampling.BILINEAR),record

def head_weights(baseface,override=None):
    x,y,w,h=baseface['bbox_norm_bottom_left'];x*=SIZE[0];w*=SIZE[0];top=(1-y-h)*SIZE[1];bottom=(1-y)*SIZE[1]
    # Manually adjustable per-identity neck boundary; default just below chin.
    cut=bottom+6
    if override:cut=override.get('head_cut_y',cut)
    # Neck-shaped boundary, NOT a horizontal splice through shoulders/clothing.
    points=[(0,0),(SIZE[0],0),(SIZE[0],top+.60*(bottom-top)),
            (x+1.15*w,top+.60*(bottom-top)),(x+1.10*w,bottom-.20*(bottom-top)),
            (x+.88*w,bottom),(x+.75*w,cut),(x+.25*w,cut),
            (x+.12*w,bottom),(x-.10*w,bottom-.20*(bottom-top)),
            (x-.15*w,top+.60*(bottom-top)),(0,top+.60*(bottom-top))]
    contour=np.asarray(baseface['face_contour_norm_top_left'])*SIZE
    if len(contour)>6:
        if contour[0,0]<contour[-1,0]:contour=contour[::-1]
        # Follow the jaw rather than crossing the original collar. Hair below the
        # jaw remains from the aligned garment source unless a manual polygon pins it.
        expanded=[(float(px+np.sign(px-(x+w/2))*4),float(py+2)) for px,py in contour]
        points=[(0,0),(SIZE[0],0),(SIZE[0],expanded[0][1])]+expanded+[(0,expanded[-1][1])]
    if override and 'head_polygon' in override:points=override['head_polygon']
    region=Image.new('L',SIZE);ImageDraw.Draw(region).polygon(points,fill=255)
    weight=np.asarray(region.filter(ImageFilter.GaussianBlur(3)),dtype=float)/255.
    # Explicitly pin the interior face after boundary feathering.
    core=Image.new('L',SIZE);ImageDraw.Draw(core).ellipse((x+.12*w,top+.03*(bottom-top),x+.88*w,bottom-.04*(bottom-top)),fill=255)
    weight[np.asarray(core)>0]=1
    return weight,dict(head_cut_y=cut,face_bbox_xyxy=[x,top,x+w,bottom])
