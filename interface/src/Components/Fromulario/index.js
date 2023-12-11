import React, { useEffect, useState } from 'react';
import './formulario.css'
import HistoryModal from '../HistoryModal';
import AddModal from '../addModal';

const Formulario = () => {
  const [dataFromApi, setDataFromApi] = useState([]);
  const [selectedRow, setSelectedRow] = useState(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [historyData, setHistoryData] = useState([])
  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false)

  useEffect(() => {
    fetchStock();
  }, []);

  useEffect(() => {
    if (selectedRow) {
      handleHistory(selectedRow);
    }
  }, [selectedRow]);

  const handleSelection = (row) => {
    setSelectedRow(row);
  };
  const handleDelete = () => {
    if (selectedRow) {
      const deleteUrl = `http://127.0.0.1:5000/tracked-stocks-delete?symbol=${selectedRow}`;
      
      fetch(deleteUrl, {
        method: 'DELETE',
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          fetchStock();
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }
  };
  const handleHistory = async () => {
    try {
      if (selectedRow) {
        const response = await fetch(`http://127.0.0.1:5000/stock-history?symbol=${selectedRow}`);
        const data = await response.json();
        setHistoryData(data);
      }
    } catch (error) {
      console.error('Error fetching historical data:', error);
    }
  };
  const handleOpenHistoryModal = () => {
    if (selectedRow) {
      setIsHistoryModalOpen(true);
    }
  }
  const handleCloseHistoryModal = () => {
    setIsHistoryModalOpen(false)
  }
  const handleAddModal = () => {
    setSelectedRow(null)
    setIsAddModalOpen(true);
  };
  const handleCloseAddModal = () => {
    setIsAddModalOpen(false);
  };
  const fetchStock = () => {
    const apiUrl = `http://127.0.0.1:5000/tracked-stocks-list`
    fetch(apiUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((apiData) => {
      setDataFromApi(apiData); // Store the data in the state
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  };
  const onAdd = () => {
    fetchStock()
  }
  return(
    <div className="list-container">
      <div className='list-item normal-cursor'>
        <p className='col-header'>Name</p>
        <p className='col-header'>Min Price</p>
        <p className='col-header'>Max Price</p>
      </div>
      {dataFromApi.map((rowData) => (
        <div
          key={rowData.symbol}
          className={`list-item ${selectedRow === rowData.symbol ? 'selected' : ''}`}
          onClick={() => handleSelection(rowData.symbol)}
        >
          <p>
            {rowData.symbol}
          </p>
          <p>
            {rowData.maxValue}
          </p>
          <p>
            {rowData.minValue}
          </p>
        </div>
    ))}

    <div className="action-buttons">
      <button onClick={handleAddModal}>Add</button>
      <button onClick={handleDelete}>Delete</button>
      <button onClick={handleOpenHistoryModal}>History</button>
    </div>
    <AddModal isOpen={isAddModalOpen} onClose={handleCloseAddModal} data={dataFromApi}  onAdd={onAdd}/>
    <HistoryModal isOpen={isHistoryModalOpen} onClose={handleCloseHistoryModal} historyData={historyData}/>
  </div>
  ) 
};

export default Formulario;
