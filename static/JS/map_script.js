// The ymaps.ready() function will be called when
// all the API components are loaded and the DOM tree is generated.
function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
  //@function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2)
  //@brief receives latitude and longitude from two points and
  //    returns the distance between them
  //@param lat1 Latitude from point 1
  //@param lon1 Longitude from point 1
  //@param lat2 Latitude from point 2
  //@param lon2 Longitude from point 2
  //@returns distance on Earth's globe between two points
  //@note formula extrated from: https://www.codegrepper.com/code-examples/
  //  javascript/distance+between+2+coordinates+formula
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2-lat1);  // deg2rad below
  var dLon = deg2rad(lon2-lon1); 
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c; // Distance in km
  return Math.floor(d);
}

function deg2rad(deg) {
  //@function deg2rad(deg)
  //@brief transforms degree units to radians
  //@param deg number representing degree units
  //@returns number in radians
  //@note formula extrated from: https://www.codegrepper.com/code-examples/
  //  javascript/distance+between+2+coordinates+formula
  return deg * (Math.PI/180)
}

ymaps.ready(init);
function init(){
    //@function init
    //@brief map initialization

    // Verification if message contains data
    var count = Object.keys(data).length;
    var route_distance = null
    //console.log(typeof count, count);
    if(count===0){
    // Default position
      var center = [55.898947, 37.632206];
    }else{
    // Map positioning on desired location
      var lon = data[0].position[0];
      var lat = data[0].position[1];
      var coords = [lat, lon];
      var center = [lat, lon];
    };

    // Creating the map.    
    var myMap = new ymaps.Map("map", {
        // The map center coordinates.
        // Default order: “latitude, longitude”.
        // To not manually determine the map center coordinates,
        // use the Coordinate detection tool.
        //center: [55.76, 37.64],
        center: center,
        // Zoom level. Acceptable values:
        // from 0 (the entire world) to 19.
        zoom: 9
      }, {
        searchControlProvider: 'yandex#search'
      }),
      // Creates a polygon on the map
      myPolygon = new ymaps.Polygon(
        [
          [[55.898947, 37.632206],
          [55.895303, 37.678343],
          [55.882793, 37.725092],
          [55.827852, 37.832385],
          [55.765478, 37.843157],
          [55.745681, 37.839878],
          [55.706056, 37.835450],
          [55.658439, 37.839277],
          [55.616010, 37.779799],
          [55.590119, 37.726879],
          [55.572044, 37.650720],
          [55.609843, 37.494288],
          [55.634385, 37.465506],
          [55.660587, 37.434873],
          [55.732388, 37.378028],
          [55.790712, 37.372943],
          [55.882707, 37.447566],
          [55.893743, 37.497854],
          [55.908575, 37.548492],
          [55.910649, 37.591162]]
        ],
      null,
      { draggable: false }
      );
      // Creates a point on the map
      objects = ymaps.geoQuery([
        {
            type: 'Point',
            //coordinates: [lon, lat]
            //coordinates: [55.76, 37.64]
            coordinates: coords
        }
      ]), 
    
    //Check if point is within selected region  
    myMap.geoObjects.add(myPolygon);
    var objectsInsideObject = objects.searchInside(myPolygon);
    // Red icon if point within area
    objectsInsideObject.setOptions('preset', 'islands#redIcon');  
    // Blue icon if point outside area.
    objects.remove(objectsInsideObject).setOptions('preset', 'islands#blueIcon');
    //console.log(objectsInsideObject.getLength());
    // If object not in reagion calculate distance
    if (objectsInsideObject.getLength() === 0){
      var route_distance = getDistanceFromLatLonInKm(lat, lon, 55.898947, 37.632206)
      document.getElementById("my_distance").innerHTML = route_distance;
      //console.log(route_distance);
    // If object in region don't show/calculate distance  
    }else{
      document.getElementById("my_distance").style.visibility="hidden";  
      document.getElementById("distance_message").style.visibility="hidden";
    }
    objects.addToMap(myMap);
    
}
