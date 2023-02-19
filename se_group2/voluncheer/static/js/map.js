let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.730610, lng: -73.935242 },
    zoom: 8,
  });

  const park = { lat: 40.698479, lng: -73.990626 };
  const afri = { lat: 40.714444, lng: -74.004357 };
  const square = { lat: 40.731245, lng: -73.997115 };
  const marker1 = new google.maps.Marker({
    position: park,
    map: map,
  });
  const marker2 = new google.maps.Marker({
    position: afri,
    map: map,
  });
  const marker3 = new google.maps.Marker({
    position: square,
    map: map,
  });
}

window.initMap = initMap;