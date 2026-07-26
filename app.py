import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Race: Haiti Bus vs World",
    page_icon="\U0001F68C",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        .stAppFooter, .stAppFooter * {display: none !important;}
        .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
        iframe {height: 100vh !important; width: 100% !important; border: none !important;}
        .stAppFooter {display: none !important;}
        .css-1vq4p4l {display: none !important;}
        .stDeployButton {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

GAME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Race: Haiti Bus vs World | Gesner Deslandes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', 'Courier New', monospace; background: #0a1030; touch-action: none; }

        /* FULL SCREEN BUTTON – top-right */
        #fullscreen-btn {
            position: absolute; top: 12px; right: 12px;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 30px;
            color: white;
            padding: 6px 14px;
            font-size: 14px;
            font-family: monospace;
            z-index: 500;
            cursor: pointer;
            touch-action: manipulation;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        #fullscreen-btn:hover { background: rgba(255,255,255,0.2); }

        /* HAITIAN FLAG – bottom-right corner */
        #haiti-flag-corner {
            position: absolute; bottom: 12px; right: 12px;
            z-index: 400;
            pointer-events: none;
            opacity: 0.7;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        #haiti-flag-corner .flag-small {
            width: 40px;
            height: 24px;
            background: linear-gradient(to bottom, #00209F 50%, #D21034 50%);
            border-radius: 4px;
            border: 1px solid gold;
            box-shadow: 0 0 8px rgba(0,0,0,0.5);
        }
        #haiti-flag-corner .label {
            color: rgba(255,255,255,0.5);
            font-size: 9px;
            font-family: monospace;
            letter-spacing: 1px;
        }

        /* INFO PANEL – subtle, top-left */
        #info-panel {
            position: absolute; top: 10px; left: 10px;
            background: rgba(0,0,0,0.25);
            backdrop-filter: blur(4px);
            padding: 4px 10px;
            border-radius: 12px;
            border-left: 3px solid #D21034;
            z-index: 100;
            color: rgba(255,255,255,0.5);
            font-size: 8px;
            pointer-events: none;
            font-weight: normal;
            text-shadow: 0 0 4px black;
        }
        #info-panel .names { font-size: 7px; line-height: 1.2; }
        #info-panel .names span { color: #ffd966; }

        /* SPEED PANEL – bottom-right, above flag */
        #speed-panel {
            position: absolute; bottom: 60px; right: 12px;
            background: rgba(0,0,0,0.35);
            backdrop-filter: blur(4px);
            padding: 3px 10px;
            border-radius: 14px;
            font-family: monospace;
            font-size: 13px;
            font-weight: bold;
            color: rgba(0,255,255,0.7);
            z-index: 100;
            border: 1px solid rgba(0,255,255,0.15);
            pointer-events: none;
        }

        #message-box {
            position: absolute; bottom: 30%; left: 50%; transform: translateX(-50%);
            background: rgba(0,0,0,0.65);
            padding: 6px 14px;
            border-radius: 30px;
            color: gold;
            font-weight: bold;
            font-size: 15px;
            text-align: center;
            white-space: nowrap;
            pointer-events: none;
            z-index: 100;
            font-family: monospace;
            border: 1px solid #ffaa33;
            backdrop-filter: blur(4px);
        }

        .button-group {
            position: absolute; bottom: 24px; right: 20px;
            display: flex; gap: 10px; z-index: 200;
        }
        .btn-action {
            background: rgba(0,0,0,0.55);
            color: white;
            border: 1px solid orange;
            padding: 6px 14px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            font-family: monospace;
            font-size: 13px;
            touch-action: manipulation;
            backdrop-filter: blur(4px);
            transition: 0.15s;
        }
        .btn-action:hover { background: #ff6600; }
        .btn-action:active { transform: scale(0.92); }

        #flag-selector {
            position: absolute; top: 12px; right: 80px;
            background: rgba(0,0,0,0.35);
            backdrop-filter: blur(4px);
            padding: 4px 10px;
            border-radius: 16px;
            color: white;
            font-family: monospace;
            font-size: 10px;
            z-index: 200;
            display: flex;
            gap: 6px;
            align-items: center;
            border: 1px solid rgba(255,255,255,0.1);
        }
        select {
            background: rgba(0,0,0,0.6);
            color: white;
            border: 1px solid gold;
            border-radius: 6px;
            padding: 2px 6px;
            font-size: 10px;
        }

        /* VIRTUAL CONTROLS – positioned ABOVE START/RESET */
        #virtual-controls {
            position: fixed;
            bottom: 95px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 14px;
            z-index: 300;
            background: rgba(0,0,0,0.25);
            backdrop-filter: blur(6px);
            padding: 10px 18px;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.06);
            touch-action: none;
        }
        .ctrl-btn {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: rgba(255,255,255,0.08);
            border: 2px solid rgba(255,255,255,0.15);
            color: white;
            font-size: 22px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
            touch-action: none;
            cursor: pointer;
            transition: 0.08s;
            -webkit-tap-highlight-color: transparent;
        }
        .ctrl-btn:active {
            background: rgba(255,255,255,0.25);
            transform: scale(0.85);
        }
        .ctrl-btn.up { background: rgba(0,200,80,0.2); border-color: rgba(0,255,0,0.3); }
        .ctrl-btn.down { background: rgba(200,50,50,0.2); border-color: rgba(255,68,68,0.3); }
        .ctrl-btn.left, .ctrl-btn.right { background: rgba(50,130,255,0.2); border-color: rgba(68,170,255,0.3); }

        @media (max-width: 600px) {
            #info-panel { font-size: 6px; top: 6px; left: 6px; padding: 2px 8px; }
            #info-panel .names { font-size: 5px; }
            #speed-panel { font-size: 11px; bottom: 55px; right: 6px; padding: 2px 8px; }
            #message-box { font-size: 11px; bottom: 28%; padding: 4px 10px; white-space: nowrap; }
            #flag-selector { font-size: 8px; top: 6px; right: 60px; padding: 2px 6px; }
            #virtual-controls { gap: 8px; padding: 8px 12px; bottom: 85px; }
            .ctrl-btn { width: 42px; height: 42px; font-size: 18px; }
            .button-group { bottom: 18px; right: 12px; gap: 6px; }
            .btn-action { font-size: 11px; padding: 4px 10px; }
            #haiti-flag-corner { bottom: 8px; right: 8px; }
            #haiti-flag-corner .flag-small { width: 30px; height: 18px; }
            #haiti-flag-corner .label { font-size: 7px; }
            #fullscreen-btn { font-size: 11px; padding: 4px 10px; top: 6px; right: 6px; }
        }
    </style>
