import React, { useState } from 'react';
import Select from 'react-select';
import axios from 'axios';

const symptomsOptions = [
  { value: 'fièvre', label: 'fièvre' },
  { value: 'frissons', label: 'frissons' },
  { value: 'maux de tête', label: 'maux de tête' },
  { value: 'fatigue', label: 'fatigue' },
  { value: 'nausées', label: 'nausées' },
  { value: 'nez qui coule', label: 'nez qui coule' },
  { value: 'éternuements', label: 'éternuements' },
  { value: 'maux de gorge', label: 'maux de gorge' },
  { value: 'fièvre légère', label: 'fièvre légère' },
];

export default function Symptomes() {
    const [selectedSymptoms, setSelectedSymptoms] = useState([]);
    const [age, setAge] = useState('');
    const [result, setResult] = useState(null);

    const handleSelectChange = (selectedOptions) => {
        setSelectedSymptoms(selectedOptions.map((option) => option.value));
    };

    const handleAgeChange = (e) => {
        setAge(e.target.value);
    };

    const handleSubmit = async () => {
        try {
          const symptomsObject = {};
          symptomsOptions.forEach((symptom) => {
            symptomsObject[symptom.value] = selectedSymptoms.includes(symptom.value) ? 1 : 0;
          });
          console.log({
            Age: parseInt(age, 10),
            ...symptomsObject,
        });
          const response = await axios.post('https://21evzf38oi.execute-api.us-east-1.amazonaws.com/Test_1/check_sante', {
            Age: parseInt(age, 10),
            ...symptomsObject,
          });
          setSelectedSymptoms([])
          setAge('')
          setResult(response.data);
        } catch (error) {
          console.error('Erreur lors de la requête au backend :', error);
        }
      };

  return (
    <div className='container mt-5' id='predcit#'>
      <h1 className='mb-4'>Symptom Selector</h1>
      <div className='mb-3'>
        <label className='form-label'>Age:</label>
        <input
        
          type='number'
          className='form-control w-25'
          value={age}
          onChange={handleAgeChange}
          required
        />
      </div>
      <div className='mb-3 w-50'>
        <label className='form-label'>Symptoms:</label>
        <Select
          isMulti
          options={symptomsOptions}
          value={symptomsOptions.filter((symptom) => selectedSymptoms.includes(symptom.value))}
          onChange={handleSelectChange}
        />
      </div>
      <button className='btn btn-primary' onClick={handleSubmit}>
        Submit
      </button>
      {result && (
        <div className='mt-4'>
          <h2>Résultat :</h2>
          <p>Prediction : {result.pred}</p>
          <p>Probabilité : {(result.proba * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}