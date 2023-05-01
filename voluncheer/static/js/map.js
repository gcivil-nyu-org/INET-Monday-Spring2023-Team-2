let map;

async function initMap() {
  const nyc = { lat: 40.7504877, lng: -73.9839238 };

  const { Point } = await google.maps.importLibrary("core");
  const { InfoWindow, Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerView, Marker } = await google.maps.importLibrary("marker");

  map = new Map(document.getElementById("map"), {
    center: nyc,
    zoom: 11,
    mapId: "8e91118109e26fc7",
    mapTypeControl: true,
  });

  const organizations = JSON.parse(
    document.getElementById("organizations").textContent
  );

  const opportunities = JSON.parse(
    document.getElementById("opportunities").textContent
  );

  const input = document.getElementById("address");
  const { Autocomplete } = await google.maps.importLibrary("places");
  const autocomplete = new Autocomplete(input);
  autocomplete.bindTo("bounds", map);

  const infowindow = new InfoWindow();
  const infowindowContent = document.getElementById("infowindow-content");

  infowindow.setContent(infowindowContent);

  const marker = new Marker({
    map,
    anchorPoint: new Point(0, -29),
  });

  autocomplete.addListener("place_changed", () => {
    infowindow.close();
    marker.setVisible(false);

    const place = autocomplete.getPlace();

    if (!place.geometry || !place.geometry.location) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      window.alert(
        "No details available for input: '" + place.name + "'"
      );
      return;
    }

    
    map.setCenter(place.geometry.location);
    map.setZoom(16);
    


    marker.setPosition(place.geometry.location);
    marker.setVisible(true);
    infowindowContent.children["place-name"].textContent = place.name;
    infowindowContent.children["place-address"].textContent =
      place.formatted_address;
    infowindow.open(map, marker);
  });


  const total = organizations.length;
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add("drop");
        observer.unobserve(entry.target);
      }
    }
  });

  google.maps.event.addListenerOnce(map, "idle", () => {
    for (const org of organizations) {
      const position = {
        lat: parseFloat(org.latitude),
        lng: parseFloat(org.longitude),
      };

      const marker = new AdvancedMarkerView({
        map,
        content: buildContentOrg(org),
        position: position,
        title: org.name,
      });
      const element = marker.content;

      ["focus", "pointerenter"].forEach((event) => {
        element.addEventListener(event, () => {
          highlight(marker, org);
        });
      });
      ["blur", "pointerleave"].forEach((event) => {
        element.addEventListener(event, () => {
          unhighlight(marker, org);
        });
      });
      marker.addListener("click", (event) => {
        unhighlight(marker, org);
      });

      element.style.opacity = "0";
      element.addEventListener("animationend", (event) => {
        element.classList.remove("drop");
        element.style.opacity = "1";
      });

      const time = 1 + Math.random();

      element.style.setProperty("--delay-time", time + "s");
      observer.observe(element);
    }
  });

  google.maps.event.addListenerOnce(map, "idle", () => {
    for (const opp of opportunities) {
      const position = {
        lat: parseFloat(opp.latitude),
        lng: parseFloat(opp.longitude),
      };

      const marker = new AdvancedMarkerView({
        map,
        content: buildContentOpp(opp),
        position: position,
        title: opp.title,
      });
      const element = marker.content;

      ["focus", "pointerenter"].forEach((event) => {
        element.addEventListener(event, () => {
          highlight(marker);
        });
      });
      ["blur", "pointerleave"].forEach((event) => {
        element.addEventListener(event, () => {
          unhighlight(marker);
        });
      });
      marker.addListener("click", (event) => {
        unhighlight(marker);
      });

      element.style.opacity = "0";
      element.addEventListener("animationend", (event) => {
        element.classList.remove("drop");
        element.style.opacity = "1";
      });

      const time = 1 + Math.random();

      element.style.setProperty("--delay-time", time + "s");
      observer.observe(element);
    }
  });
}

function highlight(marker) {
  marker.content.classList.add("highlight");
  marker.element.style.zIndex = 1;
}

function unhighlight(marker) {
  marker.content.classList.remove("highlight");
  marker.element.style.zIndex = "";
}

function buildContentOrg(org) {
  const content = document.createElement("div");

  content.classList.add("org");
  content.innerHTML = `
    <div class="icon">
        <i aria-hidden="true" class="fa fa-icon fa-heart" title="${org.name}"></i>
        <span class="fa-sr-only">${org.name}</span>
    </div>
    <div class="details">
        <div class="name">${org.name}</div>
        <div class="address">${org.address}</div>
        <div class="type">${org.type}</div>
    </div>
    `;
  return content;
}

function buildContentOpp(opp) {
  const content = document.createElement("div");

  content.classList.add("opp");
  content.innerHTML = `
    <div class="icon">
        <i aria-hidden="true" class="fa fa-icon fa-handshake-angle" title="${opp.title}"></i>
        <span class="fa-sr-only">${opp.type}</span>
    </div>
    <div class="details">
        <div class="title">${opp.title}</div>
        <div class="address">${opp.address}</div>
        <div class="type">${opp.type}</div>
    </div>
    `;
  return content;
}

initMap();