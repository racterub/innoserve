window.addEventListener('load', () => {
  function block(list) {
    list.forEach(li => {
      if (li.querySelector(`[aria-label="贊助"]`) !== null) {
        li = li.querySelector(`[role='article']`);
        while (li.children.length !== 2) li = li.children[0];
        const content = li.children[1];
        content.style.filter = `blur(8px)`;
        const toBeBlocked = content.querySelectorAll('video, a, div, span, image');
        toBeBlocked.forEach((item) => {
          item.style.pointerEvents = "none";
        });
        let btn = document.createElement("BUTTON");
        btn.innerText = 'OK';
        btn.style.position = 'absolute';
        btn.style.top = '50%';
        btn.style.left = '50%';
        btn.onclick = () => {
          content.style.filter = '';
          btn.style.display = 'none';
          toBeBlocked.forEach((item) => {
            item.style.pointerEvents = "auto";
          });
        };
        li.appendChild(btn);
      }
    });
  }

  // Select the node that will be observed for mutations
  const targetNode = document.querySelector(`[role='feed']`);

  // Options for the observer (which mutations to observe)
  const config = { childList: true };

  // Callback function to execute when mutations are observed
  const callback = function(mutationsList, observer) {
      // Use traditional 'for loops' for IE 11
      for(const mutation of mutationsList) {
          if (mutation.type === 'childList') {
              block(mutation.addedNodes)
          }
      }
  };

  // Create an observer instance linked to the callback function
  const observer = new MutationObserver(callback);

  // Start observing the target node for configured mutations
  observer.observe(targetNode, config);

  block(targetNode.querySelectorAll(`[data-pagelet]`))
});
