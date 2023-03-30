let map;

async function initMap() {
  const nyc = { lat: 40.7504877, lng: -73.9839238 };

  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView } = await google.maps.importLibrary("marker");

  map = new Map(document.getElementById("map"), {
    center: nyc,
    zoom: 11,
    mapId: "8e91118109e26fc7",
  });

  const marker = new AdvancedMarkerView({
    map: map,
    position: nyc,
    title: "NYC",
  });
}

initMap();