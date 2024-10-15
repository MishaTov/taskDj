const url = `ws://${window.location.host+window.location.pathname}`;

console.log(url);

const socket = new WebSocket(url);
