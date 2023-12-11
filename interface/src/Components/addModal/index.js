import React, { useState, useEffect } from 'react';
import './addModal.css';

const AddModal = ({ isOpen, onClose, onAdd }) => {
  const [symbol, setSymbol] = useState('');
  const [minValue, setMinValue] = useState(null);
  const [maxValue, setMaxValue] = useState(null);

  const handleModalClick = (event) => {
    event.stopPropagation();
  };

  const handleConfirm = async () => {
    onClose();

    try {
      const response = await fetch('http://localhost:5000/tracked-stocks-save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol,
          minValue,
          maxValue,
        }),
      });
      
      if (response.ok) {
        console.log('Post request successful');
        onAdd();
      } else {
        console.error('Post request failed');
      }
    } catch (error) {
      console.error('Error during post request:', error);
    }
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={handleModalClick}>
        <div className="close-button" onClick={onClose}>
          <span>&times;</span>
        </div>
        <h2 className='title'>Track an asset</h2>
        <div className="price-information">
        <label>Type an asset name: </label>
          <input
            type="texts"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
          <label>Set Min Price: </label>
          <input
            type="number"
            value={minValue !== null ? minValue : ''}
            onChange={(e) => setMinValue(e.target.value !== '' ? parseFloat(e.target.value) : null)}
          />
          <label>Set Max Price: </label>
          <input
            type="number"
            value={maxValue !== null ? maxValue : ''}
            onChange={(e) => setMaxValue(e.target.value !== '' ? parseFloat(e.target.value) : null)}
          />
        </div>
        <div className='button-container'>
          <button onClick={handleConfirm}>Confirm</button>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default AddModal;
