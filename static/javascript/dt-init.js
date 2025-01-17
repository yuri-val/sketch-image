var drawingTool = new DrawingTool("#drawing-tool", {
  stamps: {
    'Molecules': [
      'https://interactions-resources.concord.org/stamps/simple-atom.svg',
      'https://interactions-resources.concord.org/stamps/diatomic.svg',
      'https://interactions-resources.concord.org/stamps/diatomic-red.svg',
      'https://interactions-resources.concord.org/stamps/triatomic.svg',
      'https://interactions-resources.concord.org/stamps/positive-atom.svg',
      'https://interactions-resources.concord.org/stamps/negative-atom.svg',
      'https://interactions-resources.concord.org/stamps/slow-particle.svg',
      'https://interactions-resources.concord.org/stamps/medium-particle.svg',
      'https://interactions-resources.concord.org/stamps/fast-particle.svg',
      'https://interactions-resources.concord.org/stamps/low-density-particles.svg'
    ],
    'Second Molecules': [
      'https://interactions-resources.concord.org/stamps/simple-atom.svg',
      'https://interactions-resources.concord.org/stamps/diatomic.svg',
      'https://interactions-resources.concord.org/stamps/diatomic-red.svg',
      'https://interactions-resources.concord.org/stamps/triatomic.svg',
      'https://interactions-resources.concord.org/stamps/positive-atom.svg',
      'https://interactions-resources.concord.org/stamps/negative-atom.svg',
      'https://interactions-resources.concord.org/stamps/slow-particle.svg',
      'https://interactions-resources.concord.org/stamps/medium-particle.svg',
      'https://interactions-resources.concord.org/stamps/fast-particle.svg',
      'https://interactions-resources.concord.org/stamps/low-density-particles.svg'
    ]
  },
  parseSVG: true,
  separatorsAfter: [
    "stamp",
    "strokeWidthPalette"
  ]
});

// Load state from localStorage on page load
var savedState = localStorage.getItem('drawingToolState');
if (savedState) {
  drawingTool.load(JSON.parse(savedState));
}

// Save state to localStorage on change
drawingTool.on('drawing:changed', function () {
  var state = drawingTool.save();
  localStorage.setItem('drawingToolState', JSON.stringify(state));
});

$("#set-background").on("click", function () {
  drawingTool.setBackgroundImage($("#background-src").val());
});
$("#resize-background").on("click", function () {
  drawingTool.resizeBackgroundToCanvas();
});
$("#resize-canvas").on("click", function () {
  drawingTool.resizeCanvasToBackground();
});
$("#shrink-background").on("click", function () {
  drawingTool.shrinkBackgroundToCanvas();
});
$("#clear").on("click", function () {
  drawingTool.clear(true);
  localStorage.removeItem('drawingToolState');
});
$("#save").on("click", function () {
  var state = drawingTool.save();
  localStorage.setItem('drawingToolState', JSON.stringify(state));
  $("#load").removeAttr("disabled");
});
$("#load").on("click", function () {
  var state = localStorage.getItem('drawingToolState');
  if (state === null) return;
  drawingTool.load(JSON.parse(state));
});
$("#download").on("click", function () {
  var canvas = document.querySelector("#drawing-tool canvas.lower-canvas");
  var dataURL = canvas.toDataURL("image/jpeg");
  var link = document.createElement("a");
  link.href = dataURL;
  link.download = "canvas.jpg";
  link.click();
});
