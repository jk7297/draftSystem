//app.js
// Authorization token that must have been created previously. Check : https://developer.spotify.com/documentation/web-api/concepts/authorization
const token = 'BQDR3DRZzB-C1ck0RAQhpnZbUcMEWSGiCCwo5V3lFME1AOzUMsaJRkXvlG7ETxIXAbmjpEcrWoaaGDIq-oZRpxAtPC2W_on-InjPJwa5n3Gb44raHDSCNl5AyVuYz3-UCIVnaaqlmT3dFA2_xxK8Z41-7JwkbsYZooHcwAHFBiGDGq2-_kBWlXvv943lOMyMC-Mg8a7-BuaBeBaT7kDIdTMXVjaexJIBMNGnU9ecKkIzRtLypWLtXVrCkTZ_sIJ_XZpmZU5Uvg64ZJYS0ON2hkuS';
async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

async function getTopTracks(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
    'v1/me/top/tracks?time_range=long_term&limit=5', 'GET'
  )).items;
}

const topTracks = await getTopTracks();
console.log(
  topTracks?.map(
    ({name, artists}) =>
      `${name} by ${artists.map(artist => artist.name).join(', ')}`
  )
);

const topTracksIds = [
    '1Z75ISc7cVet14UT60dQMA','2lEnfsBNEiCTPEopIccpVe','4c6KIKanstyrEEmOZXFHt6','3jdjgJYao76mKct23oiSv9','4X4izrkAayHsKqLsnyKL8d'
];
  
// async function getRecommendations(){
//     // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-recommendations
//     return (await fetchWebApi(
//       `v1/recommendations?limit=5&seed_tracks=${topTracksIds.join(',')}`, 'GET'
//     )).tracks;
// }

// console.log(
//     recommendedTracks.map(
//       ({name, artists}) =>
//         `${name} by ${artists.map(artist => artist.name).join(', ')}`
//     )
// );

async function getRecommendations(){
  const response = await fetch('/get_recommendations', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    }
  });
  const data = await response.json();
  return data.recommendations;
}
  
const recommendedTracks = await getRecommendations();
console.log(recommendedTracks.map(track => `${track.Name} by ${track.Artists}`));

async function fetchRecommendations(songTitle){
  const response = await fetch(`/recommendations?song_title=${songTitle}`);
    const data = await response.json();
    console.log(data);  // Or update the DOM based on the data; TO DO: sent up env for MongoDB
}

const tracksUri = [
    'spotify:track:1Z75ISc7cVet14UT60dQMA','spotify:track:2XxS9VnZuA2NnYyu5ATONB','spotify:track:2lEnfsBNEiCTPEopIccpVe','spotify:track:2z93Ew2u4nDGsD3xJIDoDy','spotify:track:4c6KIKanstyrEEmOZXFHt6','spotify:track:1NFawLNYD83yAypRJZrQHK','spotify:track:3jdjgJYao76mKct23oiSv9','spotify:track:3lDUatxIFWhuNUAiquf8fv','spotify:track:4X4izrkAayHsKqLsnyKL8d','spotify:track:7stmkVHi8kN0Nm7fMYeUwz'
];
  
async function createPlaylist(tracksUri){
    const { id: user_id } = await fetchWebApi('v1/me', 'GET')
  
    const playlist = await fetchWebApi(
      `v1/users/${user_id}/playlists`, 'POST', {
        "name": "My recommendation playlist",
        "description": "Playlist created by the tutorial on developer.spotify.com",
        "public": false
    })
  
    await fetchWebApi(
      `v1/playlists/${playlist.id}/tracks?uris=${tracksUri.join(',')}`,
      'POST'
    );
  
    return playlist;
}
  
const createdPlaylist = await createPlaylist(tracksUri);
console.log(createdPlaylist.name, createdPlaylist.id)

const playlistId = '5MLdKZ4bkRJTMUtcF9Tzlf';

<iframe
  title="Spotify Embed: Recommendation Playlist "
  src={`https://open.spotify.com/embed/playlist/5MLdKZ4bkRJTMUtcF9Tzlf?utm_source=generator&theme=0`}
  width="100%"
  height="100%"
  style={{ minHeight: '360px' }}
  frameBorder="0"
  allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
  loading="lazy"
/>

res.redirect('http://127.0.0.1:8081/callback/');