import React from 'react';
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

const type = ['Urban','Forest']

export const Form = ({ onSubmit,closeAction,setType}) => {
  let typeValue;

  const submit = (event) => {
    setType(typeValue);
    onSubmit(event);
    closeAction();
  }

  const onSelectType =  (option) => {
    console.log('You selected ', option.label)
    typeValue = option.label
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
       <div className="form-group">  
        <button className="button" type="submit" value="Submit">
          Add
        </button>
      </div>
    </form>
  );
};
export default Form;
