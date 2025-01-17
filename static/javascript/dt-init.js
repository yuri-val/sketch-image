const STAMPS_BASE_URL = 'https://interactions-resources.concord.org/stamps/';
const STORAGE_KEY = 'drawingToolState';

const STAMPS = [
  'simple-atom.svg',
  'diatomic.svg',
  'diatomic-red.svg',
  'triatomic.svg',
  'positive-atom.svg',
  'negative-atom.svg',
  'slow-particle.svg',
  'medium-particle.svg',
  'fast-particle.svg',
  'low-density-particles.svg'
];

const drawingToolConfig = {
  stamps: {
    'Molecules': STAMPS.map(stamp => `${STAMPS_BASE_URL}${stamp}`),
    'Second Molecules': STAMPS.map(stamp => `${STAMPS_BASE_URL}${stamp}`)
  },
  parseSVG: true,
  separatorsAfter: [
    "stamp",
    "strokeWidthPalette"
  ]
};

const drawingTool = new DrawingTool("#drawing-tool", drawingToolConfig);

const loadState = () => {
  const savedState = localStorage.getItem(STORAGE_KEY);
  if (savedState) {
    drawingTool.load(JSON.parse(savedState));
  }
};

const saveState = () => {
  const state = drawingTool.save();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
};

const setupEventListeners = () => {
  drawingTool.on('drawing:changed', saveState);

  const actions = {
    'set-background': () => drawingTool.setBackgroundImage($("#background-src").val()),
    'resize-background': () => drawingTool.resizeBackgroundToCanvas(),
    'resize-canvas': () => drawingTool.resizeCanvasToBackground(),
    'shrink-background': () => drawingTool.shrinkBackgroundToCanvas(),
    'clear': () => {
      drawingTool.clear(true);
      localStorage.removeItem(STORAGE_KEY);
    },
    'save': () => {
      saveState();
      $("#load").removeAttr("disabled");
    },
    'load': () => {
      const state = localStorage.getItem(STORAGE_KEY);
      if (state) drawingTool.load(JSON.parse(state));
    },
    'download': () => {
      const canvas = document.querySelector("#drawing-tool canvas.lower-canvas");
      const link = document.createElement("a");
      link.href = canvas.toDataURL("image/jpeg");
      link.download = "canvas.jpg";
      link.click();
    }
  };

  Object.entries(actions).forEach(([id, action]) => {
    $(`#${id}`).on("click", action);
  });
};

const init = () => {
  loadState();
  setupEventListeners();
};

$(document).ready(init);