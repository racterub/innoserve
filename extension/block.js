window.addEventListener('load', () => {
  function hasLabel(elem, labels) {
    return labels.some(tag => elem.querySelector(`[aria-label=${tag}]`));
  }
  function block(list) {
    list.filter(li => {
      return hasLabel(li, ["贊助", "Sponsored"]) && !hasLabel(li, ["已驗證", "Verified"]);
    }).forEach(li => {
      li = li.querySelector(`[role='article']`);
      while (li.children.length !== 2) li = li.children[0];
      const content = li.children[1];
      content.style.filter = `blur(8px)`;
      const toBeBlocked = content.querySelectorAll('video, a, div, span, image');
      toBeBlocked.forEach((item) => {
        item.style.pointerEvents = "none";
      });
      let btn = document.createElement("BUTTON");
      btn.innerText = '我明白此篇貼文具有風險';
      btn.style.border = '2px solid black';
      btn.style.borderRadius = '1rem';
      btn.style.background = 'gray';
      btn.style.color = 'white';
      btn.style.position = 'absolute';
      btn.style.top = 'calc(50% - 1rem)';
      btn.style.left = 'calc(50% - 6rem)';
      btn.style.fontSize = '1rem';
      btn.style.padding = "0 0.5rem";
      btn.onclick = () => {
        content.style.filter = '';
        btn.style.display = 'none';
        toBeBlocked.forEach((item) => {
          item.style.pointerEvents = "auto";
        });
      };
      li.appendChild(btn);
    });
  }

  // Select the node that will be observed for mutations
  const targetNode = document.querySelector(`[role='feed']`);

  // Options for the observer (which mutations to observe)
  const config = { childList: true };

  // Callback function to execute when mutations are observed
  const callback = function (mutationsList, observer) {
    // Use traditional 'for loops' for IE 11
    for (const mutation of mutationsList) {
      if (mutation.type === 'childList') {
        block([...mutation.addedNodes])
      }
    }
  };

  // Create an observer instance linked to the callback function
  const observer = new MutationObserver(callback);

  // Start observing the target node for configured mutations
  observer.observe(targetNode, config);

  block([...targetNode.querySelectorAll(`[data-pagelet]`)])
});
