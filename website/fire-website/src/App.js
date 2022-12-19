import logo from "./logo.svg";
import "./App.css";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { Icon } from "leaflet";
import { React, useState } from "react";
import pointsData from "./points.json";

function App() {
  const [points, setPoints] = useState(null);

  return (
    <MapContainer center={[39.48, -8.2245]} zoom={7} scrollWheelZoom={true}>
      {pointsData.map((eachData) => (
        <Marker
          key={eachData.Id}
          position={[eachData.Latitude, eachData.Longitude]}
          eventHandlers={{
            click: () => {
              setPoints(eachData);
            },
          }}
        >
          <Popup>
            {eachData.Location} <br /> Fun fact: {eachData.Fun_Fact}
          </Popup>
        </Marker>
      ))}

      <TileLayer
        attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
      />
    </MapContainer>
  );
}

export default App;
