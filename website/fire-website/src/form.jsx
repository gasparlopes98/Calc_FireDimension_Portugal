import React from 'react';
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

const type = ['Urban','Forest']
const district=["Aveiro",
"Beja",
"Braga",
"Bragança",
"Castelo Branco",
"Coimbra",
"Évora",
"Faro",
"Guarda",
"Leiria",
"Lisboa",
"Portalegre",
"Porto",
"Santarém",
"Setúbal",
"Viana do Castelo",
"Vila Real",
"Viseu"
]

export const Form = ({ onSubmit,closeAction}) => {
  let typeValue;
  let districtValue;

  const submit = (event) => {
    onSubmit(event,typeValue,districtValue);
    closeAction();
  }

  const onSelectType =  (option) => {
    console.log('You selected ', option.label)
    typeValue = option.label
  }

  const onSelectDistrict =  (option) => {
    console.log('You selected ', option.label)
    districtValue = option.label
  }


  return (
    <form onSubmit={submit}>
      <div className="form-group">
        <label htmlFor="name">Latitude</label>
        <input className="form-control" id="latitude" />
      </div>
      <div className="form-group">
        <label htmlFor="name">Longitude</label>
        <input className="form-control" id="longitude" />
      </div>
      <div>
        Type of Fire: 
        <Dropdown onChange={onSelectType} options={type} value={typeValue} placeholder="Select an option" />
      </div>
      <div>
        District: 
        <Dropdown onChange={onSelectDistrict} options={district} value={districtValue} placeholder="Select an option" />
      </div>
       <div className="form-group">  
        <button className="button" type="submit" value="Submit">
          Add
        </button>
      </div>
    </form>
  );
};
export default Form;
