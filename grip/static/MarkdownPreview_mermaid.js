const uml = className => {
  const blocks_noclass = document.querySelectorAll(`pre[lang="${className}"]`);
  for (let i = 0; i < blocks_noclass.length; i++) {
    const block = blocks_noclass[i];
    block.classList.add("mermaid");
  }
  const blocks = document.querySelectorAll(`pre.${className} > code`)
  // console.log(blocks)
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i]
    block.replaceWith(...block.childNodes)
  }
}
// This should be run on document load
document.addEventListener("DOMContentLoaded", () => {uml("mermaid")});

function createMermaidScript(src, isModule) {
  const script = document.createElement('script');
  if (isModule) {
    script.type = 'module';
    script.innerHTML = `
      import mermaid from '${src}';
      mermaid.initialize({
        startOnLoad: true,
        theme: '${theme}',
      });
    `;
  } else {
    script.src = src;
    script.onload = () => {
      if (window.mermaid) {
        window.mermaid.initialize({
          startOnLoad: true,
          theme: theme,
        });
      }
    };
  }
  document.head.appendChild(script);
}

function insert_mermaidjs() {
  // const cdnUrl = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  const cdnUrl = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.esm.min.mjs';
  const localUrl = '/__/grip/static/mermaid.min.js';

  fetch(cdnUrl, { method: 'HEAD' })
    .then(() => createMermaidScript(cdnUrl, true))
    .catch(() => createMermaidScript(localUrl, false));
}
insert_mermaidjs();