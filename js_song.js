window.onSpotifyWebPlaybackSDKReady = () => {
    const token = 'ZSVb47wN7Fd8De44j65zg9Ya7ayMad1T_fPbcHKuE8cBiJNz_UgoSaTNc_ky9Q5iBpCqYTGvNBYj4t0lQvOxtJLos92C29SiJjVC9P3hcC6ezan9nF1LdQTgXB3lkRy19YMzdF0tX5kDb_x3m_dn26oWo_TEzBPZ5rB5aWeNOzLJasgbL-CQAMc6l3D5L4MkwOKJFqUIos15eH9vAQ';
    const player = new Spotify.Player({
      name: 'Web Playback SDK Quick Start Player',
      getOAuthToken: cb => { cb(token); },
      volume: 0.5
    });  
// Ready
player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

// Not Ready
player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
    });
player.addListener('initialization_error', ({ message }) => { 
    console.error(message);
    });

player.addListener('authentication_error', ({ message }) => {
    console.error(message);
    });

player.addListener('account_error', ({ message }) => {
    console.error(message);
    });
player.connect();
<button id="togglePlay">Toggle Play</button>
document.getElementById('togglePlay').onclick = function() {
    player.togglePlay();
  };  
