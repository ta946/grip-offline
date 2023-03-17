const uml = className => {
  const blocks = document.querySelectorAll(`pre.${className} > code`)
  // console.log(blocks)
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i]
    block.replaceWith(...block.childNodes)
  }
}
// This should be run on document load
document.addEventListener("DOMContentLoaded", () => {uml("mermaid")});

function insert_mermaidjs() {
  var script = document.createElement('script');
  script.type = 'module';
  // import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  script.innerHTML = `
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.esm.min.mjs';
  mermaid.initialize({
      startOnLoad: true,
      theme: '${color_scheme}',
    });
  `;
  document.head.appendChild(script);
}
insert_mermaidjs();