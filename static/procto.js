
const video = document.getElementById('video')
var tab_change=0
var fullscreen=0
var det_len=0
var cheat=0
document.addEventListener("visibilitychange", event => {
  if (document.visibilityState == "visible") {
    alert("If you change tabs another "+(3-tab_change)+" times.. Test will be closed");
  } else {
    tab_change=tab_change+1;
    alert("tab is inactive");
  }

})

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('../static/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('../static/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('../static/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('../static/models')
]).then(startVideo)

function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

function isfullscreen(){
  return window.innerHeight == screen.height && window.innerWidth == screen.width;
}
document.addEventListener("fullscreenChange", function () {
          
      });
video.addEventListener('play', () => {
 
  const canvas = faceapi.createCanvasFromMedia(video)
  document.body.append(canvas)
  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)
  setInterval(async () => {

    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    det_len=det_len+detections.length

    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    
  }, 500)
  setInterval(async ()=>{

    
    if(det_len<10){
      alert("Make sure that your face is visible")
      cheat=cheat+1

    }
    if(det_len>25){
      alert("Make sure that no one is around you")
      cheat=cheat+1
    }
    if(cheat>5||tab_change>=2){
      document.getElementById('finish').click();
    }
    
    det_len=0
  },10000)
  setInterval(async ()=>{
    if( isfullscreen() == true) {
            fullscreen=1
            

          }else{
            fullscreen=0

            
          }
    console.log(fullscreen)
  },1000)

})

