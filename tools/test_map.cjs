const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync('outputs/A-Noite-Vermelha-HTML-27/JOGAR.html','utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]).join('\n');new vm.Script(script);
const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]));
for(const m of script.matchAll(/\$\('#([^']+)'\)/g))assert(ids.has(m[1]),'missing element '+m[1]);
const nav=JSON.parse(fs.readFileSync('outputs/A-Noite-Vermelha-HTML-27/assets/mapa-navegacao.json'));
const sandbox={NAV:nav,Map,Math};vm.createContext(sandbox);
let code=script.slice(script.indexOf('const collisionGrid='),script.indexOf('async function init()'));
vm.runInContext(code,sandbox);
assert.equal(vm.runInContext('blocked(-58,-30,0)',sandbox),true,'secondary house must block entry');
assert.equal(vm.runInContext('blocked(-24,1,0.12)',sandbox),false,'bar entrance must be passable');
assert.equal(vm.runInContext('blocked(-24,12,0.12)',sandbox),true,'bar counter must block');
assert.equal(nav.story.length,15);
assert(script.includes('uniform float retroFX;'));assert(script.includes("'retroFX'"));
assert(script.includes('if(!lake&&!river)discard'));
console.log(JSON.stringify({syntax:'passed',domReferences:'passed',closedHouse:'passed',tavernEntrance:'passed',counterCollision:'passed',storyPoints:nav.story.length,rendering:'not verified: browser launch unavailable'},null,2));


