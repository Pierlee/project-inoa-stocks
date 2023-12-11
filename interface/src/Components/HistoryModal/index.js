import React from 'react';
import Modal from '../Modal';
import './historyModal.css';

const HistoryModal = ({ isOpen, onClose, historyData }) => {
  const handleModalClick = (event) => {
    event.stopPropagation();
  };

  return (
    isOpen && (
      <div className="modal-overlay" onClick={onClose}>
        <div className='history-modal' onClick={handleModalClick}>
          <div className="close-button" onClick={onClose}>
            <span>&times;</span>
          </div>
          <div className="history-list-container">
            <h2>History Content</h2>
            {historyData.map((data) => (
              <div className='history-list-item' key={data.symbol}>
                <p><span>Name: </span>{data.symbol}</p>
                <p><span>Time: </span>{data.timestamp}</p>
                <p><span>Price: </span>{data.currentValue}</p>
              </div>
            ))}
            <button onClick={onClose}>Close History</button>
          </div>
        </div>
      </div>
    )
  );
};

export default HistoryModal;
