window.addEventListener('load', () => {
  const DEBUG = true;
  const script = {};

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
      const originalHeight = content.clientHeight;
      content.style.filter = `blur(8px)`;
      content.style.height = "100px";
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
      const unblock = () => {
        content.style.filter = '';
        script.gsap.to(content, { height: `${originalHeight}px`, duration: 0.6, onComplete: () => { content.style.height = "" } });
        btn.style.display = 'none';
        toBeBlocked.forEach((item) => {
          item.style.pointerEvents = "auto";
        });
      };
      btn.onclick = unblock;
      li.appendChild(btn);

      const as = content.querySelectorAll(`[role='link']`); // <a/> s
      const urls = [...as].map(e => e.href);
      const [fbUrl, storeUrl] = [urls[0], urls[3]];
      if (DEBUG) console.log({ as, urls, fbUrl, storeUrl });

      fetch('https://inno.racterub.me/', {
        body: JSON.stringify({ fbUrl, storeUrl }),
        method: "POST",
        headers: { "Content-Type": "application/json" },
      }).then((response) => {
        return response.text();
      }).then((text) => {
        if (DEBUG) console.log(text);
        if (!text) return;
        
        const { status } = JSON.parse(text);
        if (status) return;
        // unblock();
      });
    });
  }

  // Select the node that will be observed for mutations
  let targetNode = document.querySelector(`[role='feed']`);
  const parentNode = targetNode.parentNode;

  // Options for the observer (which mutations to observe)
  
  // Callback function to execute when mutations are observed
  const callback = function (mutationsList, observer) {
    // Use traditional 'for loops' for IE 11
    for (const mutation of mutationsList) {
      if (mutation.type === 'childList') {
        block([...mutation.addedNodes])
      }
    }
  };
  
  const observe = (targetNode) => {
    const config = { childList: true };
    // Create an observer instance linked to the callback function
    const observer = new MutationObserver(callback);

    // Start observing the target node for configured mutations
    observer.observe(targetNode, config);
    return observer;
  };

  let observer = observe(targetNode);
  block([...targetNode.querySelectorAll(`[data-pagelet]`)])

  fetch('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/gsap.min.js')
    .then((res) => res.text())
    .then((text) => {
      eval(text);
      script.gsap = gsap;
    })

  window.setInterval(() => {
    const newTargetNode = document.querySelector(`[role='feed']`);
    if (!newTargetNode || targetNode === newTargetNode) return;
    observer.disconnect();
    observer = observe(newTargetNode);
    block([...newTargetNode.querySelectorAll(`[data-pagelet]`)])

    targetNode = newTargetNode;
  }, 5000);
});
