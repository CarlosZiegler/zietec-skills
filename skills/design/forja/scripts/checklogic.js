// Forja · testa a lógica de cada tela .dc.html no Node, sem navegador.
// Para cada arquivo de tela (Main*, M-*, D-*): valida o JSON de data-props, instancia `class Component` com um DCLogic falso,
// confere que todo hole {{ x.y }} do template existe em renderVals(), dispara todos os handlers (até 2 níveis de objetos)
// e confere de novo. Opcional: um módulo de testes de interação do produto.
//
// uso: node checklogic.js <pasta project> [logic_tests.js]
//
// logic_tests.js exporta { "<arquivo-base>.dc.html": (fresh, chk) => { ... } }, onde
//   fresh() devolve [componente, renderVals()] novos e chk(cond, msg) registra falha.
//   O arquivo-base é o nome sem sufixo de idioma (M-Hoje-DE.dc.html → M-Hoje.dc.html); o teste roda nos 3 idiomas.
// Exemplo:
//   module.exports = { "Main.dc.html": (fresh, chk) => { let [c, v] = fresh(); chk(v.isM, "mensal por padrão");
//     v.per_y.pick(); chk(c.renderVals().isY, "toggle anual"); } };
const fs = require('fs'), path = require('path');
const dir = process.argv[2] || '.';
const tests = process.argv[3] ? require(path.resolve(process.argv[3])) : {};
const files = fs.readdirSync(dir).filter(f => /^(Main|M-|D-)/.test(f) && f.endsWith('.dc.html'));
let bad = 0;
for (const f of files) {
  const s = fs.readFileSync(path.join(dir, f), 'utf8');
  const m = s.match(/<script type="text\/x-dc" data-dc-script data-props='([^']*)'>([\s\S]*?)<\/script>/);
  if (!m) { continue; } // tela sem lógica
  try { JSON.parse(m[1].replace(/&amp;/g, '&').replace(/&#39;/g, "'").replace(/&quot;/g, '"')); }
  catch (e) { console.log(f, 'data-props inválido:', e.message); bad++; continue; }
  class DCLogic { constructor() { this.props = {}; this.state = undefined; } setState(o) { this.state = Object.assign({}, this.state || {}, o); } }
  let C;
  try { C = eval('(function(){' + m[2] + '; return Component; })()'); } catch (e) { console.log(f, 'erro ao avaliar a lógica:', e.message); bad++; continue; }
  const body = (s.split('<x-dc>')[1] || '').split('</x-dc>')[0];
  const holes = [...new Set([...body.matchAll(/\{\{\s*([^}]+?)\s*\}\}/g)].map(x => x[1]))];
  const loopVars = new Set([...body.matchAll(/as="([^"]+)"/g)].map(x => x[1]));
  const check = (v) => { const miss = []; for (const h of holes) { const parts = h.split('.'); if (['true', 'false', '$index'].includes(h) || loopVars.has(parts[0])) continue;
      let cur = v; for (const p of parts) { if (cur == null || !(p in Object(cur))) { miss.push(h); break; } cur = cur[p]; } } return miss; };
  const fire = (obj, depth) => { for (const k of Object.keys(obj)) { const v = obj[k]; if (typeof v === 'function') { v(); } else if (v && typeof v === 'object' && depth < 2 && !Array.isArray(v)) fire(v, depth + 1); } };
  let miss = [];
  try {
    const c = new C(); let vals = c.renderVals(); miss = check(vals);
    fire(vals, 0); vals = c.renderVals(); miss = miss.concat(check(vals));
    fire(vals, 0); vals = c.renderVals(); miss = miss.concat(check(vals));
  } catch (e) { console.log(f, 'erro ao rodar handlers:', e.message); bad++; continue; }
  if (miss.length) { console.log(f, 'holes sem valor', [...new Set(miss)]); bad++; }
  const base = f.replace(/-(EN|PT|DE)\.dc\.html$/, '.dc.html');
  if (tests[base]) {
    const fresh = () => { const c0 = new C(); return [c0, c0.renderVals()]; };
    const chk = (cond, msg) => { if (!cond) { console.log(f, 'falhou:', msg); bad++; } };
    try { tests[base](fresh, chk); } catch (e) { console.log(f, 'teste lançou erro:', e.message); bad++; }
  }
}
console.log('telas', files.length, bad ? 'PROBLEMAS ' + bad : 'tudo ok');
process.exitCode = bad ? 1 : 0;
