<!DOCTYPE html>
<html>
<head>
    <title>Simulador de Física - Prof. Ojeda</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
    <style>
        body { margin: 0; display: flex; flex-direction: column; align-items: center; font-family: sans-serif; background: #f0f0f0; }
        .controles { padding: 20px; background: white; border-radius: 10px; margin: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        canvas { border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    </style>
</head>
<body>

<div class="controles">
    <h2>📦 Dinâmica: Força e Atrito (Versão Ultrarrápida)</h2>
    Massa: <input type="range" id="massa" min="1" max="50" value="10"> <span id="vMassa">10</span> kg <br>
    Força F: <input type="range" id="forca" min="0" max="400" value="150"> <span id="vForca">150</span> N <br>
    Atrito (µ): <input type="range" id="mu" min="0" max="1" step="0.1" value="0.2"> <span id="vMu">0.2</span> <br><br>
    <button onclick="reiniciar()" style="padding: 10px 20px; cursor: pointer; background: #007bff; color: white; border: none; border-radius: 5px;">🚀 Iniciar / Reiniciar</button>
</div>

<script>
let x = 50, v = 0, a = 0, rodando = false;
const g = 9.8;

function setup() {
    createCanvas(800, 200);
}

function draw() {
    background(255);
    
    // Pegar valores dos inputs
    let m = float(document.getElementById('massa').value);
    let f = float(document.getElementById('forca').value);
    let mu = float(document.getElementById('mu').value);
    
    // Atualizar labels
    document.getElementById('vMassa').innerText = m;
    document.getElementById('vForca').innerText = f;
    document.getElementById('vMu').innerText = mu;

    // Lógica de Física (Igual ao C++)
    let fatMax = mu * m * g;
    let fRes = f - fatMax;
    a = fRes > 0 ? fRes / m : 0;

    if (rodando && a > 0) {
        v += a * (1/60); // 60 FPS
        x += v;
    }

    // Desenho do Cenário
    stroke(0); strokeWeight(2);
    line(0, 150, width, 150); // Chão

    // Bloco
    fill(0, 123, 255); noStroke();
    rect(x % width, 110, 40, 40); // % width faz ele voltar pro início se sair da tela

    // Setas
    fill(0, 0, 255); triangle((x%width)+85, 130, (x%width)+70, 120, (x%width)+70, 140); // Seta F
    stroke(0, 0, 255); line((x%width)+40, 130, (x%width)+75, 130);
    
    fill(255, 0, 0); triangle((x%width)-45, 145, (x%width)-30, 140, (x%width)-30, 150); // Seta Fat
    stroke(255, 0, 0); line((x%width), 145, (x%width)-35, 145);

    // Texto de status
    fill(0); noStroke(); fontSize = 16;
    text("Velocidade: " + v.toFixed(1) + " m/s", 20, 30);
    text("Aceleração: " + a.toFixed(2) + " m/s²", 20, 50);
}

function reiniciar() {
    x = 50; v = 0; rodando = true;
}
</script>
</body>
</html>
