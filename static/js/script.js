(function() {

  // JavaScript snippet handling Dark/Light mode switching

  const getStoredTheme = () => localStorage.getItem('theme');
  const setStoredTheme = theme => localStorage.setItem('theme', theme);
  const forcedTheme = document.documentElement.getAttribute('data-bss-forced-theme');
  
  // Start QR Scanner Code 
  var qrcode = window.qrcode;

  const video = document.createElement("video");
  const canvasElement = document.getElementById("qr-canvas");
  const canvas = canvasElement.getContext("2d");
  
  const qrResult = document.getElementById("qr-result");
  const outputData = document.getElementById("outputData");
  const btnScanQR = document.getElementById("btn-scan-qr");
  
  let scanning = false;
  
  qrcode.callback = res => {
    if (res) {
      outputData.innerText = res;
      scanning = false;
  
      video.srcObject.getTracks().forEach(track => {
        track.stop();
      });
  
      qrResult.hidden = false;
      canvasElement.hidden = true;
      btnScanQR.hidden = false;
    }
  };
  
  btnScanQR.onclick = () => {
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "environment" } })
      .then(function(stream) {
        scanning = true;
        qrResult.hidden = true;
        btnScanQR.hidden = true;
        canvasElement.hidden = false;
        video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
        video.srcObject = stream;
        video.play();
        tick();
        scan();
      });
  };
  
  function tick() {
    canvasElement.height = video.videoHeight;
    canvasElement.width = video.videoWidth;
    canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
  
    scanning && requestAnimationFrame(tick);
  }
  
  function scan() {
    try {
      qrcode.decode();
    } catch (e) {
      setTimeout(scan, 300);
    }
  }

  // End QR Scanner Code

  const getPreferredTheme = () => {

    if (forcedTheme) return forcedTheme;

    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }

    const pageTheme = document.documentElement.getAttribute('data-bs-theme');

    if (pageTheme) {
      return pageTheme;
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const setTheme = theme => {
    if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-bs-theme', 'dark');
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme);
    }
  };

  setTheme(getPreferredTheme());

  const showActiveTheme = (theme, focus = false) => {
    const themeSwitchers = [].slice.call(document.querySelectorAll('.theme-switcher'));

    if (!themeSwitchers.length) return;

    document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
      element.classList.remove('active');
      element.setAttribute('aria-pressed', 'false');
    });

    for (const themeSwitcher of themeSwitchers) {

      const btnToActivate = themeSwitcher.querySelector('[data-bs-theme-value="' + theme + '"]');

      if (btnToActivate) {
        btnToActivate.classList.add('active');
        btnToActivate.setAttribute('aria-pressed', 'true');
      }
    }
  };

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme();
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme());
    }
  });

  window.addEventListener('DOMContentLoaded', () => {
    showActiveTheme(getPreferredTheme());

    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(toggle => {
        toggle.addEventListener('click', (e) => {
          e.preventDefault();
          const theme = toggle.getAttribute('data-bs-theme-value');
          setStoredTheme(theme);
          setTheme(theme);
          showActiveTheme(theme);
        });
      });
  });
})();

// Start: Script for signup/signin toggle
  document.addEventListener('DOMContentLoaded', function() {
    let signInButton = document.getElementById('goToSignIn');
    let signUpButton = document.getElementById('goToSignUp');

    signInButton.addEventListener('click', function() {
      document.getElementById('signUpTab').classList.remove('show', 'active');

      let signInTabContent = document.getElementById('signInTab');
      signInTabContent.classList.add('show', 'active');
    });

    signUpButton.addEventListener('click', function() {
      document.getElementById('signInTab').classList.remove('show', 'active');

      let signUpTabContent = document.getElementById('signUpTab');
      signUpTabContent.classList.add('show', 'active');
    });
  });
//  End: Script for signup/signin toggle