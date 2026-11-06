const fs=require('fs'),vm=require('vm'),assert=require('assert');
const src=fs.readFileSync('dist/app.js','utf8');
const code=src.slice(src.indexOf('function collectSelection()'),src.indexOf('function ',src.indexOf('function collectMessage(')+10));
let n=0;const ui={selectionbar:{},selectionPreview:{}};
const ctx={selection:null,state:{notes:[]},uid:()=>String(++n),book:()=>({id:'book',title:'笔记'}),current:()=>({id:'chat'}),now:()=>1,renderNotes(){},saveSoon(){},toast(){},$:id=>ui[id],window:{getSelection:()=>({removeAllRanges(){}})}};
vm.createContext(ctx);vm.runInContext(src.slice(src.indexOf('function clearSelection()'),src.indexOf('function handleSelection()'))+code,ctx);
const message={id:'m',text:'完整长回答，包含不应进入笔记的内容',reasoning:'未选择的思考',assets:['file']};
ctx.selection={parts:[{message,text:'只留下这句'}]};ctx.collectSelection();
ctx.selection={parts:[{message,text:'另一次摘录'},{message:{...message,id:'next'},text:'跨消息片段'}]};ctx.collectSelection();
assert.equal(ctx.state.notes.length,3);assert.deepEqual(Array.from(ctx.state.notes,n=>n.text),['跨消息片段','另一次摘录','只留下这句']);
for(const note of ctx.state.notes){assert.equal(note.text,note.original);assert.equal(note.originalReasoning,'');assert.equal(note.assets.length,0);assert(!note.text.includes('完整长回答'));}
assert.equal(new Set(ctx.state.notes.map(n=>n.id)).size,3);
console.log('PASS: repeat and multi-message excerpts save only selected text, without attachments or reasoning');
