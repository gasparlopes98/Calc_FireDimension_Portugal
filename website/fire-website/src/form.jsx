import React from 'react';
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

const type = ['Urban','Forest']
const intensity = [0,1,2,3,4,5]

export const Form = ({ onSubmit,closeAction,setType,setSeverity }) => {
  let typeValue;
  let severityValue;

  const submit = (event) => {
    setType(typeValue);
    setSeverity(severityValue);
    onSubmit(event);
    closeAction();
  }

  const onSelectType =  (option) => {
    console.log('You selected ', option.label)
    typeValue = option.label
  }

  const onSelectSeverity =  (option) => {
    console.log('You selected ', option.label)
    severityValue = option.label
  }

  return (
    <form onSubmit={submit} style={{borderRadius:"25px"}}>
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
        Severity: 
        <Dropdown onChange={onSelectSeverity} style={{paddingDown:5}} options={intensity} value={severityValue} placeholder="Select an option" />
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
