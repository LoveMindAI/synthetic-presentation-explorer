import Foundation
import Vision
import AppKit
import CoreImage
import ImageIO

let args=CommandLine.arguments
guard args.count == 4 else {fatalError("usage: segment_person input output_mask output_json")}
let url=URL(fileURLWithPath:args[1])
guard let src=CGImageSourceCreateWithURL(url as CFURL,nil),let cg=CGImageSourceCreateImageAtIndex(src,0,nil) else {fatalError("Cannot read input")}
let request=VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat=kCVPixelFormatType_OneComponent8
let faceRequest=VNDetectFaceLandmarksRequest()
let handler=VNImageRequestHandler(cgImage:cg,options:[:])
try handler.perform([request,faceRequest])
guard let result=request.results?.first else {fatalError("No segmentation")}
let buffer=result.pixelBuffer
let ci=CIImage(cvPixelBuffer:buffer)
let context=CIContext()
guard let output=context.createCGImage(ci,from:ci.extent) else {fatalError("No mask image")}
let rep=NSBitmapImageRep(cgImage:output)
try rep.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:args[2]))
var faces:[[String:Any]]=[]
for f in faceRequest.results ?? [] {
 let b=f.boundingBox
 var record:[String:Any]=["bbox_norm_bottom_left":[b.origin.x,b.origin.y,b.size.width,b.size.height]]
 func points(_ r:VNFaceLandmarkRegion2D?) -> [[Double]] {
  guard let r=r else{return []}
  return (0..<r.pointCount).map {i in
   let p=r.normalizedPoints[i]
   return [Double(b.origin.x)+Double(p.x)*Double(b.size.width),1.0-(Double(b.origin.y)+Double(p.y)*Double(b.size.height))]
  }
 }
 record["left_eye_norm_top_left"]=points(f.landmarks?.leftEye)
 record["right_eye_norm_top_left"]=points(f.landmarks?.rightEye)
 record["outer_lips_norm_top_left"]=points(f.landmarks?.outerLips)
 record["face_contour_norm_top_left"]=points(f.landmarks?.faceContour)
 faces.append(record)
}
let meta:[String:Any]=["input":args[1],"input_size":[cg.width,cg.height],"mask_size":[output.width,output.height],"faces":faces,"segmentation":"Apple Vision VNGeneratePersonSegmentationRequest accurate", "os":ProcessInfo.processInfo.operatingSystemVersionString]
try JSONSerialization.data(withJSONObject:meta,options:[.prettyPrinted,.sortedKeys]).write(to:URL(fileURLWithPath:args[3]))
print("Masked \(args[1]); faces=\(faces.count)")