</head>
<body>

    <!-- HAITIAN FLAG – bottom-right corner -->
    <div id="haiti-flag-corner">
        <div class="flag-small"></div>
        <span class="label">HAITI</span>
    </div>

    <!-- FULL SCREEN BUTTON -->
    <button id="fullscreen-btn">⛶ FULL</button>

    <!-- INFO PANEL -->
    <div id="info-panel">
        <div class="names">🚌 <span>Gesner Deslandes</span> · Gesner Jr · Roosevelt · Sebastien · Zendaya</div>
    </div>

    <!-- SPEED -->
    <div id="speed-panel">🚍 <span id="speed-value">0</span> km/h</div>

    <!-- MESSAGE -->
    <div id="message-box">🏁 Choose opponent and press START</div>

    <!-- START / RESET buttons -->
    <div class="button-group">
        <button class="btn-action" id="startBtn">🚦 START</button>
        <button class="btn-action" id="resetBtn">🔄 RESET</button>
    </div>

    <!-- OPPONENT FLAG SELECTOR -->
    <div id="flag-selector">
        🏁 <select id="opponentFlag">
            <option value="dominican">🇩🇴 Dominican</option>
            <option value="usa">🇺🇸 USA</option>
            <option value="france">🇫🇷 France</option>
            <option value="brazil">🇧🇷 Brazil</option>
        </select>
    </div>

    <!-- VIRTUAL CONTROLS -->
    <div id="virtual-controls">
        <div class="ctrl-btn left" id="btn-left">◀</div>
        <div class="ctrl-btn up" id="btn-up">▲</div>
        <div class="ctrl-btn down" id="btn-down">▼</div>
        <div class="ctrl-btn right" id="btn-right">▶</div>
    </div>

    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.128.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.128.0/examples/jsm/"
            }
        }
    </script>

    <script type="module">
        import * as THREE from 'three';
        import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

        // ===== FULL SCREEN =====
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        fullscreenBtn.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen?.() || document.documentElement.webkitRequestFullscreen?.();
                fullscreenBtn.textContent = '⛶ EXIT';
            } else {
                document.exitFullscreen?.() || document.webkitExitFullscreen?.();
                fullscreenBtn.textContent = '⛶ FULL';
            }
        });
        document.addEventListener('fullscreenchange', () => {
            fullscreenBtn.textContent = document.fullscreenElement ? '⛶ EXIT' : '⛶ FULL';
        });

        // ===== SCENE SETUP =====
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a1030);
        scene.fog = new THREE.FogExp2(0x0a1030, 0.008);

        const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 8);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.shadowMap.enabled = true;
        document.body.appendChild(renderer.domElement);

        const labelRenderer = new CSS2DRenderer();
        labelRenderer.setSize(window.innerWidth, window.innerHeight);
        labelRenderer.domElement.style.position = 'absolute';
        labelRenderer.domElement.style.top = '0px';
        labelRenderer.domElement.style.left = '0px';
        labelRenderer.domElement.style.pointerEvents = 'none';
        document.body.appendChild(labelRenderer.domElement);

        // ===== LIGHTING =====
        const ambientLight = new THREE.AmbientLight(0x404060);
        scene.add(ambientLight);
        const sunLight = new THREE.DirectionalLight(0xfff5d1, 1.2);
        sunLight.position.set(20, 30, 10);
        sunLight.castShadow = true;
        sunLight.shadow.mapSize.width = 1024;
        sunLight.shadow.mapSize.height = 1024;
        scene.add(sunLight);
        const fillLight = new THREE.PointLight(0x5577aa, 0.4);
        fillLight.position.set(0, 5, 0);
        scene.add(fillLight);

        // ===== RACE CONSTANTS (faster) =====
        const ROAD_WIDTH = 6.0;
        const LANE_LIMIT = 2.7;
        const FINISH_LINE_Z = 400;
        const START_LINE_Z = 0;
        const MAX_SPEED = 45;        // faster
        const MAX_REVERSE = -8;
        const ACCEL = 2.8;           // more acceleration
        const BRAKE = 2.2;

        // ===== ROAD =====
        const roadLength = FINISH_LINE_Z + 60;
        const roadMat = new THREE.MeshStandardMaterial({ color: 0x2c2e3a, roughness: 0.7 });
        const roadPlane = new THREE.Mesh(new THREE.PlaneGeometry(ROAD_WIDTH, roadLength), roadMat);
        roadPlane.rotation.x = -Math.PI / 2;
        roadPlane.position.y = -0.05;
        roadPlane.position.z = roadLength / 2;
        roadPlane.receiveShadow = true;
        scene.add(roadPlane);

        const lineMat = new THREE.MeshStandardMaterial({ color: 0xffdd99 });
        for (let z = 5; z <= FINISH_LINE_Z + 20; z += 4) {
            const line = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.05, 2), lineMat);
            line.position.set(0, 0.02, z);
            line.castShadow = false;
            scene.add(line);
        }
        const edgeMat = new THREE.MeshStandardMaterial({ color: 0xccaa55 });
        for (let side = -1; side <= 1; side += 2) {
            for (let z = 0; z <= FINISH_LINE_Z + 20; z += 3) {
                const edge = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.08, 1.5), edgeMat);
                edge.position.set(side * (ROAD_WIDTH / 2 - 0.25), 0.03, z);
                scene.add(edge);
            }
        }

        // Start / Finish
        const startMat = new THREE.MeshStandardMaterial({ color: 0x44aa44 });
        for (let i = -3; i <= 3; i += 1) {
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.1, 1), startMat);
            stripe.position.set(i * 0.6, 0.08, START_LINE_Z);
            scene.add(stripe);
        }
        const finishMatRed = new THREE.MeshStandardMaterial({ color: 0xdd2222 });
        const finishMatWhite = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
        for (let i = -3; i <= 3; i += 1) {
            const mat = (Math.floor(i) % 2 === 0) ? finishMatRed : finishMatWhite;
            const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.1, 1), mat);
            stripe.position.set(i * 0.6, 0.08, FINISH_LINE_Z);
            scene.add(stripe);
        }
        const finishDiv = document.createElement('div');
        finishDiv.textContent = '🏁 FINISH 🏁';
        finishDiv.style.color = 'gold';
        finishDiv.style.fontSize = '20px';
        finishDiv.style.fontWeight = 'bold';
        finishDiv.style.backgroundColor = 'rgba(0,0,0,0.6)';
        finishDiv.style.padding = '4px 12px';
        finishDiv.style.borderRadius = '20px';
        finishDiv.style.border = '2px solid red';
        const finishSign = new CSS2DObject(finishDiv);
        finishSign.position.set(0, 1.5, FINISH_LINE_Z);
        scene.add(finishSign);

        // ===== OBSTACLES =====
        class Obstacle {
            constructor(z, type) {
                this.type = type;
                let mesh;
                if (type === 'rock') {
                    mesh = new THREE.Mesh(new THREE.DodecahedronGeometry(0.45), new THREE.MeshStandardMaterial({ color: 0x886e4e, roughness: 0.9 }));
                } else {
                    mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 0.6, 5), new THREE.MeshStandardMaterial({ color: 0xbc8f6b }));
                }
                const x = (Math.random() - 0.5) * (ROAD_WIDTH - 1.2);
                mesh.position.set(x, 0.1, z);
                mesh.castShadow = true;
                scene.add(mesh);
                this.mesh = mesh;
                this.z = z;
                this.x = x;
                this.active = true;
            }
            destroy() { scene.remove(this.mesh); }
        }
        let obstacles = [];
        for (let z = 50; z <= FINISH_LINE_Z - 30; z += 25) {
            if (Math.abs(z - FINISH_LINE_Z) < 15) continue;
            obstacles.push(new Obstacle(z, Math.random() > 0.6 ? 'rock' : 'log'));
        }

        // ===== ENVIRONMENT =====
        const treeTrunkMat = new THREE.MeshStandardMaterial({ color: 0x8B5A2B });
        const treeTopMat = new THREE.MeshStandardMaterial({ color: 0x5c9e3e });
        const rockMat = new THREE.MeshStandardMaterial({ color: 0x6a705c });
        for (let z = -20; z <= FINISH_LINE_Z + 50; z += 12) {
            for (let side = -1; side <= 1; side += 2) {
                if (Math.random() > 0.6) {
                    const x = side * (ROAD_WIDTH / 2 + 1.5 + Math.random() * 3);
                    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 1.2, 5), treeTrunkMat);
                    trunk.position.set(x, 0.2, z);
                    trunk.castShadow = true;
                    const top = new THREE.Mesh(new THREE.ConeGeometry(0.6, 1.0, 6), treeTopMat);
                    top.position.set(x, 0.9, z);
                    top.castShadow = true;
                    scene.add(trunk, top);
                } else if (Math.random() > 0.8) {
                    const x = side * (ROAD_WIDTH / 2 + 1.2 + Math.random() * 4);
                    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.5), rockMat);
                    rock.position.set(x, -0.2, z);
                    rock.castShadow = true;
                    scene.add(rock);
                }
            }
        }
        const cliffMat = new THREE.MeshStandardMaterial({ color: 0xaa5533 });
        for (let z = 0; z <= FINISH_LINE_Z + 50; z += 40) {
            if (Math.random() > 0.7) {
                for (let i = -2; i <= 2; i++) {
                    const rock = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.8 + Math.random(), 2), cliffMat);
                    rock.position.set(3.8 + i * 0.4, -0.2, z + i * 1.5);
                    rock.castShadow = true;
                    scene.add(rock);
                }
            }
        }

        // ===== BUS MODEL =====
        const busGroup = new THREE.Group();
        const bodyGeo = new THREE.BoxGeometry(1.4, 0.9, 2.8);
        const blueMatBus = new THREE.MeshStandardMaterial({ color: 0x2a6fdb, roughness: 0.3 });
        const body = new THREE.Mesh(bodyGeo, blueMatBus);
        body.castShadow = true;
        body.position.y = 0.45;
        busGroup.add(body);
        const redStripeMatBus = new THREE.MeshStandardMaterial({ color: 0xcc3333 });
        const stripeLeft = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), redStripeMatBus);
        stripeLeft.position.set(-0.75, 0.55, 0);
        busGroup.add(stripeLeft);
        const stripeRight = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.2, 2.6), redStripeMatBus);
        stripeRight.position.set(0.75, 0.55, 0);
        busGroup.add(stripeRight);
        const roofStripe = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.1, 2.2), redStripeMatBus);
        roofStripe.position.set(0, 0.9, 0);
        busGroup.add(roofStripe);
        const glassMatBus = new THREE.MeshStandardMaterial({ color: 0x88ccff });
        for (let i = -0.8; i <= 0.8; i += 0.8) {
            const win = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.35, 0.08), glassMatBus);
            win.position.set(i, 0.7, 0.9);
            busGroup.add(win);
            const winBack = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.35, 0.08), glassMatBus);
            winBack.position.set(i, 0.7, -0.9);
            busGroup.add(winBack);
        }
        const wheelMatBus = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.7 });
        const wheelGeo = new THREE.CylinderGeometry(0.28, 0.28, 0.4, 16);
        [[-0.8, 0.15, 1.0], [0.8, 0.15, 1.0], [-0.8, 0.15, -1.1], [0.8, 0.15, -1.1]].forEach(pos => {
            const wheel = new THREE.Mesh(wheelGeo, wheelMatBus);
            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(pos[0], pos[1], pos[2]);
            wheel.castShadow = true;
            busGroup.add(wheel);
        });
        const lightMatBus = new THREE.MeshStandardMaterial({ color: 0xffaa66, emissive: 0xff4411 });
        const leftLight = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), lightMatBus);
        leftLight.position.set(-0.55, 0.35, 1.45);
        const rightLight = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), lightMatBus);
        rightLight.position.set(0.55, 0.35, 1.45);
        busGroup.add(leftLight, rightLight);
        scene.add(busGroup);

        // ===== OPPONENT CAR =====
        const carGroup = new THREE.Group();
        const carBodyMesh = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.5, 1.8), new THREE.MeshStandardMaterial({ color: 0xdd4422, roughness: 0.4 }));
        carBodyMesh.position.y = 0.25;
        carGroup.add(carBodyMesh);
        const carRoofMesh = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.3, 1.2), new THREE.MeshStandardMaterial({ color: 0xaa3311 }));
        carRoofMesh.position.y = 0.55;
        carGroup.add(carRoofMesh);
        const wheelMatCar = new THREE.MeshStandardMaterial({ color: 0x222222 });
        [[-0.5, 0.1, 0.7], [0.5, 0.1, 0.7], [-0.5, 0.1, -0.7], [0.5, 0.1, -0.7]].forEach(pos => {
            const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.3, 12), wheelMatCar);
            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(pos[0], pos[1], pos[2]);
            wheel.castShadow = true;
            carGroup.add(wheel);
        });
        let extraStripe = null;
        scene.add(carGroup);

        let flagDiv = document.createElement('div');
        flagDiv.style.fontSize = '32px';
        flagDiv.style.filter = 'drop-shadow(0 0 2px black)';
        const carFlag = new CSS2DObject(flagDiv);
        carFlag.position.set(0, 0.7, 0);
        carGroup.add(carFlag);

        function updateCarColorsByFlag(flagValue) {
            if (extraStripe) {
                carGroup.remove(extraStripe);
                extraStripe = null;
            }
            let bodyColor, roofColor, stripeColor;
            switch (flagValue) {
                case 'dominican':
                    bodyColor = 0xffffff;
                    roofColor = 0xce1126;
                    stripeColor = 0x002b7f;
                    break;
                case 'usa':
                    bodyColor = 0xb22234;
                    roofColor = 0xffffff;
                    stripeColor = 0x3c3b6e;
                    break;
                case 'france':
                    bodyColor = 0x0055a4;
                    roofColor = 0xffffff;
                    stripeColor = 0xef4135;
                    break;
                case 'brazil':
                    bodyColor = 0x009c3b;
                    roofColor = 0xffdf00;
                    stripeColor = 0x002776;
                    break;
                default:
                    bodyColor = 0xdd4422;
                    roofColor = 0xaa3311;
                    stripeColor = null;
            }
            carBodyMesh.material = new THREE.MeshStandardMaterial({ color: bodyColor, roughness: 0.4 });
            carRoofMesh.material = new THREE.MeshStandardMaterial({ color: roofColor, roughness: 0.4 });
            if (stripeColor) {
                const stripeGeo = new THREE.BoxGeometry(0.12, 0.12, 1.6);
                const stripeMat = new THREE.MeshStandardMaterial({ color: stripeColor });
                extraStripe = new THREE.Mesh(stripeGeo, stripeMat);
                extraStripe.position.set(0, 0.38, 0);
                extraStripe.castShadow = true;
                carGroup.add(extraStripe);
            }
        }
        function updateOpponentFlagAndColors() {
            const select = document.getElementById('opponentFlag');
            const val = select.value;
            let flagEmoji = '';
            switch (val) {
                case 'dominican':
                    flagEmoji = '🇩🇴';
                    break;
                case 'usa':
                    flagEmoji = '🇺🇸';
                    break;
                case 'france':
                    flagEmoji = '🇫🇷';
                    break;
                case 'brazil':
                    flagEmoji = '🇧🇷';
                    break;
                default:
                    flagEmoji = '🏁';
            }
            flagDiv.textContent = flagEmoji;
            updateCarColorsByFlag(val);
        }
        updateOpponentFlagAndColors();
        document.getElementById('opponentFlag').addEventListener('change', updateOpponentFlagAndColors);

        // ===== RACE STATE =====
        let busZ = 0,
            carZ = 0;
        let busSpeed = 8,
            carSpeed = 8;
        let busLateral = -1.0,
            carLateral = 1.2;
        let crashed = false,
            raceActive = false,
            raceRunning = false;
        let winner = null,
            countdown = 0,
            countdownInterval = null;
        let aiTargetSpeed = 12,
            carSteering = 0;

        const startBtn = document.getElementById('startBtn');
        const resetBtn = document.getElementById('resetBtn');
        const opponentSelect = document.getElementById('opponentFlag');

        function stopCountdown() {
            if (countdownInterval) { clearInterval(countdownInterval);
                countdownInterval = null; }
        }
        function startCountdown() {
            if (countdownInterval) stopCountdown();
            countdown = 3;
            raceRunning = false;
            raceActive = true;
            document.getElementById('message-box').innerHTML = `🏁 Race starts in ${countdown}...`;
            countdownInterval = setInterval(() => {
                if (countdown > 1) {
                    countdown--;
                    document.getElementById('message-box').innerHTML = `🏁 Race starts in ${countdown}...`;
                } else if (countdown === 1) {
                    countdown--;
                    document.getElementById('message-box').innerHTML = `🏁 GO! 🏁`;
                    raceRunning = true;
                    startEngineSound();
                    engineRev();
                    setTimeout(() => {
                        if (raceActive && !winner) {
                            document.getElementById('message-box').innerHTML = `🏁 Race in progress! Use arrows to drive.`;
                        }
                    }, 1500);
                } else {
                    clearInterval(countdownInterval);
                    countdownInterval = null;
                }
            }, 1000);
        }
        function fullReset() {
            stopCountdown();
            raceActive = false;
            raceRunning = false;
            winner = null;
            crashed = false;
            finishSoundPlayed = false;
            busZ = 0;
            carZ = 0;
            busSpeed = 8;
            carSpeed = 8;
            busLateral = -1.0;
            carLateral = 1.2;
            aiTargetSpeed = 12;
            carSteering = 0;
            busGroup.position.set(busLateral, 0.2, 0);
            carGroup.position.set(carLateral, 0.2, 0);
            balloons.forEach(b => scene.remove(b.mesh));
            balloons = [];
            opponentSelect.disabled = false;
            document.getElementById('message-box').innerHTML = "🏁 Choose opponent and press START";
            startBtn.disabled = false;
            startBtn.style.opacity = '1';
            document.getElementById('speed-value').innerText = "0";
            stopEngineSound();
        }
        function startRace() {
            if (raceActive) return;
            fullReset();
            opponentSelect.disabled = true;
            startCountdown();
        }
        startBtn.addEventListener('click', startRace);
        resetBtn.addEventListener('click', fullReset);

        // ===== AI =====
        function updateAI(dt) {
            if (!raceRunning) return;
            const lookahead = 35;
            let nearestObstacle = null,
                minDist = Infinity;
            for (let obs of obstacles) {
                if (!obs.active) continue;
                const dist = obs.z - carZ;
                if (dist > 0 && dist < lookahead && Math.abs(obs.x - carLateral) < 1.2) {
                    if (dist < minDist) { minDist = dist;
                        nearestObstacle = obs; }
                }
            }
            if (nearestObstacle) {
                carSteering = (nearestObstacle.x > carLateral) ? -1.2 : 1.2;
            } else {
                if (carLateral < 1.0) carSteering = 0.8;
                else if (carLateral > 1.4) carSteering = -0.8;
                else carSteering = 0;
            }
            carLateral += carSteering * dt * 2.5;
            carLateral = Math.max(-LANE_LIMIT + 0.5, Math.min(LANE_LIMIT - 0.5, carLateral));
            let obstacleAhead = (nearestObstacle !== null);
            if (obstacleAhead) aiTargetSpeed = Math.max(5, aiTargetSpeed - 5 * dt);
            else aiTargetSpeed = Math.min(MAX_SPEED - 2, aiTargetSpeed + 3 * dt);
            if (carSpeed < aiTargetSpeed) carSpeed += ACCEL * dt;
            else if (carSpeed > aiTargetSpeed) carSpeed -= BRAKE * dt;
            carSpeed = Math.max(MAX_REVERSE, Math.min(MAX_SPEED, carSpeed));
            carZ += carSpeed * dt;
            carGroup.position.x = carLateral;
            carGroup.position.z = carZ;
            carGroup.position.y = 0.2;
        }

        // ===== KEYBOARD & VIRTUAL CONTROLS with multi-touch support =====
        const keys = { ArrowUp: false, ArrowDown: false, ArrowLeft: false, ArrowRight: false };
        window.addEventListener('keydown', (e) => {
            if (e.key.startsWith('Arrow')) e.preventDefault();
            if (!raceRunning && !(e.key === 'ArrowUp' && winner)) return;
            keys[e.key] = true;
        });
        window.addEventListener('keyup', (e) => { if (e.key.startsWith('Arrow')) keys[e.key] = false; });

        function setupVirtualButton(id, key) {
            const btn = document.getElementById(id);
            if (!btn) return;
            const start = (e) => {
                e.preventDefault();
                keys[key] = true;
                initEngineSound(); // ensure audio context is active
                // also start engine if race is running but sound not yet playing
                if (raceRunning) startEngineSound();
            };
            const end = (e) => {
                e.preventDefault();
                keys[key] = false;
            };
            // Mouse
            btn.addEventListener('mousedown', start);
            btn.addEventListener('mouseup', end);
            btn.addEventListener('mouseleave', end);
            // Touch
            btn.addEventListener('touchstart', start, { passive: false });
            btn.addEventListener('touchend', end, { passive: false });
            btn.addEventListener('touchcancel', end, { passive: false });
        }
        setupVirtualButton('btn-up', 'ArrowUp');
        setupVirtualButton('btn-down', 'ArrowDown');
        setupVirtualButton('btn-left', 'ArrowLeft');
        setupVirtualButton('btn-right', 'ArrowRight');

        // Global audio init on any user interaction
        document.addEventListener('click', () => { initEngineSound(); });
        document.addEventListener('touchstart', () => { initEngineSound(); }, { passive: true });

        function updateBus(dt) {
            if (!raceRunning) return;
            if (keys.ArrowUp) {
                busSpeed += ACCEL * dt * 1.2; // extra boost when forward pressed
                if (busSpeed > MAX_SPEED) busSpeed = MAX_SPEED;
            }
            if (keys.ArrowDown) {
                if (busSpeed > 0) busSpeed -= BRAKE * dt * 1.5;
                else busSpeed -= ACCEL * 0.9 * dt;
                if (busSpeed < MAX_REVERSE) busSpeed = MAX_REVERSE;
            }
            if (!keys.ArrowUp && !keys.ArrowDown && busSpeed !== 0) {
                busSpeed *= (1 - dt * 1.2);
                if (Math.abs(busSpeed) < 0.2) busSpeed = 0;
            }
            let turn = 0;
            if (keys.ArrowLeft) turn = -6.0;
            if (keys.ArrowRight) turn = 6.0;
            busLateral += turn * dt * (Math.abs(busSpeed) * 0.1 + 0.8);
            busLateral = Math.max(-LANE_LIMIT, Math.min(LANE_LIMIT, busLateral));
            busGroup.position.x = busLateral;
            busZ += busSpeed * dt;
            busGroup.position.z = busZ;
            busGroup.position.y = 0.2;
        }

        function checkCollisions() {
            if (!raceRunning) return;
            const busX = busLateral;
            const carX = carLateral;
            for (let obs of obstacles) {
                if (!obs.active) continue;
                if (Math.abs(obs.z - busZ) < 1.2 && Math.abs(obs.x - busX) < 0.9) {
                    crashed = true;
                    raceRunning = false;
                    raceActive = false;
                    showMessage(`💥 Bus crashed! Press RESET.`, true);
                    return;
                }
                if (Math.abs(obs.z - carZ) < 1.2 && Math.abs(obs.x - carX) < 0.8) {
                    crashed = true;
                    raceRunning = false;
                    raceActive = false;
                    showMessage(`💥 Opponent crashed! Press RESET.`, true);
                    return;
                }
            }
            if (Math.abs(busLateral) > LANE_LIMIT) {
                crashed = true;
                raceRunning = false;
                raceActive = false;
                showMessage(`💥 Bus drove off road! Press RESET.`, true);
                return;
            }
        }

        let finishSoundPlayed = false;

        function playFinishFanfare(winnerName) {
            if (finishSoundPlayed) return;
            finishSoundPlayed = true;
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            let ctx = null;
            try { ctx = new AudioCtx(); } catch (e) { return; }
            const now = ctx.currentTime;
            const masterGain = ctx.createGain();
            masterGain.gain.value = 0.5;
            masterGain.connect(ctx.destination);
            const notes = [261.63, 329.63, 392.00, 523.25];
            const durations = [0.25, 0.25, 0.25, 0.6];
            for (let i = 0; i < notes.length; i++) {
                const osc = ctx.createOscillator();
                const gainNote = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.value = notes[i];
                gainNote.gain.setValueAtTime(0.3, now + i * 0.28);
                gainNote.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.28 + durations[i]);
                osc.connect(gainNote);
                gainNote.connect(masterGain);
                osc.start(now + i * 0.28);
                osc.stop(now + i * 0.28 + durations[i]);
            }
            const noise = ctx.createBufferSource();
            const bufferSize = 4096;
            const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
            noise.buffer = buffer;
            const noiseGain = ctx.createGain();
            noiseGain.gain.setValueAtTime(0.2, now + 0.4);
            noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
            noise.connect(noiseGain);
            noiseGain.connect(masterGain);
            noise.start(now + 0.4);
            noise.stop(now + 1.2);
            const drum = ctx.createOscillator();
            drum.type = 'triangle';
            drum.frequency.value = 150;
            const drumGain = ctx.createGain();
            drumGain.gain.setValueAtTime(0.4, now);
            drumGain.gain.exponentialRampToValueAtTime(0.0001, now + 0.2);
            drum.connect(drumGain);
            drumGain.connect(masterGain);
            drum.start(now);
            drum.stop(now + 0.2);
        }

        function checkFinish() {
            if (!raceRunning) return;
            if (busZ >= FINISH_LINE_Z && winner === null) {
                winner = 'bus';
                raceRunning = false;
                raceActive = false;
                showMessage(`🏆 HAITI BUS WINS! 🎉🏆`, false);
                playFinishFanfare('bus');
                createBalloons();
                opponentSelect.disabled = false;
                stopEngineSound();
            } else if (carZ >= FINISH_LINE_Z && winner === null) {
                winner = 'car';
                raceRunning = false;
                raceActive = false;
                showMessage(`🏆 OPPONENT CAR WINS! Better luck next time! 🏆`, false);
                playFinishFanfare('car');
                createBalloons();
                opponentSelect.disabled = false;
                stopEngineSound();
            }
        }

        let balloons = [];

        function createBalloons() {
            for (let i = 0; i < 20; i++) {
                const color = new THREE.Color().setHSL(Math.random(), 0.8, 0.6);
                const balloonMat = new THREE.MeshStandardMaterial({ color });
                const balloon = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 16), balloonMat);
                const x = (Math.random() - 0.5) * 6;
                const z = FINISH_LINE_Z + (Math.random() - 0.5) * 5;
                balloon.position.set(x, 0.5, z);
                scene.add(balloon);
                balloons.push({ mesh: balloon, lift: 0, speed: 0.5 + Math.random() * 0.5 });
            }
        }

        function updateBalloons(dt) {
            for (let i = 0; i < balloons.length; i++) {
                const b = balloons[i];
                b.lift += dt * b.speed;
                b.mesh.position.y = 0.5 + b.lift;
                if (b.mesh.position.y > 8) {
                    scene.remove(b.mesh);
                    balloons.splice(i, 1);
                    i--;
                }
            }
        }

        const speedSpan = document.getElementById('speed-value');
        const msgBox = document.getElementById('message-box');
        let messageTimeout = null;

        function showMessage(text, isWarning = false, duration = 2500) {
            if (messageTimeout) clearTimeout(messageTimeout);
            msgBox.innerHTML = text;
            msgBox.style.color = isWarning ? '#ff8866' : '#ffdd99';
            messageTimeout = setTimeout(() => {
                if (!raceActive && !winner) msgBox.innerHTML = "Race over. Press RESET.";
                else if (raceActive && raceRunning) msgBox.innerHTML = "🏁 Race in progress! Use arrows to drive.";
                else if (!raceActive) msgBox.innerHTML = "Choose opponent and press START";
            }, duration);
        }

        // ===== ENGINE SOUND (will run on mobile) =====
        let engineCtx = null,
            engineNodes = null,
            engineRunning = false;

        function initEngineSound() {
            if (engineCtx && engineCtx.state === 'suspended') {
                engineCtx.resume();
                return;
            }
            if (engineCtx) return;
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            try { engineCtx = new AudioCtx(); } catch (e) { return; }
            const masterGain = engineCtx.createGain();
            masterGain.gain.value = 0.5;
            masterGain.connect(engineCtx.destination);
            const osc1 = engineCtx.createOscillator();
            osc1.type = 'sawtooth';
            osc1.frequency.value = 80;
            const gain1 = engineCtx.createGain();
            gain1.gain.value = 0;
            osc1.connect(gain1);
            gain1.connect(masterGain);
            const osc2 = engineCtx.createOscillator();
            osc2.type = 'sine';
            osc2.frequency.value = 45;
            const gain2 = engineCtx.createGain();
            gain2.gain.value = 0;
            osc2.connect(gain2);
            gain2.connect(masterGain);
            const bufferSize = 4096;
            const buffer = engineCtx.createBuffer(1, bufferSize, engineCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
            const noise = engineCtx.createBufferSource();
            noise.buffer = buffer;
            noise.loop = true;
            const noiseGain = engineCtx.createGain();
            noiseGain.gain.value = 0;
            const filter = engineCtx.createBiquadFilter();
            filter.type = 'lowpass';
            filter.frequency.value = 300;
            noise.connect(filter);
            filter.connect(noiseGain);
            noiseGain.connect(masterGain);
            engineNodes = { masterGain, osc1, gain1, osc2, gain2, noise, noiseGain, filter };
            osc1.start();
            osc2.start();
            noise.start();
            engineCtx.resume();
        }

        function startEngineSound() {
            if (!engineNodes) initEngineSound();
            if (!engineNodes) return;
            if (engineCtx.state === 'suspended') engineCtx.resume();
            engineRunning = true;
        }

        function engineRev() {
            if (!engineNodes || !engineRunning) return;
            const now = engineCtx.currentTime;
            engineNodes.osc1.frequency.setValueAtTime(80, now);
            engineNodes.osc1.frequency.linearRampToValueAtTime(250, now + 0.3);
            engineNodes.osc1.frequency.linearRampToValueAtTime(80, now + 0.6);
            engineNodes.gain1.gain.setValueAtTime(0.05, now);
            engineNodes.gain1.gain.linearRampToValueAtTime(0.2, now + 0.15);
            engineNodes.gain1.gain.linearRampToValueAtTime(0.05, now + 0.6);
            engineNodes.gain2.gain.setValueAtTime(0.02, now);
            engineNodes.gain2.gain.linearRampToValueAtTime(0.1, now + 0.2);
            engineNodes.gain2.gain.linearRampToValueAtTime(0.02, now + 0.6);
            engineNodes.noiseGain.gain.setValueAtTime(0.01, now);
            engineNodes.noiseGain.gain.linearRampToValueAtTime(0.05, now + 0.2);
            engineNodes.noiseGain.gain.linearRampToValueAtTime(0.01, now + 0.6);
        }

        function stopEngineSound() {
            if (!engineNodes) return;
            engineRunning = false;
            const now = engineCtx.currentTime;
            engineNodes.gain1.gain.setValueAtTime(0, now);
            engineNodes.gain2.gain.setValueAtTime(0, now);
            engineNodes.noiseGain.gain.setValueAtTime(0, now);
        }

        function updateEngineSound(speed) {
            if (!engineNodes || !engineRunning) return;
            const absSpd = Math.abs(speed);
            const norm = Math.min(1, absSpd / MAX_SPEED);
            engineNodes.osc1.frequency.value = 80 + norm * 270;
            engineNodes.osc2.frequency.value = 45 + norm * 135;
            engineNodes.filter.frequency.value = 200 + norm * 600;
            const g1 = 0.02 + norm * 0.25;
            const g2 = 0.01 + norm * 0.12;
            const gNoise = 0.005 + norm * 0.08;
            engineNodes.gain1.gain.value = g1;
            engineNodes.gain2.gain.value = g2;
            engineNodes.noiseGain.gain.value = gNoise;
        }

        // ===== CAMERA =====
        function updateCamera() {
            const targetX = busLateral * 0.3;
            const targetY = 3.5 + Math.min(1.2, Math.abs(busSpeed) / 20) * 0.5;
            const targetZ = busZ - 6;
            camera.position.lerp(new THREE.Vector3(targetX, targetY, targetZ), 0.1);
            camera.lookAt(busLateral, 1.0, busZ);
        }

        // ===== MAIN LOOP =====
        let lastTime = performance.now();

        function animate() {
            const now = performance.now();
            let dt = Math.min(0.033, (now - lastTime) / 1000);
            lastTime = now;

            if (raceRunning && !crashed) {
                updateBus(dt);
                updateAI(dt);
                checkCollisions();
                checkFinish();
                updateEngineSound(busSpeed);
                speedSpan.innerText = Math.floor(Math.abs(busSpeed) * 3.6);
            }
            updateBalloons(dt);
            updateCamera();

            renderer.render(scene, camera);
            labelRenderer.render(scene, camera);
            requestAnimationFrame(animate);
        }

        fullReset();
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
            labelRenderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

components.html(GAME_HTML, height=1000, scrolling=False)
