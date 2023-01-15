import logo from "./logo.svg";
import "./App.css";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  LayerGroup,
  Rectangle,
} from "react-leaflet";
import { Icon } from "leaflet";
import { React, useState } from "react";
import pointsData from "./points.json";
import Button from "@mui/material-next/Button";
import { Container } from "./container";

let fires = [];

let information_to_send = [];

const rectangle = [
  [37.31495984620076, -15.485525918583946],
  [37.0, -14],
];

function App() {
  const [points, setPoints] = useState(null);
  const [number, setNumber] = useState(0);


  const triggerText = "Add Fire";
  const onSubmit = (event,type,district) => {
    event.preventDefault(event);
    let fire = {
      latitude: event.target.latitude.value,
      longitude: event.target.longitude.value,
      type: type,
      city : district
    };
    console.log(fire)
    information_to_send.push(fire);
    setNumber(information_to_send.length);
  };

  async function push_info_to_be_processed() {
    const response = await fetch("/info/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(information_to_send),
    });
    let fire_info = await response.json();
    console.log(fire_info);
    information_to_send = [];
    setNumber(0);
    fires=fire_info
  }

  return (
    <div style={{ backgroundColor: "#1f1f1f" }}>
      <div style={{ float: "right" }}>
        <span style={{ color: "white" }}>
          Number of fires to send : {number}
        </span>
        <Container
          triggerText={triggerText}
          onSubmit={onSubmit}
        />
        <span>
          <button onClick={push_info_to_be_processed} variant="contained">
            Process
          </button>
        </span>
      </div>
      <div style={{ zIndex: "10", top: 0, left: 0 }}>
        <MapContainer center={[39.48, -8.2245]} zoom={7} scrollWheelZoom={true}>
          <TileLayer
            attribution='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
            url="https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png"
          />
          {fires.map((eachData) => (
            <Marker
              position={[eachData.latitude, eachData.longitude]}
              eventHandlers={{
                click: () => {
                  setPoints(eachData);
                },
              }}
            >
              <Popup>
                {eachData.resources_by_area.map((needed) => {
                   return <p>
                    Zone :{needed.area} <br/> Trucks: {needed.trucks} <br /> Firetrucks : {needed.trucks}{" "}
                    <br /> Helly: {needed.hely}
                  </p>;
                })}
              </Popup>
            </Marker>
          ))}
          <LayerGroup></LayerGroup>
        </MapContainer>
      </div>
    </div>
  );
}

export default App;